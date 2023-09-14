import subprocess


# subprocess

def call_subprocess(command: str) -> bool:
    try:
        return (
            bool(
                subprocess.call(
                    command,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT,
                    shell=True,
                )
            )
            == 0
        )
    except subprocess.CalledProcessError:
        return False

def check_subprocess_output(command: str) -> str:
    try:
        return subprocess.check_output(
            command, stderr=subprocess.STDOUT, shell=True, text=True
        )
    except subprocess.CalledProcessError:
        return ""

# Boot config (/boot/config.txt) - deprecated and not used anymore but can be useful

def read_config(config_file: str) -> dict[str, str]:
    config = {}

    with open(config_file, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line and not line.startswith("#"):
                splits = line.split("=", 1)  # Split only on the first '='
                if len(splits) == 2:
                    config[splits[0].strip()] = splits[1].strip()

    return config

def write_config(config: dict, config_file: str):
    with open(config_file, "w") as f:
        for k, v in config.items():
            f.write(f"{k}={v}\n")

def set_config_value(key: str, value: str, config_file: str):
    config = read_config(config_file)
    config[key] = value
    write_config(config, config_file)
