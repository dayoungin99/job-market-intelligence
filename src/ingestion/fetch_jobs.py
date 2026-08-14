import requests
from dotenv import load_dotenv
import os
import logging
import json
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")
BASE_URL = "https://api.adzuna.com/v1/api/jobs/us/search/1"

def fetch_jobs(keyword):
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": keyword,
        "results_per_page": 5
    }

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=30
        )
        
        response.raise_for_status()
        
        data = response.json()
        logging.info(f"Successfully fetched {len(data['results'])} jobs.")
        return data
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None

jobs_collected = 0
file_path = "Not Saved"

keyword = "data scientist"
data = fetch_jobs(keyword)

def validate_response(data):    
    if data is None:
        logging.warning("No job data available.")
        return False
        
    if "results" not in data:
        logging.warning("No job information available.")
        return False
        
    if len(data["results"]) == 0:
        logging.warning("No job found.")
        return False
    
    required_fields = ["id", "title", "company", "location"]

    for job in data["results"]:
        for field in required_fields:
            if field not in job:
                logging.warning(f"Missing required field: {field}")
                return False
    
    return True
        
def save_raw_json(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"data/raw/jobs_{timestamp}.json"
   
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
    
    return file_path
        
if data is not None:
    jobs_collected = len(data["results"])
    file_path = save_raw_json(data)
    logging.info(f"Raw JSON saved to {file_path}")
    
if validate_response(data):
    for job in data["results"]:
        print(f"{job['title']} - {job['company']['display_name']}")

print(f"""
      ========================
      Job Collection Summary
      ========================
      Keyword: {keyword}
      Jobs Collected: {jobs_collected}
      Raw JSON Saved: {file_path}
      """)