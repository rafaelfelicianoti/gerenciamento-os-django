import os
for v in ('DB_NAME','DB_USER','DB_PASSWORD','DB_HOST','DB_PORT'):
    print(f"{v} -> {os.environ.get(v)!r}")
