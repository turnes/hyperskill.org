import random
import string
import sqlite3


class BankSystem:
    n = 0

    def __init__(self):
        self.currentAccount = None
        self.conn = sqlite3.connect('card.s3db')
        self.cur = self.conn.cursor()
        self._db_init()

    def __new__(cls):
        if cls.n == 0:
            cls.n += 1
            return object.__new__(cls)
        return None

    def _db_init(self):
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS card (
            id INTERGER NOT NULL,
            number TEXT,
            pin TEXT,
            balance INTERGER DEFAULT 0
        )
        """)

    def _db_create_account(self):
        account = Account()
        self.cur.execute("""
        INSERT INTO card (id, number, pin, balance) VALUES
        (?, ?, ?, ?)
        """, (account.account_number, account.card_number, account.pin, 0))
        self.conn.commit()

    def _db_delete_account(self):
        self.cur.execute("""
        DELETE from card WHERE number=?
        """, (self.currentAccount.card_number,))
        self.conn.commit()

    def _db_add_income(self, card_number, value):
        balance = self._db_get_balance(card_number)
        self.cur.execute("""        
        UPDATE card SET balance=?
        WHERE number = ?
        """, (value + balance, card_number))
        self.conn.commit()
        return True

    def _db_withdraw(self, card_number, value):
        balance = self._db_get_balance(card_number)
        self.cur.execute("""        
        UPDATE card SET balance=?
        WHERE number = ?
        """, (balance - value, card_number))
        self.conn.commit()

    def _db_get_balance(self, card_number):
        self.cur.execute("""
        SELECT balance FROM card 
        WHERE number = ?
        """, (card_number,))
        return self.cur.fetchone()[0]

    def _db_find_account(self, card_number):
        self.cur.execute("""
        SELECT EXISTS (SELECT * FROM card WHERE number=?)
        """, (card_number,))
        return self.cur.fetchone()[0]

    def _transfer(self):
        print('Transfer\n')
        to_card_number = input('Enter card number: ')
        if to_card_number == self.currentAccount.card_number:
            print("You can't transfer money to the same account!")
            return False
        elif not (self.currentAccount.valid_card_number(to_card_number)):
            print("Probably you made mistake in the card number. Please try again!")
            return False
        elif self._db_find_account(to_card_number) == 0:
            print("Such a card does not exist.")
            return False
        amount = int(input("Enter how much money you want to transfer: "))
        balance = self._db_get_balance(self.currentAccount.card_number)
        if amount > balance:
            print("Not enough money!")
            return False
        self._db_add_income(to_card_number, amount)
        self._db_withdraw(self.currentAccount.card_number, amount)
        print("Success!")
        return True

    def _new_account(self):
        account = Account()
        cur = self.conn.cursor()
        cur.execute("""
        INSERT INTO card (id, number, pin, balance)
        VALUES (?, ?, ?, ?)        
        """, (account.account_number, account.card_number, account.pin, account.balance))
        self.conn.commit()
        print(f'Your card has been created'
              f'\nYour card number'
              f'\n{account.card_number}'
              f'\nYour card PIN:'
              f'\n{account.pin}')

    def _auth_user(self, card_number, pin):
        cur = self.conn.cursor()
        cur.execute("""
        SELECT * FROM card
        WHERE number = ? and pin = ?  
        """, (card_number, pin))
        return cur.fetchone()

    def _login(self):
        login_card_number = input('Enter your card number: ')
        login_pin = input('Enter your PIN: ')
        user = self._auth_user(login_card_number, login_pin)
        if user:
            print('You have successfully logged in!')
            self.currentAccount = Account(user[0], user[1], user[2], user[3])
            return True
        else:
            print('Wrong card number or PIN!')
            return False

    def menu(self):
        end_menu = 0
        while not end_menu:
            print(f'''\n1. Create an account
2. Log into account
0. Exit
''')
            choice = int(input())
            if choice == 0:
                end_menu = 1
            elif choice == 1:
                self._new_account()
            elif choice == 2:
                if self._login():
                    end_menu2 = 0
                    while not end_menu2:
                        choice = int(input('''1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
'''))
                        if choice == 0:
                            end_menu2 = 1
                            end_menu = 1
                        elif choice == 1:
                            print(f'Balance: {self._db_get_balance(self.currentAccount.card_number)}')
                        elif choice == 2:
                            income = int(input('Enter income: '))
                            if self._db_add_income(self.currentAccount.card_number, income):
                                print('Income was added!')
                        elif choice == 3:
                            self._transfer()
                        elif choice == 4:
                            self._db_delete_account()
                            print('The account has been closed!')
                            self.currentAccount = None
                            end_menu2 = 1
                        elif choice == 5:
                            self.currentAccount = None
                            end_menu2 = 1
                            print('You have successfully logged out!')
        print("Bye!")
        self.conn.close()


class Account:
    def __init__(self, account_number=None, card_number=None, pin=None, balance=0):
        self.inn = '400000'
        if account_number and card_number and pin and str(balance):
            self.account_number = account_number
            self.card_number = card_number
            self.pin = pin
            self.balance = balance
        else:

            self.account_number = self._generate_id()
            self.checksum = self._generate_checksum()
            self.card_number = self.inn + self.account_number + self.checksum
            self.pin = self._generate_pin()
            self.balance = balance

    def _generate_pin(self):
        return ''.join(random.choices(string.digits, k=4))

    def _generate_id(self):
        return ''.join(random.choices(string.digits, k=9))

    def get_balance(self):
        return self.balance

    def _generate_checksum(self):
        number = list(self.inn + self.account_number)
        total = 0
        for n in range(0, 16, 2):
            number[n] = int(number[n]) * 2
        for n in range(0, 15):
            if int(number[n]) > 9:
                number[n] = int(number[n]) - 9
            total += int(number[n])
        return '0' if total % 10 == 0 else str(10 - total % 10)

    def valid_card_number(self, card_number):
        number = list(card_number[:-1])
        total = 0
        for n in range(0, 16, 2):
            number[n] = int(number[n]) * 2
        for n in range(0, 15):
            if int(number[n]) > 9:
                number[n] = int(number[n]) - 9
            total += int(number[n])
        result = total + int(card_number[-1])
        return True if result % 10 == 0 else False

    def __str__(self):
        print(f'Card Number: {self.card_number}'
              # f'\nINN: {self.inn}'
              f'\nAccount Number: {self.account_number} '
              # f'\nChecksum: {self.checksum}'
              f'\nBalance: {self.balance}')


if __name__ == "__main__":
    atm = BankSystem()
    atm.menu()
