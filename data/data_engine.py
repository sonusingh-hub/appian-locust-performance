import csv
import random

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
    FLEET_SCHEDULE_PRODUCTS,
    VEHICLE_ON_ORDER_PRODUCTS,
    VEHICLE_ON_ORDER_VEHICLE_TYPES,
    IMMINENT_EXPIRY_PRODUCTS,
    SUSTAINABILITY_PRODUCTS,
    VEHICLE_UTILISATION_PRODUCTS,
    VEHICLE_UTILISATION_MONTHS,
    SERVICE_OVERDUE_PRODUCTS,
    SERVICE_OVERDUE_MONTHS,
    MAINTENANCE_INCLUDED_OPTIONS,
    FLEET_SCHEDULE_CLIENT_GROUPS,
    FLEET_SCHEDULE_CLIENT_NAMES,
    FLEET_SCHEDULE_BILL_TO,
    IMMINENT_EXPIRY_MONTHS,
    SUSTAINABILITY_START_DATES,
    SUSTAINABILITY_END_DATES,
    REGISTRATIONS,
    MANAGE_USER_SEARCH_VALUES,
    MANAGE_USER_FILTER_VALUES
)


class DataEngine:

    @staticmethod
    def country():
        return random.choice(COUNTRIES)

    @staticmethod
    def month():
        return random.choice(MONTHS)

    @staticmethod
    def product():
        return random.choice(PRODUCTS)

    @staticmethod
    def vehicle_type():
        return random.choice(VEHICLE_TYPES)

    @staticmethod
    def power_train():
        return random.choice(POWER_TRAINS)

    @staticmethod
    def company():
        return random.choice(COMPANIES)

    @staticmethod
    def expected_delivery():
        return random.choice(EXPECTED_DELIVERY)

    @staticmethod
    def imminent_expiry():
        return random.choice(IMMINENT_EXPIRY_OPTIONS)

    @staticmethod
    def overdue_by():
        return random.choice(OVERDUE_BY_OPTIONS)

    @staticmethod
    def maintenance_included():
        return random.choice(MAINTENANCE_INCLUDED_OPTIONS)

    @staticmethod
    def language():
        return random.choice(LANGUAGES)

    @staticmethod
    def fleet_schedule_products(count=2):
        return random.sample(
            FLEET_SCHEDULE_PRODUCTS,
            k=min(count, len(FLEET_SCHEDULE_PRODUCTS))
        )

    @staticmethod
    def fleet_schedule_products(count=2):
        return random.sample(
            FLEET_SCHEDULE_PRODUCTS,
            k=min(count, len(FLEET_SCHEDULE_PRODUCTS))
        )

    @staticmethod
    def fleet_schedule_client_groups(count=2):
        return random.sample(
            FLEET_SCHEDULE_CLIENT_GROUPS,
            k=min(count, len(FLEET_SCHEDULE_CLIENT_GROUPS))
        )

    @staticmethod
    def fleet_schedule_client_names(count=2):
        return random.sample(
            FLEET_SCHEDULE_CLIENT_NAMES,
            k=min(count, len(FLEET_SCHEDULE_CLIENT_NAMES))
        )

    @staticmethod
    def fleet_schedule_bill_to(count=2):
        return random.sample(
            FLEET_SCHEDULE_BILL_TO,
            k=min(count, len(FLEET_SCHEDULE_BILL_TO))
        )

    @staticmethod
    def country_list(count=2):
        return random.sample(
            COUNTRIES,
            k=min(count, len(COUNTRIES))
        )

    @staticmethod
    def vehicle_on_order_products(count=2):
        return random.sample(
            VEHICLE_ON_ORDER_PRODUCTS,
            k=min(count, len(VEHICLE_ON_ORDER_PRODUCTS))
        )

    @staticmethod
    def vehicle_on_order_vehicle_types(count=2):
        return random.sample(
            VEHICLE_ON_ORDER_VEHICLE_TYPES,
            k=min(count, len(VEHICLE_ON_ORDER_VEHICLE_TYPES))
        )

    @staticmethod
    def imminent_expiry_products(count=1):
        return random.sample(
            IMMINENT_EXPIRY_PRODUCTS,
            k=min(count, len(IMMINENT_EXPIRY_PRODUCTS))
        )

    @staticmethod
    def imminent_expiry_month():
        return random.choice(IMMINENT_EXPIRY_MONTHS)

    @staticmethod
    def imminent_expiry_products(count=2):
        return random.sample(
            IMMINENT_EXPIRY_PRODUCTS,
            k=min(count, len(IMMINENT_EXPIRY_PRODUCTS))
        )

    @staticmethod
    def sustainability_products(count=1):
        return random.sample(
            SUSTAINABILITY_PRODUCTS,
            k=min(count, len(SUSTAINABILITY_PRODUCTS))
        )

    @staticmethod
    def sustainability_products(count=2):
        return random.sample(
            SUSTAINABILITY_PRODUCTS,
            k=min(count, len(SUSTAINABILITY_PRODUCTS))
        )

    @staticmethod
    def sustainability_start_date():
        return random.choice(SUSTAINABILITY_START_DATES)

    @staticmethod
    def sustainability_end_date():
        return random.choice(SUSTAINABILITY_END_DATES)

    @staticmethod
    def vehicle_utilisation_month():
        return random.choice(VEHICLE_UTILISATION_MONTHS)

    @staticmethod
    def vehicle_utilisation_products(count=2):
        return random.sample(
            VEHICLE_UTILISATION_PRODUCTS,
            k=min(count, len(VEHICLE_UTILISATION_PRODUCTS))
        )

    @staticmethod
    def service_overdue_month():
        return random.choice(SERVICE_OVERDUE_MONTHS)

    @staticmethod
    def service_overdue_products(count=1):
        return random.sample(
            SERVICE_OVERDUE_PRODUCTS,
            k=min(count, len(SERVICE_OVERDUE_PRODUCTS))
        )

    @staticmethod
    def vehicle_type_list(count=2):
        return random.sample(
            VEHICLE_TYPES,
            k=min(count, len(VEHICLE_TYPES))
        )

    @staticmethod
    def power_train_list(count=2):
        return random.sample(
            POWER_TRAINS,
            k=min(count, len(POWER_TRAINS))
        )

    @staticmethod
    def registration():
        return random.choice(REGISTRATIONS)

    @staticmethod
    def manage_user_search():
        return random.choice(MANAGE_USER_SEARCH_VALUES)

    @staticmethod
    def manage_user_filters(count=2):
        return random.sample(
            MANAGE_USER_FILTER_VALUES,
            k=min(count, len(MANAGE_USER_FILTER_VALUES))
        )
    
    @staticmethod
    def get_environment_user(csv_path="data/users.csv"):
        selected_env = get_selected_environment()

        matching_users = []

        with open(csv_path, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["environment"].strip().upper() == selected_env:
                    matching_users.append(row)

        if not matching_users:
            raise ValueError(
                f"No users found in {csv_path} for environment '{selected_env}'"
            )

        user = random.choice(matching_users)

        return [
            user["username"].strip(),
            user["password"].strip()
        ]