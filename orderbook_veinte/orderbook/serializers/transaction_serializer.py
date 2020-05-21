from rest_framework import serializers
from orderbook_veinte.orderbook.models import Transactions 


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields= ['id','qty' , 'price','type_transaction']

