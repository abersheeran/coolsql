import subprocess

source_dirs = "example tests"  # TODO
subprocess.check_call(f"isort --check --diff {source_dirs}", shell=True)
subprocess.check_call(f"black --check --diff {source_dirs}", shell=True)
subprocess.check_call(f"flake8 --ignore W503,E203,E501,E731 {source_dirs}", shell=True)
