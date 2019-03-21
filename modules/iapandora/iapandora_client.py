import requests
import logging
from bs4 import BeautifulSoup


class IAPandoraClient:
    url = 'https://iapandora.nl/'

    def __init__(self):
        self.session = requests.session()
        self.username = None
        self.password = None

    def _get_csrf(self, path):
        source = self.session.get('%s%s' % (self.url, path)).text
        soup = BeautifulSoup(source, 'html.parser')
        return soup.find('input', {'name': 'csrfmiddlewaretoken'}).attrs['value']

    def _post(self, path, data={}):
        self.session.headers['X-CSRFToken'] = self.session.cookies.get('csrftoken')
        return self.session.post('%s%s' % (self.url, path), json=data)

    def _get(self, path):
        return self.session.get('%s%s' % (self.url, path))

    def is_logged_in(self):
        return self._get('profile/').status_code == 200

    def login(self, username, password):
        logging.log(logging.INFO, 'Logging in as %s' % username)
        self.username = username
        self.password = password
        csrf = self._get_csrf('auth/login')
        result = self._post('api/auth/login', {
            'csrfmiddlewaretoken': csrf, 'username': username, 'password': password
        })

        if result.status_code != 200:
            return False

        return self.is_logged_in()

    def kill(self, code):
        logging.log(logging.INFO, 'Submitting killcode %s on account %s' %
                    (code, self.username))
        if not self.is_logged_in():
            self.login(self.username, self.password)
        # todo: implement kill logic
        return False

    def puzzle(self, code):
        logging.log(logging.INFO, 'Submitting puzzlecode %s on account %s' %
                    (code, self.username))
        if not self.is_logged_in():
            self.login(self.username, self.password)
        # todo: implement puzzle logic
        return False

