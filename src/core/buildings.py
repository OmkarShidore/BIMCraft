from src.core import buildings_util

def create_bulding_record():
    buildings_util.create_building_record()

def get_building_records():
    building_records =  buildings_util.get_all_buildings()
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