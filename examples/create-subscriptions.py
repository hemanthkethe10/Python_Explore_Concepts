subscription = {
				"type": "AdvancedRouting",
				"id": "2c9f8ebf940274c601942086eecf2c50",
				"folder": "/Sub_0125",
				"account": "Accnt_0125",
				"application": "NYL-AdvancedRoute",
				"flowAttributes": {
					"userVars.createdBy": "Backflipt"
				}
}

import copy
import json

subscriptions = []
for i in range(1,2):
	subscription_copy = copy.deepcopy(subscription)
	subscription_copy["folder"] = f"/Folder{i}"
	subscriptions.append(subscription_copy)

print(json.dumps(subscriptions))

{"name":"name",}
