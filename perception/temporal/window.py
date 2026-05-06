from collections import deque


class RollingWindow:
    """Fixed-length FIFO buffer for temporal sequences."""

    def __init__(self, maxlen: int):
        self._q: deque = deque(maxlen=maxlen)

    def append(self, item) -> None:
        if item is not None:
            self._q.append(item)

    def __len__(self) -> int:
        return len(self._q)

    def as_list(self) -> list:
        return list(self._q)

    def clear(self) -> None:
        self._q.clear()
