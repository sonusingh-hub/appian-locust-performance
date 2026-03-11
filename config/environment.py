import os

ENVIRONMENTS = {
    "TEST": {
        "host": "https://orion-testanz.orix.com.au"
    },
    "PRE-PROD": {
        "host": "https://orion-preprodanz.orix.com.au"
    }
}


def get_selected_environment():
    env_name = os.getenv("APP_ENV", "TEST").strip().upper()

    if env_name not in ENVIRONMENTS:
        raise ValueError(
            f"Invalid APP_ENV '{env_name}'. Valid values are: {list(ENVIRONMENTS.keys())}"
        )

    return env_name


def get_environment_config():
    env_name = get_selected_environment()
    return ENVIRONMENTS[env_name]