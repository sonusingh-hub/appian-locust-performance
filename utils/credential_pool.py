import csv
import os
from collections import deque
from gevent.lock import Semaphore

from config.environment import get_selected_environment


class CredentialPool:
    _available_users = None
    _in_use_users = set()
    _lock = Semaphore()

    @classmethod
    def _get_credential_mode(cls):
        mode = os.getenv("LOCUST_CREDENTIAL_MODE", "reuse").strip().lower()
        return mode if mode in ("reserved", "reuse") else "reuse"

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

            mode = cls._get_credential_mode()

            if not cls._available_users:
                selected_env = get_selected_environment()
                raise RuntimeError(
                    f"No credentials available for environment '{selected_env}'. "
                    f"In-use users: {len(cls._in_use_users)}. "
                    "Add more users to data/users.csv or reduce Locust user count."
                )

            if mode == "reuse":
                # Round-robin credential reuse supports high-user scenarios
                # when unique accounts are limited.
                user = cls._available_users.popleft()
                cls._available_users.append(user)
            else:
                user = cls._available_users.popleft()
                cls._in_use_users.add(user)

            return [user[0], user[1]]

    @classmethod
    def release_user(cls, auth):
        if not auth or len(auth) < 2:
            return

        with cls._lock:
            if cls._available_users is None:
                return

            if cls._get_credential_mode() == "reuse":
                # No release bookkeeping needed for round-robin reuse mode.
                return

            user = (auth[0], auth[1])
            if user in cls._in_use_users:
                cls._in_use_users.remove(user)
                cls._available_users.append(user)

            return