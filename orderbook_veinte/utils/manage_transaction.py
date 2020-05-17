#manejo de las transacciones
#manejo de las cantidades 
#manejo de los precios 
#DJANGO MODELS
from django.db.models import Count , Avg , Min ,Sum

from orderbook_veinte.orderbook.models import Transactions ,Orders

class TransactionsManger() :
    """
        Utilities to  general transactions in the orderbook 
    
    """
    def __init__(self, side1 , side2 , qty , price ):
        self.side1 =side1
        self.side2 = side2 
        self.qty = qty 
        self.price = price 
    
    def saving_transactions (self):
        buyer = Orders.objects.get( orderId = self.side1['orderId'])
        seller =Orders.objects.get( orderId = self.side2['orderId'])
        
        if self.qty < seller.qty :
            transaction_type = 'partial'
        elif self.qty == seller.qty :
            transaction_type ='complete'
        else : 
            raise "transaction qty is not valid"
        transaction = Transactions.objects.create(
            buyer = buyer ,
            seller = seller,
            qty = self.qty ,
            type_transaction = transaction_type 

        )

    def get_number_of_transactions(self):
        transactions = Transacctions.objects.count()
        return transactions
    
    def get_number_partial_complete_transactions(self):
        partial = Transactions.objects.filter(type_transaction='partial').count()
        complete = Transactions.objects.filter(type_transaction='complete').count()
        return partial, complete

    def get_avg_transactions_partials(self):
        qty_avg = Transactions.objects.filter(type_transaction='partial').aggregate(Avg('qty'))
        price_avg = Transactions.objects.filter(type_transaction='partial').aggregate(Avg('price'))
        return qty_avg ,price_avg


    






def manage_qty(qty , type_qty = str ):
    unity = 10e8
    if type_qty in ['in' , 'out'] :
        if type_qty == 'in':
            response = float(qty)*unity
        elif type_qty == 'out' :
            response =  float(qty)/unity
        
    return response 

