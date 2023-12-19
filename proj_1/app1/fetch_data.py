import requests
from lxml import html

def fetch_data():
    # Fetch HTML content
    response = requests.get("https://eservices.tn.gov.in/eservicesnew/land/chittaCheckNewRural_en.html?lan=en")
    content = response.content

    root = html.fromstring(content)

    districts = []
    for district_element in root.xpath("//select[@id='ddlDistrict']/option"):
        district = {
            "name": district_element.text.strip(),
        }
        districts.append(district)

    talukas, villages = [], []
    for taluka_element in root.xpath("//select[@id='ddlTaluk']/option"):
        taluka = {
            "name": taluka_element.text.strip(),
        }
        talukas.append(taluka)

    for village_element in root.xpath("//select[@id='ddlVillage']/option"):
        village = {
            "name": village_element.text.strip(),
        }
        villages.append(village)

    return districts, talukas, villages
