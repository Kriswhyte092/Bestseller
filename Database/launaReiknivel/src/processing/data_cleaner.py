from collections import defaultdict


def validate_personas (raw_data):
    groups = defaultdict(list)
    for persona in raw_data:
        if persona['type'] == "group":
            continue
        groups[persona['type']].append(persona)

    users = ret_users(groups["user"])
    locations = ret_locations(groups["location"])
    positions = ret_positions(groups["position"])
    return users, locations, positions

def validate_shifts(raw_data):
    clean_shifts = []
    for shift in raw_data:
        if shift.get("timesheetProjections"):
            for projection in shift["timesheetProjections"]:
                if projection.get("status") == "approved":
                    clean_shift = {
                        "shift_id": shift.get("id"),
                        "user_id": shift.get("user", {}).get("id"),
                        "scheduled_start": shift.get("dtstart"),
                        "scheduled_end": shift.get("dtend"),
                        "clock_in": projection.get("clockIn"),
                        "clock_out": projection.get("clockOut"),
                        "break_minutes": projection.get("breakMinutes", 0),  # Default to 0 if not present
                        "status": projection.get("status"),
                        "location_id": shift.get("location", {}).get("id"),
                        "position_id": shift.get("position", {}).get("id"),
                    }
                    clean_shifts.append(clean_shift)
    return clean_shifts

def ret_users(users):
    clean_users = []
    for user in users:
        if user["active"]:

            clean_user = {
                "id": user["id"],
                "legal_name": user["legalName"],
                "lastname": user["lastname"],
                "email": user["email"],
                "active": user["active"],
            }
            clean_users.append(clean_user)
    return clean_users

def ret_locations(locations):
    clean_locations = []
    for location in locations:
        clean_location = {
            "id": location["id"],
            "name": location["name"],
            "externa_id": location["externalId"],
            "phone": location["phone"],
        }
        clean_locations.append(clean_location)
    return clean_locations


def ret_positions(positions):
    clean_positions = []
    for position in positions:
        clean_position = {
            "id": position["id"],
            "name": position["name"],
        }
        clean_positions.append(clean_position)
    return clean_positions
