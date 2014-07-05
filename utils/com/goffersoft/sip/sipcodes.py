#! /usr/bin/python


""" This Module Contains Types for Sip Response Codes
    and the corerespnding helper functions
    Types :
        1. SipRCType - Enum of Sip Status Codes
        2. SipRCDescrType - Enum of Sip Status Codes - Descriptive Text
    Method :
        1. is_1xx -> Is given code a 1xx status code type
        2. is_provisoonal -> alias for is_1xx
        3. is_2xx -> Is given code a 2xx status code type
        4. is_successful -> alias for is_2xx
        5. is_3xx -> Is given code a 3xx status code type
        6. is_redirection -> alias for is_3xx
        7. is_4xx -> Is given code a 4xx status code type
        8. is_request_failure -> alias for is_4xx
        9. is_5xx -> Is given code a 5xx status code type
       10. is_server_failure -> alias for is_5xx
       11. is_6xx -> Is given code a 5xx status code type
       12. is_global_failure -> alias for is_6xx
       13. is_experimental -> Is given code a experimental status code type
       14. is_deprecated -> Is given code a deprecated status code type
       15. is_valid -> Is given code a valid status code type
       16. get_1xx_codes -> get list of 1xx status codes
       17. get_provisional_codes -> get list of 1xx status codes
       18. get_2xx_codes -> get list of 2xx status codes
       19. get_successful_codes -> get list of 2xx status codes
       20. get_3xx_codes -> get list of 3xx status codes
       21. get_redirection_codes -> get list of 3xx status codes
       22. get_4xx_codes -> get list of 4xx status codes
       23. get_request_failure_codes -> get list of 4xx status codes
       24. get_5xx_codes -> get list of 5xx status codes
       25. get_server_failure_codes -> get list of 5xx status codes
       26. get_6xx_codes -> get list of 5xx status codes
       27. get_global_failure_codes -> get list of 5xx status codes
       28. get_experimental_codes -> get list of experimental status codes
       29. get_deprecated_codes -> get list of deprecated status codes
"""


def _readonly(value):
    return property(lambda self: value)


class _SipRCType(type):
    """ SIP Status Codes """
    # 1xx codes - Provisional
    RC_100 = _readonly('100')
    RC_TRYING = _readonly('100')
    # 101-179 Unassigned
    RC_180 = _readonly('180')
    RC_RINGING = _readonly('180')
    RC_181 = _readonly('181')
    RC_CALL_IS_BEING_FRWARDED = _readonly('181')
    RC_182 = _readonly('182')
    RC_QUEUED = _readonly('182')
    RC_183 = _readonly('183')
    # 184-198 Unassigned
    RC_SESSION_PROGRESS = _readonly('183')
    RC_199 = _readonly('199')
    RC_EARLY_DIALOG_TERMINATED = _readonly('199')

    # 2xx codes - successful
    RC_200 = _readonly('200')
    RC_OK = _readonly('200')
    # 201 Unassigned
    RC_202 = _readonly('202')
    RC_ACCEPTED = _readonly('202')
    # 203 Unassigned
    RC_204 = _readonly('204')
    RC_NO_NOTIFICATION = _readonly('204')
    # 205-299 Unassigned

    # 3xx codes - redirection
    RC_300 = _readonly('300')
    RC_MULTIPLE_CHOICES = _readonly('300')
    RC_301 = _readonly('301')
    RC_MOVED_PERMANENTLY = _readonly('301')
    RC_302 = _readonly('302')
    RC_MOVED_TEMPORARILY = _readonly('302')
    # 303-304 Unassigned
    RC_305 = _readonly('305')
    RC_USE_PROXY = _readonly('305')
    # 306-379 Unassigned
    RC_380 = _readonly('380')
    RC_ALTERNATIVE_SERVICE = _readonly('380')
    # 381-399 Unassigned

    # 4xx codes - request failure
    RC_400 = _readonly('400')
    RC_BAD_REQUEST = _readonly('400')
    RC_401 = _readonly('401')
    RC_UNAUTHORIZED = _readonly('401')
    RC_402 = _readonly('402')
    RC_PAYMENT_REQUIRED = _readonly('402')
    RC_403 = _readonly('403')
    RC_FORBIDDEN = _readonly('403')
    RC_404 = _readonly('404')
    RC_NOT_FOUND = _readonly('404')
    RC_405 = _readonly('405')
    RC_METHOD_NOT_ALLOWED = _readonly('405')
    RC_406 = _readonly('406')
    RC_NOT_ACCEPTABLE = _readonly('406')
    RC_407 = _readonly('407')
    RC_PROXY_AUTHENTICATION_REQUIRED = _readonly('407')
    RC_408 = _readonly('408')
    RC_REQUEST_TIMEOUT = _readonly('408')
    # 409 Unassigned
    RC_410 = _readonly('410')
    RC_GONE = _readonly('410')
    # 411 Unassigned
    RC_412 = _readonly('412')
    RC_CONDITIONAL_REQUEST_FAILED = _readonly('412')
    RC_413 = _readonly('413')
    RC_REQUEST_ENTITY_TOO_LARGE = _readonly('413')
    RC_414 = _readonly('414')
    RC_REQUEST_URI_TOO_LONG = _readonly('414')
    RC_415 = _readonly('415')
    RC_UNSUPPORTED_MEDIA_TYPE = _readonly('415')
    RC_416 = _readonly('416')
    RC_UNSUPPORTED_URI_SCHEME = _readonly('416')
    RC_417 = _readonly('417')
    RC_UNKNOWN_RESOURCE_RPIORITY = _readonly('417')
    # 418-419 Unassigned
    RC_420 = _readonly('420')
    RC_BAD_EXGENSION = _readonly('420')
    RC_421 = _readonly('421')
    RC_EXTENSION_REQUIRED = _readonly('421')
    RC_422 = _readonly('422')
    RC_SESSION_INTERVAL_TOO_SMALL = _readonly('422')
    RC_423 = _readonly('423')
    RC_INTERVAL_TOO_BRIEF = _readonly('423')
    RC_424 = _readonly('424')
    RC_BAD_LOCATION_INFORMATION = _readonly('424')
    # 425-427 Unassigned
    RC_428 = _readonly('428')
    RC_USE_IDENTITY_HEADER = _readonly('428')
    RC_429 = _readonly('429')
    RC_REFERRER_IDENTITY = _readonly('429')
    RC_430 = _readonly('430')
    RC_FLOW_FAILED = _readonly('430')
    # 431-432 Unassigned
    RC_433 = _readonly('433')
    RC_ANONYMITY_DISALLOWED = _readonly('433')
    # 434-435 Unassigned
    RC_436 = _readonly('436')
    RC_BAD_IDENTITY_INFO = _readonly('436')
    RC_437 = _readonly('437')
    RC_UNSUPPORTED_CERTIFICATE = _readonly('437')
    RC_438 = _readonly('438')
    RC_INVALID_IDENTITY_HEADER = _readonly('438')
    RC_439 = _readonly('439')
    RC_FIRST_HOP_LACKS_OUTBOUND_SUPPORT = _readonly('439')
    RC_440 = _readonly('440')
    RC_MAX_BREATH_EXCEEDED = _readonly('440')
    # 441-468 Unassigned
    RC_469 = _readonly('469')
    RC_BAD_INFO_PACKAGE = _readonly('469')
    RC_470 = _readonly('470')
    RC_CONSENT_NEEDED = _readonly('470')
    # 471-479 Unassigned
    RC_480 = _readonly('480')
    RC_TEMPORARILY_UNAVAILABLE = _readonly('480')
    RC_481 = _readonly('481')
    RC_CALL_OR_TRANSACTION_DOESNOT_EXIST = _readonly('481')
    RC_482 = _readonly('482')
    RC_LOOP_DETECTED = _readonly('482')
    RC_483 = _readonly('483')
    RC_TOO_MANY_LOOPS = _readonly('483')
    RC_484 = _readonly('484')
    RC_ADDRESS_INCOMPLETE = _readonly('484')
    RC_485 = _readonly('485')
    RC_AMBIGUOUS = _readonly('485')
    RC_486 = _readonly('486')
    RC_BUSY_HERE = _readonly('486')
    RC_487 = _readonly('487')
    RC_REQUEST_TERMINATED = _readonly('487')
    RC_488 = _readonly('488')
    RC_NOT_ACCEPTABLE_HERE = _readonly('488')
    RC_489 = _readonly('489')
    RC_BAD_EVENT = _readonly('489')
    # 490 Unassigned
    RC_491 = _readonly('491')
    RC_REQUEST_PENDING = _readonly('491')
    # 492 Unassigned
    RC_493 = _readonly('493')
    RC_UNDECIPHERABLE = _readonly('493')
    RC_494 = _readonly('494')
    RC_SECURITY_AGREEMENT_REQUIRED = _readonly('494')
    # 495-499 Unassigned

    # 5xx codes - server failure
    RC_500 = _readonly('500')
    RC_INTERNAL_SERVER_ERROR = _readonly('500')
    RC_501 = _readonly('501')
    RC_NOT_IMPLEMENTED = _readonly('501')
    RC_502 = _readonly('502')
    RC_BAD_GATEWAY = _readonly('502')
    RC_503 = _readonly('503')
    RC_SERVICE_UNAVAILABLE = _readonly('503')
    RC_504 = _readonly('504')
    RC_SERVER_TIMEOUT = _readonly('504')
    RC_505 = _readonly('505')
    RC_VERSION_NOT_SUPPORTED = _readonly('505')
    # 506-512 Unassigned
    RC_513 = _readonly('513')
    RC_MESSAGE_TOO_LARGE = _readonly('513')
    # 514-579 Unassigned
    RC_580 = _readonly('580')
    RC_PRECONDITION_FAILURE = _readonly('580')
    # 581-599 Unassigned

    # 6xx codes - global failure
    RC_600 = _readonly('600')
    RC_BUSY_EVERYWHERE = _readonly('600')
    # 601-602 Unassigned
    RC_603 = _readonly('603')
    RC_DECLINE = _readonly('603')
    RC_604 = _readonly('604')
    RC_DOESNOT_EXIST_ANYWHERE = _readonly('604')
    # 605 Unassigned
    RC_606 = _readonly('606')
    RC_NOT_ACCEPTABLE = _readonly('606')
    # 607-699 Unassigned


class _SipRCDescrType(type):
    """ SIP Status Codes - Descriptive Text """
    # 1xx codes - provisional
    RC_100 = _readonly('Trying')
    # 101-179 Unassigned
    RC_180 = _readonly('Ringing')
    RC_181 = _readonly('Call Is Being Forwarded')
    RC_182 = _readonly('Queued')
    RC_183 = _readonly('Session Progress')
    # 184-198 Unassigned
    RC_199 = _readonly('Early Dialog Terminated')

    # 2xx codes - successful
    RC_200 = _readonly('OK')
    # 201 Unassigned
    RC_202 = _readonly('Accepted (Deprecated)')
    # 203 Unassigned
    RC_204 = _readonly('No Notification')
    # 205-299 Unassigned

    # 3xx codes - redirection
    RC_300 = _readonly('Mutliple Choices')
    RC_301 = _readonly('Moved Permanently')
    RC_302 = _readonly('Moved Temporarily')
    RC_305 = _readonly('Use Proxy')
    RC_380 = _readonly('Alternative Service')
    # 381-399 Unassigned

    # 4xx codes - request failure
    RC_400 = _readonly('Bad Request')
    RC_401 = _readonly('Unauthorized')
    RC_402 = _readonly('Payment Required')
    RC_403 = _readonly('Forbidden')
    RC_404 = _readonly('Not Found')
    RC_405 = _readonly('Method Not Allowed')
    RC_406 = _readonly('Not Acceptable')
    RC_407 = _readonly('Proxy Authentication Required')
    RC_408 = _readonly('Request Timeout')
    # 409 Unassigned
    RC_410 = _readonly('Gone')
    # 411 Unassigned
    RC_412 = _readonly('Conditiona Request Failed')
    RC_413 = _readonly('Request Entity Too Large')
    RC_414 = _readonly('Request-URI Too Long')
    RC_415 = _readonly('Unsupported Media Type')
    RC_416 = _readonly('Unsupported URI Scheme')
    RC_417 = _readonly('Unknown Resoource-Priority')
    # 418-419 Unassigned
    RC_420 = _readonly('Bad Extension')
    RC_421 = _readonly('Extension Required')
    RC_422 = _readonly('Session Interval Too Small')
    RC_423 = _readonly('Interval Too Brief')
    RC_424 = _readonly('Bad Location Information')
    # 425-427 Unassigned
    RC_428 = _readonly('Use Identity Header')
    RC_429 = _readonly('Provide Referrer Identity')
    RC_430 = _readonly('Flow Failed')
    # 431-432 Unassigned
    RC_433 = _readonly('Anonymity Disallowed')
    # 434-435 Unassigned
    RC_436 = _readonly('Bad Identity-info')
    RC_437 = _readonly('Unsupported Certificateinfo')
    RC_438 = _readonly('Invalid Identity Header')
    RC_439 = _readonly('First Hop Lacks Outbound Support')
    RC_440 = _readonly('Max-Breadth Exceeded')
    RC_469 = _readonly('Bad Info Package')
    RC_470 = _readonly('Consent Needed')
    # 471-479 Unassigned
    RC_480 = _readonly('Temprorarily Unavailable')
    RC_481 = _readonly('Call/Transaction Does Not Exist')
    RC_482 = _readonly('Loop Detected')
    RC_483 = _readonly('Too Many Hops')
    RC_484 = _readonly('Address Incomplete')
    RC_485 = _readonly('Ambiguous')
    RC_486 = _readonly('Busy Here')
    RC_487 = _readonly('Request Terminated')
    RC_488 = _readonly('Not Acceptable Here')
    RC_489 = _readonly('Bad Event')
    RC_491 = _readonly('Request Pending')
    RC_493 = _readonly('Undecipherable')
    RC_494 = _readonly('Security Agreement Required')
    # 495-499 Unassigned

    # 5xx codes
    RC_500 = _readonly('Internal Server Error')
    RC_501 = _readonly('Not Implemented')
    RC_502 = _readonly('Bad Gateway')
    RC_503 = _readonly('Service Unavailable')
    RC_504 = _readonly('Server Timeout')
    RC_505 = _readonly('Version Not Supported')
    # 506-512 Unassigned
    RC_513 = _readonly('Message Too Large')
    # 514-579 Unassigned
    RC_580 = _readonly('Precondition Failure')
    # 581-599 Unassigned

    # 6xx codes
    RC_600 = _readonly('Busy Everywhere')
    # 601-602 Unassigned
    RC_603 = _readonly('Decline')
    RC_604 = _readonly('Does Bot Exist Anywhere')
    # 605 Unassigned
    RC_606 = _readonly('Not Acceptable')
    # 607-699 Unassigned

SipRCType = _SipRCType('SipRCType', (object,), {})
SipRCDescrType = _SipRCDescrType('SipRCDescrType',
                                 (object,), {})


codetype_1xx = (SipRCType.RC_100,
                SipRCType.RC_180,
                SipRCType.RC_181,
                SipRCType.RC_182,
                SipRCType.RC_183,
                SipRCType.RC_199)


codetype_2xx = (SipRCType.RC_200,
                SipRCType.RC_202,
                SipRCType.RC_204)


codetype_3xx = (SipRCType.RC_300,
                SipRCType.RC_301,
                SipRCType.RC_302,
                SipRCType.RC_305,
                SipRCType.RC_380)

codetype_4xx = (SipRCType.RC_400,
                SipRCType.RC_401,
                SipRCType.RC_402,
                SipRCType.RC_403,
                SipRCType.RC_404,
                SipRCType.RC_405,
                SipRCType.RC_406,
                SipRCType.RC_407,
                SipRCType.RC_408,
                SipRCType.RC_410,
                SipRCType.RC_412,
                SipRCType.RC_413,
                SipRCType.RC_414,
                SipRCType.RC_415,
                SipRCType.RC_416,
                SipRCType.RC_417,
                SipRCType.RC_420,
                SipRCType.RC_421,
                SipRCType.RC_422,
                SipRCType.RC_423,
                SipRCType.RC_424,
                SipRCType.RC_428,
                SipRCType.RC_429,
                SipRCType.RC_430,
                SipRCType.RC_433,
                SipRCType.RC_436,
                SipRCType.RC_437,
                SipRCType.RC_438,
                SipRCType.RC_439,
                SipRCType.RC_440,
                SipRCType.RC_469,
                SipRCType.RC_470,
                SipRCType.RC_480,
                SipRCType.RC_480,
                SipRCType.RC_480,
                SipRCType.RC_481,
                SipRCType.RC_482,
                SipRCType.RC_483,
                SipRCType.RC_484,
                SipRCType.RC_485,
                SipRCType.RC_486,
                SipRCType.RC_487,
                SipRCType.RC_488,
                SipRCType.RC_489,
                SipRCType.RC_491,
                SipRCType.RC_493,
                SipRCType.RC_494)


codetype_5xx = (SipRCType.RC_500,
                SipRCType.RC_501,
                SipRCType.RC_502,
                SipRCType.RC_503,
                SipRCType.RC_504,
                SipRCType.RC_505,
                SipRCType.RC_513,
                SipRCType.RC_580)


codetype_6xx = (SipRCType.RC_600,
                SipRCType.RC_603,
                SipRCType.RC_604,
                SipRCType.RC_606)


codetype_experimental = ()


codetype_deprecated = (SipRCType.RC_202,)


def is_1xx(code):
    """ Determines if the given code is a 1xx code or not"""

    if code in codetype_1xx:
        return True
    return False


is_provisional = is_1xx


def is_2xx(code):
    """ Determines if the given code is a 2xx code or not"""

    if code in codetype_2xx:
        return True
    return False


is_successful = is_2xx


def is_3xx(code):
    """ Determines if the given code is a 3xx code or not"""

    if code in codetype_3xx:
        return True
    return False


is_redirection = is_3xx


def is_4xx(code):
    """ Determines if the given code is a 4xx code or not"""

    if code in codetype_4xx:
        return True
    return False
    pass


is_request_failure = is_4xx


def is_5xx(code):
    """ Determines if the given code is a 5xx code or not"""

    if code in codetype_5xx:
        return True
    return False


is_server_failure = is_5xx


def is_6xx(code):
    """ Determines if the given code is a 6xx code or not"""

    if code in codetype_6xx:
        return True
    return False


is_global_failure = is_6xx


def is_experimental(code):
    """ Determines if the given code is a experimental code or not"""

    if code in codetype_experimental:
        return True
    return False


def is_deprecated(code):
    """ Determines if the given code is a deprecated code or not"""

    if code in codetype_deprecated:
        return True
    return False


def is_valid(code):
    """ Determines if the given code is a [1-6]xx code or not"""

    if(code in codetype_1xx or
       code in codetype_2xx or
       code in codetype_3xx or
       code in codetype_4xx or
       code in codetype_5xx):
        return True
    return False


def get_1xx_codes():
    """ returns a list (tuple) of 1xx codes """

    return codetype_1xx


get_provisional_codes = get_1xx_codes


def get_2xx_codes():
    """ returns a list (tuple) of 2xx codes """

    return codetype_2xx


get_successful_codes = get_2xx_codes


def get_3xx_codes():
    """ returns a list (tuple) of 3xx codes """

    return codetype_3xx


get_redirection_codes = get_3xx_codes


def get_4xx_codes():
    """ returns a list (tuple) of 4xx codes """

    return codetype_4xx


get_request_failure_codes = get_4xx_codes


def get_5xx_codes():
    """ returns a list (tuple) of 5xx codes """

    return codetype_5xx


get_server_failure_codes = get_5xx_codes


def get_6xx_codes():
    """ returns a list (tuple) of 6xx codes """

    return codetype_6xx


get_global_failure_codes = get_6xx_codes


def get_experimental_codes():
    """ returns a list (tuple) of experimental codes """

    return codetype_experimental


def get_deprecated_codes():
    """ returns a list (tuple) of deprecated codes """

    return codetype_deprecated


if __name__ == '__main__':
    print(SipRCType.RC_100)
    print(SipRCType.RC_200)
    print(SipRCType.RC_300)
    print(SipRCType.RC_400)
    print(SipRCType.RC_500)
    print(is_valid('100'))
    print(is_valid('200'))
    print(is_valid('300'))
    print(is_valid('400'))
    print(is_valid('500'))
    print(is_valid('600'))
    print(is_1xx('100'))
    print(is_provisional('100'))
    print(is_1xx(SipRCType.RC_100))
    print(is_1xx(SipRCType.RC_TRYING))
    print(is_1xx(SipRCType.RC_200))
    print(is_2xx(SipRCType.RC_200))
    print(is_2xx(SipRCType.RC_300))
    print(is_3xx(SipRCType.RC_300))
    print(is_3xx(SipRCType.RC_400))
    print(is_4xx(SipRCType.RC_400))
    print(is_4xx(SipRCType.RC_500))
    print(is_5xx(SipRCType.RC_500))
    print(is_5xx(SipRCType.RC_600))
    print(is_6xx(SipRCType.RC_600))
    print(is_6xx(SipRCType.RC_100))
    print(is_experimental(SipRCType.RC_200))
    print(is_experimental(SipRCType.RC_100))
    print(is_deprecated(SipRCType.RC_202))
    print(is_deprecated(SipRCType.RC_100))
