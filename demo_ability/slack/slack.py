#For slack api
import requests

import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

try:
    from urllib.parse import urlencode
except ImportError:  # Python 2
    from urllib import urlencode

try:
    from urllib.parse import parse_qsl
except ImportError:  # Python 2
    try:
        from urlparse import parse_qsl
    except ImportError:  # Python < 2.6
        from cgi import parse_qsl

try:
    string_types = basestring
except NameError:
    string_types = str

class SlackAPI(object):
  def __init__(self, client_id, client_secret, redirect_uri):
    self.client_id = client_id
    self.client_secret = client_secret
    self.redirect_uri = redirect_uri

  def get_auth_url(self, state=None, scope=None):
    scope = scope or []
    url = 'https://slack.com/oauth/authorize'
    qs = {
      'client_id': self.client_id,
      'client_secret': self.client_secret,
      'redirect_uri': self.redirect_uri,
      'scope': ','.join(scope)
    }
    return '%s?%s' % (url, urlencode(qs))

  def get_access_token(self, code):
    url = 'https://slack.com/api/oauth.access'
    qs = {
      'client_id': self.client_id,
      'client_secret': self.client_secret,
      'redirect_uri': self.redirect_uri,
      'code': code
    }

    response = requests.get(url, params=qs)
    status_code = response.status_code
    content = response.content
    print content

    if status_code == 200:
      if content['ok']:
        return content['access_token']
      else:
        return False
    else:
      return False





