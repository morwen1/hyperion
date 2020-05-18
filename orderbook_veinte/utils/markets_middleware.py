from django.http import HttpResponseBadRequest


class MarketMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
    
    
        if "orderbook" in request.path and "bid" or "ask" in request.path:
            keys = request.path.split('/')
            keys = [x for x in keys if x != '']
            qty = keys[3]
            price = keys[4]
            options = {
                "cripto": [
                    'BTC',
                    'LTC',
                    'BSF',
                    'PTR',
                    'DSH'
                ],
                "fiat": [
                    "BSV",
                    "USD",
                    "PAR",
                    "PCH"
                ]}
            if (qty in options['cripto'] or qty in options['fiat']) and (price in options['cripto'] or price in options['fiat']) and price != qty:
                return self.get_response(request)
            else:
                return HttpResponseBadRequest("market not registered  :c ")
        response = self.get_response(request)
        return response