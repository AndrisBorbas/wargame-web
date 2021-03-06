import json
from enum import Enum

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer


class MessageType(Enum):
    ERROR = (0,)
    WARNING = (1,)
    INFO = (2,)
    SUCCESS = 3


def log(message, log_var, log_level):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(log_var, {"type": "log_event", "message": message, "level": log_level.name})


class LogConsumer(WebsocketConsumer):
    def log_var(self):
        return self.scope["url_route"]["kwargs"]["log_var"]

    def connect(self):
        if not self.scope["user"].is_superuser:
            return

        async_to_sync(self.channel_layer.group_add)(self.log_var(), self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.log_var(), self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        pass

    def log_event(self, event):
        self.send(json.dumps({"level": event["level"], "message": event["message"]}))
