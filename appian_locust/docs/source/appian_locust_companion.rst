.. _appian_locust_companion:

###########################
Appian Locust Companion
###########################

Overview
_________________________________

The Appian Locust Companion (ALC) is a Google Chrome extension designed to simplify writing performance tests using the Appian Locust library. It reduces much of the manual effort in writing tests to simply point-and-click. ALC will capture your interactions and convert them into Appian Locust functions with the parameters. It provides an easy way to get started with Appian Locust based performance testing!

Getting Started
_________________________________

**1. Install the Extension** from the `Chrome Web Store <https://chromewebstore.google.com/detail/appian-locust-companion/ebgbeodgfnnkgcppfikfoclfmahcmapf?authuser=0&hl=en&pli=1>`_.

**2. Launch the Extension:** Navigate to the Appian interface where your testing flow begins, launch the ALC extension, grant requested permissions, refresh the Appian browser tab, and click Record Interactions.

**3. Generate Performance Test:** As you interact with Appian, the extension processes the requests and outputs Appian Locust function calls with relevant parameters.

Best Practices & Important Notes
_________________________________

**Component Configuration:** Appian Locust uses labels to identify which components to interact with. For better recognition during test recording add labels or test labels to the components of your Appian Application. Missing labels may result in functions printed with incomplete parameters.

**Permissions**: On the  first launch of the extension on a given domain, it will request permission to access requests made on your Appian site. Although ALC requests permission to read and modify data, the extension **only reads** data in its current implementation.

Extension Limitations
_________________________________
**Supported Interactions:** Only interactions already supported by the Appian Locust library are supported by this extension.

**Tab-Specific Behavior:** The Appian Locust Companion hooks into the site/domain that it is launched from. While it is not specifically tied to the tab it is launched from, it will not record interactions reliably in new tabs. Therefore, it is not recommended to switch tabs. To ensure smooth functioning, close the ALC window and relaunch it if you need to switch to a different domain or tab. 

**Parameter Recognition:** Some functions may appear without parameters if the extension lacks necessary information or if the components don’t have labels or test labels as mentioned above.

Support
_________________________________
Please don't hesitate to reach out to us via the Support Hub option in the Chrome Web Store if you have feedback or need assistance.
