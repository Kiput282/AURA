from collections import defaultdict
from typing import Callable

from loguru import logger

from aura.events.event import Event


EventHandler = Callable[[Event], None]


class EventBus:
    """
    Simple internal event bus for AURA.

    Responsibilities:
    - register event handlers
    - emit events
    - dispatch events to subscribers
    """

    def __init__(self):
        self._subscribers: dict[str, list[EventHandler]] = defaultdict(list)

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        self._subscribers[event_name].append(handler)
        logger.info(f"Handler subscribed to event: {event_name}")

    def emit(self, event: Event) -> int:
        handlers = self._subscribers.get(event.name, [])

        logger.info(f"Event emitted: {event.name}")

        if not handlers:
            logger.debug(f"No handlers registered for event: {event.name}")
            return 0

        handled_count = 0

        for handler in handlers:
            try:
                handler(event)
                handled_count += 1
            except Exception as error:
                logger.exception(f"Error while handling event {event.name}: {error}")

        return handled_count
