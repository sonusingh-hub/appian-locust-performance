from appian_locust import AppianTaskSet
from locust import HttpUser, task
from appian_locust.objects import AISkillObjectType


class AISkillTaskSet(AppianTaskSet):

    @task
    def create_new_AI_Skill(self):
        # Navigate to design & Create an App
        design_uiform = self.appian.visitor.visit_design()
        application_uiform = design_uiform.create_application("Example AI Skill App")
        # Click Build from left nav bar to view list of objects
        application_uiform = application_uiform.select_nav_card_by_index("leftNavbar", 1, True)

        # Create AI Skill Object
        ai_skill_name = "Example_AI_Skill"
        application_uiform.create_ai_skill_object(ai_skill_name=ai_skill_name, ai_skill_type=AISkillObjectType.DOCUMENT_CLASSIFICATION)

        # Visit Created AI Skill Object
        ai_skill_uiform = self.appian.visitor.visit_ai_skill_by_name(ai_skill_name)
        ai_skill_uiform.click_button("Create First Model")
        ai_skill_uiform.click_button("New Document Type")
        ai_skill_uiform.fill_text_field("Document Type Name", "Invoices")
        invoice_files = ["/path/Invoice 1.pdf", "/path/Invoice 2.pdf", "/path/Invoice 3.pdf", "/path/Invoice 4.pdf", "/path/Invoice 5.pdf",
                         "/path/Invoice 6.pdf", "/path/Invoice 7.pdf", "/path/Invoice 8.pdf", "/path/Invoice 9.pdf", "/path/Invoice 10.pdf"]
        ai_skill_uiform.upload_documents_to_multiple_file_upload_field(invoice_files)
        ai_skill_uiform.click_button("Create and Add Another")
        ai_skill_uiform.fill_text_field("Document Type Name", "PurchaseOrders")
        purchase_order_files = ["/path/PurchaseOrder 1.pdf", "/path/PurchaseOrder 2.pdf", "/path/PurchaseOrder 3.pdf", "/path/PurchaseOrder 4.pdf", "/path/PurchaseOrder 5.pdf",
                                "/path/PurchaseOrder 6.pdf", "/path/PurchaseOrder 7.pdf", "/path/PurchaseOrder 8.pdf", "/path/PurchaseOrder 9.pdf", "/path/PurchaseOrder 10.pdf"]
        ai_skill_uiform.upload_documents_to_multiple_file_upload_field(purchase_order_files)
        ai_skill_uiform.click_button("Create")
        ai_skill_uiform.save_ai_skill_changes()
        print("AI Skill Saved")
        ai_skill_uiform.click_button("Train Model")
        print("AI Skill Training Started")


class UserActor(HttpUser):
    tasks = [AISkillTaskSet]
    host = 'https://mysitename.net'
    auth = ["username", "password"]
