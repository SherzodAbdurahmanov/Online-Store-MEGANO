# 🛍️ Megano - API для интернет-магазина  

## 📌 Описание  
Megano — это backend-сервис для интернет-магазина, реализованный на Django REST Framework.  
Проект поддерживает аутентификацию пользователей, управление корзиной, заказами и оплатой.  

## ⚙️ Используемые технологии  
- Python 3.x  
- Django 4.x  
- Django REST Framework  
- PostgreSQL (или SQLite)  
- Black (для автоформатирования кода)  

## 🚀 Установка и запуск  

1️⃣ Клонируем репозиторий:  
git clone https://gitlab.skillbox.ru/sherzod_abdurahmanov/python_django_diploma.git
cd python_django_diploma

2️⃣ Создаём виртуальное окружение:
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

3️⃣ Устанавливаем зависимости:
pip install -r requirements.txt

4️⃣ Применяем миграции и создаём суперпользователя:
python manage.py migrate
python manage.py createsuperuser 

5️⃣ Запускаем сервер:
python manage.py runserver
Теперь API доступно по адресу http://127.0.0.1:8000/

> 
🔗 Основные эндпоинты API:
Метод	Эндпоинт	Описание
POST - /api/sign-in/ - Вход в систему
POST - /api/sign-up/ - Регистрация
GET  - /api/profile/ - Просмотр профиля
POST - /api/profile/avatar/ - Обновление аватара
GET	 - /api/catalog/products/ - Список товаров
POST - /api/basket/ - Добавить товар в корзину
POST - /api/orders/ - Создать заказ
POST - /api/payment/ - Оплатить заказ
> 


