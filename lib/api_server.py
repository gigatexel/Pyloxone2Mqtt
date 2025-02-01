from fastapi import FastAPI, HTTPException


def create_api_server(event_bus):
    app = FastAPI()

    @app.on_event("startup")
    async def startup_event():
        # The event bus is already running, so we don't start it here
        pass

    @app.post("/publish/")
    async def publish_to_event_bus(topic: str, message: str):
        try:
            await event_bus.publish(topic, {"payload": message})
            return {
                "status": "Message published to the event bus",
                "topic": topic,
                "message": message,
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return app
