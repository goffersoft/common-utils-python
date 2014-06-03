#! /usr/bin/python

import pika
import logging
import uuid
import sys
import traceback

logging.basicConfig()

method_dict = {'fibo': 'com.goffersoft.math.algo.fibo'}


def fibo(x):
    return "Hello World " + str(x)


class RpcService:
    def __init__(self, exchange, conn_params, logger=None):
        self.__logger = logger or logging.getLogger(self.__class__.__name__)
        self.__exchange = exchange
        self.__connection = pika.BlockingConnection(
            pika.ConnectionParameters(*conn_params)
            )
        self.__channel = self.__connection.channel()
        result = self.__channel.queue_declare(exclusive=True)
        self.__queue = result.method.queue
        self.__channel.exchange_declare(
            exchange=self.__exchange,
            type='topic'
            )
        for k in method_dict:
            self.__channel.queue_bind(
                exchange=self.__exchange,
                queue=self.__queue,
                routing_key=method_dict[k]
            )

    def __create_message(self, status, result):
        message = status + '\r\n\r\n'
        message += str(result) + '\r\n'
        return message

    def __on_request(self, ch, method, props, body):
        publish_failure_message = True
        try:
            args = body.split("\r\n")
            self.__logger.debug('%r', args)
            arglist = []
            i = 0
            retval = True
            for arg in args:
                if i == 0:
                    _method = arg
                    if method_dict[_method] is None:
                        retval = False
                        break
                elif arg == '':
                    i += 1
                    continue
                elif i == 2:
                    _exchange = arg
                else:
                    arglist.append(arg)
                i += 1

            if retval is False:
                message = "Failure:malformed message body :\
                           \r\n[" + body + ']\r\n'
            else:
                result = fibo(*arglist)
                message = self.__create_message('Success', result)
                self.__logger.info('%r', message)
            publish_failure_message = False
            self.__channel.basic_publish(
                exchange=_exchange,
                routing_key=method_dict[_method] + ".result",
                properties=pika.BasicProperties(
                    correlation_id=props.correlation_id
                    ),
                body=message
                )
        except:
            self.__logger.exception('Unexpected error:')
            if(publish_failure_message is True):
                error = traceback.format_exc()
                message = self.__create_message('Failure', error)
                try:
                    self.__channel.basic_publish(
                        exchange=_exchange,
                        routing_key=method_dict[_method] + ".result",
                        properties=pika.BasicProperties(
                            correlation_id=props.correlation_id
                            ),
                        body=message
                        )
                except:
                    self.__logger.exception('Unexpected error sending \
                                             exception back to client')

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
    from com.goffersoft.logging import logconf

    logconf.init_logging(default_path='../../../../' +
                         'conf/logconf_rpcservice.json')

    logger = logging.getLogger(__name__)

    rpc = RpcService(
        'rpc_exchange',
        ('localhost', )
        )
    rpc()
