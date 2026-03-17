from locust import HttpUser, between

from utils.credential_pool import CredentialPool
from config.environment import get_environment_config

from journeys.home_journey import HomeJourney
from journeys.alerts_journey import AlertsJourney
from journeys.filter_journey import FilterJourney
from journeys.export_journey import ExportJourney
from journeys.fleet_schedule_journey import FleetScheduleJourney
from journeys.vehicle_on_order_journey import VehicleOnOrderJourney
from journeys.imminent_expiry_journey import ImminentExpiryJourney
from journeys.sustainability_journey import SustainabilityJourney
from journeys.vehicle_utilisation_journey import VehicleUtilisationJourney
from journeys.service_overdue_journey import ServiceOverdueJourney
from journeys.vehicle_search_journey import VehicleSearchJourney
from journeys.update_profile_journey import UpdateProfileJourney
from journeys.manage_user_journey import ManageUserJourney
from journeys.admin_configuration_journey import AdminConfigurationJourney

ENV_CONFIG = get_environment_config()

class OrionUser(HttpUser):

    host = ENV_CONFIG["host"]

    wait_time = between(2, 5)

    tasks = {
        HomeJourney: 2,
        AlertsJourney: 3,
        FilterJourney: 1,
        ExportJourney: 0,
        FleetScheduleJourney: 6,
        VehicleOnOrderJourney: 5,
        ImminentExpiryJourney: 4,
        SustainabilityJourney: 3,
        VehicleUtilisationJourney: 3,
        ServiceOverdueJourney: 3,
        VehicleSearchJourney: 2,
        UpdateProfileJourney: 1,
        ManageUserJourney: 1,
        AdminConfigurationJourney: 1
    }

    # tasks = [HomeJourney]

    def on_start(self):
        self.auth = CredentialPool.acquire_user()

    def on_stop(self):
        CredentialPool.release_user(self.auth)