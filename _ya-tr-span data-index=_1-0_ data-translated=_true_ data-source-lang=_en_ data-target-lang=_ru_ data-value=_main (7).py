
python
from django.db import models
class User(models.Model):
    username = models.CharField(max_length=50)
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    def update_rating(self):
        self.rating = 3 * sum([p.rating for p in self.post_set.all()])
        self.rating += sum([c.rating for p in self.post_set.all() for c in p.comment_set.all()])
        self.rating += sum([c.rating for c in self.comment_set.all()])
        self.save()
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=10, choices=[('article', 'Article'), ('news', 'News')])
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()
    def dislike(self):
        self.rating -= 1
        self.save()
    def preview(self):
        return self.content[:124] + '...'
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    def like(self):
        self.rating += 1
        self.save()
    def dislike(self):
        self.rating -= 1
        self.save()
# В консоли Django shell:
# Создать двух пользователей
user1 = User.objects.create_user('user1')
user2 = User.objects.create_user('user2')
# Создать два объекта модели Author, связанные с пользователями
author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

# Добавить 4 категории в модель Category
category1 = Category.objects.create(name='Sport')
category2 = Category.objects.create(name='Politics')
category3 = Category.objects.create(name='Education')
category4 = Category.objects.create(name='Technology')
# Добавить 2 статьи и 1 новость
post1 = Post.objects.create(author=author1, post_type='article', title='Article 1', content='Content of article 1')
post2 = Post.objects.create(author=author2, post_type='article', title='Article 2', content='Content of article 2')
post3 = Post.objects.create(author=author1, post_type='news', title='News 1', content='Content of news 1')
# Присвоить им категории
post1.categories.add(category1, category2)
post2.categories.add(category3)
post3.categories.add(category1, category4)
# Создать как минимум 4 комментария к разным объектам модели Post
comment1 = Comment.objects.create(post=post1, user=user1, text='Comment 1 on post 1')
comment2 = Comment.objects.create(post=post2, user=user2, text='Comment 1 on post 2')
comment3 = Comment.objects.create(post=post1, user=user2, text='Comment 2 on post 1')
comment4 = Comment.objects.create(post=post3, user=user1, text='Comment on news 1')
# Применять функции like() и dislike() к статьям/новостям и комментариям
post1.like()
post2.dislike()
comment1.like()
comment2.dislike()
# Обновить рейтинги пользователей
author1.update_rating()
author2.update_rating()
# Вывести username и рейтинг лучшего пользователя
best_author = Author.objects.order_by('-rating').first()
print(best_author.user.username, best_author.rating)
# Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи
best_article = Post.objects.filter(post_type='article').order_by('-rating').first()
print(best_article.created_at, best_article.author.user.username, best_article.rating, best_article.title, best_article.preview())
# Вывести все комментарии к этой статье
comments = Comment.objects.filter(post=best_article)
for comment in comments:
    print(comment.created_at, comment.user.username, comment.rating, comment.text)
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from pytz import timezone

# Функция отправки письма
def send_email(to_address, subject, body):
    from_address = "your_email@gmail.com"  # Заменить на ваш адрес электронной почты
    password = "your_password"  # Заменить на ваш пароль
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_address, password)
    server.send_message(msg)
    server.quit()
# Функция для получения списка новых статей за прошедшую неделю в заданной категории
def get_new_articles(category):
    end_date = datetime.now(timezone('UTC'))
    start_date = end_date - timedelta(days=7) 
    # Здесь должна быть логика для получения списка новых статей в заданной категории 
    # в заданном временном диапазоне
    new_articles = []  # Список новых статей
    for article in articles:
        if article.category == category and start_date <= article.date <= end_date:
            new_articles.append(article)
    return new_articles
# Функция для отправки списка новых статей на почту подписчикам
def send_weekly_articles():
    subscribers = get_subscribers()  # Получение подписчиков из базы данных
    for subscriber in subscribers:
        category = subscriber.category  # Получение категории, на которую подписан пользователь
        new_articles = get_new_articles(category)  # Получение списка новых статей   
        if new_articles:
            email_body = "<h2>Новые статьи за прошедшую неделю:</h2>"
            for article in new_articles:
                article_link = f"<a href='{article.link}'>{article.title}</a>"
                email_body += f"<p>{article_link}</p>"
            send_email(subscriber.email, "Еженедельный список новых статей", email_body)
# Код для отправки приветственного письма пользователю при регистрации
def send_welcome_email(email):
    welcome_subject = "Добро пожаловать в наш новостной портал!"
    welcome_body = """
        <h3>Спасибо за регистрацию на нашем новостном портале!</h3>
        <p>Теперь вы можете подписаться на интересующие вас категории новостей.</p>
        <p>Успехов в чтении интересных статей!</p>
        """
    send_email(email, welcome_subject, welcome_body)
# Код для добавления нового подписчика в базу данных
def add_subscriber(email, category):
    # Здесь должна быть логика добавления подписчика в базу данных
    pass
