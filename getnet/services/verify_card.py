from datetime import datetime

from getnet.services import Generic


class VerifyCard(Generic):
    _endpoint: str = 'cards/verification'
    _required_params = {
        'post': {
            'body': ['number_token', 'expiration_month', 'expiration_year']
        }
    }
        
    def __init__(self, endpoint=None, data={}):
        super().__init__(endpoint=self._endpoint, data=data)
