from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField("Добавлено", auto_now_add=True)
    is_published = models.BooleanField(
        "Опубликовано", default=True, help_text="Снимите галочку, чтобы"
        " скрыть публикацию.")

    class Meta:
        abstract = True


class Category(BaseModel):
    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    title = models.CharField("Заголовок", max_length=256)
    description = models.TextField("Описание")
    slug = models.SlugField("Идентификатор", unique=True,
                            help_text="Идентификатор страницы для URL; "
                            "разрешены символы латиницы, цифры, "
                            "дефис и подчёркивание.")

    def __str__(self):
        return self.title


class Location(BaseModel):
    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"
    name = models.CharField("Название места", max_length=256)

    def __str__(self):
        return self.name


class Post(BaseModel):
    class Meta:
        default_related_name = 'posts'
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ('-pub_date',)

    title = models.CharField("Заголовок", max_length=256)
    text = models.TextField("Текст")
    pub_date = models.DateTimeField(
        "Дата и время публикации", help_text="Если установить дату и время в"
        " будущем — можно делать "
        "отложенные публикации.")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации"
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL, null=True, verbose_name="Местоположение",
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL, null=True, verbose_name="Категория",
        blank=False
    )
    image = models.ImageField('Фото', upload_to='post_images/', blank=True)

    def get_absolute_url(self):
        return reverse(
            'blog:post_detail', args=[self.pk]
        )

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField('Текст', )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор публикации")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, verbose_name='Публикация')
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        default_related_name = 'comments'
        ordering = ('created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
