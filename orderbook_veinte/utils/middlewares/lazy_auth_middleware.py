import jwt 
from config.settings.base import env
from orderbook_veinte.orderbook.models import AbstractTrader
from django.http import HttpResponseForbidden





class JwtMiddleware:
    def __init__ (self , get_response):
        self.get_response = get_response 
        self.env = env

    


    def __call__ (self , request ):
        headers = request.headers 
        if 'Authorization' in headers :

            token = headers['Authorization']
            sig_key = self.env("SIG_KEY")
            token = token.replace("Bearer " , '' )
            #TODO verify expiration and body of the jwt
            try:
                jwt.decode(token , sig_key, algorithms= ['HS256'] )
            except Exception as e :
                return HttpResponseForbidden( f"(e.e)  {e} ")

            
           
           
        #import pdb; pdb.set_trace()

        return self.get_response(request)
            



