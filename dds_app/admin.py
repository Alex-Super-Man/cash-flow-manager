from django.contrib import admin
from .models import Status, TransactionType, Category, Subcategory, Transaction

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']

@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'transaction_type', 'description', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['name', 'description']

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'description', 'created_at']
    list_filter = ['category', 'category__transaction_type', 'created_at']
    search_fields = ['name', 'description']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'created_date', 'transaction_type', 'category', 'subcategory', 
        'amount', 'status', 'created_at'
    ]
    list_filter = [
        'created_date', 'transaction_type', 'category', 'status', 'created_at'
    ]
    search_fields = ['comment', 'amount']
    date_hierarchy = 'created_date'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('created_date', 'status', 'transaction_type')
        }),
        ('Классификация', {
            'fields': ('category', 'subcategory')
        }),
        ('Финансовая информация', {
            'fields': ('amount', 'comment')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )