from fastapi import FastAPI
import os
import uvicorn

from routers import root

app = FastAPI()
app.include_router(root.routers)

if __name__ == '__main__':
    port = os.environ.get("PORT", "8080")
    options = {
            'port': int(port),
            'host': '0.0.0.0',
            'workers': 2,
            'reload': True,
        }
    uvicorn.run("main:app", **options)