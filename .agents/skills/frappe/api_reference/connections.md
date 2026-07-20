# API Reference: connections.py

**Language**: Python

**Source**: `utils/connections.py`

---

## Functions

### can_connect(sock: socket.socket, address: tuple[str, int] | str, timeout: int | float) → bool

Check whether we can connect to a socket address.

Args:
        sock: The socket object to use for the connection.
        address: The address to connect to (tuple for network, string for unix).
        timeout: Connection timeout in seconds.

Returns:
        True if connection was successful, False otherwise.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sock | socket.socket | - | - |
| address | tuple[str, int] | str | - | - |
| timeout | int | float | - | - |

**Returns**: `bool`



### is_open(scheme: str, hostname: str | None, port: int | str | None, path: str | None, timeout: int | float = 10) → bool

Check if a service is reachable via socket connection.

Args:
        scheme: The URL scheme (redis, mariadb, etc.) or 'unix'.
        hostname: The remote host to connect to.
        port: The port number to connect to.
        path: The path to the unix socket (if scheme is 'unix').
        timeout: Connection timeout in seconds.

Returns:
        True if the service is reachable, False otherwise.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scheme | str | - | - |
| hostname | str | None | - | - |
| port | int | str | None | - | - |
| path | str | None | - | - |
| timeout | int | float | 10 | - |

**Returns**: `bool`



### check_database()

**Returns**: (none)



### check_redis(redis_services = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| redis_services | None | None | - |

**Returns**: (none)



### check_connection(redis_services = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| redis_services | None | None | - |

**Returns**: (none)


