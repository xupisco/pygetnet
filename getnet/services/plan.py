from datetime import datetime

from getnet.services import Generic


class Plan(Generic):
    '''
    API Doc: https://developers.getnet.com.br/api#tag/Planos
    '''
    _endpoint: str = 'plans'
    _required_params = {
        'post': {
            'body': [
                'seller_id', 'name', 'amount',
                'currency', 'payment_types', 'period'
            ]
        }
    }
    
    amount: int = 0
    payment_types: list = []
    create_date: datetime = datetime.now()
    period: dict = {}
    
    def __init__(self, endpoint=None, data={}):
        super().__init__(endpoint=self._endpoint, data=data)
