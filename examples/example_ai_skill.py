from appian_locust import AppianTaskSet
from locust import HttpUser, task
from appian_locust.objects import AISkillObjectType
import time


class AISkillTaskSet(AppianTaskSet):

    @task
    def create_new_AI_Skill(self):
        # Navigate to design
        application_uiform = self.appian.visitor.visit_application_by_name('Record Exemplar')

        # Create AI Skill Object"
        ai_skill_name = f"Example_AI_Skill_{time.time_ns()}"
        application_uiform.create_ai_skill_object(ai_skill_name=ai_skill_name, ai_skill_type = AISkillObjectType.DOCUMENT_CLASSIFICATION)


class UserActor(HttpUser):
    tasks = [AISkillTaskSet]
    host = 'https://mysitename.net'
    auth = ["myusername", "mypassword"]
