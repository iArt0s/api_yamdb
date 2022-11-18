# Проект YaMDb

<i>Проект YaMDb собирает отзывы (Review) пользователей на произведения (Title).
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка».
Список категорий может быть расширен.
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи</i> 

<i>Задача: написать бэкенд проекта (приложение reviews) и API для него (приложение api) так,
чтобы они полностью соответствовали документации.</i> 


<i><b>Ресурсы API YaMDb</i></b>
<blockquote>
☑ Ресурс auth: аутентификация; <br>
☑ Ресурс users: пользователи; <br>
☑ Ресурс titles: произведения, к которым пишут отзывы (определённый фильм, книга или песня);  <br>
☑ Ресурс categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»). <br> 
Одно произведение может быть привязано только к одной категории. <br> 
☑ Ресурс genres: жанры произведений. <br> 
Одно произведение может быть привязано к нескольким жанрам. <br> 
☑ Ресурс reviews: отзывы на произведения.<br> 
Отзыв привязан к определённому произведению.; <br>
☑ Ресурс comments: комментарии к отзывам. <br>
Комментарий привязан к определённому отзыву.<br>
</blockquote>

<i><b>Технологии</i></b>
<blockquote>
☑ Python 3.7.0 <br> 
☑ Django REST framework
</blockquote>

<i><b>Запуск проекта в dev-режиме:</i></b><br> 
☑ Клонируйте проект с GitHub:</li>
    <blockquote>
      git@github.com:iArt0s/api_yamdb.git
    </blockquote>  
☑ Создайте и активируйте виртуальное окружение:</li>
    <blockquote>
      python -m venv venv<br> 
      source venv/Scripts/activate 
    </blockquote>  
☑ Установите зависимости из файла requirements.txt (не забудьте предварительно обновить pip!):</li>
    <blockquote>
      pip install -r requirements.txt
    </blockquote>
☑ Выполните миграции:</li>
    <blockquote>
      python manage.py migrate
    </blockquote>
☑ Создайте суперпользователя для предоставления прав админинстраторам:</li>
    <blockquote>
      python manage.py createsuperuser
    </blockquote>
 ☑ Запустите сервер разработчика:</li>
    <blockquote>
      python manage.py runserver
    </blockquote>
</li>

<i><b>Просматривайте динамическую документацию API вместе с примерами запросов через redoc/swagger (напр., http://127.0.0.1:8000/redoc/)</i></b><br> 
  

Авторы:
<b>Артем Осипов (Teamlead)</b>
<b>Дмитрий Венде</b>
<b>Елена Трембовельская</b>
