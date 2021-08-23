"""this code is based on Publisher-Subscriber pattern of: https://github.com/madhur2511/Publisher-Subscriber-Implementation\
This is a simple implementation of Publisher/Subscriber implementation in Python on a single machine and not over the network."""
import logging
from collections import defaultdict


class Broker:
    """Message Broker / Middle-ware that hosts the message queue and is responsible for making communication possible \
    between publishers and subscribers"""

    def __init__(self):
        """Initializes the Message Queue broker with an empty resource set - message queue and subscriber/topic mapping.
        This will happen only once in time (hopefully) when the message queue is first started and should run continually"""

        self.messaging_queue = []
        self.topic_subscription_mapping = defaultdict(lambda: [])

    def notify(self):
        """This is the main code in the broker which always runs until message queue has no more messages to pass\
        else, it waits for any more messages.  The Broker will delete  the message after forwarding it to the subscriber(s)"""

        for message in self.messaging_queue:
            data, topic = self.process_message(message)
            subscribers = self.get_subscribers_for_topic(topic)
            self.push_message_to_subscribers(subscribers, data)
            self.messaging_queue.remove(message)

    def on_message(self, message):
        """This is like an event that will be fired on receipt of a new message by the broker, but is implemented\
         as a method in current context of non-network based implementation. Drops message if message is lacking a topic"""

        if len(message.split(";")) >= 2:
            self.messaging_queue.append(message)
            logger.info(
                "Message received by Broker and inserted into the queue :  " + message
            )
            self.notify()
        else:
            pass

    def process_message(self, message):
        """divide  the messages received by the broker  into  data and topic"""
        message_parts = message.split(";")
        return message_parts[0], message_parts[1]

    def get_subscribers_for_topic(self, topic):
        """This method return the mapping of subscribers to a given topic"""

        subscribers = self.topic_subscription_mapping[topic]
        return subscribers

    def push_message_to_subscribers(self, subscribers, message):
        """This is like a method implemented using a socket for sending the information/messages to subscribers using ther addresses\
        but is like a method called on their instance in this case."""

        for subscriber in subscribers:
            subscriber.update(message)

    def subscribe_to_topic(self, subscriber, topic):
        """Populates the mapping of Subscribers to topics"""

        self.topic_subscription_mapping[topic].append(subscriber)

    def topic_data(self, subscriber, topic):
        """Aggregates messages on a given topic, upon request of a subscriber and prepares it for sending"""

        messages_for_topic = [
            self.process_message(message)[0]
            for message in self.messaging_queue
            if self.process_message(message)[1] == topic
        ]
        message_aggregator = ""
        for message in messages_for_topic:
            message_aggregator += message + "..."
        self.push_message_to_subscribers([subscriber], message_aggregator)


class IPublisher:
    def publish(self, message, topic):
        """Method used by publishers to publish a message on a topic to subscribers via message broker"""
        raise NotImplementedError


class Publisher(IPublisher):
    """Publisher that publishes topic wise content into the message broker"""

    def __init__(self, name, broker):
        """Initializes a publisher and provide it the details of broker to send its topic based messages to"""
        self.name = name
        self._Broker = broker

    def publish(self, message, topic):
        _message = message + ";" + topic
        logger.info(
            self.name
            + "  , Publishing a message : "
            + message
            + " in topic :  "
            + topic
        )
        self._Broker.on_message(_message)


class ISubscriber:
    def subscribe(self, topic):
        raise NotImplementedError

    def get_topic_data(self, topic):
        """Method used by subscriber to request all data/messages on a given topic at once. \
        This is again supposed to be a network call"""
        self._Broker.topic_data(self, topic)

    def update(self, message):
        """On the subscriber node, this is a call-back event fired on receipt of a message on some port but in this implementation,
        it is like a function call on the given subscriber instance"""
        raise NotImplementedError


class Subscriber(ISubscriber):
    """Subscriber that subscribes to topics with the broker"""

    def __init__(self, name, broker):
        """Initializes the subscriber and provides it the broker details to subscribe to"""
        self.name = name
        self._Broker = broker

    def subscribe(self, topic):
        self._Broker.subscribe_to_topic(self, topic)

    def update(self, message):
        logger.info(self.name + "  , Received a message : " + message)


def main():
    """A scenario is played in the main method to test/exemplify the working of this implementation.
    Logs are written to a separate file upon executing this code named, pub_sub-2-2-4-1.log using logger module in python"""

    logger.info("Starting Message Broker Service")

    broker = Broker()

    s1 = Subscriber("subscriber1", broker)
    s2 = Subscriber("subscriber2", broker)
    s3 = Subscriber("subscriber3", broker)

    # add  your code here: new  subscriber3

    s1.subscribe("topic1")
    s2.subscribe("topic2")
    s3.subscribe("topic3")

    p1 = Publisher("publisher1", broker)
    p2 = Publisher("publisher2", broker)

    p1.publish("Message1", "topic1")
    p1.publish("Message2", "topic2")
    p2.publish("Message3", "topic3")

    # Add your code here

    logger.info("Ending Message Broker Service")


if __name__ == "__main__":
    # Setting logging parameters to record log in a given file in same directory as main file with INFO level

    logger = logging.getLogger(__name__)
    file_handler = logging.FileHandler("2-2-3-1.log", mode="w")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    main()
