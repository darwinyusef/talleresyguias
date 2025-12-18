"""
Event Bus implementation using RabbitMQ.
"""
import json
import logging
from typing import Callable, Dict, List, Optional
from uuid import UUID

try:
    import pika
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import Basic, BasicProperties
except ImportError:
    pika = None

try:
    import redis
    from redis import Redis
except ImportError:
    redis = None

from .schemas import BaseEvent, EventType

logger = logging.getLogger(__name__)


class EventBus:
    """
    Event Bus usando RabbitMQ para pub/sub.
    """

    def __init__(
        self,
        rabbitmq_url: str,
        exchange_name: str = "ml_events",
        exchange_type: str = "topic",
    ):
        self.rabbitmq_url = rabbitmq_url
        self.exchange_name = exchange_name
        self.exchange_type = exchange_type
        self.connection: Optional[pika.BlockingConnection] = None
        self.channel: Optional[BlockingChannel] = None

    def connect(self):
        """Establece conexión con RabbitMQ."""
        if pika is None:
            logger.warning("pika not installed, using mock connection")
            return

        try:
            self.connection = pika.BlockingConnection(
                pika.URLParameters(self.rabbitmq_url)
            )
            self.channel = self.connection.channel()

            # Declarar exchange
            self.channel.exchange_declare(
                exchange=self.exchange_name,
                exchange_type=self.exchange_type,
                durable=True,
            )

            logger.info(f"Connected to RabbitMQ: {self.exchange_name}")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    def disconnect(self):
        """Cierra conexión con RabbitMQ."""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            logger.info("Disconnected from RabbitMQ")

    def publish(
        self,
        event: BaseEvent,
        routing_key: Optional[str] = None,
    ) -> bool:
        """Publica un evento al exchange."""
        if not self.channel:
            logger.warning("Not connected to RabbitMQ, skipping publish")
            return False

        try:
            routing_key = routing_key or event.metadata.event_type.value

            properties = BasicProperties(
                content_type="application/json",
                delivery_mode=2,  # persistent
                message_id=str(event.metadata.event_id),
                correlation_id=str(event.metadata.correlation_id)
                if event.metadata.correlation_id
                else None,
            )

            self.channel.basic_publish(
                exchange=self.exchange_name,
                routing_key=routing_key,
                body=event.model_dump_json(),
                properties=properties,
            )

            logger.info(f"Published event {event.metadata.event_type.value}")
            return True

        except Exception as e:
            logger.error(f"Failed to publish event: {e}")
            return False


class RedisEventStore:
    """Event Store usando Redis."""

    def __init__(self, redis_url: str):
        if redis is None:
            logger.warning("redis not installed, using mock store")
            self.redis_client = None
        else:
            try:
                self.redis_client: Redis = redis.from_url(
                    redis_url, decode_responses=True
                )
            except Exception as e:
                logger.error(f"Failed to connect to Redis: {e}")
                self.redis_client = None

    def store_event(self, event: BaseEvent) -> bool:
        """Almacena evento en Redis."""
        if not self.redis_client:
            logger.warning("Redis not connected, skipping store")
            return False

        try:
            event_key = f"event:{event.metadata.event_id}"
            self.redis_client.setex(
                event_key,
                86400,  # TTL 24 horas
                event.model_dump_json(),
            )
            return True
        except Exception as e:
            logger.error(f"Failed to store event: {e}")
            return False

    def get_event(self, event_id: UUID) -> Optional[BaseEvent]:
        """Recupera evento por ID."""
        if not self.redis_client:
            return None

        try:
            event_key = f"event:{event_id}"
            event_data = self.redis_client.get(event_key)
            if event_data:
                return BaseEvent.model_validate_json(event_data)
            return None
        except Exception as e:
            logger.error(f"Failed to get event: {e}")
            return None
