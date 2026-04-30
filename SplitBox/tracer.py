import json
import threading
import time

TID_COMPUTE = 0
TID_COMM = 1

class Tracer:

    def __init__(self):
        self._events = []
        self._lock = threading.Lock()
        self._start = time.time()

    def reset(self):
        with self._lock:
            self._events = []
            self._start = time.time()

    def record(self, name, pid, tid, start, end):
        with self._lock:
            self._events.append({
                "name": name,
                "ph": "X",
                "ts": (start - self._start) * 1e6,
                "dur": (end - start) * 1e6,
                "pid": pid,
                "tid": tid,
            })

    def save(self, path="trace.json"):
        with self._lock:
            events = list(self._events)
        with open(path, "w") as f:
            json.dump({"traceEvents": events}, f)

    def get_events(self):
        with self._lock:
            return list(self._events)

tracer = Tracer()
