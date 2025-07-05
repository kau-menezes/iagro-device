import os
from dotenv import load_dotenv
import requests
import qrcode
import json
import geopy
from geopy.geocoders import Nominatim
from datetime import datetime

from utils.settings_manager import set_value

load_dotenv()

API_URL = os.getenv('API')
DEVICE_CODE = os.getenv('CODE')
FRONT_URL = os.getenv('FRONT_URL')

def get_device_existence():    
    try:
        req = requests.get(f"{API_URL}/{DEVICE_CODE}")
        print(req)
        return(req)
        
    except:
        print("Could not contact the API.")
        return None
    
def check_existence():
    
    res = get_device_existence()
    
    if res is None:
        print("❌ Could not contact the API. Please check your internet connection.")
        return -1   
    
    if (res.status_code == 404):
        try:
            body = {"code": DEVICE_CODE}
            req = requests.post(f'{API_URL}/signal', json=body)
            
            if not req.ok:
                print(f"❌ Could not signal device's existence. Status: {req.status_code}")
            
        except Exception as e:
            print(f"❌ Could not signal device's existence. Log: {e}")
            
        return -1
            
    elif res.status_code == 200:
        data = res.json()
        if data.get('companyId') is not None:
            company_id = data['companyId']
            print(f"🌱 Device linked to company {company_id}")
            set_value("company_id", company_id)
            
    else:
        print(f"Response not considered. Status: {res.status_code}")
            
            
def check_connection():
    
    # checking device's connection to a company
    try:
        req = requests.get(f"{API_URL}/{DEVICE_CODE}")
        
        if req.ok:
            data = req.json()
            if data.get('companyId') is not None:
                set_value("company_id", data['companyId'])
                return 0
            else:
                return -1
        
        return -1
    
    except:
        print("Could not contact the API.")
        return None
    
def generate_qrcode():
    img = qrcode.make(FRONT_URL)
    img.save("assets/link/qrcode.png")

def save_detection_log(label, folder_path):
    geolocator = Nominatim(user_agent="plant_disease_app")
    try:
        location = geolocator.geocode("me")
        coords = {
            "latitude": location.latitude if location else None,
            "longitude": location.longitude if location else None
        }
    except Exception as e:
        print(f"Error getting location: {e}")
        coords = {"latitude": None, "longitude": None}
    log_entry = {
        "datetime": datetime.now().isoformat(),
        "location": coords,
        "disease": label
    }
    results_path = os.path.join(folder_path, "results.json")
    logs = []
    if os.path.exists(results_path):
        with open(results_path, "r") as f:
            try:
                logs = json.load(f)
            except Exception:
                logs = []
    logs.append(log_entry)
    with open(results_path, "w") as f:
        json.dump(logs, f, indent=2)
    print(f"Detection log saved to {results_path}")