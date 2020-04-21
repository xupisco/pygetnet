class BaseResponseHandler:
    def validate_required_params(self, method, sent, required):
        params = {}
        if method == 'get':
            defaults = {
                'page': 1,
                'limit': 100
            }
            params = {
                'page': sent.get('page', defaults.get('page')),
                'limit': sent.get('limit', defaults.get('limit')),
            }

        if len(sent):
            params.update(sent)
            
        if len(required):
            for param in required:
                if params.get(param) == None:
                    raise Exception('Missing required param: {}'.format(param))
        
        return params
        
    def validate_response(self, data):
        if data.get('status_code', 200) != 200:
            return {
                'error': True,
                'status_code': data.get('status_code'),
                'name': data.get('name'),
                'message': data.get('message')
            }
        
        return data


class GenericResponse:
    def __init__(self, data: dict):
        for k, v in data.items():
            setattr(self, k, v)
            
    def get_error(self):
        if self.error:
            return '{} ({}): {}'.format(self.status_code, self.name, self.message)
        else:
            return False
