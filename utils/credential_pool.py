import csv
from collections import deque
from gevent.lock import Semaphore

from config.environment import get_selected_environment


class CredentialPool:
    _available_users = None
    _in_use_users = set()
    _lock = Semaphore()

    @classmethod
    def _load_users(cls, csv_path="data/users.csv"):
        selected_env = get_selected_environment()
        users = []

        with open(csv_path, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if row["environment"].strip().upper() == selected_env:
                    username = row["username"].strip()
                    password = row["password"].strip()
                    users.append((username, password))

        if not users:
            raise ValueError(
                f"No users found in {csv_path} for environment '{selected_env}'"
            )

        cls._available_users = deque(users)
        cls._in_use_users = set()

    @classmethod
    def acquire_user(cls, csv_path="data/users.csv"):
        with cls._lock:
            if cls._available_users is None:
                cls._load_users(csv_path)

            if not cls._available_users:
                raise RuntimeError(
                    "No credentials available in users.csv for the selected environment."
                )

            user = cls._available_users.popleft()
            cls._available_users.append(user)

            return [user[0], user[1]]

    @classmethod
    def release_user(cls, auth):
        if not auth or len(auth) < 2:
            return

        with cls._lock:
            if cls._available_users is None:
                return
            # No action needed in round-robin reuse mode
            return