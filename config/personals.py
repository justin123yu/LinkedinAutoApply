'''
Author:     Sai Vignesh Golla
LinkedIn:   https://www.linkedin.com/in/saivigneshgolla/

Copyright (C) 2024 Sai Vignesh Golla

License:    GNU Affero General Public License
            https://www.gnu.org/licenses/agpl-3.0.en.html
            
GitHub:     https://github.com/GodsScion/Auto_job_applier_linkedIn

version:    2024.11.28.16.00
'''

import os
import json

###################################################### CONFIGURE YOUR TOOLS HERE ######################################################

# Load personal information from JSON file if it exists, otherwise use defaults
_personal_config_path = os.path.join(os.path.dirname(__file__), 'personal_config.json')
_personal_data = {}

if os.path.exists(_personal_config_path):
    try:
        with open(_personal_config_path, 'r', encoding='utf-8') as f:
            _personal_data = json.load(f)
    except Exception as e:
        print(f"Warning: Failed to load personal_config.json: {e}")
        print("Using default values. Please copy personal_config.json.example to personal_config.json and fill in your information.")

# >>>>>>>>>>> Easy Apply Questions & Inputs <<<<<<<<<<<

# Your legal name
first_name = _personal_data.get('personal_info', {}).get('first_name', "")
middle_name = _personal_data.get('personal_info', {}).get('middle_name', "")
last_name = _personal_data.get('personal_info', {}).get('last_name', "")

# Phone number (required), make sure it's valid.
phone_number = _personal_data.get('personal_info', {}).get('phone_number', "")

# What is your current city?
current_city = _personal_data.get('personal_info', {}).get('current_city', "")
'''
Note: If left empty as "", the bot will fill in location of jobs location.
'''

# Address, not so common question but some job applications make it required!
street = _personal_data.get('personal_info', {}).get('street', "")
state = _personal_data.get('personal_info', {}).get('state', "")
zipcode = _personal_data.get('personal_info', {}).get('zipcode', "")
country = _personal_data.get('personal_info', {}).get('country', "")

## US Equal Opportunity questions
# What is your ethnicity or race? If left empty as "", tool will not answer the question. However, note that some companies make it compulsory to be answered
ethnicity = _personal_data.get('demographic_info', {}).get('ethnicity', "")  # "Decline", "Hispanic/Latino", "American Indian or Alaska Native", "Asian", "Black or African American", "Native Hawaiian or Other Pacific Islander", "White", "Other"

# How do you identify yourself? If left empty as "", tool will not answer the question. However, note that some companies make compulsory to be answered
gender = _personal_data.get('demographic_info', {}).get('gender', "")  # "Male", "Female", "Other", "Decline" or ""

# Are you physically disabled or have a history/record of having a disability? If left empty as "", tool will not answer the question. However, note that some companies make it compulsory to be answered
disability_status = _personal_data.get('demographic_info', {}).get('disability_status', "")  # "Yes", "No", "Decline"

veteran_status = _personal_data.get('demographic_info', {}).get('veteran_status', "")  # "Yes", "No", "Decline"
##


'''
For string variables followed by comments with options, only use the answers from given options.
Some valid examples are:
* variable1 = "option1"         # "option1", "option2", "option3" or ("" to not select). Answers are case sensitive.#
* variable2 = ""                # "option1", "option2", "option3" or ("" to not select). Answers are case sensitive.#

Other variables are free text. No restrictions other than compulsory use of quotes.
Some valid examples are:
* variable3 = "Random Answer 5"         # Enter your answer. Eg: "Answer1", "Answer2"

Invalid inputs will result in an error!
'''




############################################################################################################
'''
THANK YOU for using my tool 😊! Wishing you the best in your job hunt 🙌🏻!

Sharing is caring! If you found this tool helpful, please share it with your peers 🥺. Your support keeps this project alive.

Support my work on <PATREON_LINK>. Together, we can help more job seekers.

As an independent developer, I pour my heart and soul into creating tools like this, driven by the genuine desire to make a positive impact.

Your support, whether through donations big or small or simply spreading the word, means the world to me and helps keep this project alive and thriving.

Gratefully yours 🙏🏻,
Sai Vignesh Golla
'''
############################################################################################################