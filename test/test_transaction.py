import pfin.transaction as ta
import moneyed as mn


def test_transaction():
    eur15 = mn.Money(15, 'EUR')
    i1 = ta.Income(eur15, None)
    i2 = ta.Income(eur15)

    assert i1 == i2
    
    e1 = ta.Expense(-eur15)
    e2 = ta.Expense(eur15)

    assert e1 != e2
    assert i1 != e1
    assert i1 != e2