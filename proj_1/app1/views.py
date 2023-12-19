from django.shortcuts import render
from django.http import JsonResponse
from .models import District, Taluka, Village
import requests
from bs4 import BeautifulSoup
from lxml import html
# Create your views here.

def scrape_data(request):
    # URL of the website
    url = "https://eservices.tn.gov.in/eservicesnew/land/chittaCheckNewRural_en.html?lan=en"
    content = response.content
    root = html.fromstring(content)
  
    response = requests.get(url)
    
    if response.status_code == 200:
       
        soup = BeautifulSoup(response.content, 'html.parser')

        district_options = soup.find('select', {'id': 'districtId'}).find_all('option')
        taluka_options = soup.find('select', {'id': 'talukaId'}).find_all('option')
        village_options = soup.find('select', {'id': 'villageId'}).find_all('option')

        district_data = [option.text.strip() for option in district_options]
        taluka_data = [option.text.strip() for option in taluka_options]
        village_data = [option.text.strip() for option in village_options]


        data = {
            "districts": district_data,
            "talukas": taluka_data,
            "villages": village_data
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Failed to retrieve the webpage. Status code: {}".format(response.status_code)})


def save_data(districts, talukas, villages):
  
    for district in districts:
        District.objects.create(**district)

    for taluka in talukas:
        district = District.objects.filter(name=taluka["district"]).first()
        Taluka.objects.create(name=taluka["name"], district=district)

    for village in villages:
        taluka = Taluka.objects.filter(name=village["taluka"]).first()
        Village.objects.create(name=village["name"], taluka=taluka)