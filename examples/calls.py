import os, json
from datetime import datetime

from getnet import API
from getnet.services import Customer, Plan, Subscription, \
    Card, CardToken, VerifyCard


def load_fixture(name, **kwargs):
    with open(os.path.dirname(__file__) + '/../getnet/fixtures/' + name + '.json', 'r') as f:
        content = f.read()
    f.close()
    
    for k, v in kwargs.items():
        content = content.replace('_var_' + k, v)
        
    return json.loads(content)

api = API(seller_id=os.environ.get('seller_id'),
          client_id=os.environ.get('client_id'),
          client_secret=os.environ.get('client_secret'))


new_plan_data = load_fixture('subscription_plan', seller_id=os.environ.get('seller_id'))
#new_plan = api.post(Plan, data=new_plan_data)

DOCUMENT_TYPES = ['CPF', 'CNPJ']
birth_date = datetime.strptime('18/02/1980', '%d/%m/%Y')
customer_id = 'c7190fd6-1118-4fff-ae44-849cfed00fa5'

dude_data = load_fixture('customer',
                         seller_id=os.environ.get('seller_id'),
                         customer_id=customer_id,
                         document_type=DOCUMENT_TYPES[0],
                         document_number='123456123456')
                         
dude, created = api.get_or_create(Customer,
                                  path=[customer_id],
                                  defaults=dude_data)

print(created)
print(dude.full_name)

subs_list = api.get(Subscription)
plan = api.get(Plan, path=['77aea997-eb43-4f9b-ba8f-5424ea728b17'])

if not subs_list.error and subs_list.total > 1:
    for sub in subs_list.subscriptions:
        charges = api.get(path=['charges'],
                          data={'subscription_id': sub.subscription.subscription_id})

        print(sub.customer.full_name + ': charged ' + str(charges.total) + ' times')

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
