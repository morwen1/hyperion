import redis as red


class OrderTree():
    def __init__(self,  side, baseCurrency, quoteCurrency, red):
        self.side = side
        self.red = red

        #self.KEY_PRICE_TREE = f"prices-{baseCurrency}-{quoteCurrency}-{side}"
        #self.KEY_TEMPLATE_QUOTE = f"quote-{baseCurrency}-{quoteCurrency}"
        #self.KEY_TEMPLATE_PRICE_QUOTES = f"{side}-{baseCurrency}-{quoteCurrency}-{{price}}"

        self.KEY_PRICE_TREE = 'prices-%s-%s-%s' % (baseCurrency, quoteCurrency, side) #precios
        self.KEY_TEMPLATE_QUOTE = 'quote-%s-%s-%%s' % (baseCurrency, quoteCurrency)  # cotizacion de una orden o la orden misma
        self.KEY_TEMPLATE_PRICE_QUOTES = '%s-%s-%s-%%s' % (side, baseCurrency, quoteCurrency)  # pricios de cotiziones o ordenes

    def __len__(self):
        return self.red.zcard(self.KEY_PRICE_TREE)  # se trae todos las ordenes por ese precio

    def getPrice(self, price):
        # return self.priceMap[price]
        return self.red.range(self.KEY_TEMPLATE_PRICE_QUOTES, 0,  -1)

    # def removePrice(self, price):
    #    #self.lobDepth -= 1
    #    self.priceTree.remove(price)
    #    del self.priceMap[price]

    def orderExist(self, orderId):

        return self.red.exists(self.KEY_TEMPLATE_QUOTE % orderId)  # verifica si existe la orden

    def insertOrder(self, order):
        """
        Al insertar la orden recuerda que tienes que 
        establecer el tiempo en que la orden se inserte
        """
        #import pdb; pdb.set_trace()

        price = order.price
        mapping = {price : price}

        if not self.red.exists(self.KEY_TEMPLATE_PRICE_QUOTES % price):
            self.red.zadd(self.KEY_PRICE_TREE, mapping)  # agrega el precio al zset de los precios

        #agregar ordenes 
        self.red.hmset(self.KEY_TEMPLATE_QUOTE % order.orderId, order.__dict__)
          # agrega al set de cotizaciones (ordenes)
        self.red.rpush(self.KEY_TEMPLATE_PRICE_QUOTES % price, order.orderId)  # agrega al set precio de las cotizaciones (ordenes)
        print(self.KEY_PRICE_TREE, order.orderId, self.KEY_TEMPLATE_QUOTE, self.KEY_TEMPLATE_PRICE_QUOTES)


    def updateOrderQuatity(self, orderId, newQty):
        self.red.hset(self.KEY_TEMPLATE_QUOTE % orderId, 'qty', newQty)
    #    originalVolume = order.qty
    #    self.volume += order.qty-originalVolume

    def removeOrderById(self, orderId):
        #self.nOrders -= 1

        order = self.red.hgetall(self.KEY_TEMPLATE_QUOTE % orderId)
        order_dep = {}
        for i in order.keys() : 
            order_dep[i.decode()] = order[i].decode()
        


        self.red.lrem(self.KEY_TEMPLATE_PRICE_QUOTES % order_dep['price'], 0, orderId)

        if not self.red.exists(self.KEY_TEMPLATE_PRICE_QUOTES % order_dep['price']):
            self.red.zrem(self.KEY_PRICE_TREE, order_dep['price'])

        self.red.delete(self.KEY_TEMPLATE_QUOTE % orderId)

    def maxPrice(self):

        r = self.red.zrange(self.KEY_PRICE_TREE, 0, 0)
        if r:
            #type(r[0])
            return int(r[0])
        else:
            return 0

    def minPrice (self):
        r = self.red.zrevrange(self.KEY_PRICE_TREE , 0 , 0)
        if r : 
            return int(r[0])
        else : 
            return 0  
  
    def maxPriceList(self):
        orders = []
        dict_order = {}

        for order in self.red.lrange(self.KEY_TEMPLATE_PRICE_QUOTES % self.maxPrice(), 0, -1):
            x = self.red.hgetall(self.KEY_TEMPLATE_QUOTE % int(order))
            for i in x.keys() : 
                dict_order[i.decode()] = x[i].decode()
            orders.append(dict_order)
        return orders

    def minPriceList(self):
        orders = []
        dict_order = {}
        for order in self.red.lrange(self.KEY_TEMPLATE_PRICE_QUOTES % self.minPrice(), 0, -1):

            x = self.red.hgetall(self.KEY_TEMPLATE_QUOTE % int(order))
            for i in x.keys() : 
                dict_order[i.decode()]= x[i].decode()
            orders.append(dict_order)
        return orders 

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
