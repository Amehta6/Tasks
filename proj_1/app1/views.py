from django.shortcuts import render
from django.http import JsonResponse
from .models import District, Taluka, Village
import requests
from bs4 import BeautifulSoup
# Create your views here.

def scrape_data(request):
    # URL of the website
    url = "https://eservices.tn.gov.in/eservicesnew/land/chittaCheckNewRural_en.html?lan=en"

  
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


