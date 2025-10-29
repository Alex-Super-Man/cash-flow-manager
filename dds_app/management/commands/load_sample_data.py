from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from dds_app.models import Status, TransactionType, Category, Subcategory, Transaction
from decimal import Decimal

class Command(BaseCommand):
    help = 'Загрузка демонстрационных данных в базу'

    def handle(self, *args, **options):
        self.stdout.write('Загрузка демонстрационных данных...')

        # Очистка существующих данных (осторожно!)
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
        category_business = Category.objects.create(
            name='Бизнес',
            transaction_type=type_income,
            description='Доходы от бизнеса'
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
        category_health = Category.objects.create(
            name='Здоровье',
            transaction_type=type_expense,
            description='Медицинские расходы'
        )

        # Создание подкатегорий для зарплаты
        Subcategory.objects.create(
            name='Основная зарплата',
            category=category_salary,
            description='Основная заработная плата'
        )
        Subcategory.objects.create(
            name='Премия',
            category=category_salary,
            description='Премиальные выплаты'
        )
        Subcategory.objects.create(
            name='Аванс',
            category=category_salary,
            description='Авансовые выплаты'
        )

        # Создание подкатегорий для фриланса
        Subcategory.objects.create(
            name='Веб-разработка',
            category=category_freelance,
            description='Проекты по веб-разработке'
        )
        Subcategory.objects.create(
            name='Консультации',
            category=category_freelance,
            description='Консультационные услуги'
        )
        Subcategory.objects.create(
            name='Дизайн',
            category=category_freelance,
            description='Дизайнерские работы'
        )

        # Создание подкатегорий для инвестиций
        Subcategory.objects.create(
            name='Дивиденды',
            category=category_investments,
            description='Дивиденды по акциям'
        )
        Subcategory.objects.create(
            name='Проценты по вкладу',
            category=category_investments,
            description='Процентный доход по банковским вкладам'
        )
        Subcategory.objects.create(
            name='Рост стоимости акций',
            category=category_investments,
            description='Доход от продажи акций'
        )

        # Создание подкатегорий для бизнеса
        Subcategory.objects.create(
            name='Продажи',
            category=category_business,
            description='Доходы от продаж'
        )
        Subcategory.objects.create(
            name='Услуги',
            category=category_business,
            description='Доходы от оказания услуг'
        )

        # Создание подкатегорий для продуктов
        Subcategory.objects.create(
            name='Супермаркет',
            category=category_food,
            description='Покупки в супермаркете'
        )
        Subcategory.objects.create(
            name='Рынок',
            category=category_food,
            description='Покупки на рынке'
        )
        Subcategory.objects.create(
            name='Доставка еды',
            category=category_food,
            description='Заказ готовой еды'
        )

        # Создание подкатегорий для транспорта
        Subcategory.objects.create(
            name='Общественный транспорт',
            category=category_transport,
            description='Проездные билеты, такси'
        )
        Subcategory.objects.create(
            name='Такси',
            category=category_transport,
            description='Поездки на такси'
        )
        Subcategory.objects.create(
            name='Бензин',
            category=category_transport,
            description='Заправка автомобиля'
        )
        Subcategory.objects.create(
            name='Ремонт авто',
            category=category_transport,
            description='Расходы на обслуживание автомобиля'
        )

        # Создание подкатегорий для коммунальных услуг
        Subcategory.objects.create(
            name='Электричество',
            category=category_utilities,
            description='Оплата электроэнергии'
        )
        Subcategory.objects.create(
            name='Вода',
            category=category_utilities,
            description='Оплата водоснабжения'
        )
        Subcategory.objects.create(
            name='Интернет',
            category=category_utilities,
            description='Оплата интернета'
        )
        Subcategory.objects.create(
            name='Мобильная связь',
            category=category_utilities,
            description='Оплата мобильной связи'
        )

        # Создание подкатегорий для развлечений
        Subcategory.objects.create(
            name='Кино',
            category=category_entertainment,
            description='Посещение кинотеатров'
        )
        Subcategory.objects.create(
            name='Рестораны',
            category=category_entertainment,
            description='Посещение ресторанов и кафе'
        )
        Subcategory.objects.create(
            name='Хобби',
            category=category_entertainment,
            description='Расходы на хобби'
        )
        Subcategory.objects.create(
            name='Путешествия',
            category=category_entertainment,
            description='Расходы на путешествия'
        )

        # Создание подкатегорий для здоровья
        Subcategory.objects.create(
            name='Поликлиника',
            category=category_health,
            description='Расходы на медицинские услуги'
        )
        Subcategory.objects.create(
            name='Лекарства',
            category=category_health,
            description='Покупка лекарств'
        )
        Subcategory.objects.create(
            name='Спорт',
            category=category_health,
            description='Расходы на спорт и фитнес'
        )

        # Создание демонстрационных транзакций (доходы)
        income_transactions = [
            {
                'created_date': timezone.now().date().replace(day=1),
                'status': status_completed,
                'transaction_type': type_income,
                'category': category_salary,
                'subcategory': category_salary.subcategories.get(name='Основная зарплата'),
                'amount': Decimal('75000.00'),
                'comment': 'Зарплата за текущий месяц'
            },
            {
                'created_date': timezone.now().date().replace(day=15),
                'status': status_completed,
                'transaction_type': type_income,
                'category': category_salary,
                'subcategory': category_salary.subcategories.get(name='Премия'),
                'amount': Decimal('15000.00'),
                'comment': 'Премия за успешное выполнение проекта'
            },
            {
                'created_date': timezone.now().date().replace(day=10),
                'status': status_completed,
                'transaction_type': type_income,
                'category': category_freelance,
                'subcategory': category_freelance.subcategories.get(name='Веб-разработка'),
                'amount': Decimal('25000.00'),
                'comment': 'Проект по разработке корпоративного сайта'
            },
            {
                'created_date': timezone.now().date().replace(day=20),
                'status': status_completed,
                'transaction_type': type_income,
                'category': category_investments,
                'subcategory': category_investments.subcategories.get(name='Дивиденды'),
                'amount': Decimal('5000.00'),
                'comment': 'Дивиденды по акциям Газпром'
            },
            {
                'created_date': timezone.now().date().replace(day=25),
                'status': status_pending,
                'transaction_type': type_income,
                'category': category_freelance,
                'subcategory': category_freelance.subcategories.get(name='Консультации'),
                'amount': Decimal('8000.00'),
                'comment': 'Консультация по оптимизации базы данных'
            },
        ]

        # Создание демонстрационных транзакций (расходы)
        expense_transactions = [
            {
                'created_date': timezone.now().date().replace(day=2),
                'status': status_completed,
                'transaction_type': type_expense,
                'category': category_food,
                'subcategory': category_food.subcategories.get(name='Супермаркет'),
                'amount': Decimal('7500.00'),
                'comment': 'Продукты на неделю в Пятерочке'
            },
            {
                'created_date': timezone.now().date().replace(day=3),
                'status': status_completed,
                'transaction_type': type_expense,
                'category': category_transport,
                'subcategory': category_transport.subcategories.get(name='Общественный транспорт'),
                'amount': Decimal('2500.00'),
                'comment': 'Проездной на месяц'
            },
            {
                'created_date': timezone.now().date().replace(day=5),
                'status': status_completed,
                'transaction_type': type_expense,
                'category': category_utilities,
                'subcategory': category_utilities.subcategories.get(name='Электричество'),
                'amount': Decimal('4500.00'),
                'comment': 'Оплата за электроэнергию'
            },
            {
                'created_date': timezone.now().date().replace(day=5),
                'status': status_completed,
                'transaction_type': type_expense,
                'category': category_utilities,
                'subcategory': category_utilities.subcategories.get(name='Интернет'),
                'amount': Decimal('800.00'),
                'comment': 'Оплата домашнего интернета'
            },
            {
                'created_date': timezone.now().date().replace(day=8),
                'status': status_completed,
                'transaction_type': type_expense,
                'category': category_entertainment,
                'subcategory': category_entertainment.subcategories.get(name='Кино'),
                'amount': Decimal('1500.00'),
                'comment': 'Поход в кино с друзьями'
            },
            {
                'created_date': timezone.now().date().replace(day=12),
                'status': status_completed,
                'transaction_type': type_expense,
                'category': category_entertainment,
                'subcategory': category_entertainment.subcategories.get(name='Рестораны'),
                'amount': Decimal('3200.00'),
                'comment': 'Ужин в итальянском ресторане'
            },
            {
                'created_date': timezone.now().date().replace(day=15),
                'status': status_completed,
                'transaction_type': type_expense,
                'category': category_transport,
                'subcategory': category_transport.subcategories.get(name='Бензин'),
                'amount': Decimal('3000.00'),
                'comment': 'Заправка автомобиля'
            },
            {
                'created_date': timezone.now().date().replace(day=18),
                'status': status_completed,
                'transaction_type': type_expense,
                'category': category_health,
                'subcategory': category_health.subcategories.get(name='Спорт'),
                'amount': Decimal('2000.00'),
                'comment': 'Абонемент в тренажерный зал'
            },
            {
                'created_date': timezone.now().date().replace(day=22),
                'status': status_completed,
                'transaction_type': type_expense,
                'category': category_food,
                'subcategory': category_food.subcategories.get(name='Доставка еды'),
                'amount': Decimal('1200.00'),
                'comment': 'Заказ пиццы на ужин'
            },
            {
                'created_date': timezone.now().date().replace(day=28),
                'status': status_cancelled,
                'transaction_type': type_expense,
                'category': category_entertainment,
                'subcategory': category_entertainment.subcategories.get(name='Путешествия'),
                'amount': Decimal('25000.00'),
                'comment': 'Отмененная поездка в Сочи'
            },
        ]

        # Создаем все транзакции
        all_transactions = income_transactions + expense_transactions
        
        for data in all_transactions:
            Transaction.objects.create(**data)

        # Создаем демо-пользователя для админки
        if not User.objects.filter(username='demo').exists():
            user = User.objects.create_user(
                username='demo',
                password='demo12345',
                email='demo@example.com',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(
                self.style.SUCCESS(
                    ' Создан демо-пользователь для админки:'
                    '\n   Логин: demo'
                    '\n   Пароль: demo12345'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(' Демо-пользователь уже существует')
            )

        # Выводим итоговую статистику
        self.stdout.write(
            self.style.SUCCESS(
                f'  Успешно загружено:'
                f'\n    {Status.objects.count()} статусов'
                f'\n    {TransactionType.objects.count()} типов операций' 
                f'\n    {Category.objects.count()} категорий'
                f'\n    {Subcategory.objects.count()} подкатегорий'
                f'\n    {Transaction.objects.count()} транзакций'
                f'\n\n    Общий доход: {sum(t.amount for t in Transaction.objects.filter(transaction_type=type_income))} руб'
                f'\n    Общий расход: {sum(t.amount for t in Transaction.objects.filter(transaction_type=type_expense))} руб'
                f'\n    Баланс: {sum(t.amount for t in Transaction.objects.filter(transaction_type=type_income)) - sum(t.amount for t in Transaction.objects.filter(transaction_type=type_expense))} руб'
            )
        )