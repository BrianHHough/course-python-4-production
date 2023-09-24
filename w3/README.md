# Week 3 - 

# Python Project Notes

## Health Check 
- monitoring services
- need an endpoint to reach it and get expected output from it
- 2 options:
    - 1: get code 200 and please go check this, go and check
    - 2: deeper checks - your server, FastAPI works but might loose connection to db. Hit health endpoint and check if you can connect to db, Redis, then response out of it would be... webserver ok, db ok, but redis not ok - job for external monitoring service should be external (independent of FastAPI) - needs to be independent. Cron basis - send any request to this endpoint and get pre-defined answer and gets answered.
- what you need for health check:
    - needs to be outside of the server
    - might want to check services regularly; lightweight minimum amount of data
    - cloudwatch logs - if service goes down, not logging anything... so this isn't really a health check
    - Health endpoint is a simple ping of service

## Using Python 
- web server - always serve you some HTML, why we call them web apps. Don't need full blown html, we need just data... let's get rid of html and let's gather this data in JSON... start to call this api communication, not sending html, sending raw data and then do whatever you want
- in fastapi world, framework is other way around - we are fast at delivering data.
- in health check endpoint, can return python dictionary is actually not a json, it's a python dictionary (own python data structure) that's not a json
    - if you try to do the same with flask
    - flask is different from fastapi - it's a synchronous web server for apps; slower; designed for building web apps
        - you'd have to explicitly convert to json string
    - fastapi automatically converts dictionary into json under the hood
- pydantic package: creating data structures - take any data and convert it to pydantic object allows you to take all your way to validate data against it 
    - link: https://docs.pydantic.dev/latest/
    - link: https://fastapi.tiangolo.com/
    - kind of like typescript interfaces
    - node.js/express.js/typescript
    - set up a server with uvicorn (node.js), fastapi (express.js) / pydantic for data structures (typescript)

## Arguments
- built-in arguments after `python main.py` and every token is argument
- we are using a package for more advanced ways to do CLI-type inputs into your file with `argparse` like `python main.py --data sml 
    - then you add arguments like a default and then choices and then help message
    - `required=True` makes the type required


```py
import sys
for x in sys.argv:
    print(x)
```

`python script.py this are my arguments` logs:
```bash
scrypt.py
this
are
my
arguments
```

```py
import sys
my_value = sys.argv[`]

print(my_value)
```

`python script.py 100` logs:
```bash
100
```

## Packages vs. Dictionaries

- dictionary = data structure
- packages = sdks

- some are built-in, some are external

- pip install going to pyip.org

## import vs. from
- syntax
- `import uuid` = wildcard to import anything
- `import w3.utils.database import DB` and then we can just use `DB()`
    - or could do `import w3` and then we would need to do `w3.utils.database.DB` if we are referencing it

- `import uuid` = the way you communicate with the package depends on devs... some provide high level object  into their own - can communicate with package right away
    - like wildcard in javascript imports like `import * as React from 'react'`

`process_id = str(uuid.uuid4())` - each package has a default 

- `from typing import Liast, Dict` - you are importing specific modules


## What the `if __name__ == '__main__'`
- avoid unnecessary calls of functions
- how to make scripts callable from other scripts

`script.py`
```py
...
if __name__ == '__main__':
    print(__name__)
    main()
```

if you run `python script.py` this logs `__main__`


`script2.py`
```py

# expect some striing
def printing(s):
    print(s)

print(__name__)
# if __name__ == '__main__':
#     print(__name__)
#     main()
```

## API to render the static HTML page to track the status of every process
- websocket endpoint - waits until something connects to it: `await manager.connect(websocket)`
- then creates a pool of listeners with the `@app.websocket("/ws")` of this user from this browser and this user from this browser
    - 2 way communication vs. http is 1 way communication
- listens to the 
- then sends data back to the pool of listeners/subscribers in an infinite look with the `while True`
    - fetching and then sending
- we can set some conventions: if data is managed by us, the first part of the data is type of interaction... 
    - when you hit enter (message send event)
    - when you focus on input field to see the results that someone is typing (user is typing event)
- maybe get raw data or metadata - what type of event is that? - user sends message or user is typing message
    - when you display message, send notification that event was read... maybe some metadata to expand what you can do
    - in our example, the `data = await websocket.receive_text()` and `broadcast_continuous = Thread...`
- class `ConnectionManager` in the `websocket.py` - look at this class:
    - has a list of connections `self.connections: List(Websocket) = []`
    - there is a function for connection: `async def connect(...` and then we append identifier with `self.connection...`
    - function for `async def broadcast_all` - infinite loop while True... for pool of connections, and clients connected, read from database and send JSON to those connections
        - we send data `await connection.send_json(processes)`
        - our `time.sleep(1)` = interval of log pulling to do request based on some interval of time


# Python Project Walkthrough Steps

## Step 1: Create a virtual environment for the project:

Create a virtual environment (this will make the virtual env named `venv` in the directory):
```bash
virtualenv venv
```

Activate the virtual environment with this command:
```bash
source venv/bin/activate
```

To deactivate the virtual environment, run this command:
```bash
deactivate
```

## Step 2: Set up the Database with SQLite3
- this is a local, relational db for us to work with our project

```py
sql = f"""
    create table if not exists {self._table_name}
    (
        process_id TEXT not null,
        file_name TEXT default null,
        file_path TEXT default null,
        description  TEXT default null,
        start_time TEXT default null,
        end_time TEXT default null,
        percentage TEXT default null,
    )
    """
    # execute statement
    self._connection.execute(sql)
    # commit changes to the db
    self._connection.commit()
```

### 🐞 Got a linting error on `self` here where it was saying self not recognized:

The full error was this:
```bash
"self" is not defined Pylance(reportUndefinedVariable)
(function) self: Any
```

✅ The reason for this was that it couldn't "find" self since the indentation wasn't within the DB class. Indenting the code block to be inside of the DB class fixed this error.

## Step 3: Set up the server.py file with the endpoints we need:
- health check endpoint: monitoring the alive status
- routing endpoint: for the '/' route - to serve the index.html file
- processes endpoint: reads from the database.py file

## Step 4: Run the uvicorn server

After `cd w3` into the w3 directory, we can run:
```bash
PYTHONPATH=.. python -m uvicorn server:app
```

This should print out the following in the terminal:
```bash
INFO:     Started server process [3335]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

If we go to the url: http://127.0.0.1:8000, we should see:
![](./assets/1-table-no-data.png)


### 🐞 Debugging: `ModuleNotFoundError: No module named 'w2.utils'`

When I tried to run `PYTHONPATH=.. python -m uvicorn server:app`, I got the following error in my terminal:

```bash
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/uvicorn/__main__.py", line 4, in <module>
    uvicorn.main()
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/click/core.py", line 1157, in __call__
    return self.main(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/click/core.py", line 1078, in main
    rv = self.invoke(ctx)
         ^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/click/core.py", line 1434, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/click/core.py", line 783, in invoke
    return __callback(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/uvicorn/main.py", line 404, in main
    run(
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/uvicorn/main.py", line 569, in run
    server.run()
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/uvicorn/server.py", line 60, in run
    return asyncio.run(self.serve(sockets=sockets))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/runners.py", line 190, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "uvloop/loop.pyx", line 1517, in uvloop.loop.Loop.run_until_complete
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/uvicorn/server.py", line 67, in serve
    config.load()
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/uvicorn/config.py", line 477, in load
    self.loaded_app = import_from_string(self.app)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/uvicorn/importer.py", line 24, in import_from_string
    raise exc from None
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/uvicorn/importer.py", line 21, in import_from_string
    module = importlib.import_module(module_str)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1149, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/Users/.../.../.../.../.../course-python-4-production/w3/server.py", line 8, in <module>
    from w2.utils.websocket import ConnectionManager
ModuleNotFoundError: No module named 'w2.utils'
```

I wanted to test if there is something wrong with my virtual env or something else related to the import of the w2 utils file, so I created a test script called `test_import_w2.py` to figure out what could be going wrong. (Notice later how I need to switch the imports b/c the w2 methods I tried to find don't exist - more on this later)

I ran this with: `python test_import_w2.py` but it gave this error:
`Import failed: No module named 'w2.utils'`

I then realized that the `server.py` file had a typo of trying to import utils from w2, but it should come from w3 b/c those are the websocket utils 🫠🙈 It's supposed to be this in `w3/server.py`:
```py
from w3.utils.websocket import ConnectionManager
from w3.utils.response_model import ProcessStatus
from w3.utils.database import DB
```

Same thing with the `w3/utils/websocket.py` file, this needed to import `database.py` from the w3.utils, not w2:

```py
from w3.utils.database import DB
```

But I still wanted to learn how to do the imports. This is how you import a file from one directory into another. I also learned that I needed to check which methods are being exported from the file. Notice how I needed to change the import utils from w1 and not w2.

```py
# To run:
#  cd w3
# python test_import_w2.py

import sys
from pathlib import Path

# Optionally, add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from w1.utils import Stats, DataReader

try:
    import w1.utils # This line is redundant as it's already imported above
    print("Import successful!")
except ImportError as e:
    print(f"Import failed: {e}")
```

I then run this with: `python test_import_w1.py` and then I saw the below 🥳
```
Import successful!
```

### 🐞 Debugging: Received a syntax error about the sqlite3 execute statement in `utils/database.py`

The error I got was this:
```bash
sqlite3.OperationalError: near ")": syntax error
```

The full error was this long log:

```bash
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/uvicorn/__main__.py", line 4, in <module>
    uvicorn.main()
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/click/core.py", line 1157, in __call__
    return self.main(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/click/core.py", line 1078, in main
    rv = self.invoke(ctx)
         ^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/click/core.py", line 1434, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/click/core.py", line 783, in invoke
    return __callback(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/uvicorn/main.py", line 404, in main
    run(
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/uvicorn/main.py", line 569, in run
    server.run()
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/uvicorn/server.py", line 60, in run
    return asyncio.run(self.serve(sockets=sockets))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/runners.py", line 190, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "uvloop/loop.pyx", line 1517, in uvloop.loop.Loop.run_until_complete
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/uvicorn/server.py", line 67, in serve
    config.load()
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/uvicorn/config.py", line 477, in load
    self.loaded_app = import_from_string(self.app)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/uvicorn/importer.py", line 21, in import_from_string
    module = importlib.import_module(module_str)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1149, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/Users/.../.../.../.../.../course-python-4-production/w3/server.py", line 16, in <module>
    manager = ConnectionManager()
              ^^^^^^^^^^^^^^^^^^^
  File "/Users/.../.../.../.../.../course-python-4-production/w3/utils/websocket.py", line 12, in __init__
    self.db = DB()
              ^^^^
  File "/Users/.../.../.../.../.../course-python-4-production/w3/utils/database.py", line 19, in __init__
    self.create_table()
  File "/Users/.../.../.../.../.../course-python-4-production/w3/utils/database.py", line 61, in create_table
    self._connection.execute(sql)
sqlite3.OperationalError: near ")": syntax error
```

This was all because of this very small comma in the last line of the create table sql command. I had `percentage TEXT default null,` but it needs to not have that comma as the last item: `percentage TEXT default null`

Corrected to this:

```py
sql = f"""
        create table if not exists {self._table_name}
        (
            process_id TEXT not null,
            file_name TEXT default null,
            file_path TEXT default null,
            description  TEXT default null,
            start_time TEXT default null,
            end_time TEXT default null,
            percentage TEXT default null
        )
        """
        # execute statement
        self._connection.execute(sql)
        # commit changes to the db
        self._connection.commit()
```


## Step 5: Check the Health Check endpoint

When I go to this url: http://127.0.0.1:8000/health

I see this output:
```bash
{"status":"ok"}
```

## Review the FastAPI Docs page with the CRUD functionalities:

When I go to this url: http://127.0.0.1:8000/docs

I see this output, which is a CRUD visualizer for making the operations:
![](./assets/2-docs-visualizer.png)

When we execute the GET request to the `/health` endpoint, we can see this success response:
![](./assets/3-docs-visualizer-health.png) 

In the terminal, I am seeing these logs as I do GET requests:
```bash
...
INFO:     127.0.0.1:49927 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:49927 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:49928 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:49930 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:49930 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:49930 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:49930 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:49930 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:49930 - "GET /health HTTP/1.1" 200 OK
```

## Step 6: Test the health endpoint via Pytest:

- Create a new terminal
- `cd w3`
- create a new virtual env: `source venv/bin/activate`
- run the test file (with the virtual env): `PYTHONPATH=../ venv/bin/python -m pytest test.py -s`
  - This could also work if you're using global packages: `PYTHONPATH=../ pytest test.py -s`


This is what it looks like when the 3 tests pass:
```bash
============================================== test session starts ==============================================
platform darwin -- Python 3.11.3, pytest-7.4.2, pluggy-1.3.0
rootdir: /Users/.../.../.../.../.../course-python-4-production/w3
plugins: anyio-3.7.1
collected 3 items                                                                                               

test.py [{'description': 'sample',
  'end_time': '2023-09-24 04:59:01',
  'file_name': 'sample_1.csv',
  'file_path': '/usr/sample_1.csv',
  'percentage': None,
  'process_id': 'cd43f806-c6d2-4ae7-a717-e560a1d640ec',
  'start_time': '2023-09-24 04:58:56',
  'time_taken': 5.0},
 {'description': 'sample',
  'end_time': '2023-09-24 04:59:01',
  'file_name': 'sample_2.csv',
  'file_path': '/usr/sample_2.csv',
  'percentage': None,
  'process_id': '0c91f865-6980-423b-b9c6-67d52458f556',
  'start_time': '2023-09-24 04:58:56',
  'time_taken': 5.0},
 {'description': 'sample',
  'end_time': '2023-09-24 04:59:01',
  'file_name': 'sample_3.csv',
  'file_path': '/usr/sample_3.csv',
  'percentage': None,
  'process_id': 'bf9cb199-c1cd-4b97-a055-202fa3bcc0c9',
  'start_time': '2023-09-24 04:58:56',
  'time_taken': 5.0}]
...

=============================================== 3 passed in 5.64s ===============================================
^CException ignored in: <module 'threading' from '/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/threading.py'>
Traceback (most recent call last):
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/threading.py", line 1583, in _shutdown
    lock.acquire()
KeyboardInterrupt: 
(venv) user@user-MacBook-Pro w3 % PYTHONPATH=../ venv/bin/python -m pytest test.py -s
============================================== test session starts ==============================================
platform darwin -- Python 3.11.3, pytest-7.4.2, pluggy-1.3.0
rootdir: /Users/.../.../.../.../.../course-python-4-production/w3
plugins: anyio-3.7.1
collected 3 items                                                                                               

test.py [{'description': 'sample',
  'end_time': '2023-09-24 04:59:01',
  'file_name': 'sample_1.csv',
  'file_path': '/usr/sample_1.csv',
  'percentage': None,
  'process_id': 'cd43f806-c6d2-4ae7-a717-e560a1d640ec',
  'start_time': '2023-09-24 04:58:56',
  'time_taken': 5.0},
 {'description': 'sample',
  'end_time': '2023-09-24 04:59:01',
  'file_name': 'sample_2.csv',
  'file_path': '/usr/sample_2.csv',
  'percentage': None,
  'process_id': '0c91f865-6980-423b-b9c6-67d52458f556',
  'start_time': '2023-09-24 04:58:56',
  'time_taken': 5.0},
 {'description': 'sample',
  'end_time': '2023-09-24 04:59:01',
  'file_name': 'sample_3.csv',
  'file_path': '/usr/sample_3.csv',
  'percentage': None,
  'process_id': 'bf9cb199-c1cd-4b97-a055-202fa3bcc0c9',
  'start_time': '2023-09-24 04:58:56',
  'time_taken': 5.0},
 {'description': 'sample',
  'end_time': '2023-09-24 05:12:11',
  'file_name': 'sample_1.csv',
  'file_path': '/usr/sample_1.csv',
  'percentage': None,
  'process_id': 'c72bf65e-0172-420a-a5ab-21a0c5dc4faf',
  'start_time': '2023-09-24 05:12:06',
  'time_taken': 5.0},
 {'description': 'sample',
  'end_time': '2023-09-24 05:12:11',
  'file_name': 'sample_2.csv',
  'file_path': '/usr/sample_2.csv',
  'percentage': None,
  'process_id': 'e2219b75-7e20-4eca-899a-b036903ec0c3',
  'start_time': '2023-09-24 05:12:06',
  'time_taken': 5.0},
 {'description': 'sample',
  'end_time': '2023-09-24 05:12:11',
  'file_name': 'sample_3.csv',
  'file_path': '/usr/sample_3.csv',
  'percentage': None,
  'process_id': 'dacaf458-1107-41e2-8d58-85fff7deff60',
  'start_time': '2023-09-24 05:12:06',
  'time_taken': 5.0}]
...

=============================================== 3 passed in 5.64s ===============================================
```



### 🐞 Debugging: `ModuleNotFoundError: No module named 'httpx'`

I tried to run the `test.py` file and got this error: `ModuleNotFoundError: No module named 'httpx'` and the the full error log was this:
```bash
============================= test session starts ==============================
platform darwin -- Python 3.11.3, pytest-7.2.2, pluggy-1.3.0
rootdir: /Users/.../.../.../.../.../course-python-4-production/w3
plugins: anyio-4.0.0
collected 0 items / 1 error                                                    

==================================== ERRORS ====================================
___________________________ ERROR collecting test.py ___________________________
ImportError while importing test module '/Users/.../.../.../.../.../course-python-4-production/w3/test.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
test.py:8: in <module>
    from fastapi.testclient import TestClient
/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/fastapi/testclient.py:1: in <module>
    from starlette.testclient import TestClient as TestClient  # noqa
/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/starlette/testclient.py:16: in <module>
    import httpx
E   ModuleNotFoundError: No module named 'httpx'
=========================== short test summary info ============================
ERROR test.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
=============================== 1 error in 0.45s ===============================
```

I needed to `pip install httpx` for this to work!

By doing this, we are installing this package inside of the `venv` folder and if you go to `venv/lib` you will see this listed as one of the packages in there.

However, there is no directory-level requirements file about this. A way to create a `requirements.txt` file out of this list of items in the directory is to run this command:
```bash
pip freeze > requirements.txt
```

Now I see a `requirements.txt` file in this subdirectory `w3/requirements.txt` that looks like this:
```txt
anyio==4.0.0
certifi==2023.7.22
h11==0.14.0
httpcore==0.18.0
httpx==0.25.0
idna==3.4
sniffio==1.3.0
```

When I tried to run the test, I was still getting that error about it not finding `httpx`... so I tried to understand if it's running the python in the venv or my global version of python. 

There is a way we can run the python that is in the virtual env but not the global python version with `venv/bin/python` so that is what we will do. First we must install a couple of packages:

```bash
pip install pytest matplotlib pydantic uvicorn fastapi tqdm starlette
```

What I needed to do was to install all the packages within the virtual env to be able to run the test command in the terminal.

### 🐞 Debugging: `sqlite3.OperationalError: unrecognized token: "218de651"`

When I tried to run: `PYTHONPATH=../ venv/bin/python -m pytest test.py -s`, I got this error:

```bash
============================= test session starts ==============================
platform darwin -- Python 3.11.3, pytest-7.4.2, pluggy-1.3.0
rootdir: /Users/.../.../.../.../.../course-python-4-production/w3
plugins: anyio-3.7.1
collected 3 items                                                              

test.py F..

=================================== FAILURES ===================================
__________________________ TestApp.test_db_operations __________________________

self = <test.TestApp testMethod=test_db_operations>

    def test_db_operations(self):
    
        example_data = [{
            'process_id': str(uuid.uuid4()),
            'start_time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'file_name': 'sample_1.csv',
            'file_path': '/usr/sample_1.csv',
            'description': 'sample'
        }, {
            'process_id': str(uuid.uuid4()),
            'start_time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'file_name': 'sample_2.csv',
            'file_path': '/usr/sample_2.csv',
            'description': 'sample'
        }, {
            'process_id': str(uuid.uuid4()),
            'start_time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'file_name': 'sample_3.csv',
            'file_path': '/usr/sample_3.csv',
            'description': 'sample'
        }]
        for each in example_data:
>           self.db.insert(process_id=each['process_id'], start_time=each['start_time'], file_name=each['file_name'],
                           file_path=each['file_path'], description=each['description'])

test.py:59: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <utils.database.DB object at 0x128659dd0>
process_id = '218de651-726a-4f3a-9937-1c4795f6f388'
start_time = '2023-09-24 04:04:54', file_name = 'sample_1.csv'
file_path = '/usr/sample_1.csv', description = 'sample', end_time = None
percentage = None

    def insert(self, process_id, start_time, file_name=None, file_path=None,
               description=None, end_time=None, percentage=None) -> None:
        """
        Insert a record into the table
    
        :param process_id: Assign an id to the process
        :param start_time: Start time for the process
        :param file_name: File being process
        :param file_path: Path to the file being processed
        :param description: Description of the file/process
        :param end_time: End time for the process
        :param percentage: Percentage of process completed
        :return: None
        """
    ######################################## YOUR CODE HERE ##################################################
        sql = f"""
        insert into {self._table_name}
        (
            process_id,
            file_name,
            file_path,
            description,
            start_time,
            end_time,
            percentage
        )
        values
        (
            {process_id},
            {file_name},
            {file_path},
            {description},
            {start_time},
            {end_time},
            {percentage}
    
        )
        """
        # execute statement
>       self._connection.execute(sql)
E       sqlite3.OperationalError: unrecognized token: "218de651"

utils/database.py:105: OperationalError
=========================== short test summary info ============================
FAILED test.py::TestApp::test_db_operations - sqlite3.OperationalError: unrecognized token: "218de651"
========================= 1 failed, 2 passed in 0.83s ==========================

```


This error tells us some good information:
```bash
self._connection.execute(sql)
E       sqlite3.OperationalError: unrecognized token: "218de651"

utils/database.py:105: OperationalError
```

There is an error in our `database.py` file - probably something with the execution of our sqlite3 database. There was an issue with how we were calling the values of our database objects, as some are strings and not objects:

I had to change this:
```py
sql = f"""
        insert into {self._table_name}
        (
            process_id,
            file_name,
            file_path,
            description,
            start_time,
            end_time,
            percentage
        )
        values
        (
            {process_id},
            {file_name},
            {file_path},
            {description},
            {start_time},
            {end_time},
            {percentage}
        
        )
        """
```

To this:
```py
sql = f"""
        insert into {self._table_name}
        (
            process_id,
            file_name,
            file_path,
            description,
            start_time,
            end_time,
            percentage
        )
        values
        (
            '{process_id}',
            '{file_name}',
            '{file_path}',
            '{description}',
            '{start_time}',
            '{end_time}',
            {percentage}
        )
        """
```

That solved that error!


### 🐞 Debugging: `sqlite3.OperationalError: no such column: None`

When I tried to run: `PYTHONPATH=../ venv/bin/python -m pytest test.py -s`, I got this error:

```bash
============================= test session starts ==============================
platform darwin -- Python 3.11.3, pytest-7.4.2, pluggy-1.3.0
rootdir: /Users/.../.../.../.../.../course-python-4-production/w3
plugins: anyio-3.7.1
collected 3 items                                                              

test.py F..

=================================== FAILURES ===================================
__________________________ TestApp.test_db_operations __________________________

self = <test.TestApp testMethod=test_db_operations>

    def test_db_operations(self):
    
        example_data = [{
            'process_id': str(uuid.uuid4()),
            'start_time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'file_name': 'sample_1.csv',
            'file_path': '/usr/sample_1.csv',
            'description': 'sample'
        }, {
            'process_id': str(uuid.uuid4()),
            'start_time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'file_name': 'sample_2.csv',
            'file_path': '/usr/sample_2.csv',
            'description': 'sample'
        }, {
            'process_id': str(uuid.uuid4()),
            'start_time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'file_name': 'sample_3.csv',
            'file_path': '/usr/sample_3.csv',
            'description': 'sample'
        }]
        for each in example_data:
>           self.db.insert(process_id=each['process_id'], start_time=each['start_time'], file_name=each['file_name'],
                           file_path=each['file_path'], description=each['description'])

test.py:59: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <utils.database.DB object at 0x10f76a950>
process_id = '67287dd3-9811-4aa2-a2a5-1f8cd37374ff'
start_time = '2023-09-24 04:36:51', file_name = 'sample_1.csv'
file_path = '/usr/sample_1.csv', description = 'sample', end_time = None
percentage = None

    def insert(self, process_id, start_time, file_name=None, file_path=None,
               description=None, end_time=None, percentage=None) -> None:
        """
        Insert a record into the table
    
        :param process_id: Assign an id to the process
        :param start_time: Start time for the process
        :param file_name: File being process
        :param file_path: Path to the file being processed
        :param description: Description of the file/process
        :param end_time: End time for the process
        :param percentage: Percentage of process completed
        :return: None
        """
    ######################################## YOUR CODE HERE ##################################################
        sql = f"""
        insert into {self._table_name}
        (
            process_id,
            file_name,
            file_path,
            description,
            start_time,
            end_time,
            percentage
        )
        values
        (
            '{process_id}',
            '{file_name}',
            '{file_path}',
            '{description}',
            '{start_time}',
            '{end_time}',
            {percentage}
    
        )
        """
        # execute statement
>       self._connection.execute(sql)
E       sqlite3.OperationalError: no such column: None

utils/database.py:105: OperationalError
=========================== short test summary info ============================
FAILED test.py::TestApp::test_db_operations - sqlite3.OperationalError: no such column: None
========================= 1 failed, 2 passed in 0.81s ==========================
```

What is happening is that there are 2 columns that are allowed to have NULL values, but we still need them as columns in the database table for this to work. The values themselves can be NONE/NULL, but the column names need to still exist fo those values to be NULL.

A way that we can fix this is with parameter substitution, a feature provided by many database libraries, including sqlite3, which helps us prevent SQL injection attacks. We will create SQL commands using placeholders (`?,?,?...` in our code) for parameters, and then provide the actual parameter values separately (`col_values` in our code). The database library will then automatically quote the parameters as necessary, which can help prevent SQL injection attacks and also takes care of quoting issues like the issue we just ran into where


Our `insert()` function then looks like this:
```py
def insert(self, process_id, start_time, file_name=None, file_path=None,
               description=None, end_time=None, percentage=None) -> None:
        """
        Insert a record into the table

        :param process_id: Assign an id to the process
        :param start_time: Start time for the process
        :param file_name: File being process
        :param file_path: Path to the file being processed
        :param description: Description of the file/process
        :param end_time: End time for the process
        :param percentage: Percentage of process completed
        :return: None
        """

        col_values = [
            process_id, 
            file_name, 
            file_path, 
            description, 
            start_time, 
            end_time, 
            percentage
        ]

        sql = f"""
        insert into {self._table_name}
        (
            process_id,
            file_name,
            file_path,
            description,
            start_time,
            end_time,
            percentage
        )
        values
        (
            ?,?,?,?,?,?,?
        )
        """
        # execute statement
        self._connection.execute(sql, col_values)
        # commit changes to the db
        self._connection.commit()

```


## Step 7: After tests pass, run `main.py` with `test` data 

To run the `main.py` file with the `tst` data inside of our virtual env, run:
```bash
PYTHONPATH=../ venv/bin/python main.py --type tst 
```

This then updated the entire table with populated data (21 items total):
![](./assets/4-run-main-first-time-1.png)
...
![](./assets/4-run-main-first-time-2.png)

If we go to http://127.0.0.1:8000/processes, we will see the JSON of all of these entry logs:
![](./assets/4-run-main-first-time-processes.png)

### 🐞 Debugging: `main.py` cannot find the `w2.utils` for `utils.database`

I tried to run the above command and got this as the output log error:
```bash
Traceback (most recent call last):
  File "/Users/.../.../.../.../.../course-python-4-production/w3/main.py", line 7, in <module>
    from w2.utils.database import DB
ModuleNotFoundError: No module named 'w2.utils'
```

I needed to change:

```py
from w2.utils.database import DB
```
to
```py
from w3.utils.database import DB
```

Now it can find the database.py file we wrote that uses sqlite3, since this lives only in w3, not w2.

### 🐞 Debugging: If the `index.html` file cannot render the websocket connection to the data:


Update the protocol from `ws` to `wss` if you're working on non-localhost
```html
var ws = new WebSocket(`wss://localhost:8000/ws`);
```

Make sure that the URL of the websocket matches what is being rendered:
```html
var ws = new WebSocket(`wss://1233456.crb.app/ws`);
```


# Run tests with prints 
```
PYTHONPATH=../ pytest test.py -s
```

# Run tests without prints 
```
PYTHONPATH=../ pytest test.py
```

# Run the data processing code
````
# Run on `test` data
PYTHONPATH=../ python main.py --type tst

# Run on `small` data
PYTHONPATH=../ python main.py --type sml

# Run on the `big` data
PYTHONPATH=../ python main.py --type bg
````

# Start FastAPI server
````
PYTHONPATH=.. uvicorn server:app --workers 2
````