from typing import Tuple, List

import time
import requests
import datetime
import random
import string
from geopy.geocoders import Nominatim
from geopy.distance import distance as geodistance
from geopy.point import Point

from rich.console import Console
from rich.table import Table, Column
from rich.live import Live

rich_console = Console()

TX_JSON_URLS = [
    # "https://www.vaccinespotter.org/api/v0/stores/TX/albertsons.json",
    # "https://www.vaccinespotter.org/api/v0/stores/TX/cvs.json",
    # # "https://www.vaccinespotter.org/api/v0/stores/TX/heb.json",
    # "https://www.vaccinespotter.org/api/v0/stores/TX/sams_club.json",
    # "https://www.vaccinespotter.org/api/v0/stores/TX/walgreens.json",
    # "https://www.vaccinespotter.org/api/v0/stores/TX/walmart.json",
]

TX_BOOKING_URLS = {
    "albertsons": "https://www.mhealthappointments.com/covidappt",
    "cvs": "https://www.cvs.com/vaccine/intake/store/covid-screener/covid-qns",
    "heb": "https://vaccine.heb.com/",
    "sams_club": "https://www.samsclub.com/pharmacy/immunization?imzType=covid",
    "walgreens": "https://www.walgreens.com/findcare/vaccination/covid-19/location-screening",
    "walmart": "https://www.walmart.com/pharmacy/clinical-services/immunization/scheduled?imzType=covid&r=yes",
}

IFTTT_WEBHOOK_HEY = ""
ADDRESS = ""
ZIPCODE = ""

GEO_INSTANCE = Nominatim(user_agent="vaccine-tracker-sr")
LOCAL_GEO_QUERY = {"address": ADDRESS, "postalcode": ZIPCODE}
LOCAL_GEO = GEO_INSTANCE.geocode(query=LOCAL_GEO_QUERY)

CITY_GEO = {
    "Abilene, TX": Point(32.44645, -99.7475905, 0.0),
    "Alvarado, TX": Point(32.4095565, -97.21028810404624, 0.0),
    "Amarillo, TX": Point(35.2072185, -101.8338246, 0.0),
    "Athens, TX": Point(32.2044416, -95.854914, 0.0),
    "Austin, TX": Point(30.2711286, -97.7436995, 0.0),
    "Beaumont, TX": Point(30.0860459, -94.1018461, 0.0),
    "Brownsville, TX": Point(25.9140256, -97.4890856, 0.0),
    "Bryan, TX": Point(30.6743643, -96.3699632, 0.0),
    "Canyon Lake, TX": Point(29.8643185, -98.2437802, 0.0),
    "Cleveland, TX": Point(30.3417711, -95.0854786, 0.0),
    "Crowley, TX": Point(32.5782835, -97.3609829, 0.0),
    "Cypress, TX": Point(29.9691116, -95.6971686, 0.0),
    "Denison, TX": Point(33.7556593, -96.536658, 0.0),
    "El Paso, TX": Point(31.7754152, -106.464634, 0.0),
    "Elgin, TX": Point(30.349351, -97.3705762, 0.0),
    "Forney, TX": Point(32.747893, -96.4719289, 0.0),
    "Georgetown, TX": Point(30.671598, -97.65500660120435, 0.0),
    "Gladewater, TX": Point(32.5365333, -94.9427169, 0.0),
    "Granbury, TX": Point(32.4407788, -97.7926088, 0.0),
    "Greenville, TX": Point(33.1384488, -96.1108066, 0.0),
    "Lake Worth, TX": Point(32.8048507, -97.44502, 0.0),
    "Katy, TX": Point(29.7857853, -95.8243956, 0.0),
    "Lakeway, TX": Point(30.3644888, -97.9875325, 0.0),
    "Laredo, TX": Point(27.5199841, -99.4953764, 0.0),
    "Lubbock, TX": Point(33.5635206, -101.879336, 0.0),
    "Lufkin, TX": Point(31.3386242, -94.7288558, 0.0),
    "Marshall, TX": Point(32.5447756, -94.3661004, 0.0),
    "Mesquite, TX": Point(32.7666103, -96.599472, 0.0),
    "Midland, TX": Point(31.9973662, -102.0779482, 0.0),
    "Odessa, TX": Point(31.8457149, -102.367687, 0.0),
    "Orange, TX": Point(30.1228634, -93.9041169, 0.0),
    "Paris, TX": Point(33.6617962, -95.555513, 0.0),
    "Pearland, TX": Point(29.5639758, -95.2864299, 0.0),
    "Pharr, TX": Point(26.1947962, -98.1836216, 0.0),
    "Plano, TX": Point(33.0136764, -96.6925096, 0.0),
    "Red Oak, TX": Point(32.5117104, -96.80836332870047, 0.0),
    "Richardson, TX": Point(32.9481789, -96.7297206, 0.0),
    "Richmond, TX": Point(29.5821811, -95.7607832, 0.0),
    "Roanoke, TX": Point(33.0040126, -97.2258483, 0.0),
    "Robstown, TX": Point(27.7903032, -97.6688843, 0.0),
    "Rockwall, TX": Point(32.8923464, -96.4066987, 0.0),
    "San Angelo, TX": Point(31.4648357, -100.4398442, 0.0),
    "Schertz, TX": Point(29.5641617, -98.2695702, 0.0),
    "Temple, TX": Point(31.098207, -97.3427847, 0.0),
    "Texarkana, TX": Point(33.44628645, -94.07638067493534, 0.0),
    "The Woodlands, TX": Point(30.1734194, -95.504686, 0.0),
    "Tyler, TX": Point(32.3512601, -95.3010624, 0.0),
    "Waco, TX": Point(31.549333, -97.1466695, 0.0),
    "Weatherford, TX": Point(32.7589648, -97.7970748, 0.0),
    "Wichita Falls, TX": Point(33.9137085, -98.4933873, 0.0),
    "Arlington, TX": Point(32.701938999999996, -97.10562379033699, 0.0),
    "Atlanta, TX": Point(33.1162131, -94.1663493, 0.0),
    "Bay City, TX": Point(28.9827565, -95.969402, 0.0),
    "Borger, TX": Point(35.6678204, -101.3973876, 0.0),
    "Canton, TX": Point(32.555664, -95.8640507, 0.0),
    "Cedar Hill, TX": Point(32.5888072, -96.9553675, 0.0),
    "Corsicana, TX": Point(32.091299, -96.4646821, 0.0),
    "Decatur, TX": Point(33.2342834, -97.5861393, 0.0),
    "Elsa, TX": Point(26.2966228, -97.9931057, 0.0),
    "Fort Worth, TX": Point(32.753177, -97.3327459, 0.0),
    "Garland, TX": Point(32.912624, -96.6388833, 0.0),
    "Grand Prairie, TX": Point(32.657368000000005, -97.02846624175038, 0.0),
    "Houston, TX": Point(29.7589382, -95.3676974, 0.0),
    "Huntsville, TX": Point(30.7235263, -95.5507771, 0.0),
    "Jacinto City, TX": Point(29.7673433, -95.2336723, 0.0),
    "Kingsville, TX": Point(27.5158689, -97.856109, 0.0),
    "La Marque, TX": Point(29.3685674, -94.9713134, 0.0),
    "Livingston, TX": Point(30.711029, -94.9329898, 0.0),
    "Mansfield, TX": Point(32.5631924, -97.1416768, 0.0),
    "Mathis, TX": Point(28.0942916, -97.8274111, 0.0),
    "Mineola, TX": Point(32.6633387, -95.4880308, 0.0),
    "Mineral Wells, TX": Point(32.8084605, -98.1128223, 0.0),
    "New Braunfels, TX": Point(29.7028266, -98.1257348, 0.0),
    "Pasadena, TX": Point(29.6910625, -95.2091006, 0.0),
    "Pflugerville, TX": Point(30.4393696, -97.6200043, 0.0),
    "Princeton, TX": Point(33.1801161, -96.4980424, 0.0),
    "Rowlett, TX": Point(32.9029017, -96.56388, 0.0),
    "San Antonio, TX": Point(29.4246002, -98.4951405, 0.0),
    "San Marcos, TX": Point(29.8826436, -97.9405828, 0.0),
    "Seabrook, TX": Point(29.5633199, -95.019723, 0.0),
    "Sherman, TX": Point(36.2452294, -101.8858689, 0.0),
    "Silsbee, TX": Point(30.3490978, -94.1779626, 0.0),
    "Stephenville, TX": Point(32.2191836, -98.2130634, 0.0),
    "Sulphur Springs, TX": Point(33.1384886, -95.6010143, 0.0),
    "Tomball, TX": Point(30.0971621, -95.6160549, 0.0),
    "Gainesville, TX": Point(33.6259414, -97.1333453, 0.0),
    "Humble, TX": Point(29.9988312, -95.2621553, 0.0),
    "Addison, TX": Point(32.9604305, -96.83025951893629, 0.0),
    "Allen, TX": Point(33.1031744, -96.6705503, 0.0),
    "Aransas Pass, TX": Point(27.909666, -97.1503865, 0.0),
    "Balcones Heights, TX": Point(29.489573, -98.5501765, 0.0),
    "Bandera, TX": Point(29.7643475, -99.234526, 0.0),
    "Baytown, TX": Point(29.7355047, -94.9774274, 0.0),
    "Bedford, TX": Point(32.844017, -97.1430671, 0.0),
    "Bee Cave, TX": Point(30.3085373, -97.94501, 0.0),
    "Beverly Hills, TX": Point(31.5215557, -97.1538919, 0.0),
    "Breckenridge, TX": Point(32.7558392, -98.9032554, 0.0),
    "Bowie, TX": Point(33.4198886, -94.4479626, 0.0),
    "Cameron, TX": Point(26.1291189, -97.4134281, 0.0),
    "Carrollton, TX": Point(32.9537349, -96.8902816, 0.0),
    "Celina, TX": Point(33.3238976, -96.785342, 0.0),
    "Cedar Park, TX": Point(30.5217116, -97.827833, 0.0),
    "Center, TX": Point(31.7954512, -94.1790862, 0.0),
    "Clear Lake Shores, TX": Point(29.547452, -95.0321506, 0.0),
    "Cibolo, TX": Point(29.5707831, -98.2330927, 0.0),
    "College Station, TX": Point(30.5955289, -96.3071042, 0.0),
    "Commerce, TX": Point(33.2442615, -95.9006353, 0.0),
    "Conroe, TX": Point(30.3118769, -95.4560512, 0.0),
    "Coppell, TX": Point(32.9552598, -97.0155703, 0.0),
    "Corinth, TX": Point(33.1540091, -97.0647322, 0.0),
    "Corpus Christi, TX": Point(27.7477253, -97.4014129, 0.0),
    "Dallas, TX": Point(32.7762719, -96.7968559, 0.0),
    "Dickinson, TX": Point(29.4607876, -95.0513173, 0.0),
    "Denton, TX": Point(33.1838787, -97.1413417, 0.0),
    "Euless, TX": Point(32.8457865, -97.0667142473263, 0.0),
    "Edinburg, TX": Point(26.3013982, -98.1624501, 0.0),
    "Farmers Branch, TX": Point(32.9265137, -96.8961151, 0.0),
    "Floresville, TX": Point(29.1335781, -98.1561192, 0.0),
    "Freeport, TX": Point(28.9541368, -95.3596617, 0.0),
    "Friendswood, TX": Point(29.5293998, -95.2010447, 0.0),
    "Frisco, TX": Point(33.1506744, -96.8236116, 0.0),
    "Galveston, TX": Point(29.299328, -94.7945882, 0.0),
    "Grapevine, TX": Point(32.9337381, -97.0788754, 0.0),
    "Harlingen, TX": Point(26.1908241, -97.6959794, 0.0),
    "Heath, TX": Point(32.8445305, -96.47184564700122, 0.0),
    "Hurst, TX": Point(32.8234621, -97.1705678, 0.0),
    "Irving, TX": Point(32.8295183, -96.9442177, 0.0),
    "Jacksonville, TX": Point(31.963778, -95.2705042, 0.0),
    "Keller, TX": Point(32.9299655, -97.2271249, 0.0),
    "Kilgore, TX": Point(32.399730399999996, -94.86460773852411, 0.0),
    "Killeen, TX": Point(31.1171441, -97.727796, 0.0),
    "Kyle, TX": Point(29.9892816, -97.877174, 0.0),
    "Lake Jackson, TX": Point(29.0338575, -95.4343859, 0.0),
    "La Porte, TX": Point(29.6657838, -95.0193729, 0.0),
    "Lamesa, TX": Point(32.7357287, -101.9550202, 0.0),
    "League City, TX": Point(29.5074538, -95.0949303, 0.0),
    "Lewisville, TX": Point(33.046233, -96.994174, 0.0),
    "Liberty, TX": Point(30.0856736, -94.7856262, 0.0),
    "Longview, TX": Point(32.5007031, -94.74049, 0.0),
    "Manvel, TX": Point(29.4664706, -95.355714, 0.0),
    "Marble Falls, TX": Point(30.5781414, -98.2753857, 0.0),
    "Mcallen, TX": Point(26.2043691, -98.230082, 0.0),
    "Mckinney, TX": Point(33.1976496, -96.6154471, 0.0),
    "Mission, TX": Point(26.2159066, -98.3252932, 0.0),
    "Missouri City, TX": Point(29.6185669, -95.5377215, 0.0),
    "Montgomery, TX": Point(30.301949, -95.5065944, 0.0),
    "Nassau Bay, TX": Point(29.5446753, -95.0910413, 0.0),
    "North Richland Hills, TX": Point(32.8342952, -97.2289029, 0.0),
    "Port Aransas, TX": Point(27.8332175, -97.0618324, 0.0),
    "Port Arthur, TX": Point(29.8988618, -93.9288723, 0.0),
    "Richland Hills, TX": Point(32.8159623, -97.2280695, 0.0),
    "River Oaks, TX": Point(32.7770737, -97.394463, 0.0),
    "Rockport, TX": Point(28.0205733, -97.0544341, 0.0),
    "Rosenberg, TX": Point(29.5571825, -95.8085623, 0.0),
    "Rosharon, TX": Point(29.3521203, -95.460341, 0.0),
    "Round Rock, TX": Point(30.508235, -97.6788934, 0.0),
    "Seminole, TX": Point(32.7189926, -102.6449101, 0.0),
    "Snyder, TX": Point(32.7180803, -100.9182313, 0.0),
    "South Padre Island, TX": Point(26.1036887, -97.1646938, 0.0),
    "Southlake, TX": Point(32.9412363, -97.1341783, 0.0),
    "Spring, TX": Point(30.0798826, -95.4172549, 0.0),
    "Sugar Land, TX": Point(29.6196787, -95.6349463, 0.0),
    "The Colony, TX": Point(33.0890094, -96.8863922, 0.0),
    "Universal City, TX": Point(29.5480071, -98.2911235, 0.0),
    "Victoria, TX": Point(28.8026443, -96.9766308, 0.0),
    "Vidor, TX": Point(30.1316001, -94.0154542, 0.0),
    "Watauga, TX": Point(32.8579056, -97.2547371, 0.0),
    "Waxahachie, TX": Point(32.3944908, -96.8439365, 0.0),
    "Webster, TX": Point(29.5351724, -95.1161564, 0.0),
    "West Columbia, TX": Point(29.1438582, -95.6452249, 0.0),
    "Westlake, TX": Point(32.991226, -97.1943701, 0.0),
    "Wharton, TX": Point(29.2454534, -96.2291474, 0.0),
    "Wylie, TX": Point(33.0151201, -96.5388789, 0.0),
    "Winnsboro, TX": Point(32.9573449, -95.2902224, 0.0),
}


def miles_distance_from_local_geo(remote_coordinates: Tuple[int, int]) -> int:
    local_coordinates = LOCAL_GEO.latitude, LOCAL_GEO.longitude
    return geodistance(local_coordinates, remote_coordinates).miles


def entry_coordinates(entry: dict, is_heb: bool) -> Tuple[int, int]:

    city_geo_instance = None
    city_name = entry.get("name")
    latitude, longitude = entry.get("latitude"), entry.get("longitude")

    if is_heb:
        return latitude, longitude

    if not latitude and city_name not in CITY_GEO.keys():
        CITY_GEO[city_name] = GEO_INSTANCE.geocode(query=city_name)

    if not latitude:
        city_geo_instance = CITY_GEO[city_name]
        latitude, longitude = city_geo_instance.latitude, city_geo_instance.longitude

    return latitude, longitude


def filter_results_by_provider(
    json_url: str,
    include_unavailable: bool = False,
    miles_threshold: int = 50,
    is_heb: bool = False,
) -> list:
    result = requests.get(json_url)
    result_json: List[dict] = (
        result.json() if not is_heb else result.json().get("locations")
    )

    filtered_results = []

    for entry in result_json:
        if result_entry_filter(entry, include_unavailable, miles_threshold, is_heb):
            entry["miles"] = str(
                round(miles_distance_from_local_geo(entry_coordinates(entry, is_heb)))
            )

            filtered_results.append(entry)

    return filtered_results


def result_entry_filter(
    entry: dict,
    include_unavailable: bool = False,
    miles_threshold: int = 50,
    is_heb: bool = False,
) -> bool:
    remote_coordinates = entry_coordinates(entry, is_heb)
    miles_distance = miles_distance_from_local_geo(remote_coordinates)

    appointments_available = (
        include_unavailable
        or entry.get("appointments_available")
        or entry.get("openAppointmentSlots")
    )

    return miles_distance <= miles_threshold and appointments_available


def notification(brand, location, url):
    report = {}
    report["value1"] = brand
    report["value2"] = location
    report["value3"] = url if url else TX_BOOKING_URLS.get(brand)
    requests.post(
        f"https://maker.ifttt.com/trigger/appts_available/with/key/{IFTTT_WEBHOOK_KEY}",
        data=report,
    )


def filtered_results_for_all_providers(
    include_unavailable: bool = False, miles_threshold: int = 50
) -> list:
    results_table = Table(
        "brand",
        "city",
        Column("distance", justify="right"),
        Column("has appointments", style="green"),
        "url",
    )
    appts_available = False
    filtered_results = []
    for provider_url in TX_JSON_URLS:
        filtered_results_for_provider = filter_results_by_provider(
            json_url=provider_url,
            include_unavailable=include_unavailable,
            miles_threshold=miles_threshold,
        )
        filtered_results.extend(filtered_results_for_provider)

    cache_buster = "".join(random.choice(string.digits) for i in range(20))
    filtered_results_for_provider = filter_results_by_provider(
        json_url=f"https://heb-ecom-covid-vaccine.hebdigital-prd.com/vaccine_locations.json?q={cache_buster}",
        include_unavailable=include_unavailable,
        miles_threshold=miles_threshold,
        is_heb=True,
    )
    filtered_results.extend(filtered_results_for_provider)

    for result in sorted(filtered_results, key=lambda r: int(r["miles"])):
        appointment_availability = result.get("appointments_available") or result.get(
            "openAppointmentSlots"
        )
        has_appointments = "Yes" if appointment_availability else ""
        if appointment_availability:
            notification(
                result.get("brand") if result.get("brand") else "heb",
                result["city"],
                result.get("url"),
            )
            if not appts_available:
                appts_available = True

        results_table.add_row(
            result.get("brand") if result.get("brand") else "HEB direct",
            result.get("city"),
            result.get("miles"),
            has_appointments,
            result.get("url") if result.get("url") else TX_BOOKING_URLS.get(brand),
        )

    if appts_available:
        print("\a")

    return results_table


if __name__ == "__main__":
    with Live(
        filtered_results_for_all_providers(miles_threshold=50), refresh_per_second=4
    ) as live:
        while True:
            live.update(filtered_results_for_all_providers(miles_threshold=50))
            print(f'last updated at {datetime.datetime.now().strftime("%H:%M:%S")}')
            time.sleep(45)
