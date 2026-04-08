# Week 10: Message Queues & Apache Kafka

> Master asynchronous communication and event streaming

---

## 📖 High-Level Overview

Message queues enable asynchronous communication between services, providing:
- Decoupling of producers and consumers
- Load leveling and buffering
- Fault tolerance and reliability
- Event-driven architectures

### Key Topics:
1. **Message Queue Concepts** - Queues vs Topics, pub/sub
2. **Apache Kafka** - Architecture, partitions, consumers
3. **RabbitMQ Basics** - Exchanges, queues, bindings
4. **Design Patterns** - Event sourcing, CQRS
5. **Best Practices** - Idempotency, ordering, monitoring

---

## 🔬 Low-Level Details

### Message Queue Fundamentals

#### Queue vs Topic (Pub/Sub)

```
QUEUE (Point-to-Point):
Producer ──▶ [Queue] ──▶ Consumer
                         (One consumer processes each message)

Each message is delivered to ONE consumer.
Example: Task distribution

TOPIC (Publish/Subscribe):
Producer ──▶ [Topic] ──▶ Consumer 1
                    ──▶ Consumer 2
                    ──▶ Consumer 3
                    (All consumers get a copy)

Each message is delivered to ALL subscribers.
Example: Event notifications
```

#### Common Message Patterns

```
1. Work Queue (Competing Consumers)
   ┌──────────┐     ┌──────────┐
   │ Producer │────▶│  Queue   │────▶ Consumer 1
   └──────────┘     └──────────┘────▶ Consumer 2
                                ────▶ Consumer 3
   
   Use: Distribute CPU-intensive tasks

2. Publish/Subscribe
   ┌──────────┐     ┌──────────┐     ┌────────────┐
   │ Producer │────▶│ Exchange │────▶│ Queue 1    │──▶ Consumer 1
   └──────────┘     └──────────┘────▶│ Queue 2    │──▶ Consumer 2
                                     └────────────┘

   Use: Broadcast events

3. Request/Reply
   ┌──────────┐     ┌──────────┐     ┌──────────┐
   │ Requester│────▶│ Request Q│────▶│ Responder│
   │          │◀────│ Reply Q  │◀────│          │
   └──────────┘     └──────────┘     └──────────┘

   Use: RPC-style communication
```

---

## 🦊 Apache Kafka Deep Dive

### What is Kafka?

Apache Kafka is a distributed event streaming platform:
- High throughput (millions of events/second)
- Durability (persistent storage)
- Scalable (distributed by design)
- Real-time processing

### Kafka Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        KAFKA CLUSTER                            │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                       ZooKeeper                             ││
│  │        (Cluster management, leader election)                ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Broker 1   │  │  Broker 2   │  │  Broker 3   │             │
│  │             │  │             │  │             │             │
│  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │             │
│  │ │Topic A  │ │  │ │Topic A  │ │  │ │Topic A  │ │             │
│  │ │Partition│ │  │ │Partition│ │  │ │Partition│ │             │
│  │ │   0     │ │  │ │   1     │ │  │ │   2     │ │             │
│  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │             │
│  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │             │
│  │ │Topic B  │ │  │ │Topic B  │ │  │ │Topic B  │ │             │
│  │ │Partition│ │  │ │Partition│ │  │ │Partition│ │             │
│  │ │   0     │ │  │ │   1     │ │  │ │   0     │ │             │
│  │ │(replica)│ │  │ │(replica)│ │  │ │(leader) │ │             │
│  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
          ▲                                      │
          │                                      ▼
    ┌──────────┐                          ┌──────────────┐
    │ Producer │                          │   Consumer   │
    │          │                          │    Group     │
    └──────────┘                          └──────────────┘
```

### Core Concepts

#### Topics and Partitions

```
TOPIC: A category/feed name for records
       Similar to a database table

PARTITION: An ordered, immutable sequence of records
           Enables parallelism

Topic "orders" with 3 partitions:

Partition 0: [0][1][2][3][4][5][6]...
Partition 1: [0][1][2][3]...
Partition 2: [0][1][2][3][4][5]...

Each partition:
- Has its own offset (position)
- Can be on different brokers
- Has replicas for fault tolerance
```

#### Producers

```python
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: k.encode('utf-8') if k else None,
    acks='all',  # Wait for all replicas
    retries=3
)

# Send message
def send_order(order):
    # Key determines partition (same key → same partition → ordering)
    future = producer.send(
        topic='orders',
        key=order['user_id'],  # Partition key
        value=order
    )
    
    # Block until sent (or handle asynchronously)
    try:
        record_metadata = future.get(timeout=10)
        print(f"Sent to {record_metadata.topic}:{record_metadata.partition}:{record_metadata.offset}")
    except Exception as e:
        print(f"Failed to send: {e}")

# Example
send_order({
    'order_id': '12345',
    'user_id': 'user_abc',
    'items': [{'sku': 'A1', 'qty': 2}],
    'total': 99.99
})

# Always flush before exit
producer.flush()
producer.close()
```

**Producer Acknowledgments (acks):**
```
acks=0:   Fire and forget (fastest, least reliable)
acks=1:   Wait for leader (balanced)
acks=all: Wait for all replicas (slowest, most reliable)
```

#### Consumers and Consumer Groups

```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'orders',
    bootstrap_servers=['localhost:9092'],
    group_id='order-processor',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    auto_commit_interval_ms=5000,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Consume messages
for message in consumer:
    print(f"Received: {message.topic}:{message.partition}:{message.offset}")
    print(f"Key: {message.key}, Value: {message.value}")
    
    # Process the order
    process_order(message.value)

# With manual commit
consumer = KafkaConsumer(
    'orders',
    group_id='order-processor',
    enable_auto_commit=False
)

for message in consumer:
    try:
        process_order(message.value)
        consumer.commit()  # Commit after successful processing
    except Exception as e:
        print(f"Processing failed: {e}")
        # Message will be redelivered
```

**Consumer Groups:**
```
Consumer Group "order-processor":

Topic "orders" (3 partitions)

                  ┌──────────────┐
Partition 0 ────▶ │ Consumer 1   │
                  └──────────────┘
                  ┌──────────────┐
Partition 1 ────▶ │ Consumer 2   │
                  └──────────────┘
                  ┌──────────────┐
Partition 2 ────▶ │ Consumer 3   │
                  └──────────────┘

Each partition is consumed by ONE consumer in the group.
Max consumers = number of partitions.
Adding more consumers than partitions → some consumers idle.
```

#### Replication

```
Topic "orders", Partition 0, Replication Factor = 3

Broker 1: Partition 0 (Leader)     ◀── Writes/Reads
Broker 2: Partition 0 (Follower)   ← Replicates from leader
Broker 3: Partition 0 (Follower)   ← Replicates from leader

If Broker 1 fails:
- ZooKeeper/KRaft detects failure
- Broker 2 or 3 becomes new leader
- Producers/consumers automatically switch
```

### Kafka Use Cases

| Use Case | Description |
|----------|-------------|
| **Event Streaming** | Real-time data pipelines between systems |
| **Log Aggregation** | Collect logs from multiple services |
| **Metrics** | Operational monitoring data |
| **Activity Tracking** | User behavior, clickstreams |
| **Event Sourcing** | Store all state changes as events |
| **Stream Processing** | Real-time analytics with Kafka Streams |

---

## 🐰 RabbitMQ Overview

### RabbitMQ vs Kafka

| Feature | RabbitMQ | Kafka |
|---------|----------|-------|
| **Model** | Message broker | Event streaming |
| **Delivery** | Push-based | Pull-based |
| **Message retention** | Until consumed | Configurable retention |
| **Ordering** | Per-queue | Per-partition |
| **Replay** | Not supported | Supported |
| **Throughput** | ~10K msgs/sec | ~1M msgs/sec |
| **Best for** | Complex routing, RPC | High-volume streaming |

### RabbitMQ Concepts

```
EXCHANGE: Receives messages from producers, routes to queues

QUEUE: Stores messages until consumed

BINDING: Rules for routing from exchange to queue

Exchange Types:
- Direct:  Route by exact routing key
- Fanout:  Broadcast to all bound queues
- Topic:   Route by pattern (*.log, order.#)
- Headers: Route by message headers
```

### RabbitMQ Example

```python
import pika

# Producer
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

# Declare exchange and queue
channel.exchange_declare(exchange='orders', exchange_type='direct')
channel.queue_declare(queue='order_processing', durable=True)
channel.queue_bind(exchange='orders', queue='order_processing', routing_key='new')

# Send message
channel.basic_publish(
    exchange='orders',
    routing_key='new',
    body='{"order_id": "123"}',
    properties=pika.BasicProperties(
        delivery_mode=2,  # Persistent
    )
)
connection.close()

# Consumer
def callback(ch, method, properties, body):
    print(f"Received: {body}")
    # Process order
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='order_processing', on_message_callback=callback)
channel.start_consuming()
```

---

## 🎨 Event-Driven Patterns

### Event Sourcing

```
Traditional:
┌─────────────────────────────────────────────┐
│ Current State: {balance: 100}               │
└─────────────────────────────────────────────┘

Event Sourcing:
┌─────────────────────────────────────────────┐
│ Event 1: AccountCreated {balance: 0}        │
│ Event 2: Deposited {amount: 150}            │
│ Event 3: Withdrawn {amount: 50}             │
│ ─────────────────────────────────────────── │
│ Current State: {balance: 100}               │
└─────────────────────────────────────────────┘

Benefits:
- Complete audit trail
- Time travel (rebuild state at any point)
- Event replay for new projections
```

### CQRS (Command Query Responsibility Segregation)

```
Traditional:
┌──────────────────────────────────────────────────────┐
│                  Same Model                          │
│     Reads ◀──────────────────────────▶ Writes        │
└──────────────────────────────────────────────────────┘

CQRS:
┌─────────────────────┐           ┌─────────────────────┐
│   Command Model     │           │    Query Model      │
│  (Write-optimized)  │           │  (Read-optimized)   │
│                     │           │                     │
│  - Validations      │   Events  │  - Denormalized     │
│  - Business logic   │ ────────▶ │  - Materialized     │
│  - Event generation │           │    views            │
└─────────────────────┘           └─────────────────────┘
        ▲                                   │
        │                                   ▼
   Commands                              Queries
   (create, update)                      (read)
```

### Transactional Outbox Pattern

```
Problem: How to atomically update DB and publish event?

Solution: Transactional Outbox

┌─────────────────────────────────────────────────────┐
│                    Database                         │
│  ┌───────────────────┬───────────────────────────┐  │
│  │   Orders Table    │    Outbox Table           │  │
│  │                   │                           │  │
│  │ order_id: 123     │  id: 1                    │  │
│  │ status: created   │  aggregate_id: 123        │  │
│  │                   │  event_type: OrderCreated │  │
│  │                   │  payload: {...}           │  │
│  │                   │  published: false         │  │
│  └───────────────────┴───────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                           │
        Outbox Processor   │ (Poll or CDC)
                           ▼
                    ┌─────────────┐
                    │   Kafka     │
                    └─────────────┘
```

```python
# Transactional write
with db.transaction():
    db.insert_order(order)
    db.insert_outbox_event(OrderCreatedEvent(order))

# Outbox processor (separate process)
def process_outbox():
    events = db.get_unpublished_events(limit=100)
    for event in events:
        kafka.publish(event.topic, event.payload)
        db.mark_published(event.id)
```

---

## 📝 Practice Problems

### Kafka Design

| # | Problem | Focus |
|---|---------|-------|
| 1 | Design order processing pipeline | Topics, partitions, consumer groups |
| 2 | Handle exactly-once delivery | Idempotency, transactions |
| 3 | Design real-time analytics pipeline | Stream processing |
| 4 | Handle consumer failure and rebalancing | Partition assignment |

### Implementation Exercises

| # | Exercise | Focus |
|---|----------|-------|
| 5 | Set up local Kafka with Docker | Environment setup |
| 6 | Implement producer with retries | Error handling |
| 7 | Implement consumer with manual commit | At-least-once |
| 8 | Build dead letter queue | Error handling |

### Hints

<details>
<summary>Exactly-Once Processing</summary>

```python
# Approach 1: Idempotent consumer
class OrderProcessor:
    def process(self, message):
        order_id = message.value['order_id']
        
        # Check if already processed
        if db.order_exists(order_id):
            return  # Skip duplicate
        
        # Process
        with db.transaction():
            db.insert_order(message.value)
            # Store offset with the data
            db.update_offset(message.partition, message.offset)

# Approach 2: Kafka transactions (producer side)
producer = KafkaProducer(
    transactional_id='my-transactional-id',
    enable_idempotence=True
)
producer.init_transactions()

try:
    producer.begin_transaction()
    producer.send('output-topic', value=result)
    producer.send_offsets_to_transaction(
        {TopicPartition('input-topic', 0): OffsetAndMetadata(offset + 1)},
        consumer_group_id='my-group'
    )
    producer.commit_transaction()
except Exception:
    producer.abort_transaction()
```
</details>

<details>
<summary>Dead Letter Queue</summary>

```python
def consume_with_dlq():
    consumer = KafkaConsumer('orders', group_id='processor')
    dlq_producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    
    MAX_RETRIES = 3
    
    for message in consumer:
        retries = 0
        while retries < MAX_RETRIES:
            try:
                process_order(message.value)
                consumer.commit()
                break
            except RecoverableError:
                retries += 1
                time.sleep(2 ** retries)  # Exponential backoff
            except Exception as e:
                # Non-recoverable error → send to DLQ
                dlq_producer.send(
                    'orders-dlq',
                    key=message.key,
                    value=message.value,
                    headers=[
                        ('error', str(e).encode()),
                        ('original_topic', b'orders')
                    ]
                )
                consumer.commit()
                break
        else:
            # Max retries exceeded → send to DLQ
            dlq_producer.send('orders-dlq', value=message.value)
            consumer.commit()
```
</details>

---

## 📚 Resources

- **Apache Kafka Documentation**: https://kafka.apache.org/documentation/
- **Confluent Kafka Tutorials**: https://developer.confluent.io/
- **RabbitMQ Tutorials**: https://www.rabbitmq.com/getstarted.html
- **Book**: "Designing Event-Driven Systems" by Ben Stopford (free)

---

## ✅ Week 10 Checklist

- [ ] Understand queue vs pub/sub models
- [ ] Know Kafka architecture (brokers, partitions, replicas)
- [ ] Implement Kafka producer with proper configs
- [ ] Implement Kafka consumer with consumer groups
- [ ] Understand offset management
- [ ] Know when to use Kafka vs RabbitMQ
- [ ] Implement transactional outbox pattern
- [ ] Design event-driven architecture

