data_models = [
    {
        "lockInfo": {},
        "shareWithAllApps": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "appsSharedWith": {
            "fullAccess": [],
            "readAccessOnly": []
        },
        "shareWithAllFlows": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "flowsSharedWith": {
            "fullAccess": [
                "67729a8bc29b51553c4973d7",
                "67729a3ec29b51553c4971c2"
            ],
            "readAccessOnly": []
        },
        "_id": "676d023ec29b51553c48806d",
        "updatedAt": "2025-05-01T10:59:52.765Z",
        "createdAt": "2024-12-26T07:14:06.950Z",
        "updatedBy": "hemanthkethe@backflipt.com",
        "createdBy": "hemanthkethe@backflipt.com",
        "locked": False,
        "createCallbackOperationId": "",
        "embedDataModelInfo": {},
        "primaryKey": "",
        "indices": [
            {
                "name": "createdAt_1",
                "key": {
                    "createdAt": 1
                }
            },
            {
                "name": "requestId_1",
                "key": {
                    "requestId": 1
                }
            },
            {
                "name": "partnerId_1",
                "key": {
                    "partnerId": 1
                }
            },
            {
                "name": "partnerName_1",
                "key": {
                    "partnerName": 1
                }
            }
        ],
        "dataSchema": {
            "requestId": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "partnerId": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "status": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "createdAt": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "createdBy": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "lastActivityTime": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "isClaimed": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "claimedBy": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "isAccountCreated": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "onBoardingContact": {
                "type": "Object",
                "searchable": True
            },
            "prodConnectionInfo": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "testConnectionInfo": {
                "type": "Object",
                "searchable": True
            },
            "submittedOn": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "partnerName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "createdByName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "clamiedByName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "snowInfo": {
                "type": "Object",
                "searchable": True
            },
            "eftrNumber": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "fileAttachment": {
                "type": "Object",
                "searchable": True
            },
            "testBusinessUnit": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            }
        },
        "tenantId": "backflipt.com",
        "appId": "6718c073cc4fca2655437982",
        "description": "",
        "name": "Onboarding Requests - G",
        "__v": 1,
        "containedByTreeList": []
    },
    {
        "lockInfo": {},
        "shareWithAllApps": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "appsSharedWith": {
            "fullAccess": [
                "659d4d89ba5910cf775d71f9",
                "683d56afaed74b904b019639"
            ],
            "readAccessOnly": []
        },
        "shareWithAllFlows": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "flowsSharedWith": {
            "fullAccess": [
                "64f845754d4dc1a0de4fed4e",
                "665f08b6b312e0962468740d",
                "6694f41c452663cbbc160f2f",
                "67123287cc4fca265542dd16",
                "671232accc4fca265542dee5",
                "66472c9f78be6c62e8444e89",
                "67729a3ec29b51553c4971c2",
                "67729a8bc29b51553c4973d7",
                "683ff87aaed74b904b16e768",
                "683ff89caed74b904b16e8af"
            ],
            "readAccessOnly": [
                "6570506d0bc42c570250d183"
            ]
        },
        "_id": "676d023ec29b51553c488066",
        "updatedAt": "2025-06-04T07:50:33.517Z",
        "createdAt": "2024-12-26T07:14:06.949Z",
        "updatedBy": "hemanthkethe@backflipt.com",
        "createdBy": "hemanthkethe@backflipt.com",
        "locked": False,
        "createCallbackOperationId": "",
        "embedDataModelInfo": {},
        "primaryKey": "",
        "indices": [],
        "dataSchema": {
            "authMethod": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "email": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "password": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "server": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "port": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "oauth2": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "scope": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            }
        },
        "tenantId": "backflipt.com",
        "appId": "6718c073cc4fca2655437982",
        "description": "",
        "name": "Email Settings - G",
        "__v": 1,
        "containedByTreeList": []
    },
    {
        "lockInfo": {},
        "shareWithAllApps": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "appsSharedWith": {
            "fullAccess": [],
            "readAccessOnly": [
                "683d56afaed74b904b019639"
            ]
        },
        "shareWithAllFlows": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "flowsSharedWith": {
            "fullAccess": [],
            "readAccessOnly": []
        },
        "_id": "676d023ec29b51553c48806a",
        "updatedAt": "2025-06-03T12:08:51.186Z",
        "createdAt": "2024-12-26T07:14:06.950Z",
        "updatedBy": "hemanthkethe@backflipt.com",
        "createdBy": "hemanthkethe@backflipt.com",
        "locked": False,
        "createCallbackOperationId": "",
        "embedDataModelInfo": {},
        "primaryKey": "",
        "indices": [],
        "dataSchema": {
            "entityId": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "signinPageUrl": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "signoutPageUrl": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "idpCertificate": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "enabled": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "decryptKey": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "logoutPublicCertificate": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "scope": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            }
        },
        "tenantId": "backflipt.com",
        "appId": "6718c073cc4fca2655437982",
        "description": "",
        "name": "SSO Settings - G",
        "__v": 1,
        "containedByTreeList": []
    },
    {
        "lockInfo": {},
        "shareWithAllApps": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "appsSharedWith": {
            "fullAccess": [],
            "readAccessOnly": [
                "683d56afaed74b904b019639"
            ]
        },
        "shareWithAllFlows": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "flowsSharedWith": {
            "fullAccess": [
                "6728c029cc4fca26554505ee",
                "6728c043cc4fca2655450689"
            ],
            "readAccessOnly": [
                "665f08b6b312e0962468740d",
                "6694f41c452663cbbc160f2f",
                "67123287cc4fca265542dd16",
                "671232accc4fca265542dee5",
                "66472c9f78be6c62e8444e89",
                "683ff87aaed74b904b16e768",
                "683ff89caed74b904b16e8af",
                "67729a8bc29b51553c4973d7",
                "67729a3ec29b51553c4971c2"
            ]
        },
        "_id": "676d023ec29b51553c488067",
        "updatedAt": "2025-08-05T10:59:36.141Z",
        "createdAt": "2024-12-26T07:14:06.950Z",
        "updatedBy": "hemanthkethe@backflipt.com",
        "createdBy": "hemanthkethe@backflipt.com",
        "locked": False,
        "createCallbackOperationId": "",
        "embedDataModelInfo": {},
        "primaryKey": "",
        "indices": [
            {
                "name": "partnerId_1",
                "key": {
                    "partnerId": 1
                }
            },
            {
                "name": "partnerName_1",
                "key": {
                    "partnerName": 1
                }
            },
            {
                "name": "createdBy_1",
                "key": {
                    "createdBy": 1
                }
            }
        ],
        "dataSchema": {
            "partnerId": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "partnerName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "website": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "description": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "contacts": {
                "type": "Array",
                "searchable": True
            },
            "createdAt": {
                "type": "Number",
                "searchable": False
            },
            "createdBy": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "accounts": {
                "type": "Array",
                "searchable": False
            },
            "isDeleted": {
                "type": "Boolean"
            },
            "clients": {
                "type": "Array",
                "searchable": False
            },
            "externalAccounts": {
                "type": "Array",
                "searchable": False
            },
            "name": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            }
        },
        "tenantId": "backflipt.com",
        "appId": "6718c073cc4fca2655437982",
        "description": "Stores the data of partner profiles section",
        "name": "Partner Profiles - G",
        "__v": 1,
        "containedByTreeList": []
    },
    {
        "lockInfo": {},
        "shareWithAllApps": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "appsSharedWith": {
            "fullAccess": [],
            "readAccessOnly": []
        },
        "shareWithAllFlows": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "flowsSharedWith": {
            "fullAccess": [
                "67729a3ec29b51553c4971c2",
                "67729a8bc29b51553c4973d7"
            ],
            "readAccessOnly": []
        },
        "containedByTreeList": [],
        "_id": "676d023ec29b51553c488068",
        "updatedAt": "2025-05-01T10:59:52.767Z",
        "createdAt": "2024-12-26T07:14:06.950Z",
        "updatedBy": "hemanthkethe@backflipt.com",
        "createdBy": "hemanthkethe@backflipt.com",
        "locked": False,
        "createCallbackOperationId": "",
        "embedDataModelInfo": {},
        "primaryKey": "",
        "indices": [],
        "dataSchema": {
            "0": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "1": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "2": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "3": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "4": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            }
        },
        "tenantId": "backflipt.com",
        "appId": "6718c073cc4fca2655437982",
        "description": "",
        "name": "Status Change Log - G"
    },
    {
        "lockInfo": {
            "userEmail": "hemanthkethe@backflipt.com",
            "lockedAt": "2025-09-04T06:03:04.919Z"
        },
        "shareWithAllApps": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "appsSharedWith": {
            "fullAccess": [
                "66853bc7452663cbbc1301f3",
                "65c5a95ff50d5937f338816d",
                "659d4d89ba5910cf775d71f9",
                "67f60dc4dd5c0eeb5d3fb7e0",
                "67f6215fdd5c0eeb5d402933",
                "67f6115edd5c0eeb5d3fd453",
                "67f668a2dd5c0eeb5d412dcb",
                "67f8f65add5c0eeb5d46a88b",
                "67f90ad9dd5c0eeb5d46f68c",
                "67fcc618dd5c0eeb5d4f89dd",
                "67fe448ddd5c0eeb5d52f525",
                "67ff86f8dd5c0eeb5d55a567",
                "6805d5a1dd5c0eeb5d61d19e",
                "6808db9557e8dc6fd4616c3a",
                "6809dfe557e8dc6fd461e376",
                "6809e82357e8dc6fd461fc84",
                "680b4d7457e8dc6fd462d7aa",
                "680b862157e8dc6fd46349f1",
                "680f239c57e8dc6fd463b124",
                "680f5c2357e8dc6fd4640396",
                "6810c10b57e8dc6fd46501a9",
                "6813312e57e8dc6fd466fe86",
                "681347bf57e8dc6fd4673778",
                "6818496257e8dc6fd4719bb4",
                "68219544aed74b904b574e39",
                "6821c52caed74b904b57c5ff",
                "6822f0b5aed74b904b58a20d",
                "6822ea23aed74b904b58838e",
                "6824485faed74b904b59f369",
                "682d9777aed74b904b81b4b2",
                "68370139aed74b904bcb7329",
                "68380964aed74b904bd59e57",
                "683ed8e8aed74b904b0db24a",
                "683eda56aed74b904b0dd1f9",
                "683d56afaed74b904b019639",
                "68481540aed74b904b6cda8d",
                "68525a004ed8b092f0a765c7",
                "68525b954ed8b092f0a77b44",
                "685cf03ab143f880b34fc5cc",
                "6864e0a3f6c7bc931273b0fe",
                "686b65d473ad4b3cf43998d2",
                "686b6c4173ad4b3cf439b041",
                "686f5b9f41e49727ae144d53",
                "6870df7d21b403cea5b423dd",
                "68836ba03f2ab0989bda541f",
                "6886295c3f2ab0989bda8342",
                "6894735c3f2ab0989bdc5492",
                "68998570d44e0e9673f97b2d",
                "68b92a926ee7964437379144"
            ],
            "readAccessOnly": []
        },
        "shareWithAllFlows": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "flowsSharedWith": {
            "fullAccess": [
                "64f845504d4dc1a0de4fecd3",
                "67729a8bc29b51553c4973d7",
                "6728c029cc4fca26554505ee",
                "6728c043cc4fca2655450689"
            ],
            "readAccessOnly": []
        },
        "_id": "676d023ec29b51553c48806e",
        "updatedAt": "2025-09-04T06:03:18.125Z",
        "createdAt": "2024-12-26T07:14:06.950Z",
        "updatedBy": "hemanthkethe@backflipt.com",
        "createdBy": "hemanthkethe@backflipt.com",
        "locked": True,
        "createCallbackOperationId": "",
        "embedDataModelInfo": {},
        "primaryKey": "",
        "indices": [
            {
                "name": "lastLoginTime_-1",
                "key": {
                    "lastLoginTime": -1
                }
            },
            {
                "name": "firstName_1_lastName_1_email_1",
                "key": {
                    "firstName": 1,
                    "lastName": 1,
                    "email": 1
                }
            }
        ],
        "dataSchema": {
            "firstName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "lastName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "email": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "phone": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "role": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "password": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "createdAt": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "lastLoginAt": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "fullName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "status": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "createdBy": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "userId": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "isDeleted": {
                "type": "Boolean"
            },
            "isRegistered": {
                "type": "Boolean"
            },
            "testBusinessUnit": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "accountDetails": {
                "type": "Object",
                "searchable": False
            },
            "accountInfo": {
                "type": "Object",
                "searchable": True
            },
            "prodBusinessUnit": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "isSnowUser": {
                "type": "Boolean"
            },
            "resetPasswordToken": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            }
        },
        "tenantId": "backflipt.com",
        "appId": "6718c073cc4fca2655437982",
        "description": "",
        "name": "Users -SFR - G",
        "__v": 1,
        "containedByTreeList": []
    },
    {
        "lockInfo": {},
        "shareWithAllApps": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "appsSharedWith": {
            "fullAccess": [],
            "readAccessOnly": []
        },
        "shareWithAllFlows": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "flowsSharedWith": {
            "fullAccess": [],
            "readAccessOnly": []
        },
        "containedByTreeList": [],
        "_id": "676d023ec29b51553c48806c",
        "updatedAt": "2025-05-01T10:59:52.776Z",
        "createdAt": "2024-12-26T07:14:06.950Z",
        "updatedBy": "hemanthkethe@backflipt.com",
        "createdBy": "hemanthkethe@backflipt.com",
        "locked": False,
        "createCallbackOperationId": "",
        "embedDataModelInfo": {},
        "primaryKey": "",
        "indices": [],
        "dataSchema": {
            "comment": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "commentedAt": {
                "type": "Number",
                "searchable": False
            },
            "commentedBy": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "isInternal": {
                "type": "Boolean"
            }
        },
        "tenantId": "backflipt.com",
        "appId": "6718c073cc4fca2655437982",
        "description": "",
        "name": "Comments - G"
    },
    {
        "lockInfo": {},
        "shareWithAllApps": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "appsSharedWith": {
            "fullAccess": [],
            "readAccessOnly": [
                "66853bc7452663cbbc1301f3",
                "683d56afaed74b904b019639"
            ]
        },
        "shareWithAllFlows": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "flowsSharedWith": {
            "fullAccess": [
                "64f845754d4dc1a0de4fed4e",
                "66d2ddab74f3f02f3c333886",
                "66d3342e74f3f02f3c335f6d",
                "6728bfabcc4fca2655450447",
                "6728bfe7cc4fca2655450553",
                "6728c029cc4fca26554505ee",
                "6728c043cc4fca2655450689"
            ],
            "readAccessOnly": [
                "665f08b6b312e0962468740d",
                "6694f41c452663cbbc160f2f",
                "67123287cc4fca265542dd16",
                "671232accc4fca265542dee5",
                "66472c9f78be6c62e8444e89",
                "683ff87aaed74b904b16e768",
                "683ff89caed74b904b16e8af"
            ]
        },
        "_id": "676d023ec29b51553c48806b",
        "updatedAt": "2025-06-04T07:51:29.437Z",
        "createdAt": "2024-12-26T07:14:06.950Z",
        "updatedBy": "hemanthkethe@backflipt.com",
        "createdBy": "hemanthkethe@backflipt.com",
        "locked": False,
        "createCallbackOperationId": "",
        "embedDataModelInfo": {},
        "primaryKey": "",
        "indices": [],
        "dataSchema": {
            "serviceName": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "userName": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "password": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "baseUri": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "scope": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            }
        },
        "tenantId": "backflipt.com",
        "appId": "6718c073cc4fca2655437982",
        "description": "",
        "name": "Service Settings - G",
        "__v": 1,
        "containedByTreeList": []
    },
    {
        "lockInfo": {},
        "shareWithAllApps": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "appsSharedWith": {
            "fullAccess": [],
            "readAccessOnly": [
                "662a3e14c3427af2df2b3642",
                "659d4d89ba5910cf775d71f9"
            ]
        },
        "shareWithAllFlows": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "flowsSharedWith": {
            "fullAccess": [
                "67729a3ec29b51553c4971c2",
                "67729a8bc29b51553c4973d7"
            ],
            "readAccessOnly": []
        },
        "containedByTreeList": [],
        "_id": "676d023ec29b51553c48806f",
        "updatedAt": "2025-05-01T10:59:52.769Z",
        "createdAt": "2024-12-26T07:14:06.950Z",
        "updatedBy": "hemanthkethe@backflipt.com",
        "createdBy": "hemanthkethe@backflipt.com",
        "locked": False,
        "createCallbackOperationId": "",
        "embedDataModelInfo": {},
        "primaryKey": "",
        "indices": [],
        "dataSchema": {
            "name": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "uniqueTemplateName": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "updatedAt": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "updatedBy": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "teamplateContent": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            }
        },
        "tenantId": "backflipt.com",
        "appId": "6718c073cc4fca2655437982",
        "description": "",
        "name": "Email Templates - G"
    },
    {
        "lockInfo": {},
        "shareWithAllApps": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "appsSharedWith": {
            "fullAccess": [
                "66853bc7452663cbbc1301f3"
            ],
            "readAccessOnly": [
                "683d56afaed74b904b019639"
            ]
        },
        "shareWithAllFlows": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "flowsSharedWith": {
            "fullAccess": [
                "64f845754d4dc1a0de4fed4e",
                "6728c029cc4fca26554505ee",
                "6728c043cc4fca2655450689"
            ],
            "readAccessOnly": []
        },
        "_id": "676d023ec29b51553c488069",
        "updatedAt": "2025-06-03T12:11:31.472Z",
        "createdAt": "2024-12-26T07:14:06.950Z",
        "updatedBy": "hemanthkethe@backflipt.com",
        "createdBy": "hemanthkethe@backflipt.com",
        "locked": False,
        "createCallbackOperationId": "",
        "embedDataModelInfo": {},
        "primaryKey": "",
        "indices": [],
        "dataSchema": {
            "scope": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "testLoginKey": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "prodLoginKey": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "testpgpEncryptionKey": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "prodpgpEncryptionKey": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "uid": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "gid": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "homePath": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "accountName": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "additionalSettings": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            }
        },
        "tenantId": "backflipt.com",
        "appId": "6718c073cc4fca2655437982",
        "description": "",
        "name": "ST Settings - G",
        "__v": 1,
        "containedByTreeList": []
    },
    {
        "lockInfo": {},
        "shareWithAllApps": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "appsSharedWith": {
            "fullAccess": [],
            "readAccessOnly": []
        },
        "shareWithAllFlows": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "flowsSharedWith": {
            "fullAccess": [],
            "readAccessOnly": []
        },
        "containedByTreeList": [],
        "_id": "676d023ec29b51553c488070",
        "updatedAt": "2025-05-01T10:59:52.770Z",
        "createdAt": "2024-12-26T07:14:06.950Z",
        "updatedBy": "hemanthkethe@backflipt.com",
        "createdBy": "hemanthkethe@backflipt.com",
        "locked": False,
        "createCallbackOperationId": "",
        "embedDataModelInfo": {},
        "primaryKey": "",
        "indices": [],
        "dataSchema": {
            "fileName": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "fileId": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "contentType": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "uploadedAt": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "uploadedBy": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            }
        },
        "tenantId": "backflipt.com",
        "appId": "6718c073cc4fca2655437982",
        "description": "",
        "name": "Files - G"
    },
    {
        "lockInfo": {},
        "shareWithAllApps": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "appsSharedWith": {
            "fullAccess": [],
            "readAccessOnly": [
                "683d56afaed74b904b019639"
            ]
        },
        "shareWithAllFlows": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "flowsSharedWith": {
            "fullAccess": [
                "6728c043cc4fca2655450689",
                "6728c029cc4fca26554505ee",
                "67729a3ec29b51553c4971c2"
            ],
            "readAccessOnly": [
                "683ff87aaed74b904b16e768",
                "683ff89caed74b904b16e8af"
            ]
        },
        "_id": "676d023ec29b51553c488071",
        "updatedAt": "2025-06-04T07:49:19.933Z",
        "createdAt": "2024-12-26T07:14:06.950Z",
        "updatedBy": "hemanthkethe@backflipt.com",
        "createdBy": "hemanthkethe@backflipt.com",
        "locked": False,
        "createCallbackOperationId": "",
        "embedDataModelInfo": {},
        "primaryKey": "",
        "indices": [],
        "dataSchema": {
            "requestId": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "requestDate": {
                "type": "Number",
                "searchable": False
            },
            "accountName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "instance": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "createdAt": {
                "type": "Number",
                "searchable": False
            },
            "createdBy": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "partnerId": {
                "type": "Number",
                "searchable": True
            },
            "status": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "accountUserName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "accountEmail": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "accountId": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "businessUnit": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "requestedBy": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "userLoginName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "requestedByName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "createdByName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            }
        },
        "tenantId": "backflipt.com",
        "appId": "6718c073cc4fca2655437982",
        "description": "",
        "name": "ST Accounts - G",
        "__v": 1,
        "containedByTreeList": []
    },
    {
        "lockInfo": {},
        "shareWithAllApps": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "appsSharedWith": {
            "fullAccess": [],
            "readAccessOnly": []
        },
        "shareWithAllFlows": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "flowsSharedWith": {
            "fullAccess": [],
            "readAccessOnly": []
        },
        "containedByTreeList": [],
        "_id": "676d023ec29b51553c488072",
        "updatedAt": "2025-05-01T10:59:52.773Z",
        "createdAt": "2024-12-26T07:14:06.950Z",
        "updatedBy": "hemanthkethe@backflipt.com",
        "createdBy": "hemanthkethe@backflipt.com",
        "locked": False,
        "createCallbackOperationId": "",
        "embedDataModelInfo": {},
        "primaryKey": "",
        "indices": [],
        "dataSchema": {
            "scope": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "enabled": {
                "type": "Boolean"
            },
            "ITSMName": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "SNow": {
                "type": "Object",
                "searchable": False
            }
        },
        "tenantId": "backflipt.com",
        "appId": "6718c073cc4fca2655437982",
        "description": "",
        "name": "ITSM Settings - G"
    },
    {
        "lockInfo": {},
        "shareWithAllApps": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "appsSharedWith": {
            "fullAccess": [],
            "readAccessOnly": [
                "655a5f3ae875242ab346df81"
            ]
        },
        "shareWithAllFlows": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "flowsSharedWith": {
            "fullAccess": [
                "67729a3ec29b51553c4971c2",
                "67729a8bc29b51553c4973d7"
            ],
            "readAccessOnly": []
        },
        "containedByTreeList": [],
        "_id": "676d023ec29b51553c488073",
        "updatedAt": "2025-05-01T10:59:52.774Z",
        "createdAt": "2024-12-26T07:14:06.950Z",
        "updatedBy": "hemanthkethe@backflipt.com",
        "createdBy": "hemanthkethe@backflipt.com",
        "locked": False,
        "createCallbackOperationId": "",
        "embedDataModelInfo": {},
        "primaryKey": "",
        "indices": [],
        "dataSchema": {
            "requestId": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "createdAt": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "submittedOn": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "modifiedOn": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "type": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "instanceType": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "direction": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "partnerId": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "partnerName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "source": {
                "type": "Object",
                "searchable": True
            },
            "sourceDetails": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "partnerAccount": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "fileNamingPattern": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "routes": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "routeId": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "status": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "currentRoutes": {
                "type": "Array",
                "searchable": True
            },
            "requestType": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "createdByName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "claimedByName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "partner": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "externalOwner": {
                "type": "Object",
                "searchable": True
            },
            "existingFileID": {
                "type": "Object",
                "searchable": True
            },
            "account": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "clientName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "fileId": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "idValue": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "createdBy": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "snowInfo": {
                "type": "Object",
                "searchable": True
            }
        },
        "tenantId": "backflipt.com",
        "appId": "6718c073cc4fca2655437982",
        "description": "",
        "name": "Routing Requests - G"
    },
    {
        "lockInfo": {},
        "shareWithAllApps": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "appsSharedWith": {
            "fullAccess": [],
            "readAccessOnly": []
        },
        "shareWithAllFlows": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "flowsSharedWith": {
            "fullAccess": [
                "6728c029cc4fca26554505ee",
                "6728c043cc4fca2655450689"
            ],
            "readAccessOnly": []
        },
        "containedByTreeList": [],
        "_id": "676d023ec29b51553c488074",
        "updatedAt": "2025-05-01T10:59:52.777Z",
        "createdAt": "2024-12-26T07:14:06.950Z",
        "updatedBy": "hemanthkethe@backflipt.com",
        "createdBy": "hemanthkethe@backflipt.com",
        "locked": False,
        "createCallbackOperationId": "",
        "embedDataModelInfo": {},
        "primaryKey": "",
        "indices": [],
        "dataSchema": {
            "routeId": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "routeName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "direction": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "status": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "createdBy": {
                "type": "Number",
                "searchable": True
            },
            "createdAt": {
                "type": "Number",
                "searchable": False
            },
            "clientName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "routeVersions": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "partnerName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "partnerId": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "referenceId": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "partnerAccount": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "instanceType": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "subscriptionFolderId": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "notes": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "claimedBy": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "submittedOn": {
                "type": "Number",
                "searchable": False
            },
            "lastActivityTime": {
                "type": "Number",
                "searchable": False
            },
            "createdByName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "fileDetails": {
                "type": "Object",
                "searchable": True
            },
            "stRouteId": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "isDeleted": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "destinationType": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "subscriptionFolder": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "fileNamingPattern": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            }
        },
        "tenantId": "backflipt.com",
        "appId": "6718c073cc4fca2655437982",
        "description": "",
        "name": "Routes - G"
    },
    {
        "lockInfo": {},
        "shareWithAllApps": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "appsSharedWith": {
            "fullAccess": [
                "659d4d89ba5910cf775d71f9",
                "683d56afaed74b904b019639"
            ],
            "readAccessOnly": []
        },
        "shareWithAllFlows": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "flowsSharedWith": {
            "fullAccess": [
                "665f08b6b312e0962468740d",
                "6694f41c452663cbbc160f2f",
                "67123287cc4fca265542dd16",
                "671232accc4fca265542dee5",
                "66472c9f78be6c62e8444e89",
                "67729a3ec29b51553c4971c2",
                "67729a8bc29b51553c4973d7",
                "683ff87aaed74b904b16e768",
                "683ff89caed74b904b16e8af"
            ],
            "readAccessOnly": []
        },
        "_id": "676d023ec29b51553c488075",
        "updatedAt": "2025-06-04T07:48:37.914Z",
        "createdAt": "2024-12-26T07:14:06.950Z",
        "updatedBy": "hemanthkethe@backflipt.com",
        "createdBy": "hemanthkethe@backflipt.com",
        "locked": False,
        "createCallbackOperationId": "",
        "embedDataModelInfo": {},
        "primaryKey": "",
        "indices": [],
        "dataSchema": {
            "userEmailId": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "accessToken": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "refreshToken": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "expiresOn": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            }
        },
        "tenantId": "backflipt.com",
        "appId": "6718c073cc4fca2655437982",
        "description": "",
        "name": "Outbound Email Token - G",
        "__v": 1,
        "containedByTreeList": []
    },
    {
        "lockInfo": {},
        "shareWithAllApps": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "appsSharedWith": {
            "fullAccess": [
                "683d56afaed74b904b019639"
            ],
            "readAccessOnly": []
        },
        "shareWithAllFlows": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "flowsSharedWith": {
            "fullAccess": [
                "6728c029cc4fca26554505ee",
                "6728c043cc4fca2655450689"
            ],
            "readAccessOnly": []
        },
        "_id": "676d023ec29b51553c488076",
        "updatedAt": "2025-06-03T12:06:18.101Z",
        "createdAt": "2024-12-26T07:14:06.950Z",
        "updatedBy": "hemanthkethe@backflipt.com",
        "createdBy": "hemanthkethe@backflipt.com",
        "locked": False,
        "createCallbackOperationId": "",
        "embedDataModelInfo": {},
        "primaryKey": "",
        "indices": [],
        "dataSchema": {
            "status": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "createdAt": {
                "type": "Number",
                "searchable": False
            },
            "createdBy": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "instance": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "name": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "baseFolder": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "sNowCostCenter": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "ownerName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "ownerEmail": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "secondaryOwnerName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "secondaryOwnerEmail": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "buAccountName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "createdByName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "businessUnitId": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            }
        },
        "tenantId": "backflipt.com",
        "appId": "6718c073cc4fca2655437982",
        "description": "",
        "name": "Business Units - G",
        "__v": 1,
        "containedByTreeList": []
    },
    {
        "lockInfo": {
            "userEmail": "viswanaths@backflipt.com",
            "lockedAt": "2025-08-04T06:46:34.100Z"
        },
        "shareWithAllApps": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "appsSharedWith": {
            "fullAccess": [],
            "readAccessOnly": [
                "683d56afaed74b904b019639"
            ]
        },
        "shareWithAllFlows": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "flowsSharedWith": {
            "fullAccess": [
                "6728c029cc4fca26554505ee",
                "6728c043cc4fca2655450689"
            ],
            "readAccessOnly": [
                "665f08b6b312e0962468740d",
                "6694f41c452663cbbc160f2f",
                "67123287cc4fca265542dd16",
                "671232accc4fca265542dee5",
                "66472c9f78be6c62e8444e89",
                "683ff89caed74b904b16e8af",
                "683ff87aaed74b904b16e768",
                "67729a3ec29b51553c4971c2",
                "67729a8bc29b51553c4973d7"
            ]
        },
        "_id": "676d023ec29b51553c488077",
        "updatedAt": "2025-08-04T06:46:56.917Z",
        "createdAt": "2024-12-26T07:14:06.950Z",
        "updatedBy": "hemanthkethe@backflipt.com",
        "createdBy": "hemanthkethe@backflipt.com",
        "locked": True,
        "createCallbackOperationId": "",
        "embedDataModelInfo": {},
        "primaryKey": "",
        "indices": [],
        "dataSchema": {
            "clientId": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "clientName": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "createdAt": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "partnerId": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            }
        },
        "tenantId": "backflipt.com",
        "appId": "6718c073cc4fca2655437982",
        "description": "",
        "name": "ST Clients - G",
        "__v": 1,
        "containedByTreeList": []
    },
    {
        "lockInfo": {},
        "shareWithAllApps": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "appsSharedWith": {
            "fullAccess": [],
            "readAccessOnly": []
        },
        "shareWithAllFlows": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "flowsSharedWith": {
            "fullAccess": [
                "6728c029cc4fca26554505ee",
                "6728c043cc4fca2655450689"
            ],
            "readAccessOnly": []
        },
        "containedByTreeList": [],
        "_id": "676d023ec29b51553c488078",
        "updatedAt": "2025-05-01T10:59:52.782Z",
        "createdAt": "2024-12-26T07:14:06.950Z",
        "updatedBy": "hemanthkethe@backflipt.com",
        "createdBy": "hemanthkethe@backflipt.com",
        "locked": False,
        "createCallbackOperationId": "",
        "embedDataModelInfo": {},
        "primaryKey": "",
        "indices": [],
        "dataSchema": {
            "accessLevel": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "bu": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "siteName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "protocol": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "server": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "port": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "networkZone": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "transferMode": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "userName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "loginType": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "loginValue": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "siteContact": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "attributes": {
                "type": "Array",
                "searchable": True
            },
            "createdByName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "status": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "account": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "createdBy": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "internalSiteId": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "fileDetails": {
                "type": "Object",
                "searchable": True
            }
        },
        "tenantId": "backflipt.com",
        "appId": "6718c073cc4fca2655437982",
        "description": "",
        "name": "Internal Sites - G"
    },
    {
        "lockInfo": {},
        "shareWithAllApps": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "appsSharedWith": {
            "fullAccess": [],
            "readAccessOnly": [
                "683d56afaed74b904b019639"
            ]
        },
        "shareWithAllFlows": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "flowsSharedWith": {
            "fullAccess": [],
            "readAccessOnly": [
                "665f08b6b312e0962468740d",
                "6694f41c452663cbbc160f2f",
                "67123287cc4fca265542dd16",
                "671232accc4fca265542dee5",
                "66472c9f78be6c62e8444e89",
                "683ff87aaed74b904b16e768",
                "683ff89caed74b904b16e8af"
            ]
        },
        "_id": "676d023ec29b51553c488079",
        "updatedAt": "2025-06-04T07:47:59.484Z",
        "createdAt": "2024-12-26T07:14:06.950Z",
        "updatedBy": "hemanthkethe@backflipt.com",
        "createdBy": "hemanthkethe@backflipt.com",
        "locked": False,
        "createCallbackOperationId": "",
        "embedDataModelInfo": {},
        "primaryKey": "",
        "indices": [],
        "dataSchema": {
            "fileId": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "type": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "idValue": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "partnerId": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "clientName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "environment": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "website": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "description": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "account": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "division": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "dataSensitivity": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "createdAt": {
                "type": "Number",
                "searchable": False
            },
            "createdBy": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "isDeleted": {
                "type": "Boolean"
            },
            "partnerName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "lastActivityTime": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "fileDetails": {
                "type": "Array",
                "searchable": True
            }
        },
        "tenantId": "backflipt.com",
        "appId": "6718c073cc4fca2655437982",
        "description": "",
        "name": "File ID - G",
        "__v": 1,
        "containedByTreeList": []
    },
    {
        "lockInfo": {},
        "shareWithAllApps": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "appsSharedWith": {
            "fullAccess": [],
            "readAccessOnly": []
        },
        "shareWithAllFlows": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "flowsSharedWith": {
            "fullAccess": [
                "6728c029cc4fca26554505ee",
                "6728c043cc4fca2655450689"
            ],
            "readAccessOnly": []
        },
        "containedByTreeList": [],
        "_id": "676d023ec29b51553c48807a",
        "updatedAt": "2025-05-01T10:59:52.787Z",
        "createdAt": "2024-12-26T07:14:06.950Z",
        "updatedBy": "hemanthkethe@backflipt.com",
        "createdBy": "hemanthkethe@backflipt.com",
        "locked": False,
        "createCallbackOperationId": "",
        "embedDataModelInfo": {},
        "primaryKey": "",
        "indices": [],
        "dataSchema": {
            "lastRunAt": {
                "type": "Number",
                "searchable": False
            },
            "lastScheduledRunAt": {
                "type": "Number",
                "searchable": False
            },
            "scheduleInfo": {
                "type": "Object",
                "searchable": False
            },
            "lastManualRunAt": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "isFirstRunCompleted": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "emailDistributionList": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "isSyncSuccess": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "syncType": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "triggeredBy": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "currentRunStartedAt": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "excelMapping": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            }
        },
        "tenantId": "backflipt.com",
        "appId": "6718c073cc4fca2655437982",
        "description": "",
        "name": "Sync Settings - G"
    },
    {
        "lockInfo": {},
        "shareWithAllApps": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "appsSharedWith": {
            "fullAccess": [],
            "readAccessOnly": []
        },
        "shareWithAllFlows": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "flowsSharedWith": {
            "fullAccess": [
                "6728c029cc4fca26554505ee",
                "6728c043cc4fca2655450689"
            ],
            "readAccessOnly": []
        },
        "containedByTreeList": [],
        "_id": "676d023ec29b51553c48807b",
        "updatedAt": "2025-05-01T10:59:52.789Z",
        "createdAt": "2024-12-26T07:14:06.950Z",
        "updatedBy": "hemanthkethe@backflipt.com",
        "createdBy": "hemanthkethe@backflipt.com",
        "locked": False,
        "createCallbackOperationId": "",
        "embedDataModelInfo": {},
        "primaryKey": "",
        "indices": [],
        "dataSchema": {
            "type": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "aPIStatusCode": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "status": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "message": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "name": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            }
        },
        "tenantId": "backflipt.com",
        "appId": "6718c073cc4fca2655437982",
        "description": "",
        "name": "Sync Status Report - G"
    },
    {
        "lockInfo": {},
        "shareWithAllApps": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "appsSharedWith": {
            "fullAccess": [],
            "readAccessOnly": []
        },
        "shareWithAllFlows": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "flowsSharedWith": {
            "fullAccess": [
                "6728c029cc4fca26554505ee",
                "6728c043cc4fca2655450689"
            ],
            "readAccessOnly": []
        },
        "containedByTreeList": [],
        "_id": "676d023ec29b51553c48807c",
        "updatedAt": "2025-05-01T10:59:52.790Z",
        "createdAt": "2024-12-26T07:14:06.950Z",
        "updatedBy": "hemanthkethe@backflipt.com",
        "createdBy": "hemanthkethe@backflipt.com",
        "locked": False,
        "createCallbackOperationId": "",
        "embedDataModelInfo": {},
        "primaryKey": "",
        "indices": [],
        "dataSchema": {
            "id": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "name": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "description": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "type": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "managedByCG": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "routeTemplate": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "account": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "condition": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "conditionType": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "failureEmailNotification": {
                "type": "Boolean"
            },
            "failureEmailTemplate": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "failureEmailName": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "successEmailNotification": {
                "type": "Boolean"
            },
            "successEmailTemplate": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "successEmailName": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "triggeringEmailNotification": {
                "type": "Boolean"
            },
            "triggeringEmailName": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "triggeringEmailTemplate": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "steps": {
                "type": "Array",
                "searchable": False
            },
            "stepStatuses": {
                "type": "Array",
                "searchable": False
            },
            "businessUnits": {
                "type": "Array",
                "searchable": False
            },
            "subscriptions": {
                "type": "Array",
                "searchable": False
            },
            "additionalAttributes": {
                "type": "Object",
                "searchable": False
            },
            "metadata": {
                "type": "Object",
                "searchable": False
            }
        },
        "tenantId": "backflipt.com",
        "appId": "6718c073cc4fca2655437982",
        "description": "",
        "name": "Template Routes - G"
    },
    {
        "lockInfo": {},
        "shareWithAllApps": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "appsSharedWith": {
            "fullAccess": [],
            "readAccessOnly": []
        },
        "shareWithAllFlows": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "flowsSharedWith": {
            "fullAccess": [
                "6728c029cc4fca26554505ee",
                "6728c043cc4fca2655450689"
            ],
            "readAccessOnly": []
        },
        "containedByTreeList": [],
        "_id": "676d023ec29b51553c48807d",
        "updatedAt": "2025-05-01T10:59:52.791Z",
        "createdAt": "2024-12-26T07:14:06.950Z",
        "updatedBy": "hemanthkethe@backflipt.com",
        "createdBy": "hemanthkethe@backflipt.com",
        "locked": False,
        "createCallbackOperationId": "",
        "embedDataModelInfo": {},
        "primaryKey": "",
        "indices": [],
        "dataSchema": {
            "id": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "name": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "description": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "type": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "managedByCG": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "routeTemplate": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "account": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "condition": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "conditionType": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "failureEmailNotification": {
                "type": "Boolean"
            },
            "failureEmailTemplate": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "failureEmailName": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "successEmailNotification": {
                "type": "Boolean"
            },
            "successEmailTemplate": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "successEmailName": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "triggeringEmailNotification": {
                "type": "Boolean"
            },
            "triggeringEmailName": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "triggeringEmailTemplate": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "steps": {
                "type": "Array",
                "searchable": False
            },
            "stepStatuses": {
                "type": "Array",
                "searchable": False
            },
            "businessUnits": {
                "type": "Array",
                "searchable": False
            },
            "subscriptions": {
                "type": "Array",
                "searchable": False
            },
            "additionalAttributes": {
                "type": "Object",
                "searchable": False
            },
            "metadata": {
                "type": "Object",
                "searchable": False
            }
        },
        "tenantId": "backflipt.com",
        "appId": "6718c073cc4fca2655437982",
        "description": "",
        "name": "Simple Routes - G"
    },
    {
        "lockInfo": {},
        "shareWithAllApps": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "appsSharedWith": {
            "fullAccess": [],
            "readAccessOnly": []
        },
        "shareWithAllFlows": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "flowsSharedWith": {
            "fullAccess": [],
            "readAccessOnly": []
        },
        "containedByTreeList": [],
        "_id": "677df9b1c29b51553c4bca1a",
        "updatedAt": "2025-05-01T10:59:52.794Z",
        "createdAt": "2025-01-08T04:06:09.554Z",
        "updatedBy": "hemanthkethe@backflipt.com",
        "createdBy": "nikhiladevathi@backflipt.com",
        "locked": False,
        "createCallbackOperationId": "",
        "embedDataModelInfo": {},
        "primaryKey": "",
        "indices": [],
        "dataSchema": {
            "importUsersFile": {
                "type": "Object",
                "searchable": False
            },
            "userRecords": {
                "type": "Array",
                "searchable": False
            },
            "userStats": {
                "type": "Object",
                "searchable": False
            },
            "updatedAt": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "updatedBy": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "isSuccess": {
                "type": "Boolean"
            },
            "isRunning": {
                "type": "Boolean"
            }
        },
        "tenantId": "backflipt.com",
        "appId": "6718c073cc4fca2655437982",
        "description": "",
        "name": "Bulk Users Import Details - G"
    },
    {
        "lockInfo": {},
        "shareWithAllApps": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "appsSharedWith": {
            "fullAccess": [
                "66853bc7452663cbbc1301f3",
                "65c5a95ff50d5937f338816d",
                "683d56afaed74b904b019639"
            ],
            "readAccessOnly": []
        },
        "shareWithAllFlows": {
            "fullAccess": False,
            "readAccessOnly": False
        },
        "flowsSharedWith": {
            "fullAccess": [
                "64f845504d4dc1a0de4fecd3",
                "67729a8bc29b51553c4973d7",
                "6728c029cc4fca26554505ee",
                "6728c043cc4fca2655450689"
            ],
            "readAccessOnly": []
        },
        "_id": "67891386148dac226cda7246",
        "updatedAt": "2025-06-03T11:30:53.994Z",
        "createdAt": "2025-01-16T14:11:18.383Z",
        "updatedBy": "hemanthkethe@backflipt.com",
        "createdBy": "nikhiladevathi@backflipt.com",
        "locked": False,
        "createCallbackOperationId": "",
        "embedDataModelInfo": {},
        "primaryKey": "",
        "indices": [
            {
                "name": "lastLoginTime_-1",
                "key": {
                    "lastLoginTime": -1
                }
            },
            {
                "name": "firstName_1_lastName_1_email_1",
                "key": {
                    "firstName": 1,
                    "lastName": 1,
                    "email": 1
                }
            }
        ],
        "dataSchema": {
            "firstName": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "lastName": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "email": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "phone": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "role": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "processedOn": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "status": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "comment": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "userId": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "userExists": {
                "type": "Boolean"
            },
            "businessUnit": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "stAccount": {
                "type": "Object",
                "searchable": False
            },
            "userStatus": {
                "type": "Object",
                "searchable": False
            },
            "userInvitedStatus": {
                "type": "Object",
                "searchable": False
            },
            "businessUnitStatus": {
                "type": "Object",
                "searchable": False
            },
            "stAccountStatus": {
                "type": "Object",
                "searchable": False
            },
            "importUsersFileId": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            }
        },
        "tenantId": "backflipt.com",
        "appId": "6718c073cc4fca2655437982",
        "description": "",
        "name": "Bulk Users - G",
        "__v": 1,
        "containedByTreeList": []
    },
    {
        "lockInfo": {
            "userEmail": "viswanaths@backflipt.com",
            "lockedAt": "2025-08-05T09:09:16.453Z"
        },
        "shareWithAllApps": {
            "readAccessOnly": False,
            "fullAccess": False
        },
        "appsSharedWith": {
            "readAccessOnly": [],
            "fullAccess": []
        },
        "shareWithAllFlows": {
            "readAccessOnly": False,
            "fullAccess": False
        },
        "flowsSharedWith": {
            "readAccessOnly": [
                "67729a8bc29b51553c4973d7",
                "67729a3ec29b51553c4971c2"
            ],
            "fullAccess": [
                "6728c029cc4fca26554505ee",
                "6728c043cc4fca2655450689"
            ]
        },
        "_id": "683d6ea5aed74b904b02575e",
        "name": "Transfer Sites - G",
        "description": "",
        "appId": "6718c073cc4fca2655437982",
        "locked": True,
        "tenantId": "backflipt.com",
        "dataSchema": {
            "stReferenceId": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "siteName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "transferType": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "account": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "server": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "port": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "downloadFolder": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "downloadPattern": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "uploadFolder": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "userName": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "password": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "loginType": {
                "type": "Boolean"
            },
            "stCertificateId": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "networkZone": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "additionalAttributes": {
                "type": "Object",
                "searchable": False
            },
            "instance": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "transferSiteId": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            }
        },
        "indices": [],
        "primaryKey": "stReferenceId",
        "containedByTreeList": [],
        "embedDataModelInfo": {},
        "createCallbackOperationId": "",
        "createdBy": "karthikmsp@backflipt.com",
        "updatedBy": "karthikmsp@backflipt.com",
        "createdAt": "2025-06-02T09:28:05.580Z",
        "updatedAt": "2025-08-05T09:09:34.775Z",
        "__v": 0
    },
    {
        "lockInfo": {
            "userEmail": "viswanaths@backflipt.com",
            "lockedAt": "2025-08-05T09:09:37.165Z"
        },
        "shareWithAllApps": {
            "readAccessOnly": False,
            "fullAccess": False
        },
        "appsSharedWith": {
            "readAccessOnly": [],
            "fullAccess": []
        },
        "shareWithAllFlows": {
            "readAccessOnly": False,
            "fullAccess": False
        },
        "flowsSharedWith": {
            "readAccessOnly": [
                "67729a8bc29b51553c4973d7",
                "67729a3ec29b51553c4971c2"
            ],
            "fullAccess": [
                "6728c029cc4fca26554505ee",
                "6728c043cc4fca2655450689"
            ]
        },
        "_id": "683d6ff8aed74b904b02607d",
        "name": "Certificates - G",
        "description": "",
        "appId": "6718c073cc4fca2655437982",
        "locked": True,
        "tenantId": "backflipt.com",
        "dataSchema": {
            "stReferenceId": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "certificateName": {
                "type": "String",
                "encrypt": False,
                "searchable": True
            },
            "subject": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "type": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "usage": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "expirationTime": {
                "type": "Number",
                "searchable": False
            },
            "creationTime": {
                "type": "Number",
                "searchable": False
            },
            "signAlgorithm": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "validityPeriod": {
                "type": "Number",
                "searchable": False
            },
            "account": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "validationStatus": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "accessLevel": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "fingerprint": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "keyAlgorithm": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "issuer": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "serialNumber": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "keySize": {
                "type": "Number",
                "searchable": False
            },
            "version": {
                "type": "Number",
                "searchable": False
            },
            "additionalAttributes": {
                "type": "Object",
                "searchable": False
            },
            "instance": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            },
            "certificateId": {
                "type": "String",
                "encrypt": False,
                "searchable": False
            }
        },
        "indices": [],
        "primaryKey": "stReferenceId",
        "containedByTreeList": [],
        "embedDataModelInfo": {},
        "createCallbackOperationId": "",
        "createdBy": "karthikmsp@backflipt.com",
        "updatedBy": "karthikmsp@backflipt.com",
        "createdAt": "2025-06-02T09:33:44.276Z",
        "updatedAt": "2025-08-05T09:09:55.320Z",
        "__v": 0
    }
]

def extract_model_info(data_models):
    """
    Extract name, _id, and dataSchema from data models in a well-constructed human-readable JSON format.
    The dataSchema is transformed for easier understanding with clear field descriptions.
    
    Args:
        data_models (list): List of data model dictionaries
        
    Returns:
        str: Formatted JSON string with extracted information
    """
    import json
    
    def transform_schema_for_readability(schema):
        """
        Transform the data schema to be more human-readable and understandable.
        """
        if not schema:
            return {}
        
        transformed_schema = {}
        
        for field_name, field_config in schema.items():
            # Create a more readable field description
            field_info = {
                "field_name": field_name,
                "data_type": field_config.get("type", "Unknown"),
                "is_encrypted": field_config.get("encrypt", False),
                "is_searchable": field_config.get("searchable", False),
                "description": generate_field_description(field_name, field_config)
            }
            
            # Add any additional properties that might be useful
            additional_props = {}
            for key, value in field_config.items():
                if key not in ["type", "encrypt", "searchable"]:
                    additional_props[key] = value
            
            if additional_props:
                field_info["additional_properties"] = additional_props
            
            transformed_schema[field_name] = field_info
        
        return transformed_schema
    
    def generate_field_description(field_name, field_config):
        """
        Generate a human-readable description for a field based on its name and configuration.
        """
        field_type = field_config.get("type", "Unknown")
        is_encrypted = field_config.get("encrypt", False)
        is_searchable = field_config.get("searchable", False)
        
        # Generate description based on field name patterns
        description_parts = []
        
        # Type description
        type_descriptions = {
            "String": "Text data",
            "Number": "Numeric data",
            "Boolean": "True/False value",
            "Object": "Complex data structure",
            "Array": "List of items",
            "Date": "Date and time information"
        }
        
        description_parts.append(type_descriptions.get(field_type, f"{field_type} data"))
        
        # Security and searchability
        if is_encrypted:
            description_parts.append("(encrypted for security)")
        else:
            description_parts.append("(not encrypted)")
            
        if is_searchable:
            description_parts.append("(searchable)")
        else:
            description_parts.append("(not searchable)")
        
        # Field-specific descriptions based on common patterns
        field_lower = field_name.lower()
        if "id" in field_lower:
            description_parts.append("- Unique identifier")
        elif "name" in field_lower:
            description_parts.append("- Name or title")
        elif "email" in field_lower:
            description_parts.append("- Email address")
        elif "date" in field_lower or "time" in field_lower:
            description_parts.append("- Date/time information")
        elif "status" in field_lower:
            description_parts.append("- Current status or state")
        elif "created" in field_lower:
            description_parts.append("- Creation information")
        elif "updated" in field_lower:
            description_parts.append("- Last update information")
        elif "password" in field_lower:
            description_parts.append("- Authentication credential")
        elif "token" in field_lower:
            description_parts.append("- Authentication or access token")
        
        return " ".join(description_parts)
    
    extracted_models = []
    
    for model in data_models:
        # Extract the required fields
        model_info = {
            "model_name": model.get("name", ""),
            "model_id": model.get("_id", ""),
            "description": model.get("description", ""),
            "total_fields": len(model.get("dataSchema", {})),
            "data_schema": transform_schema_for_readability(model.get("dataSchema", {}))
        }
        extracted_models.append(model_info)
    
    # Format with proper indentation for human readability
    formatted_json = json.dumps(extracted_models, indent=2, ensure_ascii=False)
    
    return formatted_json

def create_schema_summary(data_models):
    """
    Create a simplified summary of data schemas for easy understanding.
    
    Args:
        data_models (list): List of data model dictionaries
        
    Returns:
        str: Formatted summary string
    """
    summary_lines = []
    summary_lines.append("=" * 80)
    summary_lines.append("DATA MODELS SUMMARY")
    summary_lines.append("=" * 80)
    
    for i, model in enumerate(data_models, 1):
        name = model.get("name", "Unknown Model")
        model_id = model.get("_id", "No ID")
        description = model.get("description", "No description available")
        schema = model.get("dataSchema", {})
        
        summary_lines.append(f"\n{i}. {name}")
        summary_lines.append(f"   ID: {model_id}")
        summary_lines.append(f"   Description: {description}")
        summary_lines.append(f"   Total Fields: {len(schema)}")
        
        if schema:
            summary_lines.append("   Fields:")
            for field_name, field_config in schema.items():
                field_type = field_config.get("type", "Unknown")
                is_encrypted = field_config.get("encrypt", False)
                is_searchable = field_config.get("searchable", False)
                
                # Create a simple field description
                field_desc = f"      • {field_name} ({field_type})"
                if is_encrypted:
                    field_desc += " [ENCRYPTED]"
                if is_searchable:
                    field_desc += " [SEARCHABLE]"
                
                summary_lines.append(field_desc)
        
        summary_lines.append("-" * 60)
    
    return "\n".join(summary_lines)

def save_extracted_models(data_models, output_file="extracted_models.json"):
    """
    Extract model information and save to a JSON file.
    
    Args:
        data_models (list): List of data model dictionaries
        output_file (str): Output file path
    """
    extracted_data = extract_model_info(data_models)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(extracted_data)
    
    print(f"Extracted model information saved to {output_file}")
    return extracted_data

def save_schema_summary(data_models, output_file="schema_summary.txt"):
    """
    Save a human-readable summary of all data schemas.
    
    Args:
        data_models (list): List of data model dictionaries
        output_file (str): Output file path
    """
    summary = create_schema_summary(data_models)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"Schema summary saved to {output_file}")
    return summary

# Example usage
if __name__ == "__main__":
    print("Generating enhanced data model information...")
    print("=" * 60)
    
    # Create and display schema summary (easier to read)
    print("\n1. SCHEMA SUMMARY (Human-readable format):")
    print("-" * 40)
    summary = create_schema_summary(data_models[:3])  # Show first 3 models for demo
    print(summary)
    
    # Extract detailed JSON information
    print("\n2. DETAILED JSON FORMAT:")
    print("-" * 40)
    extracted_json = extract_model_info(data_models[:2])  # Show first 2 models for demo
    print(extracted_json)
    
    # Save both formats to files
    print("\n3. SAVING TO FILES:")
    print("-" * 40)
    save_extracted_models(data_models, "detailed_models.json")
    save_schema_summary(data_models, "schema_summary.txt")
    
    print("\nFiles created:")
    print("• detailed_models.json - Complete JSON with enhanced schema descriptions")
    print("• schema_summary.txt - Human-readable summary format")