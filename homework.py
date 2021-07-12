import datetime as dt


class Record:
    """Ведет запись входных параметров"""
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if isinstance(date, str):
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        else:
            self.date = dt.date.today()
    

class Calculator:
    """Определяет лимит"""
    def __init__(self, limit) -> None:
        self.limit = limit
        self.records = []

    def add_record(self, record):
        """Добавляет запись"""
        self.records.append(record)

    def get_today_stats(self):
        """Считает сколько потрачено/съедено за сегодня"""
        today = dt.date.today()
        summ = 0
        for record in self.records:
            if record.date == today:
                summ += record.amount
        return summ

    def get_week_stats(self):
        """Считать, сколько потрачено/получено за последние 7 дней"""
        today = dt.date.today()
        last_day = today - dt.timedelta(weeks=1)
        summ = 0
        for record in self.records:
            if last_day < record.date <= today:
                summ += record.amount
        return summ

    def remained(self):
        """Определяет сколько можно потратить/(можно или нужно получть)"""
        return self.limit - self.get_today_stats()


class CashCalculator(Calculator):
    """Калькулятор денег. Курс валют на 11.07.2021"""
    RUB_RATE = 1
    USD_RATE = 74.42
    EURO_RATE = 88.35

    def __init__(self, limit: float):
        """Определяет лимит денег"""
        super().__init__(limit)

    def get_today_cash_remained(self, currency):
        """Принимает траты денег за сегодня"""
        cash_remained = self.remained()
        currencies = {
            'rub': ['руб', self.RUB_RATE],
            'usd': ['USD', self.USD_RATE],
            'eur': ['Euro', self.EURO_RATE]}
        cur_name, cur_rate = currencies.get(currency)
        cash_remained = round(cash_remained / cur_rate, 2)
        if cash_remained > 0:
            return f"На сегодня осталось {cash_remained} {cur_name}"
        elif cash_remained == 0:
            return 'Денег нет, держись'
        else:
            return ('Денег нет, держись: твой долг - '
                    f'{abs(cash_remained)} {cur_name}')


class CaloriesCalculator(Calculator):

    """Калькулятор каллорий"""
    def get_calories_remained(self):
        calories_remained = self.remained()
        if calories_remained > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    'но с общей калорийностью '
                    f'не более {calories_remained} кКал')
        else:
            return 'Хватит есть!'


calor_calc = CaloriesCalculator(100)
calor_calc.add_record(Record(70, 'Макдональдс'))
print(calor_calc.get_calories_remained())

calc_calc1 = CashCalculator(150)
calc_calc1.add_record(Record(100, 'На пиво'))
print(calc_calc1.get_today_cash_remained('eur'))
print(calc_calc1.get_today_cash_remained('usd'))
