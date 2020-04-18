from datetime import datetime

from getnet.models import Generic, Customer, Plan


class Subscription(Generic):
    _endpoint: str = 'subscriptions'
    _relations = {
        'customer': Customer,
        'plan': Plan
    }
    
    seller_id: str
    order_id: str
    create_date: datetime
    end_date: datetime
    payment_date: datetime
    next_scheduled_date: datetime
    subscription: dict
    customer: Customer
    plan: Plan
    device: dict
    status: str
    status_details: str
    payment: dict
    
    def __init__(self, data):
        super().__init__(self._endpoint, data=data)
