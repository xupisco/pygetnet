from datetime import datetime

from getnet.services import Generic


class CardToken(Generic):
    _endpoint: str = 'tokens/card'
    _required_params = {
        'post': {
            'body': ['card_number',]
        }
    }
        
    def __init__(self, endpoint=None, data={}):
        super().__init__(endpoint=self._endpoint, data=data)


class VerifyCard(Generic):
    _endpoint: str = 'cards/verification'
    _required_params = {
        'post': {
            'body': ['number_token', 'expiration_month', 'expiration_year']
        }
    }
        
    def __init__(self, endpoint=None, data={}):
        super().__init__(endpoint=self._endpoint, data=data)


class Card(Generic):
    _endpoint: str = 'cards'
    _required_params = {
        'get': {
            'qs': ['customer_id']
        }
    }
    
    def __init__(self, endpoint=None, data={}):
        super().__init__(endpoint=self._endpoint, data=data)
