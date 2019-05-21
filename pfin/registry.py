class Registry:
    def __init__(self):
        self._categories = set()
        self._accounts = set()
        self._transactions = list()

    def add_transaction(self, ta):
        self._transactions.append(ta)
        self._categories.add(ta.category)
        self._accounts.update(ta.affected_accounts())
