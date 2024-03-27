from threading import Thread, Event
import queue
from boot import *

class WebSocketHandler:
    def __init__(self):
        self.tick_queue = queue.Queue()
        self.api = ShoonyaApiPy()
        self.feed_opened = False
        self.finished_event = Event()  # Event to signal that the WebSocket thread has finished

    def event_handler_feed_update(self, tick_data):
        print(type(tick_data))
        print(f"feed update ", tick_data['lp'])
        self.tick_queue.put((tick_data['ts'], tick_data['lp']))

    def event_handler_order_update(self, tick_data):
        print(f"order update {tick_data}")

    def open_callback(self):
        self.feed_opened = True

    def start(self):
        self.api.start_websocket(
            order_update_callback=self.event_handler_order_update,
            subscribe_callback=self.event_handler_feed_update,
            socket_open_callback=self.open_callback
        )
        self.finished_event.set()  # Signal that the WebSocket thread has finished

    def subscribe(self, instruments):
        while not self.feed_opened:
            pass  # Wait until the feed is opened

        self.api.subscribe(instruments)

    def run(self):
        thread = Thread(target=self.start)
        thread.start()
        thread.join()  # Wait for the WebSocket thread to finish

    def get_next_tick(self):
        try:
            return self.tick_queue.get_nowait()
        except queue.Empty:
            return None