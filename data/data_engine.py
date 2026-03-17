import csv
import random
from functools import lru_cache

from config.environment import get_selected_environment
from config.test_data import (
    COUNTRIES,
    MONTHS,
    PRODUCTS,
    VEHICLE_TYPES,
    POWER_TRAINS,
    COMPANIES,
    EXPECTED_DELIVERY,
    IMMINENT_EXPIRY_OPTIONS,
    OVERDUE_BY_OPTIONS,
    LANGUAGES,
    CLIENT_GROUPS,
    CLIENT_NAMES,
    BILL_TO,
    FLEET_SCHEDULE_PRODUCTS,
    VEHICLE_ON_ORDER_PRODUCTS,
    VEHICLE_ON_ORDER_VEHICLE_TYPES,
    IMMINENT_EXPIRY_PRODUCTS,
    SUSTAINABILITY_PRODUCTS,
    VEHICLE_UTILISATION_PRODUCTS,
    SERVICE_OVERDUE_PRODUCTS,
    SERVICE_OVERDUE_MONTHS,
    MAINTENANCE_INCLUDED_OPTIONS,
    SUSTAINABILITY_START_DATES,
    SUSTAINABILITY_END_DATES,
    REGISTRATIONS,
    MANAGE_USER_SEARCH_VALUES,
    MANAGE_USER_FILTER_VALUES
)


class DataEngine:

    PRODUCT_WEIGHTS = {
        "Fleet Managed": 20,
        "Finance Lease": 10,
        "Operating Lease": 50,
        "Novated Lease": 30,
    }

    VEHICLE_TYPE_WEIGHTS = {
        "Light Commercial": 30,
        "Passenger": 50,
        "Truck": 10,
        "Trailer": 20,
    }

    POWER_TRAIN_WEIGHTS = {
        "Internal Combustion Engine": 30,
        "Hybrid Electric Vehicle": 50,
        "Mild Hybrid Electric Vehicle": 20,
        "Extended-Range Electric Vehicle": 10,
        "Plug-In Hybrid Electric Vehicle": 20,
        "Battery Electric Vehicle": 40,
    }

    @staticmethod
    def _choice(options):
        if not options:
            raise ValueError("No options available for random choice")
        return random.choice(options)

    @staticmethod
    def _sample(options, count):
        if not options:
            return []
        return random.sample(options, k=min(count, len(options)))

    @staticmethod
    def _weighted_sample(options, count, weights_map):
        if not options:
            return []

        count = min(count, len(options))
        if count <= 0:
            return []

        # Weighted sampling without replacement.
        remaining = list(options)
        selected = []

        for _ in range(count):
            if not remaining:
                break

            weights = [max(float(weights_map.get(option, 1)), 0.0) for option in remaining]
            if sum(weights) <= 0:
                # Fallback to uniform if all provided weights are zero.
                selected_option = random.choice(remaining)
            else:
                selected_option = random.choices(remaining, weights=weights, k=1)[0]

            selected.append(selected_option)
            remaining.remove(selected_option)

        return selected

    @staticmethod
    @lru_cache(maxsize=16)
    def _users_for_environment(csv_path, selected_env):
        matching_users = []
        with open(csv_path, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get("environment", "").strip().upper() == selected_env:
                    username = row.get("username", "").strip()
                    password = row.get("password", "").strip()
                    if username and password:
                        matching_users.append((username, password))
        return tuple(matching_users)

    @staticmethod
    def country():
        return DataEngine._choice(COUNTRIES)

    @staticmethod
    def country_list(count=2):
        return DataEngine._sample(COUNTRIES, count)

    @staticmethod
    def month():
        return DataEngine._choice(MONTHS)

    @staticmethod
    def product():
        return DataEngine._choice(PRODUCTS)

    @staticmethod
    def vehicle_type():
        return DataEngine._choice(VEHICLE_TYPES)

    @staticmethod
    def vehicle_type_list(count=2):
        return DataEngine._weighted_sample(
            VEHICLE_TYPES,
            count,
            DataEngine.VEHICLE_TYPE_WEIGHTS,
        )

    @staticmethod
    def power_train():
        return DataEngine._choice(POWER_TRAINS)

    @staticmethod
    def power_train_list(count=2):
        return DataEngine._weighted_sample(
            POWER_TRAINS,
            count,
            DataEngine.POWER_TRAIN_WEIGHTS,
        )

    @staticmethod
    def company():
        return DataEngine._choice(COMPANIES)

    @staticmethod
    def expected_delivery():
        return DataEngine._choice(EXPECTED_DELIVERY)

    @staticmethod
    def imminent_expiry():
        return DataEngine._choice(IMMINENT_EXPIRY_OPTIONS)

    @staticmethod
    def overdue_by():
        return DataEngine._choice(OVERDUE_BY_OPTIONS)

    @staticmethod
    def maintenance_included():
        return DataEngine._choice(MAINTENANCE_INCLUDED_OPTIONS)

    @staticmethod
    def language():
        return DataEngine._choice(LANGUAGES)

    @staticmethod
    def client_groups(count=2):
        return DataEngine._sample(CLIENT_GROUPS, count)

    @staticmethod
    def client_names(count=2):
        return DataEngine._sample(CLIENT_NAMES, count)

    @staticmethod
    def bill_to(count=2):
        return DataEngine._sample(BILL_TO, count)

    @staticmethod
    def fleet_schedule_products(count=2):
        return DataEngine._weighted_sample(
            FLEET_SCHEDULE_PRODUCTS,
            count,
            DataEngine.PRODUCT_WEIGHTS,
        )

    @staticmethod
    def fleet_schedule_client_groups(count=2):
        return DataEngine.client_groups(count)

    @staticmethod
    def fleet_schedule_client_names(count=2):
        return DataEngine.client_names(count)

    @staticmethod
    def fleet_schedule_bill_to(count=2):
        return DataEngine.bill_to(count)

    @staticmethod
    def vehicle_on_order_products(count=2):
        return DataEngine._weighted_sample(
            VEHICLE_ON_ORDER_PRODUCTS,
            count,
            DataEngine.PRODUCT_WEIGHTS,
        )

    @staticmethod
    def vehicle_on_order_vehicle_types(count=2):
        return DataEngine._weighted_sample(
            VEHICLE_ON_ORDER_VEHICLE_TYPES,
            count,
            DataEngine.VEHICLE_TYPE_WEIGHTS,
        )

    @staticmethod
    def imminent_expiry_month():
        return DataEngine._choice(MONTHS)

    @staticmethod
    def imminent_expiry_products(count=2):
        return DataEngine._weighted_sample(
            IMMINENT_EXPIRY_PRODUCTS,
            count,
            DataEngine.PRODUCT_WEIGHTS,
        )

    @staticmethod
    def sustainability_products(count=2):
        return DataEngine._weighted_sample(
            SUSTAINABILITY_PRODUCTS,
            count,
            DataEngine.PRODUCT_WEIGHTS,
        )

    @staticmethod
    def sustainability_start_date():
        return DataEngine._choice(SUSTAINABILITY_START_DATES)

    @staticmethod
    def sustainability_end_date():
        return DataEngine._choice(SUSTAINABILITY_END_DATES)

    @staticmethod
    def vehicle_utilisation_month():
        return DataEngine._choice(MONTHS)

    @staticmethod
    def vehicle_utilisation_products(count=2):
        return DataEngine._weighted_sample(
            VEHICLE_UTILISATION_PRODUCTS,
            count,
            DataEngine.PRODUCT_WEIGHTS,
        )

    @staticmethod
    def vehicle_utilisation_imminent_expiry():
        return DataEngine.imminent_expiry()

    @staticmethod
    def service_overdue_month():
        return DataEngine._choice(SERVICE_OVERDUE_MONTHS)

    @staticmethod
    def service_overdue_products(count=1):
        return DataEngine._weighted_sample(
            SERVICE_OVERDUE_PRODUCTS,
            count,
            DataEngine.PRODUCT_WEIGHTS,
        )

    @staticmethod
    def registration():
        return DataEngine._choice(REGISTRATIONS)

    @staticmethod
    def manage_user_search():
        return DataEngine._choice(MANAGE_USER_SEARCH_VALUES)

    @staticmethod
    def manage_user_filters(count=2):
        return DataEngine._sample(MANAGE_USER_FILTER_VALUES, count)

    @staticmethod
    def home_country_list(count=1):
        return DataEngine._sample(COUNTRIES, count)

    @staticmethod
    def home_client_groups(count=1):
        return DataEngine.client_groups(count)

    @staticmethod
    def home_client_names(count=1):
        return DataEngine.client_names(count)

    @staticmethod
    def home_bill_to(count=1):
        return DataEngine.bill_to(count)

    @staticmethod
    def get_environment_user(csv_path="data/users.csv"):
        selected_env = get_selected_environment()

        matching_users = DataEngine._users_for_environment(csv_path, selected_env)

        if not matching_users:
            raise ValueError(
                f"No users found in {csv_path} for environment '{selected_env}'"
            )

        username, password = random.choice(matching_users)
        return [username, password]