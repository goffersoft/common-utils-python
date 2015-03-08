#! /usr/bin/python

from com.goffersoft.utils.utils import readonly
import com.goffersoft.utils.uid


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


class _HttpRCType(type):
    """HTTP Status Codes"""
    # 1xx codes
    RC_100 = readonly('100')
    RC_CONTINUE = readonly('100')
    RC_101 = readonly('101')
    RC_SWITCHING_PROTOCOLS = readonly('101')
    RC_102 = readonly('102')
    RC_PROCESSING = readonly('102')
    # 103-199 Unassigned

    # 2xx codes
    RC_200 = readonly('200')
    RC_OK = readonly('200')
    RC_201 = readonly('201')
    RC_CREATED = readonly('201')
    RC_202 = readonly('202')
    RC_ACCEPTED = readonly('202')
    RC_203 = readonly('203')
    RC_NON_AUTHORITATIVE_INFORMATION = readonly('203')
    RC_204 = readonly('204')
    RC_NO_CONTENT = readonly('204')
    RC_205 = readonly('205')
    RC_RESET_CONTENT = readonly('205')
    RC_206 = readonly('206')
    RC_PARTIAL_CONTENT = readonly('206')
    RC_207 = readonly('207')
    RC_MULTI_STATUS = readonly('207')
    RC_208 = readonly('208')
    RC_ALREADY_REPORTED = readonly('208')
    # 209-225 Unassigned
    RC_226 = readonly('226')
    RC_IM_USED = readonly('226')
    # 227-299 Unassigned

    # 3xx codes
    RC_300 = readonly('300')
    RC_MULTIPLE_CHOICES = readonly('300')
    RC_301 = readonly('301')
    RC_MOVED_PERMANENTLY = readonly('301')
    RC_302 = readonly('302')
    RC_FOUND = readonly('302')
    RC_303 = readonly('303')
    RC_SEE_OTHER = readonly('303')
    RC_304 = readonly('304')
    RC_NOT_MODIFIED = readonly('304')
    RC_305 = readonly('305')
    RC_USE_PROXY = readonly('305')
    # 306 Unassigned
    RC_307 = readonly('307')
    RC_TEMPORARY_REDIRECT = readonly('307')
    RC_308 = readonly('308')
    RC_PERMANENT_REDIRECT = readonly('308')
    # 309-399 Unassigned

    # 4xx codes
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
    RC_409 = readonly('409')
    RC_CONFLICT = readonly('409')
    RC_410 = readonly('410')
    RC_GONE = readonly('410')
    RC_411 = readonly('411')
    RC_LENGTH_REQUIRED = readonly('411')
    RC_412 = readonly('412')
    RC_PRECONDITION_FAILED = readonly('412')
    RC_413 = readonly('413')
    RC_PAYLOAD_TOO_LARGE = readonly('413')
    RC_414 = readonly('414')
    RC_URI_TOO_LONG = readonly('414')
    RC_415 = readonly('415')
    RC_UNSUPPORTED_MEDIA_TYPE = readonly('415')
    RC_416 = readonly('416')
    RC_REQUESTED_RANGE_NOT_SATISFIABLE = readonly('416')
    RC_417 = readonly('417')
    RC_EXPECTATION_FAILED = readonly('417')
    # 418-421 Unassigned
    RC_422 = readonly('422')
    RC_UNPROCESSABLE_ENTITY = readonly('422')
    RC_423 = readonly('423')
    RC_LOCKED = readonly('423')
    RC_424 = readonly('424')
    RC_FAILED_DEPENDENCY = readonly('424')
    # 425 Unassigned
    RC_426 = readonly('426')
    RC_UGRADE_REQUIRED = readonly('426')
    # 427 Unassigned
    RC_428 = readonly('428')
    RC_PRECONDITION_REQUIRED = readonly('428')
    RC_429 = readonly('429')
    RC_TOO_MANY_REQUESTS = readonly('429')
    # 430 Unassigned
    RC_431 = readonly('431')
    RC_REQUEST_HEADER_FIELDS_TOO_LARGE = readonly('431')
    # 432-499 Unassigned

    # 5xx codes
    RC_500 = readonly('500')
    RC_INTERNAL_SERVER_ERROR = readonly('500')
    RC_501 = readonly('501')
    RC_NOT_IMPLEMENTED = readonly('501')
    RC_502 = readonly('502')
    RC_BAD_GATEWAY = readonly('502')
    RC_503 = readonly('503')
    RC_SERVICE_UNAVAILABLE = readonly('503')
    RC_504 = readonly('504')
    RC_GATEWAY_TIMEOUT = readonly('504')
    RC_505 = readonly('505')
    RC_HTTP_VERSION_NOT_SUPPORTED = readonly('505')
    RC_506 = readonly('506')
    RC_VARIANT_ALSO_NEGOTIATES = readonly('506')
    RC_507 = readonly('507')
    RC_INSUFFICIENT_STORAGE = readonly('507')
    RC_508 = readonly('508')
    RC_LOOP_DETCTED = readonly('508')
    # 509 Unassigned
    RC_510 = readonly('510')
    RC_NOT_EXTENDED = readonly('510')
    RC_511 = readonly('511')
    RC_NETWORK_AUTHENTICATION_FAILED = readonly('511')
    # 512-599 Unassigned


class _HttpRCDescrType(type):
    """HTTP Status Codes - Descriptive Text"""
    # 1xx codes
    RC_100 = readonly('Continue')
    RC_101 = readonly('Switching Protocols')
    RC_102 = readonly('Processing')
    # 103-199 Unassigned

    # 2xx codes
    RC_200 = readonly('OK')
    RC_201 = readonly('Created')
    RC_202 = readonly('Accepted')
    RC_203 = readonly('Non-Authoritative Information')
    RC_204 = readonly('No Content')
    RC_205 = readonly('Reset Content')
    RC_206 = readonly('Partial Content')
    RC_207 = readonly('Multi-Status')
    RC_208 = readonly('Already Supported')
    # 209-225 Unassigned
    RC_226 = readonly('IM Used')
    # 227-299 Unassigned

    # 3xx codes
    RC_300 = readonly('Mutliple Choices')
    RC_301 = readonly('Moved Permanently')
    RC_302 = readonly('Found')
    RC_303 = readonly('See Other')
    RC_304 = readonly('Not Modified')
    RC_305 = readonly('Use Proxy')
    RC_307 = readonly('Temporary Redirect')
    RC_308 = readonly('Permanent Redirect')
    # 309-399 Unassigned

    # 4xx codes
    RC_400 = readonly('Bad Request')
    RC_401 = readonly('Unauthorized')
    RC_402 = readonly('Payment Required')
    RC_403 = readonly('Forbidden')
    RC_404 = readonly('Not Found')
    RC_405 = readonly('Method Not Allowed')
    RC_406 = readonly('Not Acceptable')
    RC_407 = readonly('Proxy Authentication Required')
    RC_408 = readonly('Request Timeout')
    RC_409 = readonly('Conflict')
    RC_410 = readonly('Gone')
    RC_411 = readonly('Length Required')
    RC_412 = readonly('Precondition Failed')
    RC_413 = readonly('Payload Too Large')
    RC_414 = readonly('URI Too Long')
    RC_415 = readonly('Unsupported Media Type')
    RC_416 = readonly('Requested Range Not Satisfiable')
    RC_417 = readonly('Expectation Failed')
    # 418-421 Unassigned
    RC_422 = readonly('Unprocessable Entity')
    RC_423 = readonly('Locked')
    RC_424 = readonly('Failed Dependency')
    RC_426 = readonly('Upgrade Required')
    RC_428 = readonly('Precondition Failed')
    RC_429 = readonly('Too Many Requests')
    RC_431 = readonly('Request Header Fields Too Large')
    # 432-499 Unassigned

    # 5xx codes
    RC_500 = readonly('Internal Server Error')
    RC_501 = readonly('Not Implemented')
    RC_502 = readonly('Bad Gateway')
    RC_503 = readonly('Service Unavailable')
    RC_504 = readonly('Gateway Timeout')
    RC_505 = readonly('HTTP Version Not Supported')
    RC_506 = readonly('Variant Also Negotiates (Experimental)')
    RC_507 = readonly('Insufficient Storage')
    RC_508 = readonly('Loop Detected')
    RC_510 = readonly('Not Extended')
    RC_511 = readonly('Network Authentication Failed')
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
    """Determines if the given code is a 1xx code or not"""
    if code in codetype_1xx:
        return True
    return False


def is_2xx(code):
    """Determines if the given code is a 2xx code or not"""
    if code in codetype_2xx:
        return True
    return False


def is_3xx(code):
    """Determines if the given code is a 3xx code or not"""
    if code in codetype_3xx:
        return True
    return False


def is_4xx(code):
    """Determines if the given code is a 4xx code or not"""
    if code in codetype_4xx:
        return True
    return False


def is_5xx(code):
    """Determines if the given code is a 5xx code or not"""
    if code in codetype_5xx:
        return True
    return False


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
    """Determines if the given code is a [1-5]xx code or not"""
    if(code in codetype_1xx or
       code in codetype_2xx or
       code in codetype_3xx or
       code in codetype_4xx or
       code in codetype_5xx):
        return True
    return False


def get_1xx_codes():
    """returns a list (tuple) of 1xx codes"""
    return codetype_1xx


def get_2xx_codes():
    """returns a list (tuple) of 2xx codes"""
    return codetype_2xx


def get_3xx_codes():
    """returns a list (tuple) of 3xx codes"""
    return codetype_3xx


def get_4xx_codes():
    """returns a list (tuple) of 4xx codes"""
    return codetype_4xx


def get_5xx_codes():
    """returns a list (tuple) of 5xx codes"""
    return codetype_5xx


def get_experimental_codes():
    """returns a list (tuple) of experimental codes"""
    return codetype_experimental


def get_deprecated_codes():
    """returns a list (tuple) of deprecated codes"""
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
