from locust import HttpUser, between

from utils.credential_pool import CredentialPool
from config.environment import get_environment_config

from journeys.fleet_schedule_journey import FleetScheduleJourney
from journeys.filter_journey import FilterJourney
from journeys.export_journey import ExportJourney
from journeys.vehicle_on_order_journey import VehicleOnOrderJourney
from journeys.imminent_expiry_journey import ImminentExpiryJourney
from journeys.sustainability_journey import SustainabilityJourney
from journeys.vehicle_utilisation_journey import VehicleUtilisationJourney
from journeys.service_overdue_journey import ServiceOverdueJourney
from journeys.update_profile_journey import UpdateProfileJourney
from journeys.alerts_journey import AlertsJourney
from journeys.home_vehicle_search_journey import HomeVehicleSearchJourney
from journeys.manage_user_journey import ManageUserJourney
from journeys.admin_configuration_journey import AdminConfigurationJourney

ENV_CONFIG = get_environment_config()


class OrionUser(HttpUser):

    host = ENV_CONFIG["host"]

    wait_time = between(2, 5)

    tasks = {
        AlertsJourney: 3,
        FilterJourney: 5,
        ExportJourney: 2,
        HomeVehicleSearchJourney: 1,
        FleetScheduleJourney: 8,
        VehicleOnOrderJourney: 4,
        ImminentExpiryJourney: 3,
        SustainabilityJourney: 2,
        VehicleUtilisationJourney: 3,
        ServiceOverdueJourney: 3,
        UpdateProfileJourney: 1,
        ManageUserJourney: 1,
        AdminConfigurationJourney: 1
    }

    # tasks = [AlertsJourney]

    def on_start(self):
        self.auth = CredentialPool.acquire_user()

    def on_stop(self):
        CredentialPool.release_user(self.auth)