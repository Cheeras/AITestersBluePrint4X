class Bank:

    def __init__(self,account_number, balance):
        self.balance = balance #public
        self.__acccount_number = account_number # private

    def check_balance(self):
        print(self.balance)

    def deposit(self,amount):
        self.balance = self.balance + amount

    def show_me_account_number(self,is_auth):
        if is_auth == True:
            print(self.__acccount_number)
        else:
            print("Not Allowed")

icici = Bank(987654321,100)
icici.deposit(1000)
icici.check_balance()
icici.show_me_account_number(True)