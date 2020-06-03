import jwt 

from orderbook_veinte.orderbook.models import AbstractTrader

class JwtMiddleware:
    def __init__ (self , get_response):
        self.get_response = get_response 
    
    


    def __call__ (self , request ):
        headers = request.headers 
        if 'Authorization' in headers :
            token = headers['Authorization']

            token = token.replace("Bearer " , '' )
            decoded_token  = jwt.decode(token , algorithms= ['HS256'],verify=False )
            user = AbstractTrader()
            user.trader_id = decoded_token['id']
            request.user = user
        #import pdb; pdb.set_trace()

        return self.get_response(request)
            



