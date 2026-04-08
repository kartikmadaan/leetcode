# Week 12: Mock Interviews & Integration

> Put it all together with full practice sessions

---

## 📖 High-Level Overview

This final week focuses on:
- Simulating real interview conditions
- Practicing end-to-end problem solving
- Reviewing common mistakes
- Building confidence through repetition

---

## 🎯 Mock Interview Format

### Coding Interview (45-60 minutes)

```
STRUCTURE:
┌─────────────────────────────────────────────────────────────────┐
│  0-5 min   │ Introduction, problem statement                   │
│  5-10 min  │ Clarifying questions, examples                    │
│  10-15 min │ Discuss approach, get interviewer buy-in          │
│  15-40 min │ Code implementation                               │
│  40-50 min │ Testing, edge cases, optimization discussion      │
│  50-60 min │ Questions for interviewer                         │
└─────────────────────────────────────────────────────────────────┘
```

### System Design Interview (45-60 minutes)

```
STRUCTURE:
┌─────────────────────────────────────────────────────────────────┐
│  0-5 min   │ Clarify requirements (functional & non-functional)│
│  5-10 min  │ Back-of-envelope estimations                      │
│  10-25 min │ High-level design (draw components)               │
│  25-45 min │ Deep dive on critical components                  │
│  45-55 min │ Address bottlenecks, trade-offs                   │
│  55-60 min │ Questions for interviewer                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 💻 Full Coding Problems

### Problem Set A: Arrays & Strings

<details>
<summary>Problem 1: Meeting Scheduler (Medium)</summary>

**Problem:**
Given two lists of availability intervals for two people, find all common time slots of duration `duration` minutes.

**Example:**
```
slots1 = [[10, 50], [60, 120], [140, 210]]
slots2 = [[0, 15], [60, 70]]
duration = 8

Output: [60, 68]
```

**Approach Hints:**
1. Sort both lists by start time
2. Two-pointer technique
3. Find overlap and check if >= duration

**Follow-ups:**
- What if there are N people?
- What about different timezones?
</details>

<details>
<summary>Problem 2: LRU Cache (Medium)</summary>

**Problem:**
Implement an LRU (Least Recently Used) cache with `get` and `put` operations in O(1).

**Approach Hints:**
1. HashMap for O(1) lookup
2. Doubly linked list for O(1) insertion/deletion
3. Track most/least recently used with list order

**Key Implementation Points:**
- Node structure: key, value, prev, next
- HashMap: key → Node
- Move to front on access
- Remove from back when capacity exceeded
</details>

<details>
<summary>Problem 3: Word Search II (Hard)</summary>

**Problem:**
Given a board of characters and a list of words, find all words that exist in the board. Each word must be constructed from adjacent cells (horizontally or vertically).

**Approach Hints:**
1. Build Trie from word list
2. DFS from each cell
3. Match against Trie nodes
4. Prune branches as words are found
</details>

### Problem Set B: Trees & Graphs

<details>
<summary>Problem 4: Serialize and Deserialize N-ary Tree (Hard)</summary>

**Problem:**
Design an algorithm to serialize and deserialize an N-ary tree (each node can have any number of children).

**Approach Hints:**
1. Preorder traversal
2. Encode number of children with each node
3. Format: "value,numChildren,child1,child2,..."
</details>

<details>
<summary>Problem 5: Course Schedule III (Hard)</summary>

**Problem:**
Given courses with duration and deadline, find maximum number of courses you can take.

**Approach Hints:**
1. Sort by deadline
2. Greedy with max-heap
3. If current course exceeds deadline, swap with longest taken course
</details>

### Problem Set C: Dynamic Programming

<details>
<summary>Problem 6: Regular Expression Matching (Hard)</summary>

**Problem:**
Implement regex matching with `.` and `*` support.

**Approach Hints:**
1. 2D DP: dp[i][j] = s[:i] matches p[:j]
2. Handle `.` - matches any single char
3. Handle `*` - match zero or more of preceding element
4. Base case: empty pattern matches empty string
</details>

<details>
<summary>Problem 7: Edit Distance with Operations (Medium)</summary>

**Problem:**
Find minimum cost to convert word1 to word2 with different costs for insert, delete, replace.

**Extension of classic edit distance with weighted operations.**
</details>

---

## 🏗️ Full System Design Problems

### Problem 1: Design Twitter

<details>
<summary>Requirements & Hints</summary>

**Functional Requirements:**
- Post tweets
- Follow/unfollow users
- View home timeline (tweets from followed users)
- Search tweets

**Non-Functional:**
- 500M users, 200M DAU
- Average 200 tweets read/day, 2 tweets posted/day
- Low latency for timeline (< 200ms)

**Key Design Decisions:**
1. **Fan-out on write vs read:**
   - Fan-out on write for most users (precompute timelines)
   - Fan-out on read for celebrities (too many followers)
   
2. **Data Model:**
   - Users table
   - Tweets table
   - Follows table
   - Timelines (cached lists per user)

3. **Components:**
   - Tweet service
   - Timeline service
   - Fan-out service
   - Search service (inverted index)
   - Cache layer (Redis for timelines)
</details>

### Problem 2: Design Uber

<details>
<summary>Requirements & Hints</summary>

**Functional Requirements:**
- Riders request rides
- Drivers accept rides
- Real-time location tracking
- Payment processing
- Ride matching

**Key Challenges:**
1. **Location Matching:**
   - Geospatial indexing (QuadTree, S2/H3)
   - Match riders to nearby drivers
   
2. **Real-time Updates:**
   - WebSocket connections for live tracking
   - Location updates every few seconds

3. **Scalability:**
   - Partition by geography
   - Handle millions of concurrent rides
</details>

### Problem 3: Design a Distributed Rate Limiter

<details>
<summary>Requirements & Hints</summary>

**Requirements:**
- Limit requests per user/IP
- Distributed across multiple servers
- Low latency
- Handle failures gracefully

**Approaches:**
1. **Token Bucket with Redis:**
   - Store bucket state in Redis
   - Lua script for atomic operations

2. **Sliding Window Log:**
   - Redis sorted set with timestamps
   - ZREMRANGEBYSCORE + ZADD

3. **Considerations:**
   - Clock skew between servers
   - Race conditions
   - Failover behavior
</details>

### Problem 4: Design a Notification System

<details>
<summary>Requirements & Hints</summary>

**Requirements:**
- Support push, SMS, email notifications
- Millions of users
- Near real-time delivery
- Template management
- User preferences

**Components:**
1. **Notification Service:**
   - API to trigger notifications
   - Template rendering
   - Rate limiting

2. **Worker Queue:**
   - SQS/Kafka for async processing
   - Different queues per channel

3. **Channel Adapters:**
   - Push: FCM/APNs
   - SMS: Twilio
   - Email: SES

4. **Considerations:**
   - Deduplication
   - Retry with exponential backoff
   - Priority levels
</details>

---

## 📋 Interview Checklist

### Before the Interview

- [ ] Get good sleep the night before
- [ ] Have water nearby
- [ ] Test your audio/video setup
- [ ] Have a pen and paper for notes
- [ ] Review your resume and past projects

### During Coding Interview

- [ ] Read the problem completely
- [ ] Ask clarifying questions
- [ ] Talk through examples
- [ ] Discuss approach BEFORE coding
- [ ] Start with brute force, then optimize
- [ ] Write clean, readable code
- [ ] Test with examples
- [ ] Discuss time/space complexity

### During System Design

- [ ] Clarify scope and requirements
- [ ] Ask about scale (users, data, requests)
- [ ] Do back-of-envelope calculations
- [ ] Start high-level, then deep dive
- [ ] Consider trade-offs explicitly
- [ ] Address failure scenarios
- [ ] Don't forget caching and CDN

### Common Mistakes to Avoid

| Mistake | How to Avoid |
|---------|--------------|
| Jumping into code too fast | Spend 5-10 min on approach first |
| Not communicating | Think out loud constantly |
| Getting stuck silently | Ask for hints, explain where you're stuck |
| Ignoring edge cases | Explicitly list and handle them |
| Over-engineering | Start simple, add complexity as needed |
| Poor time management | Watch the clock, move on if stuck |

---

## 📅 Week 12 Schedule

| Day | Morning (2 hrs) | Evening (2 hrs) |
|-----|-----------------|-----------------|
| 1 | Full coding mock (2 problems) | Review solutions |
| 2 | Full system design mock | Review and iterate |
| 3 | Coding: DP + Graphs | Review patterns |
| 4 | System design: Data-intensive | Review trade-offs |
| 5 | Full coding mock | Behavioral prep |
| 6 | Full system design mock | Review feedback |
| 7 | Light review, rest | Prepare questions to ask |

---

## 💬 Behavioral Questions

### STAR Method

```
SITUATION: Set the context
TASK:      Describe your responsibility
ACTION:    Explain what you did
RESULT:    Share the outcome (quantify if possible)
```

### Common Questions

1. **Tell me about yourself**
   - 2-minute pitch: current role → past experience → why this role

2. **Tell me about a challenging project**
   - Technical challenge, how you overcame it, learnings

3. **Conflict with a teammate**
   - How you handled it professionally, resolution

4. **A time you failed**
   - What happened, what you learned, how you grew

5. **Why this company?**
   - Research the company, align with your goals

---

## 🎓 Final Tips

### Coding Interviews

```
1. PRACTICE UNDER PRESSURE
   - Use timer (45 minutes)
   - Practice with someone watching
   - Record yourself and review

2. PATTERNS OVER PROBLEMS
   - Focus on recognizing patterns
   - 150 problems with deep understanding > 500 rushed

3. COMMUNICATE CONSTANTLY
   - Your thought process matters as much as the solution
   - Ask for feedback: "Does this approach make sense?"
```

### System Design Interviews

```
1. DRIVE THE CONVERSATION
   - Don't wait for prompts
   - Show initiative and ownership

2. TRADE-OFFS ARE KEY
   - Every decision has pros and cons
   - Explicitly state them

3. IT'S A CONVERSATION
   - Interviewer wants to see how you think
   - Ask questions and iterate
```

---

## ✅ Final Checklist

- [ ] Completed all 11 weeks of material
- [ ] Solved 100+ LeetCode problems
- [ ] Designed 10+ systems end-to-end
- [ ] Practiced under timed conditions
- [ ] Did at least 3 mock interviews
- [ ] Prepared behavioral stories
- [ ] Researched target companies
- [ ] Prepared questions to ask interviewers

---

## 🎉 You're Ready!

Remember:
- It's okay to not know everything
- Show your problem-solving process
- Be curious and engaged
- Learn from every interview

**Good luck! You've got this! 🚀**

