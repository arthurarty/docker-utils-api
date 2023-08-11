import os

from dotenv import load_dotenv
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from docker_utils import DockerCommandEnum, run_docker_command

load_dotenv()


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def check_api_key(api_key: str = Depends(oauth2_scheme)):
    if api_key != os.getenv('EXT_API_KEY'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )


@app.get("/", dependencies=[Depends(check_api_key)])
async def root():
    return {"message": "Hello World"}


@app.get("/docker-up-build", dependencies=[Depends(check_api_key)])
def docker_up_build(background_tasks: BackgroundTasks):
    """
    Runs the docker build command
    """
    background_tasks.add_task(
        run_docker_command, DockerCommandEnum.DOCKER_UP_BUILD, use_call_back=True
    )
    msg = 'Request received, call back will be sent'
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'msg': msg}
    )


@app.get("/docker-down", dependencies=[Depends(check_api_key)])
def docker_down():
    """
    Runs docker compose down
    """
    return run_docker_command(DockerCommandEnum.DOCKER_DOWN)


@app.get("/docker-status", dependencies=[Depends(check_api_key)])
def docker_status():
    """
    Run docker status
    """
    return run_docker_command(DockerCommandEnum.DOCKER_SERVICES_STATUS, print_output=True)
