from src.bim_core import buildings_utils

REQUIRED_BUILDING_FIELDS = ['name', 'description', 'owner_history', 'address_lines', 'town', 'region', 'country']

def add_building_record(request_data):
    missing_parameters = [field for field in REQUIRED_BUILDING_FIELDS if field not in request_data or not request_data[field]]
    if missing_parameters:
        return f"Operation Failed, missing key: {missing_parameters}", 400
    result = buildings_utils.create_building_record(request_data)
    if result:
        return "Added building record", 201
    else:
        return "Operation Failed", 500

def get_building_records():
    building_records =  buildings_utils.get_all_buildings()
    response_data = []
    for building in building_records:
        building_dict = {
            "building_id": building.building_id,
            "name": building.name,
            "description": building.description,
            "owner_history": building.owner_history,
            "address_lines": building.address_lines,
            "postal_box": building.postal_box,
            "town": building.town,
            "region": building.region,
            "postal_code": building.postal_code,
            "country": building.country
        }
        response_data.append(building_dict)
    return response_data

def delete_bulding_record(bulding_id):
    result = buildings_utils.delete_bulding_by_id(bulding_id)
    if result[0]==True:
        return "Bulding deleted", result[1]
    else:
        return "Operation Failed", 500