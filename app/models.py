# Create your models here.

from django.db import models
from django.core.validators import MinValueValidator

class Profile(models.Model):
    name = models.CharField("Имя", max_length=255)
    description = models.TextField(verbose_name="Описание", blank = True)
    birth_date = models.DateField("Дата рождения")
    purchased_items = models.ManyToManyField(
        "Item",
        verbose_name="Корзина",
        related_name="items",
        blank = True,
    )

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural="Профили"
        ordering=["-name"]

    def __str__(self):
        return self.name

class User(models.Model):
    login = models.CharField('Логин', max_length=255, unique=True)
    password = models.CharField('Пароль', max_length=255)
    profile = models.OneToOneField(
        Profile,
        verbose_name="Профиль",
        related_name = "user",
        blank=False,
        null=False,
        on_delete = models.CASCADE,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-profile"]

    def __str__(self):
        return self.login

class Group(models.Model):
    name = models.CharField("Название", max_length=255, unique=True)
    admin = models.ForeignKey(
        User,
        verbose_name="Админ группы",
        related_name = "group_admin",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    users = models.ManyToManyField(
        User,
        verbose_name="Участники",
        related_name="group_users",
        blank = True,
    )

    class Meta:
        verbose_name="Группа"
        verbose_name_plural="Группы"
        ordering = ["-name"]

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField("Название", max_length=255)
    text = models.TextField("Текст", blank=False)
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )
    edited_at = models.DateTimeField(
        verbose_name="Дата редактирования",
        auto_now=True,
    )
    group = models.ForeignKey(
        Group,
        verbose_name="Группа",
        related_name="group_posts",
        blank=False,
        null = False,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        related_name="user_posts",
        blank = False,
        null = True,
        on_delete=models.SET_NULL,
    )
    image_field=models.ImageField(
        verbose_name="Изображение",
        upload_to='posts/',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name="Пост"
        verbose_name_plural="Посты"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class Comment(models.Model):
    text = models.TextField('Комментарий', blank = False)
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )
    edited_at = models.DateTimeField(
        verbose_name="Дата редактирования",
        auto_now=True,
    )
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        related_name = "user_comments",
        blank = False,
        null = True,
        on_delete=models.SET_NULL,
    )
    post = models.ForeignKey(
        Post,
        verbose_name="Пост",
        related_name="post_comments",
        blank = False,
        null = False,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-created_at"]

    def __str__(self):
        # if self.author:
        #     return f'{self.author} - {self.text}'
        # else:
        #     return f'Аноним - {self.text}'
        if self.author:
            return f'{self.author} - {self.created_at}'
        else:
            return f'{self.created_at}'

class Item(models.Model):
    TYPE_CHOISES=[
        ('default', 'Неизвестно'),
        ('toy', 'Игрушка'),
        ('food', 'Еда'),
    ]

    name = models.CharField("Название", max_length=255, blank=False)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    type=models.CharField(choices=TYPE_CHOISES, default="default", blank=True, max_length=255)
    price = models.FloatField(
        "Цена",
        validators=[MinValueValidator(0.0)],
        default=0.0
        )

    class Meta:
        verbose_name="Вещь"
        verbose_name_plural="Вещи"
        ordering=["-type","-name"]

    def __str__(self):
        return f'{self.type} - {self.name}'