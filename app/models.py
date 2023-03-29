from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Contact(models.Model):
    
    name = models.CharField(
        max_length=50,
        verbose_name='Имя'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Пользватель'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активный?'
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания записи'
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления записи'
    )
    
    def __str__(self) -> str:
    
        return self.name
    
    def get_absolute_url(self):
        return reverse("contact-detail", kwargs={"pk": self.pk})
    
    def get_absolute_edit_url(self):
        return reverse("edit-contact", kwargs={"pk": self.pk})
    
    def get_absolute_delete_url(self):
        return reverse("contact-delete", kwargs={"pk": self.pk})
    
    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ['name', '-updated_date']
    

class PhoneNumber(models.Model):
    
    number = models.CharField(
        max_length=10,
        verbose_name='Тел. номер'
    )
    contact = models.ForeignKey(
        Contact,
        on_delete=models.PROTECT,
        verbose_name='Контакт',
        related_name='phone_numbers'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активный?'
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания записи'
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления записи'
    )
    
    def __str__(self) -> str:
        return f'{self.contact.name} -> {self.number}'
    
    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'
        ordering = ['contact__name', '-updated_date']