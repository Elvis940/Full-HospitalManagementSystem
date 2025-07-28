# receptionist/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AppointmentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket connecting...")  # Debugging
        await self.channel_layer.group_add("appointments", self.channel_name)
        await self.accept()
        print("WebSocket connected!")  # Debugging

    async def disconnect(self, close_code):
        print(f"WebSocket disconnected with code: {close_code}")
        await self.channel_layer.group_discard("appointments", self.channel_name)

    async def appointment_update(self, event):
        print("Sending update:", event)  # Debugging
        await self.send(text_data=json.dumps(event))