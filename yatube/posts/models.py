from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200,
                             help_text='Введите название группы',
                             verbose_name='Название группы')
    slug = models.SlugField(unique=True,
                            help_text='Введите адрес группы',
                            verbose_name='Адрес группы')
    description = models.TextField(max_length=400,
                                   help_text='Введите описание группы',
                                   verbose_name='Описание группы')

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(help_text='Введите текст поста',
                            verbose_name='текст поста')
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True, null=True)

    class Meta:
        ordering = ('-pub_date', )

    def __str__(self):
        return self.text[:15]
