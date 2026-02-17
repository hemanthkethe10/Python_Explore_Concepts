import json

def extract_data_type_description(input_file, output_file):
    """
    Extract only data_type and description from the detailed_models.json file
    """
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    extracted_data = []
    
    for model in data:
        model_info = {
            "model_name": model.get("model_name", ""),
            "model_id": model.get("model_id", ""),
            "fields": {}
        }
        
        if "data_schema" in model:
            for field_name, field_info in model["data_schema"].items():
                model_info["fields"][field_name] = {
                    "data_type": field_info.get("data_type", ""),
                    "description": field_info.get("description", "")
                }
        
        extracted_data.append(model_info)
    
    # Write to output file
    with open(output_file, 'w') as f:
        json.dump(extracted_data, f, indent=2)
    
    print(f"Extracted data saved to {output_file}")
    print(f"Total models processed: {len(extracted_data)}")

if __name__ == "__main__":
    input_file = "/Users/hemanthk/Repos/Python/detailed_models.json"
    output_file = "/Users/hemanthk/Repos/Python/data_type_description_only.json"
    
    extract_data_type_description(input_file, output_file)

