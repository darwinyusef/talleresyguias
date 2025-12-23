"""
Kafka Producer de Ejemplo

Genera eventos sintéticos y los envía a Kafka para testing del pipeline
de streaming ML.

Ejecutar:
    python kafka_producer_example.py --rate 10
"""

from kafka import KafkaProducer
import json
import random
import time
from datetime import datetime
import argparse

class UserEventGenerator:
    """
    Generador de eventos de usuario sintéticos
    """

    EVENT_TYPES = ["page_view", "click", "form_submit", "email_open", "purchase"]

    def __init__(self, seed=42):
        random.seed(seed)
        self.user_counter = 10000

    def generate_event(self):
        """
        Generar un evento de usuario aleatorio
        """
        user_id = random.randint(10000, 15000)

        age = max(18, min(70, int(random.gauss(35, 12))))

        base_salary = 30000 + (age - 18) * 2000
        salary = max(25000, min(200000, base_salary + random.gauss(0, 15000)))

        web_visits = max(1, min(50, int(random.expovariate(1/8))))

        email_opens = max(0, min(30, int(random.expovariate(1/5))))

        event_type = random.choices(
            self.EVENT_TYPES,
            weights=[0.4, 0.3, 0.15, 0.1, 0.05]
        )[0]

        event = {
            "event_id": f"evt_{int(time.time()*1000)}_{user_id}",
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "age": age,
            "salary": round(salary, 2),
            "web_visits": web_visits,
            "email_opens": email_opens
        }

        return event

def create_producer():
    """
    Crear productor de Kafka
    """
    try:
        producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda v: v.encode('utf-8') if v else None,
            acks='all',
            retries=3
        )
        return producer
    except Exception as e:
        print(f"❌ Error connecting to Kafka: {e}")
        print("   Make sure Kafka is running on localhost:9092")
        return None

def produce_events_continuous(producer, topic, rate_per_second):
    """
    Producir eventos continuamente a un rate específico
    """
    generator = UserEventGenerator()

    events_sent = 0
    start_time = time.time()

    print(f"🚀 Producing events to topic '{topic}' at {rate_per_second} events/second")
    print(f"   Press Ctrl+C to stop\n")

    try:
        while True:
            event = generator.generate_event()

            future = producer.send(
                topic,
                key=str(event['user_id']),
                value=event
            )

            events_sent += 1

            if events_sent % 100 == 0:
                elapsed = time.time() - start_time
                actual_rate = events_sent / elapsed

                print(f"📊 Sent {events_sent} events | "
                      f"Rate: {actual_rate:.1f} events/sec | "
                      f"Last event: {event['event_type']} for user {event['user_id']}")

            time.sleep(1.0 / rate_per_second)

    except KeyboardInterrupt:
        elapsed = time.time() - start_time
        actual_rate = events_sent / elapsed

        print(f"\n\n🛑 Stopped producing events")
        print(f"📊 Summary:")
        print(f"   Total events sent: {events_sent}")
        print(f"   Duration: {elapsed:.1f}s")
        print(f"   Average rate: {actual_rate:.1f} events/sec")

    finally:
        producer.flush()
        producer.close()

def produce_events_batch(producer, topic, num_events):
    """
    Producir un batch de eventos
    """
    generator = UserEventGenerator()

    print(f"🚀 Producing {num_events} events to topic '{topic}'...")

    start_time = time.time()

    for i in range(num_events):
        event = generator.generate_event()

        producer.send(
            topic,
            key=str(event['user_id']),
            value=event
        )

        if (i + 1) % 1000 == 0:
            print(f"   Sent {i+1}/{num_events} events...")

    producer.flush()

    elapsed = time.time() - start_time
    rate = num_events / elapsed

    print(f"\n✅ Sent {num_events} events in {elapsed:.2f}s ({rate:.1f} events/sec)")

    producer.close()

def produce_events_burst(producer, topic, bursts, events_per_burst, delay_seconds):
    """
    Producir eventos en bursts (útil para testing de backpressure)
    """
    generator = UserEventGenerator()

    print(f"🚀 Producing {bursts} bursts of {events_per_burst} events")
    print(f"   Delay between bursts: {delay_seconds}s\n")

    total_sent = 0

    try:
        for burst in range(bursts):
            print(f"💥 Burst {burst+1}/{bursts}...")

            start_time = time.time()

            for i in range(events_per_burst):
                event = generator.generate_event()

                producer.send(
                    topic,
                    key=str(event['user_id']),
                    value=event
                )

            producer.flush()

            elapsed = time.time() - start_time
            rate = events_per_burst / elapsed

            print(f"   ✅ Sent {events_per_burst} events in {elapsed:.2f}s ({rate:.0f} events/sec)")

            total_sent += events_per_burst

            if burst < bursts - 1:
                print(f"   ⏸️  Waiting {delay_seconds}s...\n")
                time.sleep(delay_seconds)

    except KeyboardInterrupt:
        print("\n\n🛑 Stopped producing bursts")

    print(f"\n📊 Total events sent: {total_sent}")

    producer.close()

def main():
    """
    Main con CLI
    """
    parser = argparse.ArgumentParser(description='Kafka Event Producer')

    parser.add_argument(
        '--topic',
        type=str,
        default='user-events',
        help='Kafka topic (default: user-events)'
    )

    parser.add_argument(
        '--mode',
        type=str,
        choices=['continuous', 'batch', 'burst'],
        default='continuous',
        help='Production mode (default: continuous)'
    )

    parser.add_argument(
        '--rate',
        type=int,
        default=10,
        help='Events per second for continuous mode (default: 10)'
    )

    parser.add_argument(
        '--num-events',
        type=int,
        default=1000,
        help='Number of events for batch mode (default: 1000)'
    )

    parser.add_argument(
        '--bursts',
        type=int,
        default=5,
        help='Number of bursts for burst mode (default: 5)'
    )

    parser.add_argument(
        '--events-per-burst',
        type=int,
        default=100,
        help='Events per burst (default: 100)'
    )

    parser.add_argument(
        '--delay',
        type=int,
        default=10,
        help='Delay between bursts in seconds (default: 10)'
    )

    args = parser.parse_args()

    print("="*70)
    print("KAFKA EVENT PRODUCER")
    print("="*70)

    producer = create_producer()

    if not producer:
        return

    print(f"\n✅ Connected to Kafka")
    print(f"   Topic: {args.topic}")
    print(f"   Mode: {args.mode}\n")

    if args.mode == 'continuous':
        produce_events_continuous(producer, args.topic, args.rate)
    elif args.mode == 'batch':
        produce_events_batch(producer, args.topic, args.num_events)
    elif args.mode == 'burst':
        produce_events_burst(
            producer,
            args.topic,
            args.bursts,
            args.events_per_burst,
            args.delay
        )

if __name__ == "__main__":
    main()
