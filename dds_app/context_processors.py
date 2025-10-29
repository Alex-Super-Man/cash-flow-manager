def global_stats(request):
    """Глобальная статистика для всех шаблонов"""
    from .models import Transaction
    from django.db.models import Sum, Q
    
    if request.user.is_authenticated:
        total_income = Transaction.objects.filter(
            transaction_type__name='Пополнение'
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        total_expense = Transaction.objects.filter(
            transaction_type__name='Списание'
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        return {
            'global_balance': total_income - total_expense,
            'global_income': total_income,
            'global_expense': total_expense,
        }
    
    return {}