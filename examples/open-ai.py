from langflow.custom import Component
from langflow.io import MessageTextInput, Output
from langflow.schema import Data
import pymongo


class CustomComponent(Component):
    display_name = "Custom Component"
    description = "Use as a template to create your own component."
    documentation: str = "http://docs.langflow.org/components/custom"
    icon = "custom_components"
    name = "CustomComponent"

    inputs = [
        MessageTextInput(name="input_value", display_name="Input Value", value="Hello, World!"),
    ]

    outputs = [
        Output(display_name="Output", name="output", method="build_output"),
        Output(display_name="Records", name="records", method="fetch_documents"),
    ]

    def build_output(self) -> Data:
        data = Data(value=self.input_value)
        self.status = data
        return data
    def fetch_documents(self) -> Data:
     try:
        client = pymongo.MongoClient(
        "mongodb+srv://sentinel-ai-user:4JlNDabpekHtCkoq@bb-non-prod.i8ab8.mongodb.net/?retryWrites=true&w=majority",
        tls=True,
        tlsAllowInvalidCertificates=True
        )
        db = client['sentinel-ai']
        collection = db['finance_apps']
        print("Fetching documents...")
        query = {}
        projection = {}
        cursor = collection.find(query, projection)
        print(f"Fetched documents:{cursor}")
        return Data(value=cursor)
     except Exception as e:
      print(f"Error fetching documents: {e}")