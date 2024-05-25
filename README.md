# Проект: SPA Комментарии

Этот проект представляет собой одностраничное приложение (SPA) для управления комментариями. Пользователи могут
оставлять комментарии, отвечать на комментарии других пользователей, а также просматривать комментарии с различными
параметрами сортировки.

## Основные функции

1. **Добавление комментариев:**
    - Пользователи могут оставлять комментарии с указанием имени, e-mail, домашней страницы, текста комментария и
      CAPTCHA.
    - Поля:
        - **User Name:** обязательное, цифры и буквы латинского алфавита.
        - **E-mail:** обязательное, формат email.
        - **Home page:** необязательное, формат URL.
        - **CAPTCHA:** обязательное.
        - **Text:** обязательное, без запрещенных HTML тегов.

2. **Отображение комментариев:**
    - Каскадное отображение комментариев.
    - Возможность сортировки по User Name, E-mail и дате добавления.
    - Пагинация: 25 комментариев на страницу.
    - Защита от XSS атак и SQL инъекций.

3. **Работа с файлами:**
    - Поддержка изображений (JPG, GIF, PNG) и текстовых файлов (TXT) до 100 кб.
    - Автоматическое уменьшение изображений до 320x240 пикселей.

## Технологии

- **Backend:**
    - Django
    - Django ORM
    - PostgreSQL
    - Celery
    - Redis
- **Frontend:**
    - HTML
    - CSS
- **Инфраструктура:**
    - Docker для контейнеризации
    - Redis для кеширования и брокера сообщений
    - PostgreSQL для базы данных

## Установка и запуск

### Предварительные требования

- Docker и Docker Compose установлены на вашем компьютере.
- Учетная запись для базы данных PostgreSQL.

### Инструкция по установке

1. **Клонируйте репозиторий:**
   ```sh
   git clone https://github.com/reeeade/SPA_Comment.git
   cd SPA_Comment

2. **Создайте файл .env и укажите переменные окружения:**
    ```sh
    POSTGRES_DB=spa_comment
    POSTGRES_USER=user
    POSTGRES_PASSWORD=password
    POSTGRES_HOST=postgres
    POSTGRES_PORT=5432

    REDIS_URL=redis://redis:6379/0

    DJANGO_SECRET_KEY=your_secret_key

3. **Запустите Docker Compose:**

    ```sh
    docker-compose up --build

4. **Выполните миграции базы данных:**

    ```sh
    docker-compose exec web python manage.py migrate

5. **Создайте суперпользователя для доступа к админ-панели:**

    ```sh
    docker-compose exec web python manage.py createsuperuser

6. **Запустите сервер разработки:**

    ```sh
    docker-compose up

## Использование

1. **Добавление комментариев:**

   - Перейдите на главную страницу.
   - Заполните форму добавления комментария и отправьте её.
   - Поля CAPTCHA должны быть правильно заполнены.

2. **Просмотр комментариев:**

   - Комментарии отображаются в каскадном виде.
   - Используйте параметры сортировки для упорядочивания комментариев по имени пользователя, e-mail и дате добавления.
   - Пагинация позволяет просматривать по 25 комментариев на странице.

3. **Ответы на комментарии:**
   - Нажмите кнопку "Ответить" под комментарием для добавления ответа.

## Вклад и разработка

1. **Создание новой ветки:**

    ```sh
    git checkout -b feature/название_ветки

2. **Внесение изменений:**

   - Внесите необходимые изменения в код.
   - Напишите тесты для новых функций.

3. **Коммит изменений:**

    ```sh
    git add .
    git commit -m "feat: краткое описание изменений"

4. **Отправка изменений:**

    ```sh
    git push origin feature/название_ветки

5. **Создание Pull Request:**
   - Перейдите в репозиторий на GitHub.
   - Создайте новый Pull Request с вашими изменениями.

## Примеры кода
### Реализация кеширования для страницы списка комментариев

```python
from django.core.cache import cache
from comments.models import Comment
from django.core.paginator import Paginator
from django.shortcuts import render


def list_comments(request):
    sort_by = request.GET.get('sort_by', 'created_at')
    sort_order = request.GET.get('sort_order', 'desc')
    page_number = request.GET.get('page', 1)

    cache_key = f'comments_{sort_by}_{sort_order}_page_{page_number}'
    page_obj = cache.get(cache_key)

    if not page_obj:
        if sort_order == 'asc':
            comment_list = Comment.objects.filter(parent__isnull=True).order_by(sort_by)
        else:
            comment_list = Comment.objects.filter(parent__isnull=True).order_by(f'-{sort_by}')

        paginator = Paginator(comment_list, 25)
        page_obj = paginator.get_page(page_number)
        cache.set(cache_key, page_obj, timeout=60 * 10)
        print("Fetching from DB")
    else:
        print("Fetching from Cache")

    return render(request, 'list_comments.html',
                  {'page_obj': page_obj, 'sort_by': sort_by, 'sort_order': sort_order})
```

##  Заключение

Проект предоставляет функционал для добавления и управления комментариями с использованием современных технологий и
лучших практик разработки. Внедрение кеширования и использование Docker для контейнеризации обеспечивают высокую
производительность и удобство развертывания приложения.

## Примечание

Во время разработки основное внимание уделялось backend-части приложения с использованием Django, PostgreSQL, Celery и
Redis. Фронтенд реализован с использованием базового HTML и CSS, без сложных визуальных эффектов и панели с кнопками для
вставки HTML тегов.

Документация и инструкции по развертыванию обеспечивают лёгкость использования и модификации проекта.