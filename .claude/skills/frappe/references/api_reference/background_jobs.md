# API Reference: background_jobs.py

**Language**: Python

**Source**: `utils/background_jobs.py`

---

## Classes

### FrappeWorker

**Inherits from**: Worker

#### Methods

##### work(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### run_maintenance_tasks(self)

Attempt to start a scheduler in case the worker doing scheduling died.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### start_frappe_scheduler(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### FrappeWorkerNoFork

**Inherits from**: FrappeWorker

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### work(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### execute_job(self, job: 'Job', queue: 'Queue')

Execute job in same thread/process, do not fork()

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| job | 'Job' | - | - |
| queue | 'Queue' | - | - |


##### no_fork_exception_handler(self, job, exc_type, exc_value, traceback)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| job | None | - | - |
| exc_type | None | - | - |
| exc_value | None | - | - |
| traceback | None | - | - |


##### get_heartbeat_ttl(self, job: 'Job') → int

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| job | 'Job' | - | - |

**Returns**: `int`


##### kill_horse(self, sig = signal.SIGKILL)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sig | None | signal.SIGKILL | - |




## Functions

### get_queues_timeout() → dict[str, int]

Method returning a mapping of queue name to timeout for that queue

:return: Dictionary of queue name to timeout

**Returns**: `dict[str, int]`



### enqueue(method: str | Callable, queue: str = 'default', timeout: int | None = None, event: str | None = None, is_async: bool = True, job_name: str | None = None, now: bool = False, enqueue_after_commit: bool = False) → Job | Any

Enqueue method to be executed using a background worker

:param method: method string or method object
:param queue: should be either long, default or short
:param timeout: should be set according to the functions
:param event: this is passed to enable clearing of jobs from queues
:param is_async: if is_async=False, the method is executed immediately, else via a worker
:param job_name: [DEPRECATED] can be used to name an enqueue call, which can be used to prevent
duplicate calls
:param now: if now=True, the method is executed via frappe.call()
:param enqueue_after_commit: if True, the job will be enqueued after the current transaction is
committed
:param on_success: Success callback
:param on_failure: Failure callback
:param at_front: Enqueue the job at the front of the queue or not
:param kwargs: keyword arguments to be passed to the method
:param deduplicate: do not re-queue job if it's already queued, requires job_id.
:param job_id: Assigning unique job id, which can be checked using `is_job_enqueued`
:param at_front_when_starved: If the queue appears to be starved then new jobs are
automatically inserted in LIFO fashion.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| method | str | Callable | - | - |
| queue | str | 'default' | - |
| timeout | int | None | None | - |
| event | str | None | None | - |
| is_async | bool | True | - |
| job_name | str | None | None | - |
| now | bool | False | - |
| enqueue_after_commit | bool | False | - |

**Returns**: `Job | Any`



### enqueue_doc(doctype, name = None, method = None, queue = 'default', timeout = 300, now = False)

Enqueue a method to be run on a document

:param doctype: DocType of the document on which you want to run the event
:param name: Name of the document on which you want to run the event
:param method: method string or method object
:param queue: (optional) should be either long, default or short
:param timeout: (optional) should be set according to the functions
:param kwargs: keyword arguments to be passed to the method

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | None | - |
| method | None | None | - |
| queue | None | 'default' | - |
| timeout | None | 300 | - |
| now | None | False | - |

**Returns**: (none)



### run_doc_method(doctype, name, doc_method)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| doc_method | None | - | - |

**Returns**: (none)



### execute_job(site, method, event, job_name, kwargs, user = None, is_async = True, retry = 0)

Executes job in a worker, performs commit/rollback and logs if there is any error

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| site | None | - | - |
| method | None | - | - |
| event | None | - | - |
| job_name | None | - | - |
| kwargs | None | - | - |
| user | None | None | - |
| is_async | None | True | - |
| retry | None | 0 | - |

**Returns**: (none)



### start_worker(queue: str | None = None, quiet: bool = False, rq_username: str | None = None, rq_password: str | None = None, burst: bool = False, strategy: DequeueStrategy | None = DequeueStrategy.DEFAULT) → NoReturn

Wrapper to start rq worker. Connects to redis and monitors these queues.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| queue | str | None | None | - |
| quiet | bool | False | - |
| rq_username | str | None | None | - |
| rq_password | str | None | None | - |
| burst | bool | False | - |
| strategy | DequeueStrategy | None | DequeueStrategy.DEFAULT | - |

**Returns**: `NoReturn`



### start_worker_pool(queue: str | None = None, num_workers: int = 1, quiet: bool = False, burst: bool = False) → NoReturn

Start worker pool with specified number of workers.

WARNING: This feature is considered "EXPERIMENTAL".

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| queue | str | None | None | - |
| num_workers | int | 1 | - |
| quiet | bool | False | - |
| burst | bool | False | - |

**Returns**: `NoReturn`



### get_worker_name(queue)

When limiting worker to a specific queue, also append queue name to default worker name

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| queue | None | - | - |

**Returns**: (none)



### get_jobs(site = None, queue = None, key = 'method')

Gets jobs per queue or per site or both

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| site | None | None | - |
| queue | None | None | - |
| key | None | 'method' | - |

**Returns**: (none)



### get_queue_list(queue_list = None, build_queue_name = False)

Defines possible queues. Also wraps a given queue in a list after validating.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| queue_list | None | None | - |
| build_queue_name | None | False | - |

**Returns**: (none)



### get_workers(queue = None)

Return a list of Worker objects tied to a queue object if queue is passed, else return a list of all workers.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| queue | None | None | - |

**Returns**: (none)



### get_running_jobs_in_queue(queue)

Return a list of Jobs objects that are tied to a queue object and are currently running.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| queue | None | - | - |

**Returns**: (none)



### get_queue(qtype: str, is_async: bool = True) → Queue

Return a Queue object tied to a redis connection.

:param qtype: Queue type, should be either long, default or short
:param is_async: Whether the job should be executed asynchronously or in the same process
:return: Queue object

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| qtype | str | - | - |
| is_async | bool | True | - |

**Returns**: `Queue`



### validate_queue(queue: str, default_queue_list: list | None = None) → None

Validates if the queue is in the list of default queues.

:param queue: The queue to be validated
:param default_queue_list: Optionally, a custom list of queues to validate against
:return:

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| queue | str | - | - |
| default_queue_list | list | None | None | - |

**Returns**: `None`



### get_redis_conn(username = None, password = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| username | None | None | - |
| password | None | None | - |

**Returns**: (none)



### get_redis_connection_without_auth()

**Returns**: (none)



### get_queues(connection = None) → list[Queue]

Get all the queues linked to the current bench.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| connection | None | None | - |

**Returns**: `list[Queue]`



### generate_qname(qtype: str) → str

Generate qname by combining bench ID and queue type.

qnames are useful to define namespaces of customers.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| qtype | str | - | - |

**Returns**: `str`



### is_queue_accessible(qobj: Queue) → bool

Checks whether queue is relate to current bench or not.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| qobj | Queue | - | - |

**Returns**: `bool`



### enqueue_test_job()

**Returns**: (none)



### test_job(s)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| s | None | - | - |

**Returns**: (none)



### create_job_id(job_id: str | None = None) → str

Generate unique job id for deduplication

:param job_id: Optional job id, if not provided, a UUID is generated for it
:return: Unique job id, namespaced by site

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| job_id | str | None | None | - |

**Returns**: `str`



### is_job_enqueued(job_id: str) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| job_id | str | - | - |

**Returns**: `bool`



### get_job_status(job_id: str) → JobStatus | None

Get RQ job status, returns None if job is not found.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| job_id | str | - | - |

**Returns**: `JobStatus | None`



### get_job(job_id: str) → Job | None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| job_id | str | - | - |

**Returns**: `Job | None`



### set_niceness()

Background processes should have slightly lower priority than web processes.

Calling this function increments the niceness of process by configured value or default.
Note: This function should be called only once in process' lifetime.

**Returns**: (none)



### truncate_failed_registry(job, connection, type, value, traceback)

Ensures that number of failed jobs don't exceed specified limits.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| job | None | - | - |
| connection | None | - | - |
| type | None | - | - |
| value | None | - | - |
| traceback | None | - | - |

**Returns**: (none)



### _check_queue_size(q: Queue)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| q | Queue | - | - |

**Returns**: (none)



### _site_count() → int

**Returns**: `int`



### _start_sentry()

**Returns**: (none)



### enqueue_call()

**Returns**: (none)



### add_to_dict(job)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| job | None | - | - |

**Returns**: (none)


