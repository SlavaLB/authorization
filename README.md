-   Создаем виртуальное окружение:
```
python -m venv venv
```

-   Активируем виртуальное окружение:
```
source venv/scripts/activate
```

-   Устанавливаем зависимости:
```
pip install -r requirements.txt
```


- Зпускаем Redis локально:
```
docker run -d --name redis -p 6379:6379 redis
```

-  Запуск сервера
```
uvicorn fast_app:app --host 127.0.0.1 --port 8000 --reload 
```

-  Документация
```
http://127.0.0.1:8000/docs
```