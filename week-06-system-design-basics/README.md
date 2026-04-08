# Week 6: System Design Fundamentals

> Build the foundation for designing large-scale distributed systems

---

## 📖 High-Level Overview

System design interviews test your ability to:
- Design scalable, reliable, and performant systems
- Make informed trade-offs
- Communicate your thought process clearly
- Handle ambiguity and scope the problem

### Key Topics This Week:
1. **Scalability Concepts** - Horizontal vs Vertical scaling
2. **Load Balancing** - Distribution strategies
3. **API Design** - RESTful principles, rate limiting
4. **CDN & Caching** - Content delivery basics
5. **Estimation** - Back-of-the-envelope calculations

---

## 🔬 Low-Level Details

### System Design Interview Framework

```
1. UNDERSTAND THE PROBLEM (5 minutes)
   - Clarify requirements (functional & non-functional)
   - Ask about scale, users, data volume
   - Identify core features

2. ESTIMATE SCALE (5 minutes)
   - Users, requests/second, storage
   - Bandwidth, latency requirements

3. HIGH-LEVEL DESIGN (10 minutes)
   - Draw main components
   - Data flow between components
   - Identify potential bottlenecks

4. DEEP DIVE (15 minutes)
   - Database schema & choices
   - API design
   - Detailed component design

5. WRAP UP (5 minutes)
   - Address bottlenecks
   - Discuss trade-offs
   - Future improvements
```

### Scalability Concepts

#### Vertical Scaling (Scale Up)
- Add more CPU, RAM, storage to a single machine
- **Pros:** Simple, no code changes needed
- **Cons:** Hardware limits, single point of failure, expensive

#### Horizontal Scaling (Scale Out)
- Add more machines to the system
- **Pros:** No hardware limits, better fault tolerance, cost-effective
- **Cons:** Increased complexity, need for load balancing

```
Vertical:                    Horizontal:
┌─────────────┐              ┌─────────┐ ┌─────────┐ ┌─────────┐
│             │              │ Server  │ │ Server  │ │ Server  │
│   BIG       │              │   1     │ │   2     │ │   3     │
│   SERVER    │              └─────────┘ └─────────┘ └─────────┘
│             │                      ▲         ▲         ▲
│             │                      └─────────┼─────────┘
└─────────────┘                            Load Balancer
```

### Load Balancing

#### Algorithms

| Algorithm | Description | Use Case |
|-----------|-------------|----------|
| **Round Robin** | Rotate through servers sequentially | Equal server capacity |
| **Weighted Round Robin** | Assign weights based on capacity | Varying server specs |
| **Least Connections** | Route to server with fewest active connections | Variable request duration |
| **IP Hash** | Hash client IP to determine server | Session persistence |
| **Least Response Time** | Route to fastest responding server | Performance-critical |

#### Layer 4 vs Layer 7 Load Balancing

```
Layer 4 (Transport):
- Based on IP and TCP/UDP ports
- Faster, less overhead
- No content inspection

Layer 7 (Application):
- Based on HTTP headers, URLs, cookies
- Content-aware routing
- SSL termination, compression
- More flexible but slower
```

#### Health Checks
```
- Active: Load balancer pings servers periodically
- Passive: Monitor response codes during actual requests
- Combination: Use both for reliability
```

### API Design

#### REST Principles

```
1. Stateless: Each request contains all needed information
2. Client-Server: Separation of concerns
3. Cacheable: Responses can be cached
4. Uniform Interface: Consistent naming conventions
5. Layered System: Components can be layered

HTTP Methods:
- GET    /users       → List users
- GET    /users/{id}  → Get specific user
- POST   /users       → Create user
- PUT    /users/{id}  → Update user (full)
- PATCH  /users/{id}  → Update user (partial)
- DELETE /users/{id}  → Delete user
```

#### API Versioning
```
1. URL Path: /api/v1/users
2. Query Parameter: /api/users?version=1
3. Header: Accept: application/vnd.api+json;version=1
```

#### Rate Limiting

**Why?**
- Prevent abuse and DDoS attacks
- Ensure fair resource allocation
- Control costs

**Algorithms:**

```python
# Token Bucket
class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate  # tokens per second
        self.last_refill = time.time()
    
    def consume(self, tokens=1):
        self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
    
    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, 
                          self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

# Sliding Window Log
class SlidingWindowLog:
    def __init__(self, window_size, max_requests):
        self.window_size = window_size
        self.max_requests = max_requests
        self.requests = []  # timestamps
    
    def allow_request(self):
        now = time.time()
        # Remove old requests
        self.requests = [t for t in self.requests 
                         if t > now - self.window_size]
        
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False
```

### Content Delivery Network (CDN)

#### How CDN Works
```
User Request → CDN Edge Server (Nearby)
                    ↓
        Cache HIT? → Return cached content
                    ↓ No
        Fetch from Origin → Cache → Return to user
```

#### CDN Benefits
- **Reduced Latency:** Content served from nearby edge servers
- **Reduced Origin Load:** Cache handles most requests
- **DDoS Protection:** Distributed infrastructure absorbs attacks
- **Scalability:** Handle traffic spikes without origin scaling

#### Push vs Pull CDN

| Push CDN | Pull CDN |
|----------|----------|
| Upload content proactively | Fetch content on first request |
| Full control over cache | Automatic caching |
| Good for static content | Good for dynamic content |
| More storage costs | Initial request latency |

### Back-of-the-Envelope Estimation

#### Key Numbers to Remember

```
Latency:
- L1 cache reference:           0.5 ns
- L2 cache reference:           7 ns
- RAM reference:                100 ns
- SSD random read:              150 μs
- HDD random read:              10 ms
- Send 1KB over 1 Gbps:         10 μs
- Round trip within datacenter: 500 μs
- Round trip cross-country:     150 ms

Data:
- 1 character = 1 byte (ASCII) or 2-4 bytes (UTF-8)
- 1 English word ≈ 5 characters
- 1 page of text ≈ 2 KB
- 1 image (compressed) ≈ 200 KB - 2 MB
- 1 minute of video (720p) ≈ 60 MB

Scale:
- 1 day = 86,400 seconds ≈ 100,000 seconds
- 1 million requests/day ≈ 12 requests/second
- 1 billion requests/day ≈ 12,000 requests/second
```

#### Estimation Template

```
Users:
- Daily Active Users (DAU): X million
- Requests per user per day: Y

Traffic:
- Requests per second = (DAU × Y) / 86,400 seconds
- Peak traffic = 2-3x average

Storage:
- Data per user: Z KB/MB
- Total storage = Users × Data per user × Growth factor
- Storage growth per year: A TB

Bandwidth:
- Average request size: B KB
- Bandwidth = Requests/second × Request size
```

---

## 📊 System Design Components Cheat Sheet

```
┌─────────────────────────────────────────────────────────────────┐
│                        INTERNET                                 │
└─────────────────────────────────────────────────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │         CDN           │ ← Static assets
                    └───────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │     Load Balancer     │ ← Distribute traffic
                    └───────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
┌───────┴───────┐     ┌─────────┴─────────┐     ┌───────┴───────┐
│  Web Server   │     │    Web Server     │     │  Web Server   │
│   (Stateless) │     │    (Stateless)    │     │   (Stateless) │
└───────────────┘     └───────────────────┘     └───────────────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │    API Gateway /      │ ← Rate limiting,
                    │    Service Mesh       │   Authentication
                    └───────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
┌───────┴───────┐     ┌─────────┴─────────┐     ┌───────┴───────┐
│   Service A   │     │     Service B     │     │   Service C   │
│  (Microservice)│    │   (Microservice)  │     │  (Microservice)│
└───────────────┘     └───────────────────┘     └───────────────┘
        │                       │                       │
        │             ┌─────────┴─────────┐             │
        │             │      Cache        │             │
        │             │  (Redis/Memcached)│             │
        │             └───────────────────┘             │
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
┌───────┴───────┐     ┌─────────┴─────────┐     ┌───────┴───────┐
│   Database    │     │     Database      │     │  Object Store │
│   (Primary)   │────▶│     (Replica)     │     │     (S3)      │
└───────────────┘     └───────────────────┘     └───────────────┘
                                │
                    ┌───────────┴───────────┐
                    │    Message Queue      │ ← Async processing
                    │   (Kafka/RabbitMQ)    │
                    └───────────────────────┘
```

---

## 📝 Practice Problems

### Estimation Exercises

| # | Problem | Focus Area |
|---|---------|------------|
| 1 | Estimate Twitter's QPS (Queries Per Second) | Traffic calculation |
| 2 | How much storage does YouTube need for 1 day? | Storage estimation |
| 3 | Design the bandwidth requirements for Netflix | Bandwidth calculation |
| 4 | Estimate the number of servers needed for a chat app | Capacity planning |

### Design Exercises

| # | System | Key Concepts | Difficulty |
|---|--------|--------------|------------|
| 1 | **URL Shortener** | Hash functions, database design, caching | Easy |
| 2 | **Pastebin** | Object storage, expiration, unique IDs | Easy |
| 3 | **Rate Limiter** | Token bucket, sliding window, distributed | Medium |
| 4 | **Key-Value Store** | Consistent hashing, replication, partitioning | Medium |

### Hints for Practice Problems

<details>
<summary>URL Shortener Hints</summary>

1. **Unique ID Generation:**
   - Counter-based (with distributed ID generator)
   - Hash-based (MD5/SHA256, take first N chars)
   - Base62 encoding of auto-increment ID

2. **Key Considerations:**
   - How to handle collisions?
   - Custom URLs feature?
   - Analytics and click tracking?
   - Expiration policy?

3. **Storage:**
   - NoSQL for simplicity (key = short URL, value = long URL)
   - Read-heavy workload → caching is crucial
</details>

<details>
<summary>Rate Limiter Hints</summary>

1. **Algorithm Choice:**
   - Token Bucket: Good for bursty traffic
   - Sliding Window: More accurate but memory-intensive
   - Fixed Window: Simple but allows bursts at window edges

2. **Distributed Challenges:**
   - Synchronization across servers
   - Redis for shared counter storage
   - Race conditions with INCR operations

3. **Where to Implement:**
   - API Gateway level
   - Individual service level
   - Both for defense in depth
</details>

---

## 📚 Recommended Resources

### Articles
- [System Design Primer](https://github.com/donnemartin/system-design-primer) - Comprehensive overview
- [High Scalability](http://highscalability.com/) - Real-world architecture case studies

### Videos
- [Gaurav Sen's System Design](https://www.youtube.com/c/GauravSensei) - Beginner-friendly
- [Tech Dummies](https://www.youtube.com/c/TechDummiesNarendraL) - In-depth designs

### Books
- "Designing Data-Intensive Applications" by Martin Kleppmann
- "System Design Interview" by Alex Xu

---

## ✅ Week 6 Checklist

- [ ] Understand horizontal vs vertical scaling trade-offs
- [ ] Know different load balancing algorithms
- [ ] Practice back-of-the-envelope calculations
- [ ] Design a basic URL shortener end-to-end
- [ ] Understand CDN push vs pull strategies
- [ ] Implement a rate limiter algorithm

