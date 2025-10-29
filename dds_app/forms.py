from django import forms
from .models import Transaction, Status, TransactionType, Category, Subcategory

class TransactionForm(forms.ModelForm):
    """Форма для создания и редактирования транзакций"""
    
    class Meta:
        model = Transaction
        fields = [
            'created_date', 'status', 'transaction_type', 
            'category', 'subcategory', 'amount', 'comment'
        ]
        widgets = {
            'created_date': forms.DateInput(
                attrs={
                    'type': 'date', 
                    'class': 'form-control',
                    'required': 'required'
                }
            ),
            'status': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'transaction_type': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required',
                'id': 'id_transaction_type'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required',
                'id': 'id_category'
            }),
            'subcategory': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required',
                'id': 'id_subcategory'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'required': 'required',
                'placeholder': '0.00'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Введите комментарий к транзакции...'
            }),
        }
        labels = {
            'created_date': 'Дата операции',
            'status': 'Статус',
            'transaction_type': 'Тип операции',
            'category': 'Категория',
            'subcategory': 'Подкатегория',
            'amount': 'Сумма (руб)',
            'comment': 'Комментарий'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Устанавливаем начальные queryset для зависимых полей
        if self.instance and self.instance.pk:
            # При редактировании существующей записи
            self.fields['category'].queryset = Category.objects.filter(
                transaction_type=self.instance.transaction_type
            )
            self.fields['subcategory'].queryset = Subcategory.objects.filter(
                category=self.instance.category
            )
        else:
            # При создании новой записи
            self.fields['category'].queryset = Category.objects.none()
            self.fields['subcategory'].queryset = Subcategory.objects.none()
            
            # Если в запросе уже есть transaction_type
            if 'transaction_type' in self.data:
                try:
                    transaction_type_id = int(self.data.get('transaction_type'))
                    self.fields['category'].queryset = Category.objects.filter(
                        transaction_type_id=transaction_type_id
                    )
                except (ValueError, TypeError):
                    pass
            
            if 'category' in self.data:
                try:
                    category_id = int(self.data.get('category'))
                    self.fields['subcategory'].queryset = Subcategory.objects.filter(
                        category_id=category_id
                    )
                except (ValueError, TypeError):
                    pass

class TransactionFilterForm(forms.Form):
    """Форма для фильтрации транзакций"""
    
    start_date = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={
            'type': 'date', 
            'class': 'form-control'
        }),
        label='С'
    )
    
    end_date = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={
            'type': 'date', 
            'class': 'form-control'
        }),
        label='По'
    )
    
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Статус',
        empty_label="Все статусы"
    )
    
    transaction_type = forms.ModelChoiceField(
        queryset=TransactionType.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Тип операции',
        empty_label="Все типы"
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Категория',
        empty_label="Все категории"
    )
    
    subcategory = forms.ModelChoiceField(
        queryset=Subcategory.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Подкатегория',
        empty_label="Все подкатегории"
    )

class ReferenceItemForm(forms.Form):
    """Базовая форма для элементов справочников"""
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите название...'
        }),
        label='Название'
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Введите описание...'
        }),
        label='Описание'
    )