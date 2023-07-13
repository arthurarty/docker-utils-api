from fastapi import FastAPI

from docker_utils import DockerCommandEnum, run_docker_command


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/docker-up-build")
def docker_up_build():
    """
    Runs the docker build command
    """
    return run_docker_command(DockerCommandEnum.DOCKER_UP_BUILD)


@app.get("/docker-down")
def docker_down():
    """
    Runs docker compose down
    """
    return run_docker_command(DockerCommandEnum.DOCKER_DOWN)
