#! /usr/bin/python


""" This Module Contains Types for Http Response Codes
    and the corerespnding helper functions
    Types :
        1. HttpRCType - Enum of Http Status Codes
        2. HttpRCDescrType - Enum of Http Status Codes - Descriptive Text
    Method :
        1. is_1xx -> Is given code a 1xx status code type
        2. is_2xx -> Is given code a 2xx status code type
        3. is_3xx -> Is given code a 3xx status code type
        4. is_4xx -> Is given code a 4xx status code type
        5. is_5xx -> Is given code a 5xx status code type
        6. is_experimental -> Is given code a experimental status code type
        7. is_deprecated -> Is given code a deprecated status code type
        8. is_valid -> Is given code a valid status code type
        9. get_1xx_codes -> get list of 1xx status codes
       10. get_2xx_codes -> get list of 2xx status codes
       11. get_3xx_codes -> get list of 3xx status codes
       12. get_4xx_codes -> get list of 4xx status codes
       13. get_5xx_codes -> get list of 5xx status codes
       14. get_experimental_codes -> get list of experimental status codes
       15. get_deprecated_codes -> get list of deprectated status codes
"""


def _readonly(value):
    return property(lambda self: value)


class _HttpRCType(type):
    """ HTTP Status Codes """
    # 1xx codes
    RC_100 = _readonly('100')
    RC_CONTINUE = _readonly('100')
    RC_101 = _readonly('101')
    RC_SWITCHING_PROTOCOLS = _readonly('101')
    RC_102 = _readonly('102')
    RC_PROCESSING = _readonly('102')
    # 103-199 Unassigned

    # 2xx codes
    RC_200 = _readonly('200')
    RC_OK = _readonly('200')
    RC_201 = _readonly('201')
    RC_CREATED = _readonly('201')
    RC_202 = _readonly('202')
    RC_ACCEPTED = _readonly('202')
    RC_203 = _readonly('203')
    RC_NON_AUTHORITATIVE_INFORMATION = _readonly('203')
    RC_204 = _readonly('204')
    RC_NO_CONTENT = _readonly('204')
    RC_205 = _readonly('205')
    RC_RESET_CONTENT = _readonly('205')
    RC_206 = _readonly('206')
    RC_PARTIAL_CONTENT = _readonly('206')
    RC_207 = _readonly('207')
    RC_MULTI_STATUS = _readonly('207')
    RC_208 = _readonly('208')
    RC_ALREADY_REPORTED = _readonly('208')
    # 209-225 Unassigned
    RC_226 = _readonly('226')
    RC_IM_USED = _readonly('226')
    # 227-299 Unassigned

    # 3xx codes
    RC_300 = _readonly('300')
    RC_MULTIPLE_CHOICES = _readonly('300')
    RC_301 = _readonly('301')
    RC_MOVED_PERMANENTLY = _readonly('301')
    RC_302 = _readonly('302')
    RC_FOUND = _readonly('302')
    RC_303 = _readonly('303')
    RC_SEE_OTHER = _readonly('303')
    RC_304 = _readonly('304')
    RC_NOT_MODIFIED = _readonly('304')
    RC_305 = _readonly('305')
    RC_USE_PROXY = _readonly('305')
    # 306 Unassigned
    RC_307 = _readonly('307')
    RC_TEMPORARY_REDIRECT = _readonly('307')
    RC_308 = _readonly('308')
    RC_PERMANENT_REDIRECT = _readonly('308')
    # 309-399 Unassigned

    # 4xx codes
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
    RC_409 = _readonly('409')
    RC_CONFLICT = _readonly('409')
    RC_410 = _readonly('410')
    RC_GONE = _readonly('410')
    RC_411 = _readonly('411')
    RC_LENGTH_REQUIRED = _readonly('411')
    RC_412 = _readonly('412')
    RC_PRECONDITION_FAILED = _readonly('412')
    RC_413 = _readonly('413')
    RC_PAYLOAD_TOO_LARGE = _readonly('413')
    RC_414 = _readonly('414')
    RC_URI_TOO_LONG = _readonly('414')
    RC_415 = _readonly('415')
    RC_UNSUPPORTED_MEDIA_TYPE = _readonly('415')
    RC_416 = _readonly('416')
    RC_REQUESTED_RANGE_NOT_SATISFIABLE = _readonly('416')
    RC_417 = _readonly('417')
    RC_EXPECTATION_FAILED = _readonly('417')
    # 418-421 Unassigned
    RC_422 = _readonly('422')
    RC_UNPROCESSABLE_ENTITY = _readonly('422')
    RC_423 = _readonly('423')
    RC_LOCKED = _readonly('423')
    RC_424 = _readonly('424')
    RC_FAILED_DEPENDENCY = _readonly('424')
    # 425 Unassigned
    RC_426 = _readonly('426')
    RC_UGRADE_REQUIRED = _readonly('426')
    # 427 Unassigned
    RC_428 = _readonly('428')
    RC_PRECONDITION_REQUIRED = _readonly('428')
    RC_429 = _readonly('429')
    RC_TOO_MANY_REQUESTS = _readonly('429')
    # 430 Unassigned
    RC_431 = _readonly('431')
    RC_REQUEST_HEADER_FIELDS_TOO_LARGE = _readonly('431')
    # 432-499 Unassigned

    # 5xx codes
    RC_500 = _readonly('500')
    RC_INTERNAL_SERVER_ERROR = _readonly('500')
    RC_501 = _readonly('501')
    RC_NOT_IMPLEMENTED = _readonly('501')
    RC_502 = _readonly('502')
    RC_BAD_GATEWAY = _readonly('502')
    RC_503 = _readonly('503')
    RC_SERVICE_UNAVAILABLE = _readonly('503')
    RC_504 = _readonly('504')
    RC_GATEWAY_TIMEOUT = _readonly('504')
    RC_505 = _readonly('505')
    RC_HTTP_VERSION_NOT_SUPPORTED = _readonly('505')
    RC_506 = _readonly('506')
    RC_VARIANT_ALSO_NEGOTIATES = _readonly('506')
    RC_507 = _readonly('507')
    RC_INSUFFICIENT_STORAGE = _readonly('507')
    RC_508 = _readonly('508')
    RC_LOOP_DETCTED = _readonly('508')
    # 509 Unassigned
    RC_510 = _readonly('510')
    RC_NOT_EXTENDED = _readonly('510')
    RC_511 = _readonly('511')
    RC_NETWORK_AUTHENTICATION_FAILED = _readonly('511')
    # 512-599 Unassigned


class _HttpRCDescrType(type):
    """ HTTP Status Codes - Descriptive Text """
    # 1xx codes
    RC_100 = _readonly('Continue')
    RC_101 = _readonly('Switching Protocols')
    RC_102 = _readonly('Processing')
    # 103-199 Unassigned

    # 2xx codes
    RC_200 = _readonly('OK')
    RC_201 = _readonly('Created')
    RC_202 = _readonly('Accepted')
    RC_203 = _readonly('Non-Authoritative Information')
    RC_204 = _readonly('No Content')
    RC_205 = _readonly('Reset Content')
    RC_206 = _readonly('Partial Content')
    RC_207 = _readonly('Multi-Status')
    RC_208 = _readonly('Already Supported')
    # 209-225 Unassigned
    RC_226 = _readonly('IM Used')
    # 227-299 Unassigned

    # 3xx codes
    RC_300 = _readonly('Mutliple Choices')
    RC_301 = _readonly('Moved Permanently')
    RC_302 = _readonly('Found')
    RC_303 = _readonly('See Other')
    RC_304 = _readonly('Not Modified')
    RC_305 = _readonly('Use Proxy')
    RC_307 = _readonly('Temporary Redirect')
    RC_308 = _readonly('Permanent Redirect')
    # 309-399 Unassigned

    # 4xx codes
    RC_400 = _readonly('Bad Request')
    RC_401 = _readonly('Unauthorized')
    RC_402 = _readonly('Payment Required')
    RC_403 = _readonly('Forbidden')
    RC_404 = _readonly('Not Found')
    RC_405 = _readonly('Method Not Allowed')
    RC_406 = _readonly('Not Acceptable')
    RC_407 = _readonly('Proxy Authentication Required')
    RC_408 = _readonly('Request Timeout')
    RC_409 = _readonly('Conflict')
    RC_410 = _readonly('Gone')
    RC_411 = _readonly('Length Required')
    RC_412 = _readonly('Precondition Failed')
    RC_413 = _readonly('Payload Too Large')
    RC_414 = _readonly('URI Too Long')
    RC_415 = _readonly('Unsupported Media Type')
    RC_416 = _readonly('Requested Range Not Satisfiable')
    RC_417 = _readonly('Expectation Failed')
    # 418-421 Unassigned
    RC_422 = _readonly('Unprocessable Entity')
    RC_423 = _readonly('Locked')
    RC_424 = _readonly('Failed Dependency')
    RC_426 = _readonly('Upgrade Required')
    RC_428 = _readonly('Precondition Failed')
    RC_429 = _readonly('Too Many Requests')
    RC_431 = _readonly('Request Header Fields Too Large')
    # 432-499 Unassigned

    # 5xx codes
    RC_500 = _readonly('Internal Server Error')
    RC_501 = _readonly('Not Implemented')
    RC_502 = _readonly('Bad Gateway')
    RC_503 = _readonly('Service Unavailable')
    RC_504 = _readonly('Gateway Timeout')
    RC_505 = _readonly('HTTP Version Not Supported')
    RC_506 = _readonly('Variant Also Negotiates (Experimental)')
    RC_507 = _readonly('Insufficient Storage')
    RC_508 = _readonly('Loop Detected')
    RC_510 = _readonly('Not Extended')
    RC_511 = _readonly('Network Authentication Failed')
    # 512-599 Unassigned


HttpRCType = _HttpRCType('HttpRCType', (object,), {})
HttpRCDescrType = _HttpRCDescrType('HttpRCDescrType',
                                   (object,), {})


codetype_1xx = (HttpRCType.RC_100,
                HttpRCType.RC_101,
                HttpRCType.RC_102)


codetype_2xx = (HttpRCType.RC_200,
                HttpRCType.RC_201,
                HttpRCType.RC_202,
                HttpRCType.RC_203,
                HttpRCType.RC_204,
                HttpRCType.RC_205,
                HttpRCType.RC_206,
                HttpRCType.RC_207,
                HttpRCType.RC_208,
                HttpRCType.RC_226)


codetype_3xx = (HttpRCType.RC_300,
                HttpRCType.RC_301,
                HttpRCType.RC_302,
                HttpRCType.RC_303,
                HttpRCType.RC_304,
                HttpRCType.RC_305,
                HttpRCType.RC_307,
                HttpRCType.RC_308)

codetype_4xx = (HttpRCType.RC_400,
                HttpRCType.RC_401,
                HttpRCType.RC_402,
                HttpRCType.RC_403,
                HttpRCType.RC_404,
                HttpRCType.RC_405,
                HttpRCType.RC_406,
                HttpRCType.RC_407,
                HttpRCType.RC_408,
                HttpRCType.RC_409,
                HttpRCType.RC_410,
                HttpRCType.RC_411,
                HttpRCType.RC_412,
                HttpRCType.RC_413,
                HttpRCType.RC_414,
                HttpRCType.RC_415,
                HttpRCType.RC_416,
                HttpRCType.RC_417,
                HttpRCType.RC_422,
                HttpRCType.RC_423,
                HttpRCType.RC_424,
                HttpRCType.RC_426,
                HttpRCType.RC_428,
                HttpRCType.RC_429,
                HttpRCType.RC_431)


codetype_5xx = (HttpRCType.RC_500,
                HttpRCType.RC_501,
                HttpRCType.RC_502,
                HttpRCType.RC_503,
                HttpRCType.RC_504,
                HttpRCType.RC_505,
                HttpRCType.RC_506,
                HttpRCType.RC_507,
                HttpRCType.RC_508,
                HttpRCType.RC_510,
                HttpRCType.RC_511)


codetype_experimental = (HttpRCType.RC_506,)


codetype_deprecated = ()


def is_1xx(code):
    """ Determines if the given code is a 1xx code or not"""

    if code in codetype_1xx:
        return True
    return False


def is_2xx(code):
    """ Determines if the given code is a 2xx code or not"""

    if code in codetype_2xx:
        return True
    return False


def is_3xx(code):
    """ Determines if the given code is a 3xx code or not"""

    if code in codetype_3xx:
        return True
    return False


def is_4xx(code):
    """ Determines if the given code is a 4xx code or not"""

    if code in codetype_4xx:
        return True
    return False
    pass


def is_5xx(code):
    """ Determines if the given code is a 5xx code or not"""

    if code in codetype_5xx:
        return True
    return False


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
    """ Determines if the given code is a [1-5]xx code or not"""

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


def get_2xx_codes():
    """ returns a list (tuple) of 2xx codes """

    return codetype_2xx


def get_3xx_codes():
    """ returns a list (tuple) of 3xx codes """

    return codetype_3xx


def get_4xx_codes():
    """ returns a list (tuple) of 4xx codes """

    return codetype_4xx


def get_5xx_codes():
    """ returns a list (tuple) of 5xx codes """

    return codetype_5xx


def get_experimental_codes():
    """ returns a list (tuple) of experimental codes """

    return codetype_experimental


def get_deprecated_codes():
    """ returns a list (tuple) of deprecated codes """

    return codetype_deprecated


if __name__ == '__main__':
    print(HttpRCType.RC_200)
    print(HttpRCType.RC_300)
    print(HttpRCType.RC_400)
    print(HttpRCType.RC_500)
    print(is_valid('100'))
    print(is_valid('200'))
    print(is_valid('300'))
    print(is_valid('400'))
    print(is_valid('500'))
    print(is_valid('600'))
    print(is_1xx('100'))
    print(is_1xx(HttpRCType.RC_100))
    print(is_1xx(HttpRCType.RC_CONTINUE))
    print(is_1xx(HttpRCType.RC_200))
    print(is_2xx(HttpRCType.RC_200))
    print(is_2xx(HttpRCType.RC_300))
    print(is_3xx(HttpRCType.RC_300))
    print(is_3xx(HttpRCType.RC_400))
    print(is_4xx(HttpRCType.RC_400))
    print(is_4xx(HttpRCType.RC_500))
    print(is_5xx(HttpRCType.RC_500))
    print(is_5xx(HttpRCType.RC_500))
    print(is_experimental(HttpRCType.RC_506))
    print(is_experimental(HttpRCType.RC_100))
    print(is_deprecated(HttpRCType.RC_506))
    print(is_deprecated(HttpRCType.RC_100))
