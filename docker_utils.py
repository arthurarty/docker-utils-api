import shlex
import subprocess
from enum import Enum


class DockerCommandEnum(Enum):
    DOCKER_DOWN = "DOCKER_DOWN"
    DOCKER_UP_BUILD = "DOCKER_UP_BUILD"


DOCKER_COMMAND_MAPPING = {
    DockerCommandEnum.DOCKER_DOWN: "docker compose down",
    DockerCommandEnum.DOCKER_UP_BUILD: "docker compose -f docker-compose.yml -f docker-compose.prod.yml up --detach --build"
}


def run_docker_command(docker_command: DockerCommandEnum) -> subprocess.CompletedProcess:
    return subprocess.run(
        shlex.split(DOCKER_COMMAND_MAPPING.get(docker_command)),
        check=True,
        capture_output=True,
        encoding="utf-8",
        timeout=500,
    )
