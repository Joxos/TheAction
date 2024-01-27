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

Using a subscription dictionary is strongly recommended and bind them by `events_manager.multi_subscribe()`.

## Dev Tips

Do not call `game.clear()` when drawing sprites.

Instead, append a sprite to `game.draw_list`.
