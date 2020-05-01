from datetime import datetime, date, time
from dateutil import parser


class Generic:
    _endpoint = None
    _writable = True
    _relations = {}
    _required_params = {
        'get': {
            'qs': [],
            'path': []
        },
        'post': {
            'body': []
        }
    }

    def __init__(self, endpoint=None, data={}):
        self._endpoint = endpoint

        for k, v in data.items():
            if getattr(self, k) is not None:
                v = self._match_basic_value_type(v, type(getattr(self, k)))
            if type(v) == dict:
                if self._relations.get(k):
                    v = self._relations.get(k)(data=v)
                else:
                    v = Generic(self._endpoint, v)

            setattr(self, k, v)

    def __getattr__(self, name):
        return None

    def _match_basic_value_type(self, v, t):
        if t is datetime:
            return parser.parse(str(v))
        try:
            return t(v)
        finally:
            return v

    @classmethod
    def get_endpoint(cls):
        return cls._endpoint

    @classmethod
    def get_params(cls):
        return cls._required_params

    @classmethod
    def can_write(cls):
        return cls._writable

    def as_dict(self):
        ad = {}
        for attr in self.__dict__.keys():
            if not attr.startswith('_'):
                try:
                    ad.update({attr: getattr(self, attr).as_dict()})
                except AttributeError:
                    ad.update({attr: getattr(self, attr)})
        return ad
