from pfin.account import Account
from moneyed import Money, EUR, USD
import pytest


def test_emptyaccount():
    a = Account('Giro', 'EUR')
    assert a.name == 'Giro'
    assert a.currency == EUR
    assert a.balance == Money(0, EUR)


def test_nonemptyaccount():
    u = Account('my Depot', USD, 15.22)
    assert u.currency == USD
    assert u.balance == Money(15.22, USD)


def test_mismatch():
    with pytest.raises(TypeError):
        Account('Cant Decide', 'CNY', Money(13, EUR))
