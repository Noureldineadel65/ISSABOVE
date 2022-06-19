import requests
import datetime as dt
import smtplib
import time
def get_user_location():
    response = requests.get("https://ipinfo.io/json")
    response.raise_for_status()
    LAT, LNG = response.json()["loc"].split(",")
    return {
        "LAT": float(LAT),
        "LNG": float(LNG)
    }


def get_sun_location(lat, lng):
    response = requests.get("https://api.sunrise-sunset.org/json", params={
        "lat": lat,
        "lng": lng,
        "formatted": 0
    })
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    return sunrise, sunset
def get_iss_location():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    data = response.json()
    iss_position = data["iss_position"]
    return {"LAT": float(iss_position["longitude"]), "LNG":float(iss_position["latitude"])}

def get_distance(current_loc, to_compare):
    lat_dif = abs(current_loc[0] - to_compare[0])
    lng_dif = abs(current_loc[1] - to_compare[1])
    return lat_dif, lng_dif
USER_LOCATION = {"LAT": 30.0626, "LNG": 31.2497}
sunrise, sunset = get_sun_location(USER_LOCATION["LAT"], USER_LOCATION["LNG"])
current_hour = dt.datetime.now().hour
while True:
    time.sleep(60)
    if current_hour <= sunrise or current_hour >= sunset:
        iss_location = get_iss_location()
        print(iss_location)
        is_iss_near = all([x < 5 for x in get_distance((USER_LOCATION["LAT"], USER_LOCATION["LNG"]),
                                                       (iss_location["LAT"], iss_location["LNG"]))])
        if is_iss_near:
            with smtplib.SMTP('smtp-mail.outlook.com', 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login("", "")
                smtp.sendmail(from_addr="jzblbot@outlook.com", to_addrs="noureldine.adel22@gmail.com",
                              msg=f"Subject:NOUR LOOK ABOVE!\n\nThe ISS IS LITERALLY ABOVE YOU RIGHT NOW!\n\nCaptured at: {dt.datetime.now()}\nAt Location of: {USER_LOCATION}")
