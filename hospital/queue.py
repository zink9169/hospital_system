# hospital/queue.py
from collections import deque

class AppointmentQueue:
    def __init__(self):
        self.queue = deque()

    def add_appointment(self, appointment):
        self.queue.append(appointment)

    def get_queue(self):
        return list(self.queue)

    def remove_appointment(self):
        if self.queue:
            return self.queue.popleft()
        return None

# Initialize a global instance of the queue
appointment_queue = AppointmentQueue()
