import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)
        
    def get_today_stats(self):
        count = 0
        today = dt.date.today()
        for record in self.records:
            if record.date == today:
                count += record.amount
        return count

    def get_week_stats(self):
        count = 0
        today = dt.date.today()
        week_ago = today - dt.timedelta(days=7)
        for record in self.records:
            if record.date <= today and record.date >= week_ago:
                count += record.amount
        return count

    @property
    def remaining_amount(self):
        return self.limit - self.get_today_stats()


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is not None:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        else:
            self.date = dt.date.today()


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

        converted_remaining_amount = round(
            (self.get_today_stats() - self.limit) / self.currency_list[currency][0], 2)

        if self.get_today_stats() < self.limit:
            converted_remaining_amount = round(
                self.remaining_amount / self.currency_list[currency][0], 2)
            return f'На сегодня осталось {converted_remaining_amount} {self.currency_list[currency][1]}'
        if self.get_today_stats() == self.limit:
            return f'Денег нет, держись'
        return f'Денег нет, держись: твой долг - {converted_remaining_amount} {self.currency_list[currency][1]}'
