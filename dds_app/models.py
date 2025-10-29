from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.utils import timezone

class Status(models.Model):
    """Модель для статусов транзакций"""
    name = models.CharField(max_length=100, verbose_name="Название статуса")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class TransactionType(models.Model):
    """Модель для типов операций (Пополнение/Списание)"""
    name = models.CharField(max_length=100, verbose_name="Название типа")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Тип операции"
        verbose_name_plural = "Типы операций"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Category(models.Model):
    """Модель для категорий транзакций"""
    name = models.CharField(max_length=100, verbose_name="Название категории")
    transaction_type = models.ForeignKey(
        TransactionType, 
        on_delete=models.CASCADE, 
        verbose_name="Тип операции",
        related_name='categories'
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.transaction_type})"

class Subcategory(models.Model):
    """Модель для подкатегорий транзакций"""
    name = models.CharField(max_length=100, verbose_name="Название подкатегории")
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        verbose_name="Категория",
        related_name='subcategories'
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.category})"

class Transaction(models.Model):
    """Основная модель для транзакций ДДС"""
    created_date = models.DateField(
        default=timezone.now,
        verbose_name="Дата создания"
    )
    status = models.ForeignKey(
        Status, 
        on_delete=models.PROTECT, 
        verbose_name="Статус"
    )
    transaction_type = models.ForeignKey(
        TransactionType, 
        on_delete=models.PROTECT, 
        verbose_name="Тип операции"
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT, 
        verbose_name="Категория"
    )
    subcategory = models.ForeignKey(
        Subcategory, 
        on_delete=models.PROTECT, 
        verbose_name="Подкатегория"
    )
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Сумма (руб)",
        validators=[MinValueValidator(0.01)]
    )
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
        ordering = ['-created_date', '-created_at']
    
    def __str__(self):
        return f"{self.created_date} - {self.amount} руб - {self.category}"
    
    def get_absolute_url(self):
        return reverse('transaction_list')
    
    @property
    def is_income(self):
        """Проверяет, является ли транзакция пополнением"""
        return self.transaction_type.name.lower() in ['пополнение', 'доход', 'income']