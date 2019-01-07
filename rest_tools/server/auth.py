import time
import jwt

class Auth:
    """
    Handle authentication of JWT tokens.
    """
    
    def __init__(self, secret, issuer='IceProd', algorithm='HS512', expiration=31622400, expiration_temp=86400):
        self.secret = secret
        self.issuer = issuer
        self.algorithm = algorithm
        self.max_exp = expiration
        self.max_exp_temp = expiration_temp

    def create_token(self, subject, expiration=None, type='temp', payload=None):
        """
        Create a token.

        Args:
            subject (str): the user or other owner
            expiration (int): duration in seconds for which the token is valid
            type (str): type of token
            payload (dict): any other fields that should be included

        Returns:
            str: representation of JWT token
        """
        exp = self.max_exp_temp if type == 'temp' else self.max_exp
        if expiration and exp > expiration:
            exp = expiration
        now = time.time()
        if not payload:
            payload = {}
        payload.update({
            'iss': self.issuer,
            'sub': subject,
            'exp': now+exp,
            'nbf': now,
            'iat': now,
            'type': type,
        })
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def validate(self, token):
        """
        Validate a token.

        Args:
            token (str): a JWT token

        Returns:
            dict: data inside token

        Raises:
            Exception on failure to validate.
        """
        ret = jwt.decode(token, self.secret, issuer=self.issuer, algorithms=[self.algorithm])
        if 'type' not in ret:
            raise Exception('no type information')
        return ret