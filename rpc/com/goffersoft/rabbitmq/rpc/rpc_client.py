#! /usr/bin/python

import pika
import logging
import uuid
from rpc_find import RpcFind


class RpcClient:
    def __init__(self, exchange, ns_exchange,
                 conn_params, timeout=60, logger=None):
        self.__logger = logger or logging.getLogger(self.__class__.__name__)
        self.__exchange = exchange
        self.__ns_exchange = ns_exchange
        self.__timedout = False
        self.__timeout = 0
        self.__timeout_id = None
        self.__connection = pika.BlockingConnection(
            pika.ConnectionParameters(*conn_params)
            )
        self.__channel = self.__connection.channel()
        self.__channel.exchange_declare(
            exchange=self.__exchange,
            type='topic'
            )
        result = self.__channel.queue_declare(exclusive=True)
        self.__callback_queue = result.method.queue
        self.__correlation_id = str(uuid.uuid4())
        self.__properties = pika.BasicProperties(
            correlation_id=self.__correlation_id
            )
        self.__channel.basic_consume(
            self.__on_response,
            queue=self.__callback_queue,
            no_ack=True
            )
        self.set_timeout(timeout)

    def get_timeout(self):
        return self.__timeout

    def set_timeout(self, timeout):
        if self.__timeout == timeout:
            return timeout

        prev_timeout = timeout
        self.__timeout = timeout

        if self.__timeout_id is None and timeout > 0:
            self.__timeout_id = self.__connection.add_timeout(
                self.__timeout, self. __on_timeout)
        elif self.__timeout_id is not None and timeout > 0:
            self.__connection.remove_timeout(self.__timeout_id)
            self.__timeout_id = self.__connection.add_timeout(
                self.__timeout, self.__on_timeout)
        elif self.__timeout_id is not None and timeout == 0:
            self.__connection.remove_timeout(self.__timeout_id)
            self.__timeout_id = None

        return prev_timeout

    def __on_timeout(self):
        self.__timedout = True
        self.__logger.debug('timedout waiting for a response')

    def __on_response(self, ch, method, props, body):
        if self.__correlation_id == props.correlation_id:
            self.__response = body.decode()
            self.__logger.debug('[X] = %r', self.__response)

    def __create_message(self, vartargs):
        message = self.__method + '\r\n'
        message += '\r\n'
        message += self.__exchange + '\r\n'
        message += '\r\n'
        for arg in vartargs:
            message += str(arg) + '\r\n'
        return message

    def __find(self):
        ns = RpcFind(self.__exchange, self.__ns_exchange,
                     ('localhost', ), self.__timeout)
        return ns(self.__method)

    def __call__(self, method, vartargs, method_route=None):
        self.__response = None
        self.__method = method
        if method_route is None:
            self.__method_route = self.__find()
        else:
            self.__method_route = method_route

        if self.__method_route is None:
            self.__logger.info('RpcFind timeout : cannot \
                                find route to ' + method)
            return None

        self.__message = self.__create_message(vartargs)
        self.__channel.queue_bind(
            exchange=self.__exchange,
            queue=self.__callback_queue,
            routing_key=self.__method_route + ".result"
            )
        self.__channel.basic_publish(
            exchange=self.__exchange,
            routing_key=self.__method_route,
            properties=self.__properties,
            body=self.__message.encode())

        while(self.__response is None and self.__timedout is not True):
            self.__connection.process_data_events()

        return self.__response

if __name__ == "__main__":
    import sys
    from com.goffersoft.logging import logconf

    logconf.init_logging(default_path='../../../../\
                               conf/logconf_rpcclient.json')

    logger = logging.getLogger(__name__)

    usage_string = """
    Usage : %s <method [arg [arg]]>
               """

    def print_usage_and_exit(reason):
        logger.error(reason)
        sys.exit(usage_string % sys.argv[0])

    if len(sys.argv) < 2:
        print_usage_and_exit('error : Need at least 1 arg')

    method = sys.argv[1]
    list_of_args = sys.argv[2:]

    rpc = RpcClient('rpc_exchange', 'rpc_ns_exchange', ('localhost', ))

    rpc.set_timeout(15)

    ns = RpcFind('rpc_exchange', 'rpc_ns_exchange', ('localhost', ), 15)
    result = ns(method)
    if result is None:
        logger.error('Cannot Execute ' + method + '(Not registered)')
    else:
        result = rpc(method, list_of_args, result)
        logger.info('%r', result)

    result = rpc(method, list_of_args, None)

    if result is None:
        logger.error('Cannot Execute ' + method + '(Not registered)')
    else:
        logger.info('%r', result)
