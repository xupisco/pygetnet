from datetime import date

from getnet.services import Generic


class CustomerAddress(Generic):
    def formatted(self):
        return '{}, {} - {}\n{} - {}/{} - {}\nCEP: {}'.format(
            self.street,
            self.number,
            self.complement,
            self.district,
            self.city,
            self.state,
            self.country,
            self.postal_code,
        )


class Customer(Generic):
    _endpoint: str = 'customers'
    _relations = {
        'address': CustomerAddress
    }

    birth_date: date = date.today()
    
    def __init__(self, data):
        super().__init__(self._endpoint, data=data)

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

