# Week 7: Databases & Caching

> Master data storage strategies for scalable systems

---

## 📖 High-Level Overview

This week covers critical data layer concepts:
- SQL vs NoSQL trade-offs
- Database scaling techniques
- Caching strategies and patterns
- Data consistency and indexing

### Key Topics:
1. **SQL Databases** - ACID, normalization, joins
2. **NoSQL Databases** - Types, use cases, CAP theorem
3. **Database Scaling** - Sharding, replication, partitioning
4. **Caching** - Strategies, eviction policies, Redis
5. **Indexing** - B-trees, hash indexes, full-text search

---

## 🔬 Low-Level Details

### SQL vs NoSQL

#### SQL Databases (Relational)

**Characteristics:**
- Structured data with defined schema
- ACID transactions
- Complex queries with JOINs
- Vertical scaling primarily

**ACID Properties:**
```
Atomicity:    All operations in transaction succeed or all fail
Consistency:  Data remains valid after transaction
Isolation:    Concurrent transactions don't interfere
Durability:   Committed data persists through failures
```

**Examples:** PostgreSQL, MySQL, SQLite, Oracle

**Best For:**
- Financial transactions
- Complex relationships
- Data requiring strong consistency
- Applications with stable schema

#### NoSQL Databases

**Types:**

| Type | Examples | Use Case |
|------|----------|----------|
| **Key-Value** | Redis, DynamoDB, Memcached | Caching, sessions, simple lookups |
| **Document** | MongoDB, CouchDB | Variable schema, nested data |
| **Column-Family** | Cassandra, HBase | Time-series, analytics, high write |
| **Graph** | Neo4j, Neptune | Social networks, recommendations |

**BASE Properties:**
```
Basically Available:  System guarantees availability
Soft state:           State may change over time
Eventually consistent: System will become consistent over time
```

### CAP Theorem

```
       Consistency
           /\
          /  \
         /    \
        /  CA  \    CP: Consistency + Partition Tolerance
       /________\        (MongoDB, HBase)
      /\        /\
     /  \  CP  /  \  CA: Consistency + Availability
    / AP \    /    \     (Traditional RDBMS - single node)
   /______\  /______\
Availability    Partition
                Tolerance

AP: Availability + Partition Tolerance
    (Cassandra, DynamoDB, CouchDB)

In distributed systems, you must choose 2 of 3.
Network partitions are inevitable → Choose between C and A.
```

### Database Scaling

#### Replication

**Master-Slave (Primary-Replica):**
```
┌──────────┐     Writes      ┌──────────┐
│  Master  │ ──────────────▶ │  Master  │
│   (R/W)  │                 │   (R/W)  │
└──────────┘                 └──────────┘
      │                            │
      │ Replication               │ Replication
      ▼                           ▼
┌──────────┐               ┌──────────┐
│  Slave   │               │  Slave   │
│   (R)    │               │   (R)    │
└──────────┘               └──────────┘

Benefits:
- Read scalability (distribute reads across replicas)
- High availability (promote replica on master failure)
- Backup and disaster recovery

Challenges:
- Replication lag (eventual consistency)
- Failover complexity
- Single point of write
```

**Master-Master (Multi-Primary):**
```
┌──────────┐ ◀──────────────▶ ┌──────────┐
│ Master 1 │   Replication   │ Master 2 │
│   (R/W)  │                 │   (R/W)  │
└──────────┘                 └──────────┘

Benefits:
- Write scalability
- No single point of failure

Challenges:
- Conflict resolution
- Increased complexity
- Harder to maintain consistency
```

#### Sharding (Horizontal Partitioning)

**What:** Split data across multiple databases based on a shard key.

```
                    ┌─────────────────────┐
                    │   Shard Router      │
                    │                     │
                    └─────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│   Shard 1   │       │   Shard 2   │       │   Shard 3   │
│  Users A-H  │       │  Users I-P  │       │  Users Q-Z  │
└─────────────┘       └─────────────┘       └─────────────┘
```

**Sharding Strategies:**

| Strategy | Description | Pros | Cons |
|----------|-------------|------|------|
| **Hash-based** | hash(key) % num_shards | Even distribution | Hard to add shards |
| **Range-based** | A-H, I-P, Q-Z | Range queries | Hot spots possible |
| **Directory** | Lookup table for shard | Flexible | Single point of failure |
| **Consistent Hashing** | Ring-based distribution | Easy scaling | Uneven with few nodes |

**Consistent Hashing:**
```
                    Node A
                      ●
                 /         \
            Key X           Key Y
                             ●
         ●                      ●
       Key Z                  Node B
                 \         /
                      ●
                    Node C

Keys are assigned to the next node clockwise on the ring.
Adding/removing nodes only affects neighboring keys.
Virtual nodes ensure even distribution.
```

### Indexing

#### B-Tree Index (Default for most RDBMS)
```
                    [50]
                   /    \
              [20,30]   [70,80]
             /  |  \    /  |  \
           [10][25][35][60][75][90]

- Balanced tree structure
- O(log n) search, insert, delete
- Good for range queries
- Good for equality queries
```

#### Hash Index
```
hash(key) → bucket → value

- O(1) average lookup
- Only for equality queries
- Not good for range queries
- Used in memory stores (Redis, Memcached)
```

#### Composite Index
```sql
CREATE INDEX idx_user_status ON orders(user_id, status);

-- Efficient queries:
SELECT * FROM orders WHERE user_id = 123;
SELECT * FROM orders WHERE user_id = 123 AND status = 'active';

-- NOT efficient (leftmost prefix not used):
SELECT * FROM orders WHERE status = 'active';
```

### Caching

#### Cache Strategies

**1. Cache-Aside (Lazy Loading):**
```python
def get_user(user_id):
    # Check cache first
    user = cache.get(user_id)
    if user:
        return user  # Cache hit
    
    # Cache miss - read from DB
    user = db.get_user(user_id)
    
    # Store in cache for next time
    cache.set(user_id, user, ttl=3600)
    return user

# Pros: Only cache what's needed
# Cons: Cache miss latency, stale data possible
```

**2. Write-Through:**
```python
def update_user(user_id, data):
    # Write to DB
    db.update_user(user_id, data)
    
    # Write to cache
    cache.set(user_id, data)

# Pros: Cache always up-to-date
# Cons: Write latency, cache may have unused data
```

**3. Write-Behind (Write-Back):**
```python
def update_user(user_id, data):
    # Write to cache immediately
    cache.set(user_id, data)
    
    # Async write to DB (batch or queue)
    queue.add(WriteOperation(user_id, data))

# Pros: Low write latency
# Cons: Data loss risk if cache fails
```

**4. Read-Through:**
```python
# Cache handles loading from DB automatically
user = cache.get(user_id)  # Returns from cache or loads from DB

# Similar to cache-aside but cache manages the loading
```

#### Cache Eviction Policies

| Policy | Description | Use Case |
|--------|-------------|----------|
| **LRU** (Least Recently Used) | Evict least recently accessed | General purpose |
| **LFU** (Least Frequently Used) | Evict least frequently accessed | Frequency matters |
| **FIFO** | First in, first out | Simple, predictable |
| **TTL** | Time-based expiration | Time-sensitive data |
| **Random** | Random eviction | Simple, low overhead |

#### Redis Data Structures

```python
import redis
r = redis.Redis()

# Strings
r.set('user:1:name', 'Alice')
r.get('user:1:name')
r.incr('page:views')  # Atomic increment

# Hashes (like objects)
r.hset('user:1', 'name', 'Alice')
r.hset('user:1', 'email', 'alice@example.com')
r.hgetall('user:1')

# Lists (for queues, timelines)
r.lpush('queue:tasks', 'task1')
r.rpop('queue:tasks')

# Sets (unique items)
r.sadd('user:1:followers', 'user:2', 'user:3')
r.smembers('user:1:followers')
r.sinter('user:1:followers', 'user:2:followers')  # Intersection

# Sorted Sets (leaderboards, ranking)
r.zadd('leaderboard', {'alice': 100, 'bob': 85})
r.zrange('leaderboard', 0, -1, withscores=True)  # Ascending
r.zrevrange('leaderboard', 0, 9)  # Top 10

# TTL
r.setex('session:abc', 3600, 'user:1')  # Expires in 1 hour
```

### Cache Patterns for Common Scenarios

**Caching Database Queries:**
```python
def get_user_posts(user_id, page):
    cache_key = f"user:{user_id}:posts:page:{page}"
    
    posts = cache.get(cache_key)
    if posts:
        return posts
    
    posts = db.query("SELECT * FROM posts WHERE user_id = %s LIMIT 20 OFFSET %s", 
                     user_id, (page-1)*20)
    cache.set(cache_key, posts, ttl=300)
    return posts
```

**Cache Invalidation:**
```python
def create_post(user_id, content):
    post = db.insert_post(user_id, content)
    
    # Invalidate relevant caches
    cache.delete(f"user:{user_id}:posts:*")  # Pattern delete
    cache.delete(f"user:{user_id}:post_count")
    
    return post
```

**Distributed Cache with Consistent Hashing:**
```python
class CacheCluster:
    def __init__(self, nodes):
        self.ring = ConsistentHashRing(nodes)
    
    def get(self, key):
        node = self.ring.get_node(key)
        return node.get(key)
    
    def set(self, key, value):
        node = self.ring.get_node(key)
        node.set(key, value)
```

---

## 📊 Database Selection Guide

```
┌─────────────────────────────────────────────────────────────────┐
│                    How to Choose a Database?                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │ Need ACID transactions?       │
              │ Complex relationships?        │
              └───────────────────────────────┘
                     │                │
                    YES              NO
                     │                │
                     ▼                ▼
         ┌────────────────┐  ┌────────────────────┐
         │ SQL Database   │  │ What's your        │
         │ (PostgreSQL,   │  │ primary use case?  │
         │  MySQL)        │  └────────────────────┘
         └────────────────┘           │
                          ┌───────────┼───────────┐
                          │           │           │
                          ▼           ▼           ▼
                   Simple K-V    Document     Time-Series/
                   Lookups       Storage      High Write
                          │           │           │
                          ▼           ▼           ▼
                    ┌──────────┐ ┌──────────┐ ┌──────────┐
                    │ Redis/   │ │ MongoDB  │ │ Cassandra│
                    │ DynamoDB │ │ CouchDB  │ │ HBase    │
                    └──────────┘ └──────────┘ └──────────┘
```

---

## 📝 Practice Problems

### Database Design

| # | Problem | Focus |
|---|---------|-------|
| 1 | Design schema for Twitter | Users, tweets, follows, likes |
| 2 | Design schema for e-commerce | Products, orders, inventory |
| 3 | When to use SQL vs NoSQL for a social network? | Trade-off analysis |
| 4 | Design sharding strategy for user data | Consistent hashing |

### Caching Scenarios

| # | Problem | Focus |
|---|---------|-------|
| 5 | Design cache for leaderboard | Sorted sets, real-time updates |
| 6 | Handle cache stampede | Locking, probabilistic early expiration |
| 7 | Design distributed session store | TTL, consistency |
| 8 | Cache invalidation for news feed | Write-through, pub-sub |

### Hints

<details>
<summary>Twitter Schema Hints</summary>

```sql
-- Users table
users(id, username, email, created_at)

-- Tweets with denormalized author info for read optimization
tweets(id, user_id, content, created_at, reply_to_id)

-- Follows (fan-out on write vs fan-out on read)
follows(follower_id, followee_id, created_at)

-- For timeline:
-- Option 1: Fan-out on write (write to follower timelines)
-- Option 2: Fan-out on read (query at read time)
-- Hybrid: Fan-out on write for normal users, read for celebrities
```
</details>

<details>
<summary>Cache Stampede Prevention</summary>

```python
# Problem: Cache expires, 1000 requests hit DB simultaneously

# Solution 1: Locking
def get_with_lock(key):
    value = cache.get(key)
    if value:
        return value
    
    lock = cache.acquire_lock(f"lock:{key}", timeout=5)
    if lock:
        try:
            value = db.get(key)
            cache.set(key, value)
        finally:
            lock.release()
    else:
        # Wait and retry
        time.sleep(0.1)
        return get_with_lock(key)
    
    return value

# Solution 2: Probabilistic Early Expiration
def get_with_early_refresh(key, ttl):
    value, expiry = cache.get_with_expiry(key)
    
    remaining = expiry - time.time()
    if remaining < ttl * 0.1:  # Less than 10% TTL remaining
        if random.random() < (1 - remaining / (ttl * 0.1)):
            # Probabilistically refresh
            refresh_async(key)
    
    return value
```
</details>

---

## 📚 Recommended Reading

- **"Designing Data-Intensive Applications"** - Chapter 5 (Replication), Chapter 6 (Partitioning)
- **Redis Documentation** - Data types and patterns
- **PostgreSQL Documentation** - Indexing and performance

---

## ✅ Week 7 Checklist

- [ ] Understand SQL vs NoSQL trade-offs
- [ ] Know CAP theorem and its implications
- [ ] Design sharding strategies
- [ ] Implement cache-aside pattern
- [ ] Know Redis data structures
- [ ] Handle cache invalidation scenarios
- [ ] Design database schema for a sample application

