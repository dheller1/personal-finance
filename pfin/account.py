from moneyed import Money, Currency

class Account:
    def __init__(self, name, currency, balance=0):
        if not isinstance(currency, Currency):
            currency = Currency(currency)
        if not isinstance(balance, Money):
            balance = Money(balance, currency)
        if balance.currency != currency:
            raise TypeError('Currency mismatch')

        self.name = name
        self.balance = balance
        self.currency = currency

    def __repr__(self):
        return 'Amount({self.name}, {self.balance}, {self.currency})'.format(self.name, self.balance, self.currency)
