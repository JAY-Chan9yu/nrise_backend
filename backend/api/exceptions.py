from rest_framework.exceptions import APIException


class WithdrawalUser(APIException):
    status_code = 403
    default_detail = 'This user has already been unsubscribed.'
    default_code = 'WITHDRAWAL'


class AlreadyLogout(APIException):
    status_code = 403
    default_detail = 'You are already logged out.'
    default_code = 'ALREADY_LOGOUT'
