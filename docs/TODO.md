# Requirements

Roadmap can be summarized as follows:

1. [x] Idea
2. Prototype
   1. [x] Design
   2. [x] "Validate"
   3. [x] Development
   4. [x] Tests
3. Environment
   1. [x] Language: python fs
   2. [ ] Deployment: local docker-compose
   3. Development
      1. [ ] Patterns and protocols
      2. [x] Server
         1. [x] Simple serving
         2. [ ] Logging module
         3. [ ] HTTP compliance
         4. [ ] Concurrency serving
      3. [x] Job queue
         1. [x] Enqueue and dequeue
         2. [x] Pickle persisting
         3. [x] File lock
         4. [ ] Priority dequeueing
      4. [ ] Workers
   4. Tests

# Tests

### Load test: concurrency

Perform simultaneous requests for each endpoint that is known to call complex enough chunks of code.

### Fault tolerance: failure recovery

Simulate scenarios that specifics components fail to ensure core system robustness.

### Integration: feature testing

Simulate expected scenarios that features are supposed to work