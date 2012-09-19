"""
Base module of the extension. Contains basic functions, the Auth object and the
AuthUser base class.
"""

import time, hashlib, datetime
from functools import partial

DEFAULT_HASH_ALGORITHM = hashlib.sha1

DEFAULT_USER_TIMEOUT = 3600

class Auth():
    """
    Extension initialization object containing settings for the extension.
    
    Supported settings:

    - login_url_name: Name of the URL that is used for login. It's used in
      the not_logged_in_callback if provided in the constructor.
    - not_logged_in_callback: Function to call when a user accesses a page
      without being logged in. Normally used to redirect to the login page.
      If a login_url_name is provided, it will by default redirect to that
      url. Otherwise, the default is abort(401).
    - not_permitted_callback: Function to call when a user tries to access
      a page for which he doesn't have the permission. Default: abort(401).
    - hash_algorithm: Algorithm from the hashlib library used for password
      encryption. Default: sha1.
    - user_timeout: Timeout (in seconds) after which the sesion of the user
      expires. Default: 3600. A timeout of 0 means it will never expire.
    - load_role: Function to load a role. Is called with user.role as only
      parameter.
    """

    def __init__(self, app=None, login_url_name=None):
        self.hash_algorithm = DEFAULT_HASH_ALGORITHM
        self.user_timeout = DEFAULT_USER_TIMEOUT
        self.load_role = lambda _: None

auth = Auth()
        
class AuthUser(object):
    """
    Baseclass for a user model. Contains a few convenience methods.

    Attributes:

    - username: Username of the user.
    - password: Password of the user. By default not encrypted. The 
      set_and_encrypt_password() method sets and encrypts the password.
    - salt: Salt used for the encrytion of the password.
    - role: Role of this user.  """

    role = None

    def __init__(self, username=None, password=None, salt=None, role=None):
        self.username = username
        # Storing password unmodified. Encryption of the password should 
        # happen explicitly.
        self.password = password
        self.salt = salt
        self.role = role

    def set_and_encrypt_password(self, password, salt=str(int(time.time()))):
        """
        Encrypts and sets the password. If no salt is provided, a new
        one is generated.
        """
        self.salt = salt
        self.password = encrypt(password, self.salt)

    def authenticate(self, password):
        """
        Attempts to verify the password and log the user in. Returns true if 
        succesful.
        """
        if self.password == encrypt(password, self.salt):
            return True
        return False

    def __eq__(self, other):
        return self.username == getattr(other, 'username', None)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getstate__(self):
        return self.__dict__

def encrypt(password, salt=None, hash_algorithm=None):
    """Encrypts a password based on the hashing algorithm."""
    to_encrypt = password
    if salt is not None:
        to_encrypt += salt
    if hash_algorithm is not None:
        return hash_algorithm(to_encrypt).hexdigest()
    return auth.hash_algorithm(to_encrypt).hexdigest()
