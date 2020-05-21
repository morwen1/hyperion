from rest_framework import serializers
from orderbook_veinte.orderbook.models import Transactions 


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields= ['qty' , 'price','type_transaction']

