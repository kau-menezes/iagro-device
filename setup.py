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
        return req
    except Exception as e:
        print(f"Could not contact the API. Log: {e}")
        return None

def check_existence():
    res = get_device_existence()
    if res is None:
        print("❌ Device existence check failed: No response from API.")
        return -1
    if res.status_code == 404:
        try:
            body = {"code": DEVICE_CODE}
            req = requests.post(f'{API_URL}/signal', json=body)
            if not req.ok:
                print(f"❌ Could not signal device's existence. Status: {req.status_code}")
        except Exception as e:
            print(f"❌ Could not signal device's existence. Log: {e}")
        return -1
    elif res.status_code == 200:
        try:
            data = res.json()
            if data.get('companyId') is not None:
                company_id = data['companyId']
                print(f"🌱 Device linked to company {company_id}")
                set_value("company_id", company_id)
        except Exception as e:
            print(f"❌ Error parsing API response: {e}")
    else:
        print(f"Response not considered. Status: {res.status_code}")

def check_connection():
    # checking device's connection to a company
    try:
        req = requests.get(f"{API_URL}/{DEVICE_CODE}")
        if req.ok:
            data = req.json()
            if data.get('companyId') is not None:
                return 0
            else:
                return -1
        return -1
    except Exception as e:
        print(f"Could not contact the API. Log: {e}")
        return None

def generate_qrcode():
    try:
        img = qrcode.make(FRONT_URL)
        img.save("assets/link/qrcode.png")
    except Exception as e:
        print(f"❌ Could not generate QR code: {e}")