import math
import time
from datetime import datetime
from io import StringIO


from .OrderTree import OrderTree

#django orm 
from django.db.models import  Q

#models
from orderbook_veinte.orderbook.models import Orders


#__all__ = ['OrderException', 'OrderQuantityError', 'OrderPriceError', 'Bid', 'Ask', 'Trade', 'OrderBook']
# qty = cantidad quantity
# bids = pedidos
#ask = oferta


class Order():
    def __init__(self, qty, price, traderId, timestamp, orderId):
        self.qty = int(qty)
        self.price = int(price)
        self.traderId = traderId
        self.timestamp = timestamp
        self.orderId = orderId
    
   

    def trasactions (self , tr ,newTrades, book , Order) :
        if len(newTrades) != 0 :
            #armo la transaccion en un diccionario para almacenarlo en redis
            tr2 = {}
            temp_id = 0 
            side = ''
            for i in newTrades:
                print("trades  " , i , "\n*3")

                if None in i['party2'] or i['party2'] == {}:

                    i['party2'] = self.__dict__
                    print("party2 testing",i['party2'])
                    tr2 = i['party2']
                    i['party2'].pop('orderId')
                    id_order = Orders.objects.filter(
                        Q(traderId=tr2['traderId']) & Q(price=tr2['price'])
                        ).first().orderId
                    
                    i['party2']['orderId'] = id_order
                    temp_id =i['party1'][2]
                    side = i['party1'][1]
                    i['party1'] = book.getOrderById(temp_id ,side )
                    
                    if i['party1'] == {} :
                        objprt = Orders.objects.filter(orderId = temp_id).last()

                        i['party1']['side'] = side 
                        i['party1']['qty']= objprt.qty
                        i['party1']['price']  =  objprt.price 
                        i['party1']['traderId']  =objprt.traderId
                        i['party1']['orderId']  =objprt.orderId 

                    tr.append(i)
                    

                elif None in i['party1'] or i['party1'] == {}:

                    print(i['party1'])
                    i['party1'] = self.__dict__

                    tr2 = i['party1']
                    i['party1']['orderId'] =Orders.objects.filter(
                        Q(traderId=tr2['traderId']) & Q(price=tr2['price'])
                        ).first().orderId
                    temp_id =i['party2'][2]
                    side = i['party2'][1]
                    i['party2'] = book.getOrderById(temp_id ,side )
                    if i['party2'] == {}  :
                        
                        objprt = Orders.objects.filter(orderId = temp_id).last()
                        
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
            
            if tree.side == 'bid':
                transactionRecord['party1'] = [order.traderId, 'bid', order.orderId]
                transactionRecord['party2'] = [self.traderId, 'ask', None]
            else:
                transactionRecord['party1'] = [order.traderId, 'ask', order.orderId]
                transactionRecord['party2'] = [self.traderId, 'bid',None ]
            trades.append(transactionRecord)
        #print(rades)
        return qtyToTrade, trades

#TODO "verificar las ordenes en que no puedas comprar tu orden"

class Bid(Order):
    def __init__(self, qty, price, traderId, timestamp=None, orderId=None):
        Order.__init__(self,  qty, price, traderId, timestamp, orderId)
        self.side = 'bid'

    def limitOrder(self, book, bids, asks):
        trades = []
        orderInBook = None
        #Consultar saldo del usuario 
        qtyToTrade = self.qty

        while (asks and self.price >= asks.minPrice() and qtyToTrade > 0):
            bestPriceAsks = [Ask(x['qty'], x['price'], x['traderId'], x['timestamp'], x['orderId']) for x in asks.minPriceList()]
            
            qtyToTrade, newTrades = self.processPriceLevel(book, asks, bestPriceAsks, qtyToTrade , self.price)
                                    
            trades = self.trasactions(trades , newTrades , book  ,Order)


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
            bestPriceAsks = [Ask(x['qty'], x['price'], x['traderId'], x['timestamp'], x['orderId']) for x in asks.minPriceList()]
            qtyToTrade, newTrades = self.processPriceLevel(book, asks, bestPriceAsks, qtyToTrade , self.price)
            trades += newTrades
        return trades


class Ask(Order):
    def __init__(self, qty, price, traderId, timestamp=None, orderId=None):
        Order.__init__(self, qty, price, traderId, timestamp, orderId)
        self.side = 'ask'

    def limitOrder(self, book, bids, asks):
        trades = []
        orderInBook = None
        qtyToTrade = self.qty
        while (bids and self.price <= bids.maxPrice() and qtyToTrade > 0):
            bestPriceBids = [Bid(x['qty'], x['price'], x['traderId'], x['timestamp'], x['orderId'])
                             for x in bids.maxPriceList()]
            qtyToTrade, newTrades = self.processPriceLevel(book,  bids, bestPriceBids, qtyToTrade , self.price)
            
            trades = self.trasactions(trades , newTrades , book , Order)
           
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
            bestPriceBids = [Bid(x['qty'], x['price'], x['traderId'], x['timestamp'], x['orderId'])
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

        order.timestamp = self.getTimestamp()

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