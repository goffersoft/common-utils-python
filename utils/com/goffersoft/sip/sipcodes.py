#! /usr/bin/python

from com.goffersoft.utils.utils import readonly


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


def readonly(value):
    """Internal function to support readonly enum like types"""
    return property(lambda self: value)


class _SipRCType(type):
    """SIP Status Codes"""
    # 1xx codes - Provisional
    RC_100 = readonly('100')
    RC_TRYING = readonly('100')
    # 101-179 Unassigned
    RC_180 = readonly('180')
    RC_RINGING = readonly('180')
    RC_181 = readonly('181')
    RC_CALL_IS_BEING_FRWARDED = readonly('181')
    RC_182 = readonly('182')
    RC_QUEUED = readonly('182')
    RC_183 = readonly('183')
    # 184-198 Unassigned
    RC_SESSION_PROGRESS = readonly('183')
    RC_199 = readonly('199')
    RC_EARLY_DIALOG_TERMINATED = readonly('199')

    # 2xx codes - successful
    RC_200 = readonly('200')
    RC_OK = readonly('200')
    # 201 Unassigned
    RC_202 = readonly('202')
    RC_ACCEPTED = readonly('202')
    # 203 Unassigned
    RC_204 = readonly('204')
    RC_NO_NOTIFICATION = readonly('204')
    # 205-299 Unassigned

    # 3xx codes - redirection
    RC_300 = readonly('300')
    RC_MULTIPLE_CHOICES = readonly('300')
    RC_301 = readonly('301')
    RC_MOVED_PERMANENTLY = readonly('301')
    RC_302 = readonly('302')
    RC_MOVED_TEMPORARILY = readonly('302')
    # 303-304 Unassigned
    RC_305 = readonly('305')
    RC_USE_PROXY = readonly('305')
    # 306-379 Unassigned
    RC_380 = readonly('380')
    RC_ALTERNATIVE_SERVICE = readonly('380')
    # 381-399 Unassigned

    # 4xx codes - request failure
    RC_400 = readonly('400')
    RC_BAD_REQUEST = readonly('400')
    RC_401 = readonly('401')
    RC_UNAUTHORIZED = readonly('401')
    RC_402 = readonly('402')
    RC_PAYMENT_REQUIRED = readonly('402')
    RC_403 = readonly('403')
    RC_FORBIDDEN = readonly('403')
    RC_404 = readonly('404')
    RC_NOT_FOUND = readonly('404')
    RC_405 = readonly('405')
    RC_METHOD_NOT_ALLOWED = readonly('405')
    RC_406 = readonly('406')
    RC_NOT_ACCEPTABLE = readonly('406')
    RC_407 = readonly('407')
    RC_PROXY_AUTHENTICATION_REQUIRED = readonly('407')
    RC_408 = readonly('408')
    RC_REQUEST_TIMEOUT = readonly('408')
    # 409 Unassigned
    RC_410 = readonly('410')
    RC_GONE = readonly('410')
    # 411 Unassigned
    RC_412 = readonly('412')
    RC_CONDITIONAL_REQUEST_FAILED = readonly('412')
    RC_413 = readonly('413')
    RC_REQUEST_ENTITY_TOO_LARGE = readonly('413')
    RC_414 = readonly('414')
    RC_REQUEST_URI_TOO_LONG = readonly('414')
    RC_415 = readonly('415')
    RC_UNSUPPORTED_MEDIA_TYPE = readonly('415')
    RC_416 = readonly('416')
    RC_UNSUPPORTED_URI_SCHEME = readonly('416')
    RC_417 = readonly('417')
    RC_UNKNOWN_RESOURCE_RPIORITY = readonly('417')
    # 418-419 Unassigned
    RC_420 = readonly('420')
    RC_BAD_EXGENSION = readonly('420')
    RC_421 = readonly('421')
    RC_EXTENSION_REQUIRED = readonly('421')
    RC_422 = readonly('422')
    RC_SESSION_INTERVAL_TOO_SMALL = readonly('422')
    RC_423 = readonly('423')
    RC_INTERVAL_TOO_BRIEF = readonly('423')
    RC_424 = readonly('424')
    RC_BAD_LOCATION_INFORMATION = readonly('424')
    # 425-427 Unassigned
    RC_428 = readonly('428')
    RC_USE_IDENTITY_HEADER = readonly('428')
    RC_429 = readonly('429')
    RC_REFERRER_IDENTITY = readonly('429')
    RC_430 = readonly('430')
    RC_FLOW_FAILED = readonly('430')
    # 431-432 Unassigned
    RC_433 = readonly('433')
    RC_ANONYMITY_DISALLOWED = readonly('433')
    # 434-435 Unassigned
    RC_436 = readonly('436')
    RC_BAD_IDENTITY_INFO = readonly('436')
    RC_437 = readonly('437')
    RC_UNSUPPORTED_CERTIFICATE = readonly('437')
    RC_438 = readonly('438')
    RC_INVALID_IDENTITY_HEADER = readonly('438')
    RC_439 = readonly('439')
    RC_FIRST_HOP_LACKS_OUTBOUND_SUPPORT = readonly('439')
    RC_440 = readonly('440')
    RC_MAX_BREATH_EXCEEDED = readonly('440')
    # 441-468 Unassigned
    RC_469 = readonly('469')
    RC_BAD_INFO_PACKAGE = readonly('469')
    RC_470 = readonly('470')
    RC_CONSENT_NEEDED = readonly('470')
    # 471-479 Unassigned
    RC_480 = readonly('480')
    RC_TEMPORARILY_UNAVAILABLE = readonly('480')
    RC_481 = readonly('481')
    RC_CALL_OR_TRANSACTION_DOESNOT_EXIST = readonly('481')
    RC_482 = readonly('482')
    RC_LOOP_DETECTED = readonly('482')
    RC_483 = readonly('483')
    RC_TOO_MANY_LOOPS = readonly('483')
    RC_484 = readonly('484')
    RC_ADDRESS_INCOMPLETE = readonly('484')
    RC_485 = readonly('485')
    RC_AMBIGUOUS = readonly('485')
    RC_486 = readonly('486')
    RC_BUSY_HERE = readonly('486')
    RC_487 = readonly('487')
    RC_REQUEST_TERMINATED = readonly('487')
    RC_488 = readonly('488')
    RC_NOT_ACCEPTABLE_HERE = readonly('488')
    RC_489 = readonly('489')
    RC_BAD_EVENT = readonly('489')
    # 490 Unassigned
    RC_491 = readonly('491')
    RC_REQUEST_PENDING = readonly('491')
    # 492 Unassigned
    RC_493 = readonly('493')
    RC_UNDECIPHERABLE = readonly('493')
    RC_494 = readonly('494')
    RC_SECURITY_AGREEMENT_REQUIRED = readonly('494')
    # 495-499 Unassigned

    # 5xx codes - server failure
    RC_500 = readonly('500')
    RC_INTERNAL_SERVER_ERROR = readonly('500')
    RC_501 = readonly('501')
    RC_NOT_IMPLEMENTED = readonly('501')
    RC_502 = readonly('502')
    RC_BAD_GATEWAY = readonly('502')
    RC_503 = readonly('503')
    RC_SERVICE_UNAVAILABLE = readonly('503')
    RC_504 = readonly('504')
    RC_SERVER_TIMEOUT = readonly('504')
    RC_505 = readonly('505')
    RC_VERSION_NOT_SUPPORTED = readonly('505')
    # 506-512 Unassigned
    RC_513 = readonly('513')
    RC_MESSAGE_TOO_LARGE = readonly('513')
    # 514-579 Unassigned
    RC_580 = readonly('580')
    RC_PRECONDITION_FAILURE = readonly('580')
    # 581-599 Unassigned

    # 6xx codes - global failure
    RC_600 = readonly('600')
    RC_BUSY_EVERYWHERE = readonly('600')
    # 601-602 Unassigned
    RC_603 = readonly('603')
    RC_DECLINE = readonly('603')
    RC_604 = readonly('604')
    RC_DOESNOT_EXIST_ANYWHERE = readonly('604')
    # 605 Unassigned
    RC_606 = readonly('606')
    RC_NOT_ACCEPTABLE = readonly('606')
    # 607-699 Unassigned


class _SipRCDescrType(type):
    """SIP Status Codes - Descriptive Text"""
    # 1xx codes - provisional
    RC_100 = readonly('Trying')
    # 101-179 Unassigned
    RC_180 = readonly('Ringing')
    RC_181 = readonly('Call Is Being Forwarded')
    RC_182 = readonly('Queued')
    RC_183 = readonly('Session Progress')
    # 184-198 Unassigned
    RC_199 = readonly('Early Dialog Terminated')

    # 2xx codes - successful
    RC_200 = readonly('OK')
    # 201 Unassigned
    RC_202 = readonly('Accepted (Deprecated)')
    # 203 Unassigned
    RC_204 = readonly('No Notification')
    # 205-299 Unassigned

    # 3xx codes - redirection
    RC_300 = readonly('Mutliple Choices')
    RC_301 = readonly('Moved Permanently')
    RC_302 = readonly('Moved Temporarily')
    RC_305 = readonly('Use Proxy')
    RC_380 = readonly('Alternative Service')
    # 381-399 Unassigned

    # 4xx codes - request failure
    RC_400 = readonly('Bad Request')
    RC_401 = readonly('Unauthorized')
    RC_402 = readonly('Payment Required')
    RC_403 = readonly('Forbidden')
    RC_404 = readonly('Not Found')
    RC_405 = readonly('Method Not Allowed')
    RC_406 = readonly('Not Acceptable')
    RC_407 = readonly('Proxy Authentication Required')
    RC_408 = readonly('Request Timeout')
    # 409 Unassigned
    RC_410 = readonly('Gone')
    # 411 Unassigned
    RC_412 = readonly('Conditiona Request Failed')
    RC_413 = readonly('Request Entity Too Large')
    RC_414 = readonly('Request-URI Too Long')
    RC_415 = readonly('Unsupported Media Type')
    RC_416 = readonly('Unsupported URI Scheme')
    RC_417 = readonly('Unknown Resoource-Priority')
    # 418-419 Unassigned
    RC_420 = readonly('Bad Extension')
    RC_421 = readonly('Extension Required')
    RC_422 = readonly('Session Interval Too Small')
    RC_423 = readonly('Interval Too Brief')
    RC_424 = readonly('Bad Location Information')
    # 425-427 Unassigned
    RC_428 = readonly('Use Identity Header')
    RC_429 = readonly('Provide Referrer Identity')
    RC_430 = readonly('Flow Failed')
    # 431-432 Unassigned
    RC_433 = readonly('Anonymity Disallowed')
    # 434-435 Unassigned
    RC_436 = readonly('Bad Identity-info')
    RC_437 = readonly('Unsupported Certificateinfo')
    RC_438 = readonly('Invalid Identity Header')
    RC_439 = readonly('First Hop Lacks Outbound Support')
    RC_440 = readonly('Max-Breadth Exceeded')
    RC_469 = readonly('Bad Info Package')
    RC_470 = readonly('Consent Needed')
    # 471-479 Unassigned
    RC_480 = readonly('Temprorarily Unavailable')
    RC_481 = readonly('Call/Transaction Does Not Exist')
    RC_482 = readonly('Loop Detected')
    RC_483 = readonly('Too Many Hops')
    RC_484 = readonly('Address Incomplete')
    RC_485 = readonly('Ambiguous')
    RC_486 = readonly('Busy Here')
    RC_487 = readonly('Request Terminated')
    RC_488 = readonly('Not Acceptable Here')
    RC_489 = readonly('Bad Event')
    RC_491 = readonly('Request Pending')
    RC_493 = readonly('Undecipherable')
    RC_494 = readonly('Security Agreement Required')
    # 495-499 Unassigned

    # 5xx codes
    RC_500 = readonly('Internal Server Error')
    RC_501 = readonly('Not Implemented')
    RC_502 = readonly('Bad Gateway')
    RC_503 = readonly('Service Unavailable')
    RC_504 = readonly('Server Timeout')
    RC_505 = readonly('Version Not Supported')
    # 506-512 Unassigned
    RC_513 = readonly('Message Too Large')
    # 514-579 Unassigned
    RC_580 = readonly('Precondition Failure')
    # 581-599 Unassigned

    # 6xx codes
    RC_600 = readonly('Busy Everywhere')
    # 601-602 Unassigned
    RC_603 = readonly('Decline')
    RC_604 = readonly('Does Bot Exist Anywhere')
    # 605 Unassigned
    RC_606 = readonly('Not Acceptable')
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
    """Determines if the given code is a 1xx code or not"""
    if code in codetype_1xx:
        return True
    return False


is_provisional = is_1xx


def is_2xx(code):
    """Determines if the given code is a 2xx code or not"""
    if code in codetype_2xx:
        return True
    return False


is_successful = is_2xx


def is_3xx(code):
    """Determines if the given code is a 3xx code or not"""
    if code in codetype_3xx:
        return True
    return False


is_redirection = is_3xx


def is_4xx(code):
    """Determines if the given code is a 4xx code or not"""
    if code in codetype_4xx:
        return True
    return False


is_request_failure = is_4xx


def is_5xx(code):
    """Determines if the given code is a 5xx code or not"""
    if code in codetype_5xx:
        return True
    return False


is_server_failure = is_5xx


def is_6xx(code):
    """Determines if the given code is a 6xx code or not"""
    if code in codetype_6xx:
        return True
    return False


is_global_failure = is_6xx


def is_experimental(code):
    """Determines if the given code is a experimental code or not"""
    if code in codetype_experimental:
        return True
    return False


def is_deprecated(code):
    """Determines if the given code is a deprecated code or not"""
    if code in codetype_deprecated:
        return True
    return False


def is_valid(code):
    """Determines if the given code is a [1-6]xx code or not"""
    if(code in codetype_1xx or
       code in codetype_2xx or
       code in codetype_3xx or
       code in codetype_4xx or
       code in codetype_5xx):
        return True
    return False


def get_1xx_codes():
    """returns a list (tuple) of 1xx codes """
    return codetype_1xx


get_provisional_codes = get_1xx_codes


def get_2xx_codes():
    """returns a list (tuple) of 2xx codes """
    return codetype_2xx


get_successful_codes = get_2xx_codes


def get_3xx_codes():
    """returns a list (tuple) of 3xx codes """
    return codetype_3xx


get_redirection_codes = get_3xx_codes


def get_4xx_codes():
    """returns a list (tuple) of 4xx codes """
    return codetype_4xx


get_request_failure_codes = get_4xx_codes


def get_5xx_codes():
    """returns a list (tuple) of 5xx codes """
    return codetype_5xx


get_server_failure_codes = get_5xx_codes


def get_6xx_codes():
    """returns a list (tuple) of 6xx codes """
    return codetype_6xx


get_global_failure_codes = get_6xx_codes


def get_experimental_codes():
    """returns a list (tuple) of experimental codes """
    return codetype_experimental


def get_deprecated_codes():
    """returns a list (tuple) of deprecated codes """
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
