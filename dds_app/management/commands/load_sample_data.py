from django.core.management.base import BaseCommand
from django.utils import timezone
from dds_app.models import Status, TransactionType, Category, Subcategory, Transaction
from decimal import Decimal

class Command(BaseCommand):
    help = 'Загрузка демонстрационных данных в базу'

    def handle(self, *args, **options):
        self.stdout.write('Загрузка демонстрационных данных...')

        # Очистка существующих данных
        Transaction.objects.all().delete()
        Subcategory.objects.all().delete()
        Category.objects.all().delete()
        TransactionType.objects.all().delete()
        Status.objects.all().delete()

        # Создание статусов
        status_completed = Status.objects.create(
            name='Выполнено',
            description='Операция успешно выполнена'
        )
        status_pending = Status.objects.create(
            name='Ожидание',
            description='Операция ожидает выполнения'
        )
        status_cancelled = Status.objects.create(
            name='Отменено',
            description='Операция отменена'
        )

        # Создание типов операций
        type_income = TransactionType.objects.create(
            name='Пополнение',
            description='Поступление денежных средств'
        )
        type_expense = TransactionType.objects.create(
            name='Списание',
            description='Расход денежных средств'
        )

        # Создание категорий для доходов
        category_salary = Category.objects.create(
            name='Зарплата',
            transaction_type=type_income,
            description='Доходы от основной деятельности'
        )
        category_freelance = Category.objects.create(
            name='Фриланс',
            transaction_type=type_income,
            description='Дополнительные доходы'
        )
        category_investments = Category.objects.create(
            name='Инвестиции',
            transaction_type=type_income,
            description='Доходы от инвестиций'
        )

        # Создание категорий для расходов
        category_food = Category.objects.create(
            name='Продукты',
            transaction_type=type_expense,
            description='Расходы на питание'
        )
        category_transport = Category.objects.create(
            name='Транспорт',
            transaction_type=type_expense,
            description='Расходы на транспорт'
        )
        category_utilities = Category.objects.create(
            name='Коммунальные услуги',
            transaction_type=type_expense,
            description='Расходы на ЖКХ'
        )
        category_entertainment = Category.objects.create(
            name='Развлечения',
            transaction_type=type_expense,
            description='Расходы на отдых и развлечения'
        )

        # Создание подкатегорий для зарплаты
        Subcategory.objects.create(
            name='Основная зарплата',
            category=category_salary
        )
        Subcategory.objects.create(
            name='Премия',
            category=category_salary
        )

        # Создание подкатегорий для фриланса
        Subcategory.objects.create(
            name='Веб-разработка',
            category=category_freelance
        )
        Subcategory.objects.create(
            name='Консультации',
            category=category_freelance
        )

        # Создание подкатегорий для инвестиций
        Subcategory.objects.create(
            name='Дивиденды',
            category=category_investments
        )
        Subcategory.objects.create(
            name='Проценты по вкладу',
            category=category_investments
        )

        # Создание подкатегорий для продуктов
        Subcategory.objects.create(
            name='Супермаркет',
            category=category_food
        )
        Subcategory.objects.create(
            name='Рынок',
            category=category_food
        )

        # Создание подкатегорий для транспорта
        Subcategory.objects.create(
            name='Общественный транспорт',
            category=category_transport
        )
        Subcategory.objects.create(
            name='Такси',
            category=category_transport
        )
        Subcategory.objects.create(
            name='Бензин',
            category=category_transport
        )

        # Создание подкатегорий для коммунальных услуг
        Subcategory.objects.create(
            name='Электричество',
            category=category_utilities
        )
        Subcategory.objects.create(
            name='Вода',
            category=category_utilities
        )
        Subcategory.objects.create(
            name='Интернет',
            category=category_utilities
        )

        # Создание подкатегорий для развлечений
        Subcategory.objects.create(
            name='Кино',
            category=category_entertainment
        )
        Subcategory.objects.create(
            name='Рестораны',
            category=category_entertainment
        )
        Subcategory.objects.create(
            name='Хобби',
            category=category_entertainment
        )

        # Создание демонстрационных транзакций
        transactions_data = [
            # Доходы
            {
                'created_date': timezone.now().date(),
                'status': status_completed,
                'transaction_type': type_income,
                'category': category_salary,
                'subcategory': category_salary.subcategories.first(),
                'amount': Decimal('75000.00'),
                'comment': 'Зарплата за январь'
            },
            {
                'created_date': timezone.now().date(),
                'status': status_completed,
                'transaction_type': type_income,
                'category': category_freelance,
                'subcategory': category_freelance.subcategories.first(),
                'amount': Decimal('25000.00'),
                'comment': 'Проект по веб-разработке'
            },
            {
                'created_date': timezone.now().date(),
                'status': status_pending,
                'transaction_type': type_income,
                'category': category_investments,
                'subcategory': category_investments.subcategories.first(),
                'amount': Decimal('5000.00'),
                'comment': 'Дивиденды по акциям'
            },

            # Расходы
            {
                'created_date': timezone.now().date(),
                'status': status_completed,
                'transaction_type': type_expense,
                'category': category_food,
                'subcategory': category_food.subcategories.first(),
                'amount': Decimal('7500.00'),
                'comment': 'Продукты на неделю'
            },
            {
                'created_date': timezone.now().date(),
                'status': status_completed,
                'transaction_type': type_expense,
                'category': category_transport,
                'subcategory': category_transport.subcategories.first(),
                'amount': Decimal('2500.00'),
                'comment': 'Проездной на месяц'
            },
            {
                'created_date': timezone.now().date(),
                'status': status_completed,
                'transaction_type': type_expense,
                'category': category_utilities,
                'subcategory': category_utilities.subcategories.first(),
                'amount': Decimal('4500.00'),
                'comment': 'Оплата за электричество'
            },
            {
                'created_date': timezone.now().date(),
                'status': status_completed,
                'transaction_type': type_expense,
                'category': category_entertainment,
                'subcategory': category_entertainment.subcategories.first(),
                'amount': Decimal('1500.00'),
                'comment': 'Поход в кино'
            },
        ]

        for data in transactions_data:
            Transaction.objects.create(**data)

        self.stdout.write(
            self.style.SUCCESS(
                f'Успешно загружено: '
                f'{Status.objects.count()} статусов, '
                f'{TransactionType.objects.count()} типов операций, '
                f'{Category.objects.count()} категорий, '
                f'{Subcategory.objects.count()} подкатегорий, '
                f'{Transaction.objects.count()} транзакций'
            )
        )