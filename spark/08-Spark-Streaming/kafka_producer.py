"""
Kafka Producer: Generador de Eventos de Leads
=============================================
Simula eventos de leads en tiempo real y los envía a Kafka
para ser procesados por Spark Streaming.

Eventos generados:
- Nuevos leads con características demográficas
- Acciones: web_view, email_click, form_submit
- Timestamp real
- Variación realista en arrival rate

Uso:
    python 08-Spark-Streaming/kafka_producer.py
"""

import json
import random
import time
from datetime import datetime
from typing import Dict, Any
import os

# Si Kafka no está instalado, instalar con:
# pip install kafka-python

try:
    from kafka import KafkaProducer
    from kafka.errors import KafkaError
    KAFKA_AVAILABLE = True
except ImportError:
    print("⚠️  kafka-python no instalado. Instalar con: pip install kafka-python")
    KAFKA_AVAILABLE = False

class LeadEventGenerator:
    """Genera eventos de leads sintéticos realistas"""

    ACTIONS = ["web_view", "email_click", "form_submit", "nothing"]
    SOURCES = ["google_ads", "facebook", "organic", "referral", "email_campaign"]

    def __init__(self, seed=42):
        random.seed(seed)
        self.lead_counter = 1000

    def generate_lead_event(self) -> Dict[str, Any]:
        """Genera un evento de lead aleatorio"""

        # Edad con distribución realista
        age = random.gauss(40, 15)
        age = max(18, min(70, int(age)))

        # Salary correlacionado con edad
        base_salary = 30000 + (age - 18) * 1500
        salary = base_salary + random.gauss(0, 20000)
        salary = max(20000, min(200000, salary))

        # Web visits - distribución power law
        web_visits = int(random.expovariate(1/10))
        web_visits = max(1, min(50, web_visits))

        # Last action - probabilidades diferentes
        action_weights = [0.4, 0.25, 0.25, 0.1]  # más web_view, menos nothing
        last_action = random.choices(self.ACTIONS, weights=action_weights)[0]

        # Source
        source = random.choice(self.SOURCES)

        event = {
            "lead_id": self.lead_counter,
            "timestamp": datetime.now().isoformat(),
            "age": age,
            "salary": round(salary, 2),
            "web_visits": web_visits,
            "last_action": last_action,
            "source": source
        }

        self.lead_counter += 1

        return event

class KafkaLeadProducer:
    """Producer de Kafka para eventos de leads"""

    def __init__(
        self,
        bootstrap_servers="localhost:9092",
        topic="leads-events"
    ):
        self.topic = topic

        if not KAFKA_AVAILABLE:
            raise ImportError("kafka-python no está instalado")

        print(f"🔌 Conectando a Kafka: {bootstrap_servers}")
        print(f"📤 Topic: {topic}")

        try:
            self.producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: str(k).encode('utf-8') if k else None,
                acks='all',  # Wait for all replicas
                retries=3,
                max_in_flight_requests_per_connection=1
            )
            print("✅ Conectado a Kafka exitosamente")

        except KafkaError as e:
            print(f"❌ Error conectando a Kafka: {e}")
            print("\n💡 Asegúrate de que Kafka esté corriendo:")
            print("   docker run -d --name kafka -p 9092:9092 wurstmeister/kafka")
            raise

        self.generator = LeadEventGenerator()
        self.events_sent = 0

    def send_event(self, event: Dict[str, Any]):
        """Envía un evento a Kafka"""

        try:
            # Usar lead_id como key para partitioning
            future = self.producer.send(
                self.topic,
                key=event['lead_id'],
                value=event
            )

            # Esperar confirmación (opcional, para debug)
            # record_metadata = future.get(timeout=10)

            self.events_sent += 1

            return True

        except Exception as e:
            print(f"❌ Error enviando evento: {e}")
            return False

    def run_continuous(
        self,
        events_per_second=5,
        total_events=None,
        burst_probability=0.1
    ):
        """
        Genera y envía eventos continuamente.

        Args:
            events_per_second: Tasa promedio de eventos
            total_events: Número total de eventos (None = infinito)
            burst_probability: Probabilidad de burst (10x rate)
        """

        print(f"\n⚡ Iniciando generación de eventos...")
        print(f"   Tasa: ~{events_per_second} eventos/segundo")
        print(f"   Total: {'Infinito' if total_events is None else total_events}")
        print(f"   Presiona Ctrl+C para detener\n")

        try:
            events_sent_this_run = 0

            while total_events is None or events_sent_this_run < total_events:
                # Decidir si hacer burst
                is_burst = random.random() < burst_probability
                current_rate = events_per_second * 10 if is_burst else events_per_second

                # Generar evento
                event = self.generator.generate_lead_event()

                # Enviar a Kafka
                success = self.send_event(event)

                if success:
                    events_sent_this_run += 1

                    # Log cada 10 eventos
                    if self.events_sent % 10 == 0:
                        print(f"📊 Eventos enviados: {self.events_sent} "
                              f"{'🔥 BURST' if is_burst else ''}")
                        print(f"   Último evento: Lead {event['lead_id']} - "
                              f"{event['last_action']} - "
                              f"Score estimado: {self._estimate_score(event):.2f}")

                # Sleep para controlar rate
                time.sleep(1.0 / current_rate)

        except KeyboardInterrupt:
            print(f"\n\n🛑 Deteniendo producer...")
            print(f"📈 Total eventos enviados: {self.events_sent}")

        finally:
            self.producer.flush()
            self.producer.close()
            print("✅ Producer cerrado")

    def _estimate_score(self, event: Dict[str, Any]) -> float:
        """Estima score de conversión (para visualización)"""
        score = 0.0

        if event['salary'] > 80000:
            score += 0.3
        elif event['salary'] > 50000:
            score += 0.2

        if event['web_visits'] > 20:
            score += 0.3
        elif event['web_visits'] > 10:
            score += 0.2

        if event['last_action'] == "form_submit":
            score += 0.4
        elif event['last_action'] == "email_click":
            score += 0.2

        return min(score, 1.0)

    def send_test_batch(self, count=100):
        """Envía un batch de eventos de prueba"""
        print(f"📤 Enviando {count} eventos de prueba...")

        for i in range(count):
            event = self.generator.generate_lead_event()
            self.send_event(event)

            if (i + 1) % 10 == 0:
                print(f"   Progreso: {i + 1}/{count}")

        print(f"✅ {count} eventos enviados")

def create_kafka_topic():
    """Crea el topic de Kafka si no existe"""
    try:
        from kafka.admin import KafkaAdminClient, NewTopic

        admin = KafkaAdminClient(bootstrap_servers='localhost:9092')

        topic = NewTopic(
            name='leads-events',
            num_partitions=3,
            replication_factor=1
        )

        admin.create_topics([topic])
        print("✅ Topic 'leads-events' creado")

    except Exception as e:
        print(f"⚠️  No se pudo crear topic (puede que ya exista): {e}")

def main():
    """Función principal"""
    import argparse

    parser = argparse.ArgumentParser(description="Kafka Producer para Eventos de Leads")
    parser.add_argument(
        '--rate',
        type=float,
        default=5.0,
        help='Eventos por segundo (default: 5)'
    )
    parser.add_argument(
        '--total',
        type=int,
        default=None,
        help='Total de eventos a generar (default: infinito)'
    )
    parser.add_argument(
        '--test-batch',
        type=int,
        default=None,
        help='Enviar batch de prueba y salir'
    )
    parser.add_argument(
        '--bootstrap-servers',
        type=str,
        default='localhost:9092',
        help='Kafka bootstrap servers'
    )
    parser.add_argument(
        '--create-topic',
        action='store_true',
        help='Crear topic antes de enviar eventos'
    )

    args = parser.parse_args()

    if not KAFKA_AVAILABLE:
        print("❌ kafka-python no está instalado")
        print("   Instalar con: pip install kafka-python")
        return

    # Crear topic si se solicita
    if args.create_topic:
        create_kafka_topic()

    # Crear producer
    try:
        producer = KafkaLeadProducer(
            bootstrap_servers=args.bootstrap_servers,
            topic="leads-events"
        )

        # Modo test batch
        if args.test_batch:
            producer.send_test_batch(args.test_batch)
        else:
            # Modo continuo
            producer.run_continuous(
                events_per_second=args.rate,
                total_events=args.total
            )

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

    return 0

if __name__ == "__main__":
    """
    Ejemplos de uso:

    # Modo continuo con 5 eventos/segundo
    python kafka_producer.py

    # Modo rápido con 20 eventos/segundo
    python kafka_producer.py --rate 20

    # Enviar 1000 eventos y terminar
    python kafka_producer.py --total 1000

    # Batch de prueba de 100 eventos
    python kafka_producer.py --test-batch 100

    # Crear topic primero
    python kafka_producer.py --create-topic
    """
    exit(main())
