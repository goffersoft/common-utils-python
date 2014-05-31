#! /usr/bin/python

import pika
import logging
import uuid
from rpc_find import RpcFind

logging.basicConfig()


class RpcClient:
    def __init__(self, exchange, ns_exchange, conn_params):
        self.__exchange = exchange
        self.__ns_exchange = ns_exchange
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

    def __on_response(self, ch, method, props, body):
        print "[X] = %r" % self.__message
        if self.__correlation_id == props.correlation_id:
            self.__response = body

    def __create_message(self, vartargs):
        message = self.__method + '\r\n'
        message += '\r\n'
        message += self.__exchange + '\r\n'
        message += '\r\n'
        for arg in vartargs:
            message += str(arg) + '\r\n'
        return message

    def __find(self):
        ns = RpcFind(self.__exchange, self.__ns_exchange, ('localhost', ))
        return ns(self.__method)

    def __call__(self, method, vartargs, method_route=None):
        self.__response = None
        self.__method = method
        if method_route is None:
            self.__method_route = self.__find()
        else:
            self.__method_route = method_route
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
            body=self.__message)

        while(self.__response is None):
            self.__connection.process_data_events()

        return self.__response

    def __del__(self):
        self.__channel.close()
        self.__connection.close()

if __name__ == "__main__":
    import sys

    usage_string = """
    Usage : %s <method [arg [arg]]>
               """

    def print_usage_and_exit(reason):
        print(reason)
        sys.exit(usage_string % sys.argv[0])

    if len(sys.argv) < 2:
        print_usage_and_exit("error : Need at least 1 arg")

    method = sys.argv[1]
    list_of_args = sys.argv[2:]

    rpc = RpcClient('rpc_exchange', 'rpc_ns_exchange', ('localhost', ))
    ns = RpcFind('rpc_exchange', 'rpc_ns_exchange', ('localhost', ))
    result = ns(method)
    result = rpc(method, list_of_args, result)
    print "%r" % result
    result = rpc(method, list_of_args, None)
    print "%r" % result
