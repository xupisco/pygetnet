from datetime import datetime, timedelta

import requests
import logging

from . import __version__
from getnet.utils import BaseResponseHandler, GenericResponse
from getnet.services import Generic

SANDBOX = 0
HOMOLOG = 1
PRODUCTION = 2

ENVIRONMENTS = (SANDBOX, HOMOLOG, PRODUCTION)

API_URLS = {
    SANDBOX: "https://api-sandbox.getnet.com.br",
    HOMOLOG: "https://api-homologacao.getnet.com.br",
    PRODUCTION: "https://api.getnet.com.br",
}


class API(BaseResponseHandler):
    '''
    Request params:
     - resource (or path), data  
    '''
    request: requests.Session
    seller_id: str
    client_id: str
    client_secret: str
    environment: int = 0
    access_token: str = None
    access_token_expires: int = None
                 
    def __init__(self,
                 seller_id: str,
                 client_id: str,
                 client_secret: str,
                 environment: int = HOMOLOG):
        
        self.seller_id = seller_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.environment = environment
        self.base_url = API_URLS[environment]
        self.request = requests.Session()
        
        self.request.headers.update({
            "user-agent": "pygetnet-{}".format(__version__),
            "seller_id": self.seller_id,
        })
        
        self._validate_access_token()
        
    def _validate_access_token(self):
        if not self.access_token or \
            self.access_token_expires < datetime.timestamp(datetime.now()):
        
            self.auth()    

    def auth(self) -> None:
        path = "/auth/oauth/v2/token"
        data = {
            "scope": "oob",
            "grant_type": "client_credentials"
        }
        
        response = self.request.post(
            self.base_url + path,
            data = data,
            auth = (self.client_id, self.client_secret),
        )
        
        response_data = response.json()
        
        if (response.status_code != 200):
            raise Exception('Auth error {} ({}): {}'.format(
                response.status_code,
                response_data.get('error'),
                response_data.get('error_description'))
            )
        
        self.access_token = response_data.get("access_token")
        self.access_token_expires = int(
            datetime.timestamp(
                datetime.now() + timedelta(seconds=response_data.get("expires_in"))
            )
        )
        self.request.headers.update(
            {"Authorization": "Bearer {}".format(self.access_token)}
        )
        
    def _prepare_request(self, method='get', **kwargs):
        r = kwargs.get('resource', None)
        path = kwargs.get('path', '')
        data = kwargs.get('data', {})

        r = r[0] if r else None
        
        if not r and not len(path):
            raise Exception("Resource or path MUST be provided!")
        
        self._validate_access_token()
        
        r = r or Generic
        e = r.get_endpoint() or path[0]
        path = path or [e]

        if e not in path:
            path.insert(0, e)
        
        _field = 'qs' if method == 'get' else 'body'

        data = super(API, self).validate_required_params(method, 
            data, r.get_params().get(method, {}).get(_field, {})
        )

        return r, e, '/'.join(path), data
        
    def _parse_response(self, resource, endpoint, response):
        data = super(API, self).validate_response(response.json())
        if data.get('error'):
            return GenericResponse(data)
        
        result = {
            'error': False,
            'total': data.get('total') or len(data.get(endpoint, ['dummy'])),
            'status_code': data.get('status_code', 200),
            '_meta': {
                'page': data.get('page') or 1,
                'limit': data.get('limit') or 100
            }
        }

        response_data = None

        if data.get('total', 0) or data.get(endpoint):        
            if (result.get('total') > 1):
                response_data = { endpoint: [resource(data=fields) for fields in data.get(endpoint)] }
            else:
                response_data = resource(data=data.get(endpoint)[0])
                
        if not response_data:
            response_data = resource(data=data).as_dict()
        
        result.update(response_data)
        return resource(result)
   
    def get(self, *resource, **kwargs):
        kwargs.update({ 'resource': resource })
        r, e, path, data = self._prepare_request(**kwargs)
        
        response = self.request.get(
            self.base_url + '/v1/' + path,
            params = data
        )
        
        return self._parse_response(r, e, response)

    def get_or_create(self, *resource, **kwargs):
        if not kwargs.get('defaults', None):
            raise Exception('You must provide defaults related to the calling Resource with get_or_create.')

        kwargs.update({ 'resource': resource })
        r, e, path, data = self._prepare_request(**kwargs)

        existing = self.get(r, **kwargs)

        if existing.error and existing.status_code != 404:
            raise Exception('Error getting resource.')

        if existing.status_code == 404:
            if not r.can_write():
                raise Exception('The Resource ({}) is read only!'.format(str(r)))
                
            default_data = {'data': kwargs.get('defaults')}
            data.update(default_data)

            created = self.post(r, **data)
            if created.error:
                raise Exception('Error creating resource, response: ' + created.get_error())
            return created, True
        else:
            return existing, False

    def post(self, *resource, **kwargs):
        kwargs.update({ 'resource': resource })
        r, e, path, data = self._prepare_request('post', **kwargs)
        
        response = self.request.post(
            self.base_url + '/v1/' + path,
            json = data,
            headers = {"Content-type": "application/json; charset=utf-8"}
        )
        
        return self._parse_response(r, e, response)
        
    def patch(self, *resource, **kwargs):
        kwargs.update({ 'resource': resource })
        r, e, path, data = self._prepare_request('patch', **kwargs)
        
        response = self.request.patch(
            self.base_url + '/v1/' + path,
            json = data,
            headers = {"Content-type": "application/json; charset=utf-8"}
        )
        
        return self._parse_response(r, e, response)
