from __future__ import print_function

import zmq
import ujson as json

from oct.results.models import db, Turret


class TurretsManager(object):
    """Turrets management while runing test. This class is in charge to send
    message to turrets and to store informations about active turrets
    """
    STATUS_REQUEST = {'command': 'status_request', 'msg': None}
    START = {'command': 'start', 'msg': 'open fire'}
    STOP = {'command': 'stop', 'msg': 'premature stop'}

    def __init__(self, publish_port):
        self.turrets = {}

        context = zmq.Context()
        self.publisher = context.socket(zmq.PUB)
        self.publisher.bind("tcp://*:{}".format(publish_port))

    def clean(self):
        self.publisher.close()

    def start(self):
        """Publish start message to all turrets
        """
        self.publish(self.START)

    def stop(self):
        """Publish stop message to all turrets
        """
        self.publish(self.STOP)

    def status_request(self):
        """Publish a status request message
        """
        self.publish(self.STATUS_REQUEST)

    def process_message(self, message, is_started=False):
        """Process incomming message from turret

        :param dict message: incomming message
        :param bool is_started: test started indicator
        """
        if 'status' not in message:
            return False
        message['name'] = message['turret']
        del message['turret']
        if not self.add(message, is_started):
            return self.update(message)
        return True

    def add(self, turret_data, is_started=False):
        """Add a turret object to current turrets configuration

        :param dict turret_data: the data of the turret to add
        :param bool is_started: tell if test are already runing
        """
        if turret_data.get('uuid') in self.turrets:
            return False

        turret = Turret(**turret_data)
        self.write(turret)
        self.turrets[turret.uuid] = turret

        if is_started:
            self.publish(self.START, turret.uuid)

        return True

    def update(self, turret_data):
        """Update a given turret

        :param dict turret_data: the data of the turret to update
        """
        if turret_data.get('uuid') not in self.turrets:
            return False
        turret = self.turrets[turret_data.get('uuid')]
        turret.update(**turret_data)
        self.write(turret)
        return True

    def write(self, turret):
        """Write a turret to database

        :param dict turret_data: the data of the turret to write
        """
        with db.execution_context():
            turret.save()

    def publish(self, message, channel=None):
        """Publish a message for all turrets

        :param dict message: message to send to turrets
        :pram str channel: channel to send message, default to empty string
        """
        channel = channel or ''
        data = json.dumps(message)
        self.publisher.send_string("%s %s" % (channel, data))
