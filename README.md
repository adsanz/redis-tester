# Redis tester

We just needed a way to test this before a production release, thought it might be a good idea to share it.

This is just a simple script that I used to test AWS elasticache redis cluster reachability and store a simple key-value pair.

Just execute it like this: `python3 test.py`

It should output something like this if everything went as expected:

```
Testing Redis 
================= 
Testing connection and invalidating token...
Token invalidated. Testing retrieval of hash from Redis...
Token hash --> mtm57z81xJwIJQAtcgc6xG_QGpRM5dNyYzouJUEHinU
Key exists (token is invalid): True
```

## Requirements (python modules)
- redis
- jwt
- secrets
- environ
