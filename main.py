import os

from dotenv import load_dotenv
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from docker_utils import run_bash_script

load_dotenv()


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/restart-docker")
def restart_docker():
    docker_path = os.getenv('DOCKER_COMPOSE_PATH')
    run_bash_script("restart_docker.sh", {'DOCKER_COMPOSE_PATH':docker_path})
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content='Request to restart received',
    )
