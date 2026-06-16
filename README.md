# NexusMonitor

Система учета и мониторинга инцидентов.

## Локальный запуск 

### Предварительные требования
- Python 3.10+
- Node.js 18+
- PostgreSQL 

### 1. Настройка Базы Данных
Создайте базу данных в PostgreSQL:
```bash
psql -U postgres
CREATE DATABASE nexus_db;
```
### 2. Запуск Бэкенда (FastAPI)

```bash
cd backend
cp .env.example .env && nano .env
python -m venv venv # Windows: venv\Scripts\activate # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
### 3. Запуск Фронтенда (React)

```bash
cd frontend
cp .env.example .env && nano .env
npm install
npm run dev
```
Приложение будет доступно по адресу: http://localhost:5173