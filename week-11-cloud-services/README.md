# Week 11: Cloud Services (AWS Focus)

> Master essential cloud services for modern architectures

---

## 📖 High-Level Overview

Cloud services provide managed infrastructure, reducing operational overhead. This week covers key AWS services commonly discussed in interviews:
- DynamoDB - NoSQL database
- S3 - Object storage
- Lambda - Serverless compute
- SQS/SNS - Messaging
- ElastiCache - Managed caching

### Why These Services?
- Frequently mentioned in system design interviews
- Understanding helps design scalable systems
- Similar concepts apply to other cloud providers (GCP, Azure)

---

## 🗃️ Amazon DynamoDB

### What is DynamoDB?

A fully managed NoSQL key-value and document database:
- Single-digit millisecond performance at any scale
- Built-in replication and durability
- Automatic scaling
- Pay-per-request or provisioned capacity

### Data Model

```
TABLE: Collection of items (like a collection in MongoDB)
ITEM:  Single record (like a document)
ATTRIBUTE: A piece of data within an item

Example Table: Orders

┌────────────────────────────────────────────────────────────┐
│ Partition Key │ Sort Key      │ Attributes                 │
│ (user_id)     │ (order_id)    │                            │
├───────────────┼───────────────┼────────────────────────────┤
│ user_123      │ order_001     │ {status: "shipped", ...}   │
│ user_123      │ order_002     │ {status: "pending", ...}   │
│ user_456      │ order_001     │ {status: "delivered", ...} │
└───────────────┴───────────────┴────────────────────────────┘

Primary Key Options:
1. Partition Key only (simple)
2. Partition Key + Sort Key (composite)
```

### Key Concepts

#### Partition Key
- Determines which partition stores the item
- Must be unique (if no sort key) or unique with sort key
- Should have high cardinality for even distribution

```
Good partition keys:   user_id, order_id, device_id
Bad partition keys:    status, date (hot partitions)
```

#### Sort Key
- Enables range queries within a partition
- Orders items within the partition
- Supports rich query patterns

```python
# Query examples with sort key

# Get all orders for a user
query(KeyConditionExpression="user_id = :uid")

# Get orders in date range
query(KeyConditionExpression="user_id = :uid AND order_date BETWEEN :start AND :end")

# Get orders starting with prefix
query(KeyConditionExpression="user_id = :uid AND begins_with(order_id, :prefix)")
```

### Read/Write Operations

```python
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Orders')

# Put Item (Create/Update)
table.put_item(
    Item={
        'user_id': 'user_123',
        'order_id': 'order_001',
        'status': 'pending',
        'total': 99.99,
        'items': [
            {'sku': 'ABC', 'qty': 2}
        ]
    }
)

# Get Item (by primary key)
response = table.get_item(
    Key={
        'user_id': 'user_123',
        'order_id': 'order_001'
    }
)
item = response.get('Item')

# Query (by partition key, optional sort key condition)
response = table.query(
    KeyConditionExpression=Key('user_id').eq('user_123')
)
items = response['Items']

# Query with filter (applied after query, consumes capacity)
response = table.query(
    KeyConditionExpression=Key('user_id').eq('user_123'),
    FilterExpression=Attr('status').eq('pending')
)

# Scan (full table scan - expensive!)
response = table.scan(
    FilterExpression=Attr('status').eq('pending')
)

# Update Item
table.update_item(
    Key={
        'user_id': 'user_123',
        'order_id': 'order_001'
    },
    UpdateExpression='SET #s = :status, updated_at = :time',
    ExpressionAttributeNames={'#s': 'status'},
    ExpressionAttributeValues={
        ':status': 'shipped',
        ':time': '2024-01-15T10:00:00Z'
    }
)

# Delete Item
table.delete_item(
    Key={
        'user_id': 'user_123',
        'order_id': 'order_001'
    }
)
```

### Secondary Indexes

```
GLOBAL SECONDARY INDEX (GSI):
- Different partition key and/or sort key
- Separate throughput from main table
- Eventually consistent reads only
- Can be created/deleted anytime

LOCAL SECONDARY INDEX (LSI):
- Same partition key, different sort key
- Shares throughput with main table
- Supports strongly consistent reads
- Must be created with table

Example:
Main Table:  PK=user_id, SK=order_id
GSI:         PK=status, SK=created_at    (query by status)
LSI:         PK=user_id, SK=created_at   (sort user orders by date)
```

### Capacity Modes

```
PROVISIONED:
- Specify Read/Write Capacity Units
- RCU: 1 RCU = 1 strongly consistent read of 4KB/sec
- WCU: 1 WCU = 1 write of 1KB/sec
- Use Auto Scaling for variable loads

ON-DEMAND:
- Pay per request
- No capacity planning
- Good for unpredictable workloads
- ~5x more expensive at steady state
```

### Best Practices

1. **Design for access patterns** - Know your queries before designing schema
2. **Use composite sort keys** - Enable flexible queries
3. **Avoid hot partitions** - Distribute writes evenly
4. **Use sparse indexes** - Only index items that need it
5. **Consider single-table design** - Store multiple entity types in one table

---

## 📦 Amazon S3

### What is S3?

Object storage service with:
- 99.999999999% (11 9's) durability
- Unlimited storage
- Objects up to 5TB
- Built-in versioning and lifecycle management

### S3 Concepts

```
BUCKET: Container for objects (globally unique name)
OBJECT: File + metadata
KEY:    Full path to object (including "folders")

s3://my-bucket/images/2024/photo.jpg
     │         │
     bucket    key
```

### Storage Classes

| Class | Use Case | Availability | Cost |
|-------|----------|--------------|------|
| **Standard** | Frequently accessed | 99.99% | $$$ |
| **Intelligent-Tiering** | Unknown/changing patterns | 99.9% | $$ |
| **Standard-IA** | Infrequent access | 99.9% | $$ |
| **One Zone-IA** | Infrequent, recreatable | 99.5% | $ |
| **Glacier Instant** | Archive, instant access | 99.9% | $ |
| **Glacier Flexible** | Archive, 1-5 min retrieval | 99.99% | $ |
| **Glacier Deep Archive** | Long-term archive, 12hr retrieval | 99.99% | ¢ |

### S3 Operations

```python
import boto3

s3 = boto3.client('s3')

# Upload file
s3.upload_file('local_file.txt', 'my-bucket', 'path/to/file.txt')

# Upload with metadata
s3.put_object(
    Bucket='my-bucket',
    Key='path/to/file.txt',
    Body=file_content,
    ContentType='text/plain',
    Metadata={'author': 'john'}
)

# Download file
s3.download_file('my-bucket', 'path/to/file.txt', 'local_file.txt')

# Get object
response = s3.get_object(Bucket='my-bucket', Key='path/to/file.txt')
content = response['Body'].read()

# List objects
response = s3.list_objects_v2(Bucket='my-bucket', Prefix='path/')
for obj in response.get('Contents', []):
    print(obj['Key'], obj['Size'])

# Generate presigned URL (temporary access)
url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': 'my-bucket', 'Key': 'path/to/file.txt'},
    ExpiresIn=3600  # 1 hour
)

# Delete object
s3.delete_object(Bucket='my-bucket', Key='path/to/file.txt')
```

### S3 Features

```
VERSIONING:
- Keep multiple versions of objects
- Protect against accidental deletions
- Enable for compliance requirements

LIFECYCLE POLICIES:
- Automatically transition to cheaper storage
- Delete old versions after X days
- Archive to Glacier after Y days

CROSS-REGION REPLICATION:
- Replicate objects to another region
- Disaster recovery
- Lower latency access

EVENT NOTIFICATIONS:
- Trigger Lambda on upload
- Send to SQS/SNS
- Real-time processing pipelines
```

---

## ⚡ AWS Lambda

### What is Lambda?

Serverless compute service:
- Run code without managing servers
- Pay only for compute time used
- Automatic scaling
- Integrates with many AWS services

### Lambda Concepts

```
FUNCTION: Your code package
TRIGGER:  Event that invokes function (API Gateway, S3, SQS, etc.)
HANDLER:  Entry point for your code
TIMEOUT:  Max execution time (up to 15 minutes)
MEMORY:   128MB to 10GB (CPU scales with memory)
```

### Lambda Example

```python
# lambda_function.py

import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Orders')

def lambda_handler(event, context):
    """
    event: The triggering event data
    context: Runtime information (request ID, time remaining, etc.)
    """
    
    # API Gateway event
    if 'body' in event:
        body = json.loads(event['body'])
        order_id = body.get('order_id')
    
    # Direct invocation
    elif 'order_id' in event:
        order_id = event['order_id']
    
    # S3 trigger
    elif 'Records' in event:
        for record in event['Records']:
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']
            # Process uploaded file
    
    # Process order
    try:
        response = table.get_item(Key={'order_id': order_id})
        order = response.get('Item')
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(order)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

### Common Lambda Triggers

```
API Gateway    → REST/HTTP APIs
S3             → Object created/deleted
SQS            → Process queue messages
SNS            → Pub/sub notifications
DynamoDB       → Stream changes (CDC)
EventBridge    → Scheduled events (cron)
CloudWatch     → Logs, alarms
Kinesis        → Real-time streaming
```

### Lambda Best Practices

1. **Keep functions small** - Single responsibility
2. **Minimize cold starts** - Smaller packages, provisioned concurrency
3. **Use environment variables** - Don't hardcode configs
4. **Handle errors gracefully** - Return proper error responses
5. **Use layers** - Share common dependencies

---

## 📬 SQS & SNS

### Amazon SQS (Simple Queue Service)

```
STANDARD QUEUE:
- At-least-once delivery
- Best-effort ordering
- Nearly unlimited throughput

FIFO QUEUE:
- Exactly-once processing
- Strict ordering
- 300 msg/sec (3000 with batching)

┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Producer   │────▶│    Queue    │────▶│  Consumer   │
└─────────────┘     └─────────────┘     └─────────────┘
```

```python
import boto3

sqs = boto3.client('sqs')
queue_url = 'https://sqs.region.amazonaws.com/123456/my-queue'

# Send message
sqs.send_message(
    QueueUrl=queue_url,
    MessageBody=json.dumps({'order_id': '123'}),
    MessageAttributes={
        'Priority': {
            'DataType': 'String',
            'StringValue': 'high'
        }
    },
    DelaySeconds=10  # Delay delivery
)

# Receive messages
response = sqs.receive_message(
    QueueUrl=queue_url,
    MaxNumberOfMessages=10,
    WaitTimeSeconds=20,  # Long polling
    VisibilityTimeout=60  # Time to process before redelivery
)

for message in response.get('Messages', []):
    # Process message
    body = json.loads(message['Body'])
    process_order(body)
    
    # Delete after processing
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=message['ReceiptHandle']
    )
```

### Amazon SNS (Simple Notification Service)

```
Pub/Sub:
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Publisher  │────▶│    Topic    │────▶│ Subscriber 1│
└─────────────┘     └─────────────┘────▶│ Subscriber 2│
                                   ────▶│ Subscriber 3│
                                        └─────────────┘

Subscribers can be:
- SQS queues
- Lambda functions
- HTTP endpoints
- Email addresses
- SMS
```

```python
import boto3

sns = boto3.client('sns')
topic_arn = 'arn:aws:sns:region:123456:my-topic'

# Publish message
sns.publish(
    TopicArn=topic_arn,
    Subject='New Order',
    Message=json.dumps({'order_id': '123', 'status': 'created'}),
    MessageAttributes={
        'event_type': {
            'DataType': 'String',
            'StringValue': 'order.created'
        }
    }
)

# Subscribe SQS queue to SNS topic
sns.subscribe(
    TopicArn=topic_arn,
    Protocol='sqs',
    Endpoint='arn:aws:sqs:region:123456:my-queue'
)
```

---

## 🚀 Amazon ElastiCache

### Redis vs Memcached

| Feature | ElastiCache Redis | ElastiCache Memcached |
|---------|-------------------|----------------------|
| **Data Structures** | Strings, Lists, Sets, Hashes, Sorted Sets | Strings only |
| **Persistence** | Yes (snapshots, AOF) | No |
| **Replication** | Yes (cluster mode) | No |
| **Pub/Sub** | Yes | No |
| **Lua Scripting** | Yes | No |
| **Use Case** | Full-featured caching, sessions, leaderboards | Simple caching |

### Common Patterns

```python
import redis

r = redis.Redis(host='my-cluster.cache.amazonaws.com', port=6379)

# Cache-aside pattern
def get_user(user_id):
    cache_key = f"user:{user_id}"
    
    # Check cache
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Cache miss - get from DB
    user = db.get_user(user_id)
    
    # Store in cache
    r.setex(cache_key, 3600, json.dumps(user))  # 1 hour TTL
    
    return user

# Session storage
def create_session(user_id):
    session_id = str(uuid.uuid4())
    r.setex(f"session:{session_id}", 3600, user_id)
    return session_id

# Rate limiting
def is_rate_limited(user_id, limit=100, window=60):
    key = f"rate:{user_id}"
    current = r.incr(key)
    if current == 1:
        r.expire(key, window)
    return current > limit

# Leaderboard
def update_score(user_id, score):
    r.zadd('leaderboard', {user_id: score})

def get_top_10():
    return r.zrevrange('leaderboard', 0, 9, withscores=True)
```

---

## 📊 Service Selection Guide

```
┌─────────────────────────────────────────────────────────────────┐
│                    When to Use What?                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Need fast key-value lookups?        → DynamoDB                 │
│  Need to store files/objects?        → S3                       │
│  Need serverless compute?            → Lambda                   │
│  Need to decouple services?          → SQS + SNS                │
│  Need sub-millisecond caching?       → ElastiCache              │
│  Need complex queries/joins?         → RDS (PostgreSQL/MySQL)   │
│  Need search capabilities?           → OpenSearch (Elasticsearch)│
│  Need real-time streaming?           → Kinesis                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📝 Practice Problems

### Design Exercises

| # | Problem | Services |
|---|---------|----------|
| 1 | Design a URL shortener | DynamoDB, Lambda, API Gateway |
| 2 | Design an image upload service | S3, Lambda, SQS |
| 3 | Design a real-time leaderboard | ElastiCache Redis, DynamoDB |
| 4 | Design a notification system | SNS, SQS, Lambda |

### Implementation Exercises

| # | Exercise | Focus |
|---|----------|-------|
| 5 | Create DynamoDB table with GSI | Data modeling |
| 6 | S3 upload with Lambda trigger | Event-driven |
| 7 | SQS queue with dead letter | Error handling |
| 8 | Cache-aside with ElastiCache | Caching patterns |

---

## 📚 Resources

- **AWS Documentation**: https://docs.aws.amazon.com/
- **AWS Well-Architected Framework**: Best practices
- **AWS Solutions Library**: Reference architectures
- **LocalStack**: Test AWS services locally

---

## ✅ Week 11 Checklist

- [ ] Understand DynamoDB data modeling
- [ ] Design partition and sort keys
- [ ] Know S3 storage classes
- [ ] Implement Lambda function with triggers
- [ ] Use SQS for async processing
- [ ] Implement cache patterns with ElastiCache
- [ ] Design a serverless application architecture

