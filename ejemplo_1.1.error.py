Traceback (most recent call last):

 File "app.py", line 45, in <module>
   connect_to_database()
 File "app.py", line 23, in connect_to_database
   conn = psycopg2.connect(
 File "/home/user/.local/lib/python3.8/site-packages/psycopg2/__init__.py", line 122, in connect
   conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
psycopg2.OperationalError: connection to server at "[DB_HOST_PLACEHOLDER]" (172.17.0.2), port 5432 failed: FATAL: password authentication failed for user "[DB_USER_PLACEHOLDER]"
