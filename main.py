from fastapi import FastAPI, BackgroundTasks, status
from fastapi.responses import JSONResponse
from docker_utils import DockerCommandEnum, run_docker_command


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/docker-up-build")
def docker_up_build(background_tasks: BackgroundTasks):
    """
    Runs the docker build command
    """
    background_tasks.add_task(
        run_docker_command, DockerCommandEnum.DOCKER_UP_BUILD, use_call_back=True
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content='Request received, call back will be sent'
    )


@app.get("/docker-down")
def docker_down():
    """
    Runs docker compose down
    """
    return run_docker_command(DockerCommandEnum.DOCKER_DOWN)


@app.get("/docker-status")
def docker_status():
    """
    Run docker status
    """
    return run_docker_command(DockerCommandEnum.DOCKER_SERVICES_STATUS, print_output=True)
