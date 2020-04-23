import redis as red


class OrderTree():
    def __init__(self,  side, baseCurrency, quoteCurrency , red):
        self.side = side
        self.red = red

        #self.KEY_PRICE_TREE = f"prices-{baseCurrency}-{quoteCurrency}-{side}"
        #self.KEY_TEMPLATE_QUOTE = f"quote-{baseCurrency}-{quoteCurrency}"
        #self.KEY_TEMPLATE_PRICE_QUOTES = f"{side}-{baseCurrency}-{quoteCurrency}-{{price}}"


        self.KEY_PRICE_TREE = 'prices-%s-%s-%s' % (baseCurrency, quoteCurrency, side)
        self.KEY_TEMPLATE_QUOTE = 'quote-%s-%s-%%s' % (baseCurrency, quoteCurrency) #quote id
        self.KEY_TEMPLATE_PRICE_QUOTES = '%s-%s-%s-%%s' % (side, baseCurrency, quoteCurrency) #price

    def __len__(self):
        return self.red.zcard(self.KEY_PRICE_TREE) #se trae todos las ordenes por ese precio


    def getPrice(self, price):
        # return self.priceMap[price]
        return self.red.range(self.KEY_TEMPLATE_PRICE_QUOTES, 0,  -1)


    # def removePrice(self, price):
    #    #self.lobDepth -= 1
    #    self.priceTree.remove(price)
    #    del self.priceMap[price]


    def orderExist(self, orderId):

        return self.red.exist(self.KEY_TEMPLATE_QUOTE) #verifica si existe la orden 


    def insertOrder(self, order):
        """
        Al insertar la orden recuerda que tienes que 
        establecer el tiempo en que la orden se inserte
        """
        #import pdb; pdb.set_trace()

        price = order.price
        mapping ={ 'price': price}

        if not self.red.exists(self.KEY_TEMPLATE_PRICE_QUOTES % price):
            self.red.zadd(self.KEY_PRICE_TREE, mapping ) #agrega el precio al zset de los precios

        self.red.hmset(self.KEY_TEMPLATE_QUOTE % order.orderId, order.__dict__)
        self.red.rpush(self.KEY_TEMPLATE_PRICE_QUOTES % price, order.orderId)
        print (self.KEY_PRICE_TREE  , order.orderId, self.KEY_TEMPLATE_QUOTE , self.KEY_TEMPLATE_PRICE_QUOTES)



    def updateOrderQuatity(self, orderId, newQty):
        self.red.hset(self.KEY_TEMPLATE_QUOTE % orderId, 'qty', newQty)
    #    originalVolume = order.qty
    #    self.volume += order.qty-originalVolume
    def removeOrderById(self, orderId):
        #self.nOrders -= 1

        order = self.red.hgetall(self.KEY_TEMPLATE_QUOTE % orderId)

        self.red.lrem(self.KEY_TEMPLATE_PRICE_QUOTES % order['price'], 0, orderId)

        if not self.red.exists(self.KEY_TEMPLATE_PRICE_QUOTES % order['price']):
            self.red.zrem(self.KEY_PRICE_TREE, order['price'])

        self.red.delete(self.KEY_TEMPLATE_QUOTE % orderId)

    def maxPrice(self):
        r = self.red.zrange(self.KEY_PRICE_TREE, 0, 0)
        if r:
            return int(r[0])
        else:
            return 0

    def maxPriceList(self):
        pipe = self.red.pipeline()

        for oreder in self.red.lrange(self.KEY_TEMPLATE_PRICE_QUOTES % self.maxPrice(), 0, -1):
            pipe.hgetall(self.KEY_TEMPLATE_QUOTE % order)

        return pipe.execute()

    def minPriceList(self):
        pipe = self.red.pipeline()
        for order in self.red.lrange(self.KEY_TEMPLATE_PRICE_QUOTES % self.minPrice(), 0, -1):
            pipe.hgetall(self.KEY_TEMPLATE_QUOTE % order)
        return pipe.execute()

    def getQuotes(self, reverse=False, depth=10):
        r = []
        if reverse:
            opp = self.red.zrevrange
        else:
            opp = self.red.zrange

        pipe = self.red.pipeline()
        for price in opp(self.KEY_PRICE_TREE, 0, -1):
            if depth > 0:
                depth -= 1
            else:
                break

            for order in self.red.lrange(self.KEY_TEMPLATE_PRICE_QUOTES % price, 0, -1):
                pipe.hgetall(self.KEY_TEMPLATE_QUOTE % order)

        r += pipe.execute()
        return r
