import os
import shlex
import subprocess
from enum import Enum

import requests
from dotenv import load_dotenv
from fastapi import status
from fastapi.responses import JSONResponse

from custom_logging import logger

load_dotenv()


class DockerCommandEnum(Enum):
    DOCKER_DOWN = "DOCKER_DOWN"
    DOCKER_UP_BUILD = "DOCKER_UP_BUILD"


DOCKER_COMMAND_MAPPING = {
    DockerCommandEnum.DOCKER_DOWN: "docker compose down",
    DockerCommandEnum.DOCKER_UP_BUILD: "docker compose -f docker-compose.yml -f docker-compose.prod.yml up --detach --build"
}


def send_call_back(msg: str) -> requests.Response:
    """
    Send post request to the defined CALL_BACK_URL with message
    """
    call_back_url = os.environ.get('CALL_BACK_URL')
    logger.info('Sending data to call_back_url %s', call_back_url)
    return requests.post(call_back_url, json={'msg': msg}, timeout=60)


def run_docker_command(
        docker_command: DockerCommandEnum,
        use_call_back: bool = False
    ) -> subprocess.CompletedProcess:
    base_dir = os.getcwd()
    os.chdir(os.getenv('DOCKER_COMPOSE_PATH'))
    logger.info('Done changing directory, starting docker command')
    try:
        subprocess.run(
            shlex.split(DOCKER_COMMAND_MAPPING.get(docker_command)),
            check=True,
            capture_output=True,
            encoding="utf-8",
            timeout=500,
        )
        msg = f'Docker command `{DOCKER_COMMAND_MAPPING.get(docker_command)}` complete.'
        if use_call_back:
            send_call_back(msg)
            return
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=msg
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
