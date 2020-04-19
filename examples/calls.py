import os

from getnet import API
from getnet.models import Customer, Plan, Subscription, Card, CardToken


api = API(seller_id=os.environ.get('seller_id'),
          client_id=os.environ.get('client_id'),
          client_secret=os.environ.get('client_secret'))

sub = api.get(resource=Subscription,
              path_params=['8beb3d07-9169-4e85-b45e-0effa5ed653b'])

token = api.post(resource=CardToken, payload={
    'card_number': '123',
    'customer_id': '120398120938'}
)

plans = api.get(resource=Plan)

if token.error:
    print(token.get_error())

#dudes = api.get(resource=Customer, query_params={'limit': 3})
#plans = api.get(resource=Plan)
#cards = api.get(resource=Card, query_params={'customer_id': 'bd06852a-b560-4f53-8808-659f90d8de3e'})
#card = api.get(resource=Card, path_params=['a7aa651a-102c-43a7-ba50-47dc8addddfa'])
