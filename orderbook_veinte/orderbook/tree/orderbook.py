import math
import time
from datetime import datetime
from io import StringIO


from .OrderTree import OrderTree

#django orm 
from django.db.models import  Q

#models
from orderbook_veinte.orderbook.models import Orders , OrderStatus


#__all__ = ['OrderException', 'OrderQuantityError', 'OrderPriceError', 'Bid', 'Ask', 'Trade', 'OrderBook']
# qty = cantidad quantity
# bids = pedidos
#ask = oferta


class Order():
    def __init__(self, qty, price, traderId, hash_order, timestamp, orderId  ):
        self.qty = int(qty)
        self.price = int(price)
        self.traderId = traderId
        self.timestamp = timestamp
        self.orderId = orderId
        self.hash_order = hash_order
    
   

    def trasactions (self , tr ,newTrades, book , Order ) :
        if len(newTrades) != 0 :
            status = OrderStatus.objects.get(status = 'completed')
            #armo la transaccion en un diccionario para almacenarlo en redis
            tr2 = {}
            temp_id = 0 
            side = ''
            for i in newTrades:
                print("trades  " , i , "\n*3")
                temp_id1 =i['party1'][0]
                temp_id2 = i['party2'][0]
                side1 = i['party1'][2]
                side2 = i['party2'][2]
                side1_user = i['party1'][1]
                side2_user = i['party2'][1]
                side1_hash = i['party1'][5]
                side2_hash = i['party2'][5]
                party1_red = book.getOrderById(temp_id1 ,side1 )
                party2_red = book.getOrderById(temp_id1 ,side2 )
                
                print(i)
                
                
                if party1_red == {} :

                    status_open = OrderStatus.objects.get(status ='open')
                    sideprt = (side1=='ask')
                    print(side1_hash)
                    objprt = Orders.objects.filter(hash_order = side1_hash).first()

                    i['party1'] = {}
                    i['party1']['side'] = side 
                    i['party1']['qty']= objprt.qty
                    i['party1']['price']  =  objprt.price 
                    i['party1']['traderId']  =objprt.traderId
                    i['party1']['orderId']  =objprt.orderId 

    
         

               
                if party2_red == {}  :
                    status_closed = OrderStatus.objects.get(status ='open')
                    sideprt = (side2=='ask')
                    
                    objprt = Orders.objects.filter(hash_order = side2_hash ).first()
                    i['party2'] = {}
                    i['party2']['side'] = side 
                    i['party2']['qty']= objprt.qty
                    i['party2']['price']  =  objprt.price 
                    i['party2']['traderId']  =objprt.traderId
                   # i['party2']['timestamp']  =objprt.timestamp
                    i['party2']['orderId']  =objprt.orderId 
          
                tr.append(i)
            print("tr " , tr)
            if self.side == 'bid':
                for trades in tr :
                    book.bids.saveTransaction(trades)
            if self.side == 'ask':
                for trades in tr :
                    book.asks.saveTransaction(trades)
        return tr

    def processPriceLevel(self, book, tree, orderlist, qtyToTrade , priceToTrade):
        """
        takes a price level order list an incoming and matches
        appropiate trade give the order quantity
        """
        trades = []
        
        for order in orderlist:
            print('order' , order.__dict__)
            if qtyToTrade <= 0:
                break
            if qtyToTrade < order.qty:
                tradedQty = qtyToTrade
                # Amend book order
                newBookQty = order.qty - qtyToTrade
                tree.updateOrderQuatity(order.orderId, newBookQty)
                # Incoming done with
            
                qtyToTrade = 0
                
            elif qtyToTrade == order.qty:
                tradedQty = qtyToTrade
                # hit bid or lift ask
                tree.removeOrderById(order.orderId)
                # Incoming done with
                qtyToTrade = 0
                
            else:
                tradedQty = order.qty
                # hit bid or lift ask
                tree.removeOrderById(order.orderId)
                # continue processing volume at this price
                qtyToTrade -= tradedQty
            transactionRecord = {'timestamp': book.getTimestamp(), 'price': order.price, 'qty': tradedQty}
            print(order.orderId , self.orderId)
            if tree.side == 'bid':
                transactionRecord['party1'] = [order.orderId , order.traderId, 'bid',  order.qty , order.timestamp , order.hash_order]
                transactionRecord['party2'] = [self.orderId , self.traderId, 'ask',  self.qty , self.timestamp , self.hash_order]
            else:
                transactionRecord['party1'] = [order.orderId , order.traderId, 'bid',  order.qty , order.timestamp  , order.hash_order]
                transactionRecord['party2'] = [self.orderId , self.traderId, 'ask',  self.qty , self.timestamp , self.hash_order]
            trades.append(transactionRecord)
        #print(rades)
        return qtyToTrade, trades

#TODO "verificar las ordenes en que no puedas comprar tu orden"

class Bid(Order):
    def __init__(self, qty, price, traderId, hash_order , timestamp=None, orderId=None):
        Order.__init__(self,  qty, price, traderId, hash_order, timestamp, orderId)
        self.side = 'bid'


    def limitOrder(self, book, bids, asks):
        trades = []
        orderInBook = None
        #Consultar saldo del usuario 
        qtyToTrade = self.qty

        while (asks and self.price >= asks.minPrice() and qtyToTrade > 0):
            bestPriceAsks = [Ask(x['qty'], x['price'], x['traderId'],x['hash_order'] ,x['timestamp'], x['orderId'] ) for x in asks.minPriceList()]
            
            qtyToTrade, newTrades = self.processPriceLevel(book, asks, bestPriceAsks, qtyToTrade , self.price)
            
                                   
            trades = self.trasactions(trades , newTrades , book  ,Order )

            
        # si la orden no queda en 0 inserta la orden en libro de ordenes 
        #   esperando otra orden

        if qtyToTrade > 0:
            self.orderId = book.getNextQuoteId()
            self.qty = qtyToTrade
            bids.insertOrder(self)
            orderInBook = self
        return trades, orderInBook


    def marketOrder(self, book, bids, asks):
        trades = []
        qtyToTrade = self.qty
        while qtyToTrade > 0 and self.asks:
            bestPriceAsks = [Ask(x['qty'], x['price'], x['traderId'], x['hash_order'],x['timestamp'], x['orderId'] ) for x in asks.minPriceList()]
            qtyToTrade, newTrades = self.processPriceLevel(book, asks, bestPriceAsks, qtyToTrade , self.price)
            trades += newTrades
        return trades


class Ask(Order):
    def __init__(self, qty, price, traderId , hash_order , timestamp=None, orderId=None ):
        Order.__init__(self, qty, price, traderId, hash_order , timestamp, orderId )
        self.side = 'ask'
        

    def limitOrder(self, book, bids, asks):
        trades = []
        orderInBook = None
        qtyToTrade = self.qty
        while (bids and self.price <= bids.maxPrice() and qtyToTrade > 0):
            bestPriceBids = [Bid(x['qty'], x['price'], x['traderId'], x['hash_order'] , x['timestamp'], x['orderId'] )
                             for x in bids.maxPriceList()]
            print('prices',bestPriceBids[0].__dict__)

            qtyToTrade, newTrades = self.processPriceLevel(book,  bids, bestPriceBids, qtyToTrade , self.price)
            
            trades = self.trasactions(trades , newTrades , book , Order )
           
        # si la orden no queda en 0 inserta la orden en libro de ordenes 
        #   esperando otra orden

        if qtyToTrade > 0:
            self.orderId = book.getNextQuoteId()
            self.qty = qtyToTrade
            asks.insertOrder(self)
            orderInBook = self


        return trades, orderInBook

    def marketOrder(self, book, bids, asks):
        trades = []
        qtyToTrade = self.qty
        while qtyToTrade > 0 and self.bids:
            bestPriceBids = [Bid(x['qty'], x['price'], x['traderId'], x['timestamp'], x['orderId'] )
                             for x in bids.maxPriceList()]
            qtyToTrade, newTrades = self.processPriceLevel(book, bids, bestPriceBids, qtyToTrade, self.price)
            trades += newTrades

        return trades


class Trade ():
    def __init__(self, qty, price, timestamp,
                 p1_traderId, p1_side, p1_orderId,
                 p2_traderId, p2_side, p2_orderId):
        self.qty = qty
        self.price = price
        self.p1_traderId = p1_traderId
        self.p1_side = p1_side
        self.p1_orderId = p1_orderId
        self.p2_traderId = p2_traderId
        self.p2_side = p2_side
        self.p2_orderId = p2_orderId


class OrderBook():
    def __init__(self, baseCurrency, quoteCurrency, red, tickSize=0.0001):
        self.red = red
        self.tickSize = tickSize
        self.tape = []
        self.bids = OrderTree('bid',  baseCurrency, quoteCurrency, red)
        self.asks = OrderTree('ask', baseCurrency, quoteCurrency, red)
        self._lastTimestamp = None  # private variable DONT TOUCH
        self.KEY_COUNTER_ORDER_ID = f'counter:{baseCurrency}-{quoteCurrency}-orderId'

    def processOrder(self, order):
        orderInBook = None
        if order.qty <= 0:
            raise BaseException('order.qty must be > 0 ')

        if order.price < 0:
            raise BaseException('order.qty must be > 0')

        #order.timestamp = self.getTimestamp()

        trades, orderInBook = order.limitOrder(self, self.bids, self.asks)

        return trades, orderInBook

    def cancelOrder(self, side, orderId):
        """
            depende de en que parte del arbol este la orden 
            remueve la orden y arbol se ajusta
        """
        if self.side == 'bid':
            self.bids.removeOrderById(orderId)
        elif side == 'asks':
            self.asks.removeOrderById(orderId)


    def getBestBid(self):
        return self.bids.maxPrice()

    def getWorstBid(self):
        return self.bids.minPrice()

    def getBestAsk(self):
        return self.asks.maxPrice()
    
    def getWorstAsk(self):
        return self.asks.minPrice()



    def getOrderById (self , orderId , side):
        if side == 'bid':

            order = self.bids.getOrderById(orderId)
        
        elif side =='ask':
            order = self.asks.getOrderById(orderId)

        else :
            order = {}

        return order

    def _clipPrice(self, price):
        """clips the price according to the ticketsize """
        return round(price, int(math.long10(1 / self.ticketsize)))
    
    def getTimestamp(self):
        t = time.time()
        while t == self._lastTimestamp:
            t = time.time()
        self._lastTimestamp = t
        return t

    def getNextQuoteId(self):
        return self.red.incr(self.KEY_COUNTER_ORDER_ID)
