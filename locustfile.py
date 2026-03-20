from locust import HttpUser, between

from utils.credential_pool import CredentialPool
from config.environment import get_environment_config

from journeys.alerts_journey import AlertsJourney
from journeys.export_journey import ExportJourney
from journeys.filter_journey import FilterJourney
from journeys.fleet_schedule_journey import FleetScheduleJourney
from journeys.home_journey import HomeJourney
from journeys.imminent_expiry_journey import ImminentExpiryJourney
from journeys.manage_user_journey import ManageUserJourney
from journeys.service_overdue_journey import ServiceOverdueJourney
from journeys.sustainability_journey import SustainabilityJourney
from journeys.update_profile_journey import UpdateProfileJourney
from journeys.vehicle_on_order_journey import VehicleOnOrderJourney
from journeys.vehicle_search_journey import VehicleSearchJourney
from journeys.vehicle_utilisation_journey import VehicleUtilisationJourney
from utils.waits import get_locust_wait_range

ENV_CONFIG = get_environment_config()


class OrionUser(HttpUser):

    host = ENV_CONFIG["host"]

    _wait_min, _wait_max = get_locust_wait_range()
    wait_time = between(_wait_min, _wait_max)

    # Weighted task mix — reflects realistic Orion APAC usage patterns.
    # Higher weight = more VUsers assigned to that journey proportionally.
    tasks = {
        FleetScheduleJourney: 4,
        VehicleOnOrderJourney: 4,
        AlertsJourney: 3,
        ImminentExpiryJourney: 4,
        VehicleUtilisationJourney: 4,
        ServiceOverdueJourney: 4,
        SustainabilityJourney: 3,
        FilterJourney: 1,
        VehicleSearchJourney: 2,
        ExportJourney: 0,
        UpdateProfileJourney: 0,
        ManageUserJourney: 0,
        HomeJourney: 1,
    }

    def on_start(self):
        self.auth = CredentialPool.acquire_user()

    def on_stop(self):
        CredentialPool.release_user(self.auth)