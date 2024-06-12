import json, csv

def convert_json_to_csv(json_path:str,csv_path,field_names):
    try:
        # Read the JSON array from the file
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)

        # Write the data to a CSV file
        with open(csv_path, 'w', newline='') as csv_file:
            # Extract field names from the first JSON object

            # Create a CSV writer with the specified field names
            csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)

            # Write the header
            csv_writer.writeheader()

            # Write the data with only the selected fields
            for row in data["results"]:
                csv_writer.writerow({field: row.get(field, "") for field in field_names})
        print(f'CSV file "{csv_path}" created successfully.')
    except Exception as err:
        print("error in convert_json_to_csv",err)
        return


field_names = ["title","skipped","summary-line","successful","err"]
csv_file_name = 'audit.csv'
