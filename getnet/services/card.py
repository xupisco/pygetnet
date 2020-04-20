from datetime import datetime

from getnet.services import Generic


class Card(Generic):
    _endpoint: str = 'cards'
    _required_params = {
        'get': {
            'qs': ['customer_id']
        }
    }
    
    def __init__(self, endpoint=None, data={}):
        super().__init__(endpoint=self._endpoint, data=data)
