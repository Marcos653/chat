from rest_framework.exceptions import APIException
from django.utils.translation import ugettext as _

class ForgotPasswordExpired(APIException):
    status_code = 404
    default_detail = _('Link expirado')
    default_code = 'permission_denied'

class InvalidPassword(APIException):
    status_code = 404
    default_detail = _('Senha inválida')
    default_code = 'permission_denied'

class ForgotPasswordInvalidParams(APIException):
    status_code = 404
    default_detail = _('Parametros inválidos')
    default_code = 'permission_denied'


class UserDoesNotExist(APIException):
    status_code = 404
    default_detail = _('Usuário não existe')
    default_code = 'permission_denied'        