import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []
    def add_record(self, record):
        self.records.append(record)
        
    def get_today_stats(self):
        count = 0
        for i in self.records:
            if i.date == dt.datetime.now().date():
                count += i.amount
        return count

    def get_week_stats(self):
        count = 0
        for i in self.records:
            if i.date <= dt.datetime.now().date() and i.date >= dt.datetime.now().date() - dt.timedelta(days=7):
                count += i.amount
        return count

    @property
    def remaining_amount(self):
        return self.limit - self.get_today_stats()

class Record:
    def __init__(self, amount, comment, date = None):
        self.amount = amount
        self.comment = comment
        if date:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        else:
            self.date = dt.datetime.now().date()

class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        if self.get_today_stats() < self.limit:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {self.remaining_amount} кКал'
        return f'Хватит есть!'

class CashCalculator(Calculator):
    USD_RATE = 75.07
    EURO_RATE = 89.31

    @property
    def currency_list(self):
        return {
            'rub': [1, 'руб'],
            'usd': [self.USD_RATE, 'USD'],
            'eur': [self.EURO_RATE, 'Euro']
        }

    def get_today_cash_remained(self, currency):
        self.converted_remaining_amount = round((self.get_today_stats() - self.limit) / self.currency_list[currency][0], 2)
        if self.get_today_stats() < self.limit:
            self.converted_remaining_amount = round(self.remaining_amount / self.currency_list[currency][0], 2)
            return f'На сегодня осталось {self.converted_remaining_amount} {self.currency_list[currency][1]}'
        if self.get_today_stats() == self.limit:
            return f'Денег нет, держись'
        return f'Денег нет, держись: твой долг - {self.converted_remaining_amount} {self.currency_list[currency][1]}'