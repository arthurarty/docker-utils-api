import os
import subprocess

from dotenv import load_dotenv
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from custom_logging import logger
from docker_utils import run_docker_command, DockerCommandEnum


load_dotenv()


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/docker-up-build")
def docker_up_build():
    base_dir = os.getcwd()
    try:
        os.chdir(os.getenv('DOCKER_COMPOSE_PATH'))
        run_docker_command(DockerCommandEnum.DOCKER_UP_BUILD)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content='Docker compose complete'
        )
    except FileNotFoundError as exc:
        logger.exception(exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content='Failed to execute docker compose down file not found.'
        )
    except subprocess.CalledProcessError as exc:
        logger.exception(exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content='Subproccess failed to execute.'
        )
    except subprocess.TimeoutExpired as exc:
        logger.exception(exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content='Request timed out.'
        )
    finally:
        os.chdir(base_dir)


@app.get("/docker-down")
def docker_down():
    """
    Runs docker compose down
    """
    base_dir = os.getcwd()
    try:
        os.chdir(os.getenv('DOCKER_COMPOSE_PATH'))
        run_docker_command(DockerCommandEnum.DOCKER_DOWN)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content='Docker compose complete'
        )
    except FileNotFoundError as exc:
        logger.exception(exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content='Failed to execute docker compose down file not found.'
        )
    except subprocess.CalledProcessError as exc:
        logger.exception(exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content='Subproccess failed to execute.'
        )
    except subprocess.TimeoutExpired as exc:
        logger.exception(exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content='Request timed out.'
        )
    finally:
        os.chdir(base_dir)
