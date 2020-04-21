## Simple getnet API wrapper
In development...

### If you want to try
    clone this
    rename .env.exemple to .env
    update the .env file with your credentials
    install dependencies "pip install -r requirements.txt"
    profit!

### API Doc
https://developers.getnet.com.br/api

### Wrapper Doc
This is a simple (and fast) python wrapper for Getnet API. All required fields and parameters must match the documentation.

Required `get`, `post` and `patch` params are in the service class.

There's almost "no" doc needed, all it does is convert calls and responses to python objects, trying to match type and resources. You can call direct the endpoint with the required arguments or extend the base services for yourself (thinking a better way to expose this), see some exemples below:

    import os
    
    from getnet import API
    from getnet.services import Subscription

    api = API(seller_id=os.environ.get('seller_id'),
              client_id=os.environ.get('client_id'),
              client_secret=os.environ.get('client_secret'))

    subs_list = api.get(Subscription)

    if not subs_list.error and subs_list.total > 1:
        for sub in subs_list.subscriptions:
            charges = api.get(endpoint='charges', data={
                'subscription_id': sub.subscription.subscription_id
            })
            
            print(sub.customer.full_name + ': charged ' + str(charges.total) + ' times')

Note that we can call the `get` method with a Resource (see Services) or passing the endpoint string directy.

Creating a subscription plan:

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
    new_plan = api.post(Plan, data=new_plan_data)
    print(new_plan.plan_id)

Be safe!