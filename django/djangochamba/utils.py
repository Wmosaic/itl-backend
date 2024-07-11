from graphql_jwt.utils import jwt_decode as graphql_jwt_decode
from jwt import MissingRequiredClaimError, InvalidTokenError
from graphql_jwt.utils import get_user_by_payload
from rest_framework.response import Response
from rest_framework.response import Response
from graphql_jwt.utils import jwt_payload as graphql_jwt_payload
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.utils.translation import gettext_lazy as _
import os
import binascii


def get_session_by_id(id):
    if id.logout_date != None :
        raise InvalidJwtIdError(_('Session token is expired'))

def jwt_payload(user, context=None):
    payload = graphql_jwt_payload(user, context)
    payload["jti"] = user.jwt_id
    payload["session"] = user.current_session_id
    return payload

def jwt_decode(token, context=None):
    try:
        payload = graphql_jwt_decode(token, context=None)
        user = get_user_by_payload(payload)
        _validate_jti(payload, user)
    except:
        content = _(u'You do not have permission to perform this action')
        raise Response(content, status=HTTP_400_BAD_REQUEST)

def _validate_jti(payload, user):
    if not user.is_authenticated:
        return
    if user.jwt_id is None:
        return
    if "jti" not in payload:
        raise MissingRequiredClaimError("jti")
    if payload["jti"] != user.jwt_id:
        raise InvalidJwtIdError(_('A valid authentication token is required'))
    session = get_session_by_id(id=payload["session"])
    if session.logout_date != None :
        raise InvalidJwtIdError(_('Session token is expired'))

class InvalidJwtIdError(InvalidTokenError):
    pass

def generate_jti():
    return binascii.hexlify(os.urandom(32)).decode()
