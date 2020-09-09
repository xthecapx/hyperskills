# Write your code here
import sqlite3
import random
from sqlite3 import Error


class Bank:
    cards = {}
    messages = {
        'not_logged': """1. Create an account
2. Log into account
0. Exit""",
        'logged': """1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit"""
    }

    def __init__(self):
        self.INN = '400000'
        self.checksum = '9'
        self.bank_state = 'not_logged'
        self.conn = None
        self.current_card = None

    def create_account(self):
        card_id = len(self.cards) + 1
        card_number = f'{card_id}'.zfill(9)
        checksum = self.calculate_checksum(self.INN + card_number)
        account = self.INN + card_number + checksum
        pin = f'{random.randint(0, 9999)}'.zfill(4)
        self.cards[account] = {'pin': pin, 'id': card_id, 'balance': 0}
        print('Your card has been created')
        print('Your card number:')
        print(account)
        print('Your card PIN:')
        print(pin)
        self.create_task((card_id, account, pin, 0))

    def calculate_checksum(self, acct_number):
        number = list(acct_number)
        step_1 = [int(x) * 2 if i % 2 == 0 else int(x)
                  for (i, x) in enumerate(number)]
        step_2 = [x - 9 if x > 9 else x for x in step_1]
        step_3 = 10 - sum(int(num) for num in step_2) % 10
        if step_3 == 10:
            step_3 = 0
        return str(step_3)

    def login(self):
        card = input('Enter your card number:')
        pin = input('Enter your PIN:')

        if card in self.cards and self.cards[card]['pin'] == pin:
            print('You have successfully logged in!')
            self.bank_state = 'logged'
            self.current_card = card
        else:
            print('Wrong card number or PIN!')

    def logout(self):
        self.bank_state = 'not_logged'
        self.current_card = None
        print('You have successfully logged out!')

    def balance(self):
        print(f'Balance: {self.cards[self.current_card]["balance"]}')

    def add_income(self, number, amount=None):
        income = int(input('Enter income:')) if not amount else amount
        card = self.cards[number]
        card["balance"] += income
        self.update_task((card["balance"], card["id"]))
        print('Income was added!')

    def withdraw(self, amount):
        card = self.cards[self.current_card]
        card["balance"] -= amount
        self.update_task((card["balance"], card["id"]))

    def check_receiver(self, card_number):
        temp = list(card_number).copy()
        check_digit = temp.pop()
        index = 0

        for digit in temp:
            if (index + 1) % 2 != 0:
                temp[index] = int(digit) * 2
            index += 1

        index = 0
        for digit in temp:
            if int(digit) > 9:
                temp[index] = int(digit) - 9
            index += 1

        total = 0
        for digit in temp:
            total += int(digit)

        return int(check_digit) == ((total * 9) % 10)

    def do_transfer(self):
        to = input('Enter card number:')

        if to == self.current_card:
            print("You can't transfer money to the same account!")
        elif not self.check_receiver(to):
            print('Probably you made mistake in the card number. Please try again!')
        elif to not in self.cards:
            print("Such a card does not exist.")
        else:
            amount = int(input('Enter how much money you want to transfer:'))

            if amount > self.cards[self.current_card]["balance"]:
                print('Not enough money!')
            else:
                self.add_income(to, amount)
                self.withdraw(amount)
                print('Success!')

    def create_connection(self, db_file):
        try:
            self.conn = sqlite3.connect(db_file)
            return True
        except Error as e:
            print(e)

        return False

    def update_task(self, task):
        sql = ''' UPDATE card
                  SET balance = ? 
                  WHERE id = ?'''
        cur = self.conn.cursor()
        cur.execute(sql, task)
        self.conn.commit()

    def delete_current_account(self):
        card_id = self.cards[self.current_card]['id']
        sql = f'''DELETE FROM card
                  WHERE id={int(card_id)}'''
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
        print('The account has been closed!')

    def create_table(self):
        sql_create_cards_table = """CREATE TABLE IF NOT EXISTS card (
            id integer PRIMARY KEY,
            number text NOT NULL,
            pin text NOT NULL,
            balance integer
        );"""
        try:
            c = self.conn.cursor()
            c.execute(sql_create_cards_table)
        except Error as e:
            print(e)

    def select_all_cards(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM card")
        rows = cur.fetchall()
        # print(rows)

        for row in rows:
            self.cards[row[1]] = {'pin': row[2],
                                  'id': row[0], 'balance': int(row[3])}

    def create_task(self, task):
        sql = 'INSERT INTO card VALUES(?,?,?,?)'
        cur = self.conn.cursor()
        cur.execute(sql, task)
        self.conn.commit()

    def start(self):
        self.create_connection('card.s3db')
        self.create_table()
        self.select_all_cards()

        while True:
            print(self.messages[self.bank_state])
            choice = input()
            print()

            if self.bank_state == 'not_logged':
                if choice == '1':
                    self.create_account()
                elif choice == '2':
                    self.login()
                else:
                    break
            else:
                if choice == '1':
                    self.balance()
                elif choice == '2':
                    self.add_income(self.current_card)
                elif choice == '3':
                    self.do_transfer()
                elif choice == '4':
                    self.delete_current_account()
                elif choice == '5':
                    self.logout()
                else:
                    break

        self.conn.close()


atm = Bank()
atm.start()
print('\nBye!')
