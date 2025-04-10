from django.core.validators import RegexValidator
from django.db import models

phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,12}$',
        message="Phone number must be entered in the format: "
                "'+999999999'. Up to 12 digits allowed.")


class Users(models.Model):
    email = models.EmailField(unique=True)
    phone = models.CharField(validators=[phone_regex], max_length=14, blank=True)
    fam = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    otc = models.CharField(max_length=150)

    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f'{self.fam} {self.name}'


class PerevalAdded(models.Model):
    NEW = 'new'
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    STATUS_CHOICES = [
        (NEW, "новый"),
        (PENDING,  "модератор взял в работу"),
        (ACCEPTED, "модерация прошла успешно"),
        (REJECTED,  "модерация прошла, информация не принята"),
    ]

    beauty_title = models.CharField(max_length=20, verbose_name='Тип')
    title = models.CharField(max_length=50, verbose_name='Название')
    other_titles = models.CharField(max_length=50, blank=True, verbose_name='Другие названия')
    connect = models.CharField(max_length=100, blank=True, verbose_name='Что соединяет')
    add_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, verbose_name='Ползователь', null=True)
    coords = models.ForeignKey('Coords', on_delete=models.SET_NULL, verbose_name='Координаты', blank=True, null=True)
    level = models.ForeignKey(
        'Level',
        on_delete=models.SET_NULL,
        verbose_name='Категория трудности',
        blank=True, null=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NEW)
    images = models.ManyToManyField('Images', through='PerevaladdedImages')

    class Meta:
        verbose_name = "Перевал"
        verbose_name_plural = "Перевал"

    def __str__(self):
        return self.title


class Level(models.Model):  # ок
    LEVEL_CHOICES = [
        ("н/к", "некатегорийный"),
        ("1А", "1А"),
        ("1Б", "1Б"),
        ("2А",  "2А"),
        ("2Б", "2Б"),
        ("3А",  "3А"),
        ("3Б", "3Б"),
    ]

    mark = models.CharField(max_length=5, choices=LEVEL_CHOICES, verbose_name='Категория трудности', blank=True)

    class Meta:
        verbose_name = "Категория трудности"
        verbose_name_plural = "Категория трудности"

    def __str__(self):
        return f'Категория: {self.mark}.'


class Coords(models.Model):
    latitude = models.FloatField(verbose_name='Широта', blank=True, null=True, default=0.0)
    longitude = models.FloatField(verbose_name='Долгота', blank=True, null=True, default=0.0)
    height = models.IntegerField(verbose_name='Высота над уровнем моря, м', blank=True, null=True, default=0)

    class Meta:
        verbose_name = "Координаты"
        verbose_name_plural = "Координаты"

    def __str__(self):
        return f'GPS: {self.latitude}, {self.longitude} Высота: {self.height} м'


class Images(models.Model):
    data = models.ImageField(upload_to='media/%Y/%m/%d/', verbose_name='Изображение', null=True)
    title = models.CharField(max_length=255)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Изображения"
        verbose_name_plural = "Изображения"

    def __str__(self):
        return f'{self.title}'


class PerevaladdedImages(models.Model):
    perevaladded = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE)
    images = models.ForeignKey(Images, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Перевал-Изображение"
        verbose_name_plural = "Перевал-Изображение"

    def __str__(self):
        return f'{self.images}'
