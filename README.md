# The Action

## Installation

```bash
pip install -r requirements.txt
```

## Architecture

- `config.py`: Constants and configurations.
- `events.py`
- `game_logging.py`
- `game_logic.py`
- `map.py`
- `render.py`
- `sidebar.py`
- `the_action.py`
- `utils.py`

Events are used for connections between modules.

Register your events by `events_manager.register()`, trigger them by `events_manager.new_event()`, and bind your callbacks by `events_manager.subscribe()`.

Your callbacks should accept three parameters:

```python
def my_callback(game, event: EventName, em: EventsManager):
    pass
```

Using a subscription dictionary is strongly recommended and bind them by `events_manager.multi_subscribe()` or `events_manager.import_module()`.

## Dev Tips

Do not call `game.clear()` when drawing sprites.

Instead, append a sprite to `game.draw_list`.

## Pyasync Server

The PyAsync server is a simple implementation of a server using asyncio.

### Adding a New Action

Adding a new action in `pyasync_server` could be no more easier with following steps:

1. Define a function in `actions.py`.

   The arguments reveal data you need when executing the action. Paying attention to them is quite useful when defining the package structure later.

2. Add new package type in `package.py`.

   `package` is the minimum unit where data is stored of each request. To define a new package type, you should:

   1. Add new enumeration to the class `PACKAGE` in common/package.py.

   2. Define functions to pack your new packages.

      For example, `REQUEST_MARIADB_TEST` and `ANSWER_MARIADB_TEST`.

3. Add a new flow in `unpack_and_process()` in `actions.py`

### TLS Support

TLS is disabled by default. To enable it, follow the instructions below:

Use this command to generate keys and certification annually:

```bash
openssl req -newkey rsa:2048 -nodes -keyout server.key -x509 -days 365 -out server.crt -batch
```

- -x509: to generate self-signed certification
- -days: period of validity
- -nodes: don't encrypt the private key
- -batch: use default of configured settings instead of getting them interactively

Make sure your client and server use the same `server.crt`.

DO NOT DISTRIBUTE YOUR `server.key`!!!

At last, modify `enable_tls` to `True` in `config.py`.

Now your connections are under the protection of TLS.

### Database Support

Database is disabled by default. To enable it, follow the instructions below:

Edit `requirements.txt` to enable modules related to database you need and install them with:

```bash
pip install -r requirements.txt
```

Edit `server_config.py` to set parameters for connecting the database.

Finally, use `connect()` to visit your database and do what you want.
