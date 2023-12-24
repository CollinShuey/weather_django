import datetime


import requests
from . import creds
from django.shortcuts import render

def index(request):
    API_KEY = creds.API_KEY
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=imperial"
    forcast_url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}&units=imperial"

    if request.method == "POST":
        city1 = request.POST['city1']
        city2 = request.POST.get("city2",None)

        weather_data1,daily_forcasts1 = fetch_weather_and_forecast(city1,API_KEY,current_weather_url,forcast_url)

        if city2:
            weather_data2,daily_forcasts2 = fetch_weather_and_forecast(city2,API_KEY,current_weather_url,forcast_url)
        else:
            weather_data2,daily_forcasts2 = None, None

        context = {
            "weather_data1" : weather_data1,
            "daily_forcasts1" : daily_forcasts1,
            "weather_data2" : weather_data2,
            "daily_forcasts2" : daily_forcasts2,
        }

        return render(request, "index.html",context)
 
    else:
        return render(request,"index.html")

def fetch_weather_and_forecast(city,api_key,current_weather_url,forcast_url):
    response = requests.get(current_weather_url.format(city,api_key)).json()
    lat,lon = response["coord"]["lat"], response['coord']['lon']
    forecast_response = requests.get(forcast_url.format(lat,lon,api_key)).json()

    weather_data = {
        "city": city,
        "temperature" : round(response['main']['temp'],2),
        "description" : response['weather'][0]['description'],
        "icon" :response['weather'][0]['icon'],
    }

    daily_forcasts = []
    for daily_data in forecast_response['list'][:5]:
        daily_forcasts.append({
            "day" : datetime.datetime.fromtimestamp(daily_data['dt']).strftime("%A"),
            "min_temp" : round(daily_data['main']['temp_min'],2),
            "max_temp" : round(daily_data['main']['temp_max'],2),
            "description" : daily_data['weather'][0]['description'],
            "icon" : daily_data['weather'][0]['icon'],

        })

    return weather_data,daily_forcasts