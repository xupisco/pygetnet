from datetime import datetime

from getnet.models import Generic


class Plan(Generic):
    _endpoint: str = 'plans'
    
    amount: int = 0
    payment_types: list = []
    create_date: datetime = datetime.now()
    period: dict = {}
    
    def __init__(self, endpoint=None, data={}):
        super().__init__(endpoint=self._endpoint, data=data)
