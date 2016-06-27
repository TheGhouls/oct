"""Contain all zeromq devices needed by OCT
"""
import zmq


def forwarder(frontend, backend):
    """Simple pub/sub forwarder

    :param int frontend: fontend zeromq port
    :param int backend: backend zeromq port
    """
    try:
        context = zmq.Context()

        frontend = context.socket(zmq.SUB)
        frontend.bind("tcp://*:%d" % frontend)

        backend = context.socket(zmq.PUB)
        backend.bind("tcp://*:%d" % backend)

        zmq.device(zmq.FORWARDER, frontend, backend)
    except Exception as e:
        print(e)
    finally:
        frontend.close()
        backend.close()
        context.term()


def streamer(frontend, backend):
    """Simple push/pull streamer

    :param int frontend: fontend zeromq port
    :param int backend: backend zeromq port
    """
    try:
        context = zmq.Context()

        frontend = context.socket(zmq.PULL)
        frontend.set_hwm(0)
        frontend.bind("tcp://*:%d" % frontend)

        backend = context.socket(zmq.PUSH)
        backend.bind("tcp://*:%d" % backend)
    except Exception as e:
        print(e)
    finally:
        frontend.close()
        backend.close()
        context.term()
