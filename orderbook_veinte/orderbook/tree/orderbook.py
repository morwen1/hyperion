import math , time
from io import StringIO


import OrderTree 

__all__ = ['OrderException', 'OrderQuantityError', 'OrderPriceError', 'Bid', 'Ask', 'Trade', 'OrderBook']
#qty = cantidad quantity
# bids = pedidos 
#ask = oferta
class Order():
    def __init__(self , qty , price , traderId , timestamp , orderId):
        self.qty = int(qty)
        self.price = int(price)
        self.traderId = traderId
        self.timestamp = timestamp
        self.orderId = orderId

    
    def processPriceLevel(self, book , tree , orderlist , qtyToTrade):
        """
        takes a price level order list an incoming and matches
        appropiate trade give the order quantity
        """
        trades = []

        for order in orderlist:
            if qtyToTrade <= 0 : 
                break 
            if qtyToTrade < order.qty : 
                tradedQty = qtyToTrade
                # Amend book order
                newBookQty = order.qty - qtyToTrade

                tree.updateOrderQuantity(order , orderId)
                qtyToTrade -= tradedQty

            transactionRecord = {'timestamp' : book.getTimestamp() , 'price':order.price , 'qty':tradeQty}
            if tree.side == 'bid':
                transactionRecord['party1'] = [order.traderId , 'bid' , order.orderId]
                transactionRecord['party2'] = [self.traderId , bid , None]
            else :
                transactionRecord['party1'] = [order.traderId , 'ask' , order.orderId]
                transactionRecord['party2']= [self.traderId , 'bid', None]
            trades.append(transactionRecord)
            return qtyToTrade , trades



        


class Bid(Order):
    def __init__(self , qty , price, traderId , timestamp=None , orderId =None):
        Order.__init__(self ,  qty , price ,traderId , timestamp , orderId)
        self.side = 'bid'
    

    def limitOrder (self, book , bids , asks ):
        trades = [ ]
        orderInBook= None
        qtyToTrade = self.qty
        while (asks  and self.price >= asks.minPrice() and qtyToTrade > 0 ):
            bestPriceAsks = [Ask(x['qty'] , x['price'] , x['traderId'] , x['timestamp'] , x['orderId'] ) for x in ask.minPricelist() ] 
            qtyToTrade , newTrades = self.processPriceLevel(book , asks , bestPriceAsks , qtyToTrade) 
            trades += newTrades
        if qtyToTrade > 0 : 
            self.orderId = book.getNextQuoteId() 
            self.qty = qtyToTrade 
            bids.insertOrder(self)
            orderInBook = self
        return trades , orderInBook

    def maketOrder(self,  book , bids , asks ) :
        trades = []
        qtyToTrade =self.qty 
        while qtyToTrade > 0  and self.tasks : 
            bestPriceAsks = [Ask(x['qty'] , x['price'] , x['traderId'] , x['timestamp'] , x['orderId']) for x in ask.minPriceList()]
            qtyToTrade , newTrades  = self.processPriceLevel(book , asks , bestPriceAsks , qtyToTrade)
            trades =+ trades 
            return trades 


class Ask(Order) : 
    def __init__ (self , qty , price , traderId , timestamp= None , orderId =None):
        Order.__init__(self , qty , price , traderId, timestamp, orderId)
        self.side = 'ask'
    def limitOrder(self ,book , bids , asks):
        trades = [] 
        orderInBook = None 
        qtyToTrade = self.qty 
        while (bids and self.price <= bids.maxPrice() and qtyToTrade > 0):
            bestPriceBids = [Bid(x['qty'] , x['price'] , x['traderId'] , x['timestamp'] ,x['orderId'] ) for x in range bids.maxPriceList()]
            qtyToTrade , newTrades = self.processPriceLevel(book ,  bids , bestPriceBids , qtyToTrade)
            trades += newTrades

        if qtyToTrade > 0 : 
            self.orderId = book.getNextQuoteId()
            self.qty = qtyToTrade
            asks.insertOrder(self)

        return trades , orderInBook

    def marketOrder(self , book , bids , asks ):
        trades = []
        qtyToTrade = self.qty
        while qtyToTrade > 0 and self.bids: 
            bestPriceBids = [Bid(x['qty'] , x['price'] , x['traderId'] , x['timestamp'] , x['orderId']) for x in bids.maxPriceList()]
            qtyToTrade , newTrades , self.processPriceLevel(book , bids , bestPriceBids , qtyToTrade ,  )
            trades += newTrades
    
        return trades
    

