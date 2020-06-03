
import jwt 
from orderbook_veinte.orderbook.models import AbstractTrader
from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser

class LazyAuthenticated (permissions.BasePermission):
    """
        lazy authentication 
    """

    def has_permission(self, request, view ):
        headers = request.headers 
        if 'Authorization' in headers :
            token = headers['Authorization']

            token = token.replace("Bearer " , '' )
            decoded_token  = jwt.decode(token , algorithms= ['HS256'],verify=False )
            user = AbstractTrader()
            user.trader_id = decoded_token['id']
            request.user = user
            return True

        else :
            return False
    


