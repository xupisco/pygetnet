from getnet.services import Generic, Customer, CustomerAddress


class Credit(Generic):
    """
    API Doc: https://developers.getnet.com.br/api#tag/Pagamento%2Fpaths%2F~1v1~1payments~1credit%2Fpost
    """
    _endpoint: str = 'payments/credit'
    _relations = {
        'customer': Customer,
        'billing_address': CustomerAddress
    }
    _required_params = {
        'post': {
            'body': [
                'amount', 'order', 'customer', 'device',
                'shippings', 'credit'
            ]
        }
    }
    
    def __init__(self, endpoint=None, data={}):
        super().__init__(endpoint=self._endpoint, data=data)
