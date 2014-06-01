#! /usr/bin/python

import pika
import logging
import uuid
import sys
import traceback

logging.basicConfig()

method_dict = {'fibo': 'com.goffersoft.math.algo.fibo'}


class RpcNameService:
    def __init__(self, exchange, conn_params):
        self.__exchange = exchange
        self.__connection = pika.BlockingConnection(
            pika.ConnectionParameters(*conn_params)
            )
        self.__channel = self.__connection.channel()
        self.__channel.exchange_declare(
            exchange=self.__exchange,
            type='fanout'
            )
        result = self.__channel.queue_declare(exclusive=True)
        self.__queue = result.method.queue
        self.__channel.queue_bind(
            exchange=self.__exchange,
            queue=self.__queue
            )

    def __create_message(self, method):
        message = method + '\r\n'
        message += '\r\n'
        message += method_dict[method] + '\r\n'
        return message

    def __on_request(self, ch, method, props, body):
        try:
            args = body.split("\r\n")
            print "%r" % args
            i = 0
            message = None
            if len(args) != 6:
                print "Failure:malformed message body : \r\n[" + body + ']\r\n'
            elif args[0] in method_dict and method_dict[args[0]] is not None:
                message = self.__create_message(args[0])

            if message is not None:
                print "%r" % message
                self.__channel.basic_publish(
                    exchange=args[2],
                    routing_key=str(args[4]),
                    properties=pika.BasicProperties(
                        correlation_id=props.correlation_id
                    ),
                    body=message
                )
        except:
            print "Unexpected error:", sys.exc_info()[0]
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60

    def __call__(self):
        self.__channel.basic_consume(
            self.__on_request,
            queue=self.__queue,
            no_ack=True
            )
        self.__channel.start_consuming()

    def __del__(self):
        self.__channel.close()
        self.__connection.close()


if __name__ == "__main__":
    import sys
    rpc = RpcNameService(
        (len(sys.argv) > 1 and
         sys.argv[1]) or
        'rpc_ns_exchange', ('localhost', )
        )
    rpc()
