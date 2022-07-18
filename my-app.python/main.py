from fastapi import FastAPI, Depends
import os
import uvicorn

from routers import root as router_root, author as router_author

from common import get_coll

app = FastAPI()
app.include_router(router_root.routers)
app.include_router(router_author.routers,
                   prefix="/api",
                   dependencies=[Depends(get_coll)]
                   )

if __name__ == '__main__':
    port = os.environ.get("PORT", "8080")
    options = {
            'port': int(port),
            'host': '0.0.0.0',
            'workers': 2,
            'reload': True,
        }
    uvicorn.run("main:app", **options)