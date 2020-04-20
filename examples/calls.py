import os

from getnet import API
from getnet.services import Customer, Plan, Subscription, \
    Card, CardToken, VerifyCard


api = API(seller_id=os.environ.get('seller_id'),
          client_id=os.environ.get('client_id'),
          client_secret=os.environ.get('client_secret'))


new_plan = api.post(Plan)


# Fake CC
# 5496963627704751
# 19/10/2021
# 182

token = api.post(CardToken, payload={
    'card_number': '5496963627704751',
    'customer_id': '120398120938'}
)

if not token.error:
    verify = api.post(VerifyCard, payload={
        'number_token': token.result.number_token,
        'expiration_month': 10,
        'expiration_year': 21
    })

    print(verify)

#sub = api.get(Subscription, path_params=['8beb3d07-9169-4e85-b45e-0effa5ed653b'])
#dudes = api.get(Customer, query_params={'limit': 3})
#plans = api.get(Plan)
#cards = api.get(Card, query_params={'customer_id': 'bd06852a-b560-4f53-8808-659f90d8de3e'})
#card = api.get(Card, path_params=['a7aa651a-102c-43a7-ba50-47dc8addddfa'])

pass
