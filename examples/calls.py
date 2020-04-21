import os

from getnet import API
from getnet.services import Customer, Plan, Subscription, \
    Card, CardToken, VerifyCard


api = API(seller_id=os.environ.get('seller_id'),
          client_id=os.environ.get('client_id'),
          client_secret=os.environ.get('client_secret'))


new_plan_data = {
    'seller_id': os.environ.get('seller_id'),
    'name': 'New wrapper test',
    'amount': 1,
    'currency': 'BRL',
    'payment_types': ['credit_card'],
    'period': {
        'type': 'monthly',
        'billing_cycle': 0
    }
}
#new_plan = api.post(Plan, data=new_plan_data)

subs_list = api.get(Subscription)

if not subs_list.error and subs_list.total > 1:
    for sub in subs_list.subscriptions:
        print(sub.customer.full_name)

# Fake CC
# 5496963627704751
# 19/10/2021
# 182

#sub = api.get(Subscription, path=['8beb3d07-9169-4e85-b45e-0effa5ed653b'])
#dudes = api.get(Customer, data={'limit': 3})
#plans = api.get(Plan)
#plan = api.get(Plan, path=['77aea997-eb43-4f9b-ba8f-5424ea728b17'])
#cards = api.get(Card, data={'customer_id': 'bd06852a-b560-4f53-8808-659f90d8de3e'})
#card = api.get(Card, path=['a7aa651a-102c-43a7-ba50-47dc8addddfa'])

pass
