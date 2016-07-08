"""Start a streamer or a forwarder device for multi-hq tests
"""
from __future__ import print_function

from oct.core import devices


def start_device(name, frontend, backend):
    """Start specified device

    :param str name: name of the device, MUST match one of ['forwarder', 'streamer']
    :param int frontend: frontend bind port for device
    :param int backend: backend bind port for device
    """
    device = getattr(devices, name)
    device(frontend, backend)


def run_device(args):
    start_device(args.device, args.frontend, args.backend)


def run_device_command(sp):
    """
    Main function to run oct tests.
    """
    parser = sp.add_parser('run-device', help="run an oct device for multi-HQ tests")
    parser.add_argument('device', help="The project directory", choices=['forwarder', 'streamer'])
    parser.add_argument('-f', '--frontend', help="frontend port", type=int, required=True)
    parser.add_argument('-b', '--backend', help="backend port", type=int, required=True)

    parser.set_defaults(func=run_device)
