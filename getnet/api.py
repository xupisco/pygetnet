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
            raise Exception('Auth error {} ({}): {}'.format(response.status_code, response_data.get('error'), response_data.get('error_description')))
        
        self.access_token = response_data.get("access_token")
        self.access_token_expires = int(
            datetime.timestamp(
                datetime.now() + timedelta(seconds=response_data.get("expires_in"))
            )
        )
        self.request.headers.update(
            {"Authorization": "Bearer {}".format(self.access_token)}
        )
        
    def _prepare_request(self, resource, endpoint):
        resource = resource[0] if resource else None
        
        if not resource and not endpoint:
            raise Exception("Resource or endpoint MUST be provided!")
        
        self._validate_access_token()
        
        resource = resource or Generic
        endpoint = resource.get_endpoint() or endpoint
        
        return resource, endpoint
        
    def _parse_response(self, endpoint, resource, response):
        data = super(API, self).validate_response(response.json())
        if data.get('error'):
            return GenericResponse(data)
        
        if data.get('total', 0) or data.get(endpoint):
            result = {
                'error': False,
                'page': data.get('page') or 1,
                'limit': data.get('limit') or 100,
                'total': data.get('total') or len(data.get(endpoint))
            }
        
            if (result.get('total') > 1):
                result.update({ 'results': [resource(data=fields) for fields in data.get(endpoint)] })
                return GenericResponse(result)
            else:
                return GenericResponse({ 'error': False, 'total': 1, 'result': resource(data=data.get(endpoint)[0])})
            
        return GenericResponse({ 'error': False, 'total': 1, 'result': resource(data=data)})
   
     
    def get(self, *resource, endpoint: str = None, path_params: list = [], query_params: dict = {}):
        resource, endpoint = self._prepare_request(resource, endpoint)
        
        if len(path_params):
            path_params.insert(0, '/')
            query_params = {}
        else:
            query_params = super(API, self).validate_required_params('get', 
                query_params,
                resource.get_params().get('get').get('qs')
            )
        
        response = self.request.get(
            self.base_url + '/v1/' + endpoint + ''.join(path_params),
            params = query_params
        )
        
        return self._parse_response(endpoint, resource, response)


    def post(self, *resource, endpoint: str = None, path_params: list = [], payload: dict = {}):
        resource, endpoint = self._prepare_request(resource, endpoint)

        payload = super(API, self).validate_required_params('post', 
            payload,
            resource.get_params().get('post').get('body')
        )
        
        if len(path_params):
            path_params.insert(0, '/')
        
        response = self.request.post(
            self.base_url + '/v1/' + endpoint + ''.join(path_params),
            json = payload,
            headers = {"Content-type": "application/json; charset=utf-8"}
        )
        
        return self._parse_response(endpoint, resource, response)
