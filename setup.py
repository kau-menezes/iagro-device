import os
from dotenv import load_dotenv
import requests
import qrcode
import json

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
        if res.json()['companyId'] is not None:
            company_id = res['companyId']
            print(f"🌱 Device linked to company {company_id}")
            set_value("company_id", company_id)
            
    else:
        print(f"Response not considered. Status: {res.status_code}")
            
            
def check_connection():
    
    # checking device's connection to a company
    try:
        req = requests.get(f"{API_URL}/{DEVICE_CODE}")
        
        if (req.ok):
            if req.json()['companyId'] is not None:
                return(0)
            
            else:
                return(-1)
        
        return(-1)
    
    except:
        print("Could not contact the API.")
        return None
    
def generate_qrcode():
    img = qrcode.make(FRONT_URL)
    img.save("assets/link/qrcode.png")