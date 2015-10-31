import math
import random
import sys
import threading
import time

from carrot.connection import BrokerConnection
from carrot.messaging import Publisher

class Multiplexer(object):
    def __init__(self, producer, transmitters, mean_wait):
        self.producer = producer
        self.transmitters = transmitters
        self.mean_wait = mean_wait
        self.transmitting = False
        self.threads = []

    def start_transmissions(self):
        self.transmitting = True
        for transmitter in self.transmitters:
            t = threading.Thread(target=self.transmit, 
                                args=(transmitter, self.producer, self.mean_wait))
            t.start()
        
    def stop_transmissions(self):
        self.transmitting = False

    def transmit(self, transmitter, producer, mean_wait):
        while self.transmitting:
            wait = math.fabs(random.gauss(mean_wait, 1))
            time.sleep(wait)
            msg = producer.next_message()
            transmitter.transmit(msg)

class Transmitter(object):
    def __init__(self, **kv):
        raise Exception("Not implemented")

    def transmit(self, message):
        raise Exception("Not implemented")

class FileTransmitter(Transmitter):
    def __init__(self, output_file=sys.stdout):
        if isinstance(output_file, str):
            output_file = open(output_file, 'w')
        self.output_file = output_file

    def transmit(self, message):
        self.output_file.write("%s\n" % message)

class AMQPTransmitter(Transmitter):
    def __init__(self, hostname='localhost', port=5672,
                 userid=None, password=None, virtual_host=None,
                 exchange=None):
        self.hostname = hostname
        self.port = port
        self.userid = userid
        self.password = password
        self.virtual_host = None
        self.exchange = exchange

        self.connection = BrokerConnection(hostname=self.hostname, port=self.port,
                                           userid=self.userid, password=self.password,
                                           virtual_host=self.virtual_host)
        self.publisher = Publisher(connection=self.connection,
                                   exchange=exchange)

    def transmit(self, message):
        self.publisher.send(message)
