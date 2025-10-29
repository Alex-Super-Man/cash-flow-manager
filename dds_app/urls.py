from django.urls import path
from . import views

urlpatterns = [
    # Основные маршруты для транзакций
    path('', views.TransactionListView.as_view(), name='transaction_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transactions/create/', views.TransactionCreateView.as_view(), name='transaction_create'),
    path('transactions/<int:pk>/edit/', views.TransactionUpdateView.as_view(), name='transaction_edit'),
    path('transactions/<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='transaction_delete'),
    
    # Управление справочниками
    path('references/', views.reference_management, name='reference_management'),
    
    # AJAX endpoints для динамических форм
    path('ajax/load-categories/', views.load_categories, name='ajax_load_categories'),
    path('ajax/load-subcategories/', views.load_subcategories, name='ajax_load_subcategories'),
]