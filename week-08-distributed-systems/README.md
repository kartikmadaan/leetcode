# Week 8: Distributed Systems

> Understand the principles behind large-scale distributed architectures

---

## 📖 High-Level Overview

Distributed systems are collections of independent computers that appear as a single coherent system. This week covers:
- Core distributed computing concepts
- Consistency models
- Consensus algorithms
- Fault tolerance and reliability

### Key Topics:
1. **Consistency Models** - Strong, eventual, causal
2. **Consensus Algorithms** - Paxos, Raft
3. **Distributed Transactions** - 2PC, Saga
4. **Message Queues** - At-least-once, exactly-once
5. **Microservices** - Service discovery, circuit breakers

---

## 🔬 Low-Level Details

### The Eight Fallacies of Distributed Computing

```
1. The network is reliable           → Networks fail
2. Latency is zero                   → Network calls take time
3. Bandwidth is infinite             → Data transfer has limits
4. The network is secure             → Security is necessary
5. Topology doesn't change           → Networks are dynamic
6. There is one administrator        → Multiple teams/systems
7. Transport cost is zero            → Network calls have cost
8. The network is homogeneous        → Different protocols/systems
```

### Consistency Models

#### Strong Consistency
```
All reads see the most recent write.

Client A: Write X=1 ──────────────────▶ Success
Client B:              Read X ──────────▶ Returns 1 (always)

Implementation: Synchronous replication, consensus
Trade-off: Higher latency, lower availability
Use case: Financial transactions, inventory
```

#### Eventual Consistency
```
Given enough time with no new writes, all replicas converge.

Client A: Write X=1 ──────────────────▶ Success
Client B:              Read X ──────────▶ Might return old value
Client B:                         Read X ▶ Eventually returns 1

Implementation: Asynchronous replication
Trade-off: Stale reads possible, higher availability
Use case: Social media likes, view counts
```

#### Causal Consistency
```
Causally related operations are seen in order.

Client A: Write X=1
Client A: Write Y=2 (depends on X=1)

All clients see X=1 before Y=2
But concurrent operations may be seen in any order.
```

### Consensus Algorithms

#### Why Consensus?
In distributed systems, nodes must agree on:
- Who is the leader?
- What is the order of operations?
- What value was committed?

#### Raft Algorithm (Simplified)

```
LEADER ELECTION:
1. Each node starts as FOLLOWER with random election timeout
2. If timeout expires without heartbeat → becomes CANDIDATE
3. Candidate requests votes from all nodes
4. First to get majority becomes LEADER
5. Leader sends periodic heartbeats

LOG REPLICATION:
1. Client sends request to LEADER
2. Leader appends to its log
3. Leader replicates to FOLLOWERS
4. Once majority acknowledges → COMMITTED
5. Leader responds to client

          ┌─────────────┐
          │   Leader    │ ◀─── Client requests
          │   (Node 1)  │
          └─────────────┘
                │
      ┌─────────┼─────────┐
      │ Replicate │        │
      ▼         ▼         ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│Follower │ │Follower │ │Follower │
│(Node 2) │ │(Node 3) │ │(Node 4) │
└─────────┘ └─────────┘ └─────────┘
```

**Raft Properties:**
- Only one leader at a time (per term)
- Leader handles all writes
- Committed entries are durable
- Tolerates (n-1)/2 failures for n nodes

### Distributed Transactions

#### Two-Phase Commit (2PC)

```
PHASE 1 - PREPARE:
Coordinator ──▶ "Can you commit?" ──▶ Participant 1
            ──▶ "Can you commit?" ──▶ Participant 2
            
Participants lock resources and reply YES/NO

PHASE 2 - COMMIT/ABORT:
If all YES:
    Coordinator ──▶ "COMMIT" ──▶ All Participants
Else:
    Coordinator ──▶ "ABORT" ──▶ All Participants

Problems:
- Blocking: If coordinator fails, participants are stuck
- Latency: Multiple round trips
- Not partition-tolerant
```

#### Saga Pattern

```
Instead of distributed transaction, use compensating transactions.

CHOREOGRAPHY:
Order Created ──▶ Payment Service
                      │
               Payment Completed ──▶ Inventory Service
                                          │
                                   Stock Reserved ──▶ Shipping Service

If Shipping fails:
    Shipping ──▶ Compensate Inventory ──▶ Refund Payment

ORCHESTRATION:
                 ┌─────────────────┐
                 │   Saga         │
                 │   Orchestrator  │
                 └─────────────────┘
                    │    │    │
                    ▼    ▼    ▼
               Order Payment Inventory
               
Orchestrator manages the sequence and compensations.
```

### Message Queue Semantics

#### At-Most-Once Delivery
```python
# Send once, don't retry
def send_message(msg):
    try:
        queue.publish(msg)
    except:
        pass  # Lost message is acceptable

# Use case: Logging, metrics (some loss OK)
```

#### At-Least-Once Delivery
```python
# Retry until acknowledged
def send_message(msg):
    while True:
        try:
            queue.publish(msg)
            ack = queue.wait_ack(timeout=5)
            if ack:
                break
        except:
            continue  # Retry

# Consumer must be idempotent (handle duplicates)
# Use case: Most applications
```

#### Exactly-Once Delivery
```python
# Idempotency key or transactional outbox
def process_message(msg):
    if db.exists(msg.id):
        return  # Already processed
    
    with db.transaction():
        db.insert(msg.id)  # Mark as processed
        process(msg)

# Achieved through idempotency, not queue guarantees
# Use case: Financial transactions
```

### Microservices Patterns

#### Service Discovery

```
                ┌─────────────────────┐
                │   Service Registry  │
                │   (Consul, Eureka)  │
                └─────────────────────┘
                    ▲           │
       Register     │           │  Lookup
                    │           ▼
              ┌───────────┐   ┌───────────┐
              │ Service A │   │ Service B │
              │ 10.0.1.1  │◀──│ (caller)  │
              └───────────┘   └───────────┘
```

#### Circuit Breaker

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout=60):
        self.failures = 0
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF-OPEN
        self.last_failure_time = None
    
    def call(self, func):
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.reset_timeout:
                self.state = 'HALF-OPEN'
            else:
                raise CircuitOpenError()
        
        try:
            result = func()
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self):
        self.failures = 0
        self.state = 'CLOSED'
    
    def _on_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.state = 'OPEN'

# Usage
breaker = CircuitBreaker()

def call_service():
    return breaker.call(lambda: http.get('http://service-b/api'))
```

**States:**
```
        Success
         ▲   │
         │   │ Failure
   ┌─────┴───▼─────┐          Threshold        ┌────────────┐
   │    CLOSED     │ ────────────────────────▶ │    OPEN    │
   │  (Normal)     │   reached                 │  (Failing) │
   └───────────────┘                           └────────────┘
              ▲                                       │
              │            Timeout                    │
              │      ┌─────────────────┐              │
              └──────│   HALF-OPEN     │◀─────────────┘
                     │   (Testing)     │
                     └─────────────────┘
```

#### Bulkhead Pattern

```
Isolate failures to prevent cascade

┌─────────────────────────────────────────┐
│              Application                │
│  ┌─────────────┐  ┌─────────────┐       │
│  │ Thread Pool │  │ Thread Pool │       │
│  │  Service A  │  │  Service B  │       │
│  │  (10 threads)│ │  (10 threads)│      │
│  └─────────────┘  └─────────────┘       │
└─────────────────────────────────────────┘

If Service A is slow, only its pool is affected.
Service B continues normally with its own pool.
```

### Distributed ID Generation

#### Snowflake ID (Twitter)

```
64-bit ID structure:
┌────────────┬───────────┬────────────┬────────────┐
│ 1 bit      │ 41 bits   │ 10 bits    │ 12 bits    │
│ (unused)   │ Timestamp │ Machine ID │ Sequence   │
└────────────┴───────────┴────────────┴────────────┘

- Timestamp: Milliseconds since epoch
- Machine ID: Unique identifier for each generator
- Sequence: Counter within same millisecond

Properties:
- 64-bit, roughly sortable by time
- ~4096 IDs per millisecond per machine
- No coordination needed
```

```python
class SnowflakeGenerator:
    def __init__(self, machine_id, epoch=1609459200000):
        self.machine_id = machine_id
        self.epoch = epoch
        self.sequence = 0
        self.last_timestamp = -1
    
    def generate(self):
        timestamp = int(time.time() * 1000) - self.epoch
        
        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & 0xFFF
            if self.sequence == 0:
                # Wait for next millisecond
                while timestamp <= self.last_timestamp:
                    timestamp = int(time.time() * 1000) - self.epoch
        else:
            self.sequence = 0
        
        self.last_timestamp = timestamp
        
        return ((timestamp << 22) | 
                (self.machine_id << 12) | 
                self.sequence)
```

### Clock Synchronization

#### Vector Clocks

```
Track causality between events across nodes.

Node A: [A:1, B:0, C:0] ──▶ Send msg ──▶ Node B
Node B: [A:0, B:1, C:0] ──▶ Receive ──▶ [A:1, B:2, C:0]

Comparing vector clocks:
- V1 < V2: V1 happened before V2
- V1 || V2: Concurrent (potential conflict)

Example:
[1, 0] < [1, 1]   (happens before)
[1, 0] || [0, 1]  (concurrent)
```

---

## 📊 Distributed Systems Patterns Summary

```
┌────────────────────────────────────────────────────────────────┐
│                    Pattern Selection Guide                      │
├────────────────┬───────────────────────────────────────────────┤
│ Need           │ Pattern                                       │
├────────────────┼───────────────────────────────────────────────┤
│ Strong         │ Consensus (Raft/Paxos), Synchronous           │
│ Consistency    │ replication, 2PC                              │
├────────────────┼───────────────────────────────────────────────┤
│ High           │ Eventual consistency, Async replication,      │
│ Availability   │ Multi-master                                  │
├────────────────┼───────────────────────────────────────────────┤
│ Fault          │ Circuit breaker, Bulkhead, Retry with         │
│ Tolerance      │ exponential backoff                           │
├────────────────┼───────────────────────────────────────────────┤
│ Distributed    │ Saga (choreography/orchestration)             │
│ Transactions   │                                               │
├────────────────┼───────────────────────────────────────────────┤
│ Ordering       │ Vector clocks, Lamport timestamps             │
│ Events         │                                               │
├────────────────┼───────────────────────────────────────────────┤
│ Unique IDs     │ Snowflake, UUID, ULID                         │
│                │                                               │
└────────────────┴───────────────────────────────────────────────┘
```

---

## 📝 Practice Problems

### System Design

| # | Problem | Key Concepts |
|---|---------|--------------|
| 1 | Design a distributed key-value store | Consistent hashing, replication, Raft |
| 2 | Design a distributed task scheduler | Leader election, fault tolerance |
| 3 | Design a distributed lock service | Consensus, TTL, fencing tokens |
| 4 | Design a distributed counter | CRDTs, eventual consistency |

### Concept Questions

| # | Question |
|---|----------|
| 5 | What happens in a network partition between 2PC coordinator and participant? |
| 6 | How does Raft handle leader failure during log replication? |
| 7 | Design idempotent payment processing |
| 8 | How to implement exactly-once message processing? |

### Hints

<details>
<summary>Distributed Lock Service</summary>

```python
# Requirements:
# - Mutual exclusion
# - Deadlock-free (TTL)
# - Fault-tolerant

# Simple approach with Redis
def acquire_lock(lock_name, client_id, ttl):
    return redis.set(lock_name, client_id, nx=True, ex=ttl)

def release_lock(lock_name, client_id):
    # Lua script for atomic check-and-delete
    script = """
    if redis.call('get', KEYS[1]) == ARGV[1] then
        return redis.call('del', KEYS[1])
    else
        return 0
    end
    """
    return redis.eval(script, [lock_name], [client_id])

# Problems:
# 1. Clock drift can cause TTL issues
# 2. Single Redis node = SPOF

# Better: Redlock algorithm
# - Acquire lock on majority of independent Redis nodes
# - Use fencing tokens for safety
```
</details>

<details>
<summary>Exactly-Once Processing</summary>

```python
# Approach 1: Idempotency keys
def process_payment(payment_id, amount):
    # Check if already processed
    if db.exists(f"processed:{payment_id}"):
        return get_previous_result(payment_id)
    
    # Process
    result = charge_card(amount)
    
    # Mark as processed (atomically with result)
    with db.transaction():
        db.set(f"processed:{payment_id}", True)
        db.set(f"result:{payment_id}", result)
    
    return result

# Approach 2: Transactional outbox
def process_order(order):
    with db.transaction():
        # Store the event in same transaction as business logic
        db.insert_order(order)
        db.insert_outbox_event(OrderCreatedEvent(order))
    
    # Separate process reads outbox and publishes
    # Can safely retry - won't duplicate

# Approach 3: Consumer-side deduplication
def on_message(msg):
    if cache.exists(msg.id):
        msg.ack()  # Already processed
        return
    
    process(msg)
    cache.set(msg.id, True, ttl=3600)
    msg.ack()
```
</details>

---

## 📚 Recommended Reading

- **"Designing Data-Intensive Applications"** - Chapters 7-9
- **Raft Paper** - "In Search of an Understandable Consensus Algorithm"
- **Google Spanner Paper** - Global distributed database
- **AWS Builder's Library** - Distributed systems patterns

---

## ✅ Week 8 Checklist

- [ ] Understand consistency vs availability trade-offs
- [ ] Explain CAP theorem with examples
- [ ] Know how Raft leader election works
- [ ] Understand 2PC limitations and Saga alternative
- [ ] Implement circuit breaker pattern
- [ ] Design a distributed lock
- [ ] Explain exactly-once processing strategies

