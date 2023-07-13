import subprocess
from typing import Dict, Any


def run_bash_script(script_path: str, env_vars: Dict[str, Any]):
    try:
        # Run the bash script
        subprocess.run(['bash', script_path], check=True, env=env_vars)
        print("Bash script ran successfully!")
    except subprocess.CalledProcessError as e:
        print("Error running bash script:", e)


if __name__ == "__main__":
    # Specify the path to your bash script
    bash_script_path = "restart_docker.sh"

    # Call the function to run the bash script
    run_bash_script(bash_script_path, {})
