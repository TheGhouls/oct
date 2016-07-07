"""Contain all zeromq devices needed by OCT
"""
from __future__ import print_function, unicode_literals
import zmq


def forwarder(frontend, backend):
    """Simple pub/sub forwarder

    :param int frontend: fontend zeromq port
    :param int backend: backend zeromq port
    """
    try:
        context = zmq.Context()

        front_sub = context.socket(zmq.SUB)
        front_sub.bind("tcp://*:%d" % frontend)

        front_sub.setsockopt_string(zmq.SUBSCRIBE, "")

        back_pub = context.socket(zmq.PUB)
        back_pub.bind("tcp://*:%d" % backend)

        print("forwarder started, backend on port : %d\tfrontend on port: %d" % (backend, frontend))
        zmq.proxy(front_sub, back_pub)
    except Exception as e:
        print(e)
    finally:
        front_sub.close()
        back_pub.close()
        context.term()


def streamer(frontend, backend):
    """Simple push/pull streamer

    :param int frontend: fontend zeromq port
    :param int backend: backend zeromq port
    """
    try:
        context = zmq.Context()

        front_pull = context.socket(zmq.PULL)
        front_pull.set_hwm(0)
        front_pull.bind("tcp://*:%d" % frontend)

        back_push = context.socket(zmq.PUSH)
        back_push.bind("tcp://*:%d" % backend)

        print("streamer started, backend on port : %d\tfrontend on port: %d" % (backend, frontend))
        zmq.proxy(front_pull, back_push)
    except Exception as e:
        print(e)
    finally:
        front_pull.close()
        back_push.close()
        context.term()
