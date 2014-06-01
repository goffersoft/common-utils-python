#! /usr/bin/python

import pika
import logging
import uuid

logging.basicConfig()

logger = logging.getLogger(__name__)


class RpcFind:
    def __init__(self, rpc_exchange,
                 rpc_nameservice_exchange,
                 conn_params, timeout=60):
        self.__rpc_exchange = rpc_exchange
        self.__rpc_nameservice_exchange = rpc_nameservice_exchange
        self.__timedout = False
        self.__timeout = 0
        self.__timeout_id = None
        self.__connection = pika.BlockingConnection(
            pika.ConnectionParameters(*conn_params)
            )
        self.__channel = self.__connection.channel()
        self.__channel.exchange_declare(
            exchange=self.__rpc_exchange,
            type='topic'
            )
        self.__channel.exchange_declare(
            exchange=self.__rpc_nameservice_exchange,
            type='fanout'
            )
        result = self.__channel.queue_declare(exclusive=True)
        self.__callback_queue = result.method.queue
        self.__routing_key = str(self.__callback_queue) + \
            ".RpcNameServiceClient"
        self.set_timeout(timeout)

    def __create_message(self):
        message = self.__method + '\r\n'
        message += '\r\n'
        message += self.__rpc_exchange + '\r\n'
        message += '\r\n'
        message += self.__routing_key + '\r\n'
        return message

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
        print "timedout waiting for a response "

    def __on_response(self, ch, method, props, body):
        if self.__correlation_id == props.correlation_id:
            self.__response = body

    def __call__(self, method, callback=None):
        self.__correlation_id = str(uuid.uuid4())
        self.__method = method
        properties = pika.BasicProperties(
            correlation_id=self.__correlation_id
            )
        self.__channel.queue_bind(
            exchange=self.__rpc_exchange,
            queue=self.__callback_queue,
            routing_key=self.__routing_key
            )
        self.__channel.basic_consume(
            self.__on_response,
            self.__callback_queue,
            no_ack=True
            )
        self.__channel.basic_publish(
            exchange=self.__rpc_nameservice_exchange,
            routing_key='',
            properties=properties,
            body=self.__create_message()
            )
        self.__response = None
        while(self.__response is None and self.__timedout is not True):
            self.__connection.process_data_events()

        if self.__response is not None:
            print "%r" % self.__response
            args = self.__response.split('\r\n')
            return args[2]
        else:
            return None


if __name__ == "__main__":
    import sys

    usage_string = """
    Usage : %s <method>
        """

    def print_usage_and_exit(reason):
        print(reason)
        sys.exit(usage_string % sys.argv[0])

    if len(sys.argv) != 2:
        print_usage_and_exit("error : Need 1 arg")

    method = sys.argv[1]

    rpc = RpcFind('rpc_exchange', 'rpc_ns_exchange', ('localhost',))

    rpc.set_timeout(15)

    result = rpc(method)

    if result is not None:
        print "result=%r" % result
    else:
        print "timedout waiting for a response "
