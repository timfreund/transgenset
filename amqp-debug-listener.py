from carrot.connection import BrokerConnection
from carrot.messaging import Consumer

if __name__ == '__main__':
    connection = BrokerConnection(hostname='localhost', port=5672,
                                  userid='guest', password='guest',
                                  virtual_host=None)
    consumer = Consumer(connection=connection, queue="transactions",
                        exchange="transactions")
    
    def print_message(message_data, message):
        print(message_data)
        message.ack()

    consumer.register_callback(print_message)
    consumer.wait()

