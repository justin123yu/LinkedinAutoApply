'''
Migration script to export current personal information from personals.py and questions.py to personal_config.json

Run this script once to migrate your existing configuration to JSON format.
After running, your personal information will be stored in config/personal_config.json (which is gitignored).
'''

import os
import sys
import json

# Add parent directory to path so we can import config modules
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import current values (these will use defaults if JSON doesn't exist yet)
from config.personals import (
    first_name, middle_name, last_name, phone_number, current_city,
    street, state, zipcode, country, ethnicity, gender, disability_status, veteran_status
)

from config.questions import (
    years_of_experience, require_visa, website, linkedIn, us_citizenship,
    desired_salary, current_ctc, notice_period, linkedin_headline, linkedin_summary,
    cover_letter, user_information_all, recent_employer, confidence_level
)

# Create the JSON structure
personal_config = {
    "personal_info": {
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name,
        "phone_number": phone_number,
        "current_city": current_city,
        "street": street,
        "state": state,
        "zipcode": zipcode,
        "country": country
    },
    "demographic_info": {
        "ethnicity": ethnicity,
        "gender": gender,
        "disability_status": disability_status,
        "veteran_status": veteran_status
    },
    "application_info": {
        "years_of_experience": years_of_experience,
        "require_visa": require_visa,
        "website": website,
        "linkedIn": linkedIn,
        "us_citizenship": us_citizenship,
        "desired_salary": desired_salary,
        "current_ctc": current_ctc,
        "notice_period": notice_period,
        "linkedin_headline": linkedin_headline,
        "linkedin_summary": linkedin_summary,
        "cover_letter": cover_letter,
        "user_information_all": user_information_all,
        "recent_employer": recent_employer,
        "confidence_level": confidence_level
    }
}

# Write to JSON file
config_path = os.path.join(os.path.dirname(__file__), 'personal_config.json')

if os.path.exists(config_path):
    response = input(f"personal_config.json already exists. Overwrite? (y/n): ")
    if response.lower() != 'y':
        print("Migration cancelled.")
        exit(0)

try:
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(personal_config, f, indent=2, ensure_ascii=False)
    print(f"✓ Successfully migrated personal information to {config_path}")
    print("✓ Your personal information is now stored in JSON format")
    print("✓ This file is gitignored and will not be committed to GitHub")
    print("\n⚠ IMPORTANT: Review the JSON file and update any placeholder values!")
except Exception as e:
    print(f"✗ Error creating personal_config.json: {e}")
    exit(1)

