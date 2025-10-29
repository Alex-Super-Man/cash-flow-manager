from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
from .models import Status, TransactionType, Category, Subcategory, Transaction

class ModelTests(TestCase):
    def setUp(self):
        """Настройка тестовых данных"""
        self.status = Status.objects.create(name="Выполнено")
        self.income_type = TransactionType.objects.create(name="Пополнение")
        self.expense_type = TransactionType.objects.create(name="Списание")
        
        self.category_income = Category.objects.create(
            name="Зарплата", 
            transaction_type=self.income_type
        )
        self.category_expense = Category.objects.create(
            name="Продукты", 
            transaction_type=self.expense_type
        )
        
        self.subcategory_income = Subcategory.objects.create(
            name="Основная зарплата",
            category=self.category_income
        )
        self.subcategory_expense = Subcategory.objects.create(
            name="Супермаркет",
            category=self.category_expense
        )

    def test_status_creation(self):
        """Тест создания статуса"""
        self.assertEqual(str(self.status), "Выполнено")
        self.assertEqual(self.status.name, "Выполнено")

    def test_transaction_type_creation(self):
        """Тест создания типа операции"""
        self.assertEqual(str(self.income_type), "Пополнение")
        self.assertEqual(self.income_type.name, "Пополнение")

    def test_category_creation(self):
        """Тест создания категории"""
        self.assertEqual(str(self.category_income), "Зарплата (Пополнение)")
        self.assertEqual(self.category_income.transaction_type, self.income_type)

    def test_subcategory_creation(self):
        """Тест создания подкатегории"""
        self.assertEqual(str(self.subcategory_income), "Основная зарплата (Зарплата (Пополнение))")
        self.assertEqual(self.subcategory_income.category, self.category_income)

    def test_transaction_creation(self):
        """Тест создания транзакции"""
        transaction = Transaction.objects.create(
            created_date=timezone.now().date(),
            status=self.status,
            transaction_type=self.income_type,
            category=self.category_income,
            subcategory=self.subcategory_income,
            amount=Decimal('1000.00')
        )
        
        self.assertEqual(transaction.amount, Decimal('1000.00'))
        self.assertTrue(transaction.is_income)
        self.assertFalse(transaction.transaction_type == self.expense_type)

    def test_transaction_string_representation(self):
        """Тест строкового представления транзакции"""
        transaction = Transaction.objects.create(
            created_date=timezone.now().date(),
            status=self.status,
            transaction_type=self.income_type,
            category=self.category_income,
            subcategory=self.subcategory_income,
            amount=Decimal('1000.00')
        )
        
        self.assertIn('1000.00', str(transaction))
        self.assertIn('Зарплата', str(transaction))

class ViewTests(TestCase):
    def setUp(self):
        """Настройка клиента и тестовых данных"""
        self.client = Client()
        self.status = Status.objects.create(name="Выполнено")
        self.income_type = TransactionType.objects.create(name="Пополнение")
        self.category = Category.objects.create(
            name="Зарплата", 
            transaction_type=self.income_type
        )
        self.subcategory = Subcategory.objects.create(
            name="Основная зарплата",
            category=self.category
        )

    def test_dashboard_view(self):
        """Тест главной страницы"""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dds_app/dashboard.html')
        self.assertContains(response, 'Финансовый дашборд')

    def test_transaction_list_view(self):
        """Тест страницы списка транзакций"""
        response = self.client.get(reverse('transaction_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dds_app/transaction_list.html')
        self.assertContains(response, 'Управление транзакциями')

    def test_transaction_create_view(self):
        """Тест страницы создания транзакции"""
        response = self.client.get(reverse('transaction_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dds_app/transaction_form.html')
        self.assertContains(response, 'Создание новой транзакции')

    def test_reference_management_view(self):
        """Тест страницы управления справочниками"""
        response = self.client.get(reverse('reference_management'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dds_app/reference_management.html')
        self.assertContains(response, 'Управление справочниками')

class FormTests(TestCase):
    def setUp(self):
        """Настройка тестовых данных для форм"""
        self.status = Status.objects.create(name="Выполнено")
        self.income_type = TransactionType.objects.create(name="Пополнение")
        self.expense_type = TransactionType.objects.create(name="Списание")
        
        self.category_income = Category.objects.create(
            name="Зарплата", 
            transaction_type=self.income_type
        )
        self.subcategory_income = Subcategory.objects.create(
            name="Основная зарплата",
            category=self.category_income
        )

    def test_valid_transaction_form(self):
        """Тест валидной формы транзакции"""
        from .forms import TransactionForm
        
        form_data = {
            'created_date': timezone.now().date(),
            'status': self.status.id,
            'transaction_type': self.income_type.id,
            'category': self.category_income.id,
            'subcategory': self.subcategory_income.id,
            'amount': '1000.00',
            'comment': 'Тестовая транзакция'
        }
        
        form = TransactionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_transaction_form(self):
        """Тест невалидной формы транзакции"""
        from .forms import TransactionForm
        
        form_data = {
            'created_date': timezone.now().date(),
            'status': self.status.id,
            'transaction_type': self.income_type.id,
            # Пропущены обязательные поля
            'amount': '',  # Пустая сумма
        }
        
        form = TransactionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('amount', form.errors)
        self.assertIn('category', form.errors)
        self.assertIn('subcategory', form.errors)

class URLTests(TestCase):
    def test_urls(self):
        """Тест доступности URL-адресов"""
        urls = [
            reverse('dashboard'),
            reverse('transaction_list'),
            reverse('transaction_create'),
            reverse('reference_management'),
        ]
        
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"URL {url} недоступен")