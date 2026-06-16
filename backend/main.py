from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from core.logging_config import logger  
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

Base = declarative_base()

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    status = Column(String, default="open")

try:
    logger.info("Попытка создания таблиц в базе данных...")
    Base.metadata.create_all(bind=engine)
    logger.info("Таблицы успешно проверены/созданы.")
except Exception as e:
    # exc_info=True запишет весь traceback ошибки в app.log
    logger.critical(f"Критическая ошибка при подключении к БД при старте: {e}", exc_info=True)
    # Приложение НЕ упадет, а продолжит запуск FastAPI

app = FastAPI(title="NexusMonitor API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)
def get_db():
    db = SessionLocal()
    try:
        # Быстрая проверка, живо ли соединение прямо сейчас
        db.execute(text("SELECT 1"))
        yield db
    except OperationalError as e:
        logger.error(f"Ошибка базы данных во время выполнения запроса: {e}")
        raise HTTPException(status_code=500, detail="Ошибка подключения к базе данных")
    finally:
        db.close()

@app.get("/api/incidents")
def get_incidents(db: Session = Depends(get_db)):
    logger.info("Запрос списка инцидентов")
    # Пример запроса к модели для демонстрации работы
    try:
        incidents = db.query(Incident).all()
        return {"status": "success", "data": incidents}
    except Exception as e:
        logger.error(f"Не удалось получить инциденты из базы: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
