from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Transaction, Status, TransactionType, Category, Subcategory
from .forms import TransactionForm, TransactionFilterForm

class TransactionListView(ListView):
    """Представление для списка транзакций с фильтрацией"""
    model = Transaction
    template_name = 'dds_app/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 15
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter_form = TransactionFilterForm(self.request.GET)
        
        if self.filter_form.is_valid():
            data = self.filter_form.cleaned_data
            
            # Фильтрация по дате
            if data.get('start_date'):
                queryset = queryset.filter(created_date__gte=data['start_date'])
            if data.get('end_date'):
                queryset = queryset.filter(created_date__lte=data['end_date'])
            
            # Фильтрация по справочникам
            if data.get('status'):
                queryset = queryset.filter(status=data['status'])
            if data.get('transaction_type'):
                queryset = queryset.filter(transaction_type=data['transaction_type'])
            if data.get('category'):
                queryset = queryset.filter(category=data['category'])
            if data.get('subcategory'):
                queryset = queryset.filter(subcategory=data['subcategory'])
        
        return queryset.select_related(
            'status', 'transaction_type', 'category', 'subcategory'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filter_form
        
        # Статистика для отображения
        queryset = self.get_queryset()
        total_income = sum(
            t.amount for t in queryset 
            if t.transaction_type.name.lower() in ['пополнение', 'доход']
        )
        total_expense = sum(
            t.amount for t in queryset 
            if t.transaction_type.name.lower() in ['списание', 'расход']
        )
        
        context.update({
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': total_income - total_expense,
            'total_count': queryset.count()
        })
        
        return context

class TransactionCreateView(CreateView):
    """Представление для создания новой транзакции"""
    model = Transaction
    form_class = TransactionForm
    template_name = 'dds_app/transaction_form.html'
    success_url = reverse_lazy('transaction_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Транзакция успешно создана!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)

class TransactionUpdateView(UpdateView):
    """Представление для редактирования транзакции"""
    model = Transaction
    form_class = TransactionForm
    template_name = 'dds_app/transaction_form.html'
    success_url = reverse_lazy('transaction_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Транзакция успешно обновлена!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)

class TransactionDeleteView(DeleteView):
    """Представление для удаления транзакции"""
    model = Transaction
    template_name = 'dds_app/transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Транзакция успешно удалена!')
        return super().delete(request, *args, **kwargs)

def reference_management(request):
    """Представление для управления справочниками"""
    context = {
        'statuses': Status.objects.all(),
        'transaction_types': TransactionType.objects.all(),
        'categories': Category.objects.select_related('transaction_type').all(),
        'subcategories': Subcategory.objects.select_related('category').all(),
    }
    return render(request, 'dds_app/reference_management.html', context)

def load_categories(request):
    """AJAX view для загрузки категорий по типу операции"""
    transaction_type_id = request.GET.get('transaction_type_id')
    if transaction_type_id:
        categories = Category.objects.filter(transaction_type_id=transaction_type_id)
        return render(request, 'dds_app/category_dropdown_options.html', 
                     {'categories': categories})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def load_subcategories(request):
    """AJAX view для загрузки подкатегорий по категории"""
    category_id = request.GET.get('category_id')
    if category_id:
        subcategories = Subcategory.objects.filter(category_id=category_id)
        return render(request, 'dds_app/subcategory_dropdown_options.html', 
                     {'subcategories': subcategories})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def dashboard(request):
    """Дашборд с общей статистикой"""
    transactions = Transaction.objects.all()
    
    # Базовая статистика
    total_income = sum(t.amount for t in transactions if t.is_income)
    total_expense = sum(t.amount for t in transactions if not t.is_income)
    
    # Статистика по категориям
    category_stats = []
    for category in Category.objects.all():
        category_total = sum(t.amount for t in transactions if t.category == category)
        if category_total > 0:
            category_stats.append({
                'category': category,
                'total': category_total,
                'count': transactions.filter(category=category).count()
            })
    
    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': total_income - total_expense,
        'total_transactions': transactions.count(),
        'recent_transactions': transactions.order_by('-created_date')[:5],
        'category_stats': sorted(category_stats, key=lambda x: x['total'], reverse=True)[:10]
    }
    
    return render(request, 'dds_app/dashboard.html', context)