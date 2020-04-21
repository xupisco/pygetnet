from datetime import datetime

from getnet.services import Generic, Customer, Plan


class Charge(Generic):
    _endpoint: str = 'charges'
    
    def __init__(self, data):
        super().__init__(self._endpoint, data=data)


class Subscription(Generic):
    _endpoint: str = 'subscriptions'
    _relations = {
        'customer': Customer,
        'plan': Plan
    }
    
    def __init__(self, data):
        super().__init__(self._endpoint, data=data)
