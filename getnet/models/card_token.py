from datetime import datetime

from getnet.models import Generic


class CardToken(Generic):
    _endpoint: str = 'tokens/card'
    _required_params = {
        'post': {
            'body': ['card_number', 'customer_id']
        }
    }
    
    def __init__(self, endpoint=None, data={}):
        super().__init__(endpoint=self._endpoint, data=data)
