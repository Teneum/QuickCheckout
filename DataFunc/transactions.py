import json
import datetime as dt

time = dt.datetime.now()
date = time.strftime("%Y-%m-%d")
formatted_time = time.strftime("%d%m%Y-%H%M%S")
prettytime = time.strftime("%d/%m/%Y %H-%M-%S")
transactionfile = './json/transactions.json'

def transaction_data(mode, data):
    if mode.lower() == 'r':
        with open(transactionfile, 'r') as f:
            json_data = json.load(f)
            return json_data 
    elif mode.lower() == 'w':
        with open(transactionfile, 'w') as f:
            json.dump(data, f, indent=4)

class Transactions:
    def __init__(self):
        data = transaction_data('r', data= None)
        if len(data) == 0:
            data['Total_Transactions'] = 0
            transaction_data(mode= 'w', data= data)
        else:
            pass

    def billno(self):
        data = transaction_data(mode='r', data=None)
        billno = data['Total_Transactions'] + 1
        billid = str(billno) + '-' + formatted_time
        return billid

    def newtransaction(self, customer_name, customer_phone, items_bought, total, cashierid):
        data = transaction_data(mode='r', data=None)
        data['Total_Transactions'] += 1

        billid = self.billno()

        data[billid] = {}
        data[billid]['CustomerName'] = customer_name
        data[billid]['CustomerPhone'] = customer_phone
        data[billid]['Date'] = prettytime
        data[billid]['Items'] = items_bought
        data[billid]['Total'] = total
        data[billid]['CashierID'] = cashierid
        transaction_data(mode='w', data=data)

class TransactionHistory:

    def transactionlist(self):
        data = transaction_data(mode='r', data=None)
        lst = [key for key in data]
        del lst[0]
        return lst

    def getdata(self, transaction_id):
        data = transaction_data(mode='r', data=None)
        key = data[transaction_id]
        return key



