class TransactionPartner:
    def __init__(self, name, is_self=False):
        self.name = name
        self.is_self = is_self


Self = TransactionPartner('Self', True)


class SimpleEqualityMixin:
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False


class _Transaction(SimpleEqualityMixin):
    def __init__(self, net_value, account=None, transaction_partner=None, date=None):
        self.net_value = net_value
        self.account = account
        self.transaction_partner = transaction_partner
        self.date = date

    def affects(self, account):
        return account == self.account

    def affected_accounts(self):
        return self.account if self.account is not None else []

    def net_to_account(self, account):
        if not self.affects(account):
            raise ValueError('Different accounts')
        return self.net_value


class Expense(_Transaction):
    def __init__(self, amount, account=None, receiver=None, date=None):
        super().__init__(-amount, account, receiver, date)


class Income(_Transaction):
    def __init__(self, amount, account=None, sender=None, date=None):
        super().__init__(amount, account, sender, date)


class CarryOver(_Transaction):
    def __init__(self, amount, account_from, account_to, date=None):
        assert amount >= 0.
        super().__init__(amount, Self, date)
        self.account_from = account_from
        self.account_to = account_to

    def affected_accounts(self):
        return [self.account_from, self.account_to]

    def affects(self, account):
        return account == self.account_from or account == self.account_to

    def net_to_account(self, account):
        if not self.affects(account):
            raise ValueError('Different accounts')
        if account is self.account_from:
            return -self.net_value
        elif account is self.account_to:
            return self.net_value

    def split(self):
        """ Split the CarryOver into two simple transactions, one Income and one Expense. """
        pass