from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer, BadData


def sign_openid(openid):
    s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 60 * 10)
    return s.dumps({'openid': openid}).decode()

def check_openid(sign_openid):
    s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 60 * 10)
    try:
        data = s.loads(sign_openid)
    except BadData:
        return None
    else:
        return data.get('openid')
