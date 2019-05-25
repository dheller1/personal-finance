from pfin.transaction import Transaction, Expense, Income
from pfin.category import TransactionCategory
from tablib import Dataset, Databook
import io
import os


class MyCustomFormatImportSheet:
    HeaderToTransactionMember = {'Betrag': 'net_value', 'Modus': 'account', 'Laden': 'transaction_partner',
                     'Zweck': 'description'}
    ExpectedHeaders = ['', 'Betrag', 'Modus', 'Laden', 'Zweck', 'Kat. primär', 'Kat. sek.']

    def __init__(self, sheet):
        """ Helper class to handle imported sheets from the custom table format. """
        self._sheet = sheet
        self._transactions = list()

        self._sheet.headers = self._sheet[3]  # init headers
        self._strip_irrelevant_columns()
        for header, expected in zip(self._sheet.headers, self.ExpectedHeaders):
            if header != expected:
                raise ValueError('Badly formatted sheet')

        self._strip_header_rows()

    def _strip_irrelevant_columns(self):
        """ Find the first column without a header (excluding the very first one),
        then strip all further columns from there. """
        relevant_cols = self._sheet.width
        for col, header in enumerate(self._sheet.headers):
            if col >= 1 and not header:
                relevant_cols = col
                break

        self._sheet = self._sheet.subset(cols=self._sheet.headers[:relevant_cols])

    def _strip_header_rows(self):
        while not self._sheet[0][0].strip():  # remove rows until the first date appears
            self._sheet.lpop()

    def generate_transactions(self):
        # Dates in a row propagate downwards to the following rows, until another date appears.
        self._transactions = []

        lastdate = None
        for row in self._sheet:
            if row[0]:
                lastdate = row[0]
                assert not self._is_valid_transaction(row)  # dates should not appear yet in actual transaction rows.
            elif self._is_valid_transaction(row):
                self._transactions.append(self._make_transaction(row, lastdate))

    def _make_transaction(self, row, date):
        """ Factory function to create Transaction instances from a given row in the dataset. """
        ta_dict = dict(date=date)

        cat_prim, cat_sec = None, None
        for header, content in zip(self.ExpectedHeaders[1:], row[1:]):
            if header in self.HeaderToTransactionMember:
                dictentry = self.HeaderToTransactionMember[header]
                value = content.strip()
                ta_dict[dictentry] = value
            elif header == self.ExpectedHeaders[-2]:  # Kat. prim.
                cat_prim = content.strip()
            elif header == self.ExpectedHeaders[-1]:  # Kat. sek.
                cat_sec = content.strip()

        assert cat_prim and cat_sec
        ta_dict['category'] = TransactionCategory(cat_prim, cat_sec)

        return Transaction(**ta_dict)


    @classmethod
    def _is_valid_transaction(cls, row):
        """ Check in a given `row` that content exists for each column with an expected header. """
        for col in row[1:len(cls.ExpectedHeaders)]:  # first col is date which is not yet written
            if not col.strip():
                return False
        return True



def test_tablibimport():
    importdir = os.path.join('..', 'private')
    files_to_import = list()

    for fname in os.listdir(importdir):
        if os.path.splitext(fname)[1].lower() == '.csv':
            files_to_import.append(os.path.join(importdir, fname))

    allsheets = list()
    for fname in files_to_import:
        with io.open(fname, encoding='utf-8') as f:
            sheet = MyCustomFormatImportSheet(Dataset().load(f.read()))
            sheet.generate_transactions()
            allsheets.append(sheet)

    assert len(allsheets) == len(files_to_import) == 27




    #print(book.sheets()[0].width, book.sheets()[0].height)
    #print(book.sheets()[0].get_col(1))
    #print('0:1:5: ' + book.sheets()[0][10][1])
