import math
from report.models import Cell, Village

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in KM
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def validate_report_location(report):
    if not report.reporter_latitude or not report.reporter_longitude:
        return "UNCONFIDENT", None

    user_lat = float(report.reporter_latitude)
    user_lon = float(report.reporter_longitude)

    target_lat = None
    target_lon = None
    target_name = "unknown"

    if report.incident_cell and report.incident_cell.latitude and report.incident_cell.longitude:
        target_lat = float(report.incident_cell.latitude)
        target_lon = float(report.incident_cell.longitude)
        target_name = f"Cell: {report.incident_cell.name}"

    elif report.incident_village and report.incident_village.latitude and report.incident_village.longitude:
        target_lat = float(report.incident_village.latitude)
        target_lon = float(report.incident_village.longitude)
        target_name = f"Village: {report.incident_village.name}"

    elif not report.incident_cell and not report.incident_village:
        # Autofill only if both are missing
        closest_cell = None
        min_distance = float("inf")
        for cell in Cell.objects.exclude(latitude__isnull=True, longitude__isnull=True):
            dist = haversine_distance(user_lat, user_lon, float(cell.latitude), float(cell.longitude))
            if dist < min_distance:
                min_distance = dist
                closest_cell = cell

        if closest_cell:
            report.incident_cell = closest_cell
            report.incident_sector = closest_cell.sector
            report.incident_district = closest_cell.sector.district
            report.incident_province = closest_cell.sector.district.province
            report.save(update_fields=[
                'incident_cell', 'incident_sector', 'incident_district', 'incident_province'
            ])

            target_lat = float(closest_cell.latitude)
            target_lon = float(closest_cell.longitude)
            target_name = f"Auto-filled Cell: {closest_cell.name}"

    if target_lat is None or target_lon is None:
        return "UNCONFIDENT", None

    distance_km = haversine_distance(user_lat, user_lon, target_lat, target_lon)

    if distance_km <= 7:
        return "CONFIDENT", {"distance_km": distance_km, "location_checked": target_name}
    else:
        return "UNCONFIDENT", {"distance_km": distance_km, "location_checked": target_name}
