'''
Author:     Sai Vignesh Golla
LinkedIn:   https://www.linkedin.com/in/saivigneshgolla/

Copyright (C) 2024 Sai Vignesh Golla

License:    GNU Affero General Public License
            https://www.gnu.org/licenses/agpl-3.0.en.html
            
GitHub:     https://github.com/GodsScion/Auto_job_applier_linkedIn

version:    24.12.29.12.30
'''




# from config.XdepricatedX import *

__validation_file_path = ""

def check_int(var: int, var_name: str, min_value: int=0) -> bool | TypeError | ValueError:
    if not isinstance(var, int): raise TypeError(f'The variable "{var_name}" in "{__validation_file_path}" must be an Integer!\nReceived "{var}" of type "{type(var)}" instead!\n\nSolution:\nPlease open "{__validation_file_path}" and update "{var_name}" to be an Integer.\nExample: `{var_name} = 10`\n\nNOTE: Do NOT surround Integer values in quotes ("10")X !\n\n')
    if var < min_value: raise ValueError(f'The variable "{var_name}" in "{__validation_file_path}" expects an Integer greater than or equal to `{min_value}`! Received `{var}` instead!\n\nSolution:\nPlease open "{__validation_file_path}" and update "{var_name}" accordingly.')
    return True

def check_boolean(var: bool, var_name: str) -> bool | ValueError:
    if var == True or var == False: return True
    raise ValueError(f'The variable "{var_name}" in "{__validation_file_path}" expects a Boolean input `True` or `False`, not "{var}" of type "{type(var)}" instead!\n\nSolution:\nPlease open "{__validation_file_path}" and update "{var_name}" to either `True` or `False` (case-sensitive, T and F must be CAPITAL/uppercase).\nExample: `{var_name} = True`\n\nNOTE: Do NOT surround Boolean values in quotes ("True")X !\n\n')

def check_string(var: str, var_name: str, options: list=[], min_length: int=0) -> bool | TypeError | ValueError:
    if not isinstance(var, str): raise TypeError(f'Invalid input for {var_name}. Expecting a String!')
    if min_length > 0 and len(var) < min_length: raise ValueError(f'Invalid input for {var_name}. Expecting a String of length at least {min_length}!')
    if len(options) > 0 and var not in options: raise ValueError(f'Invalid input for {var_name}. Expecting a value from {options}, not {var}!')
    return True

def check_list(var: list, var_name: str, options: list=[], min_length: int=0) -> bool | TypeError | ValueError:
    if not isinstance(var, list): 
        raise TypeError(f'Invalid input for {var_name}. Expecting a List!')
    if len(var) < min_length: raise ValueError(f'Invalid input for {var_name}. Expecting a List of length at least {min_length}!')
    for element in var:
        if not isinstance(element, str): raise TypeError(f'Invalid input for {var_name}. All elements in the list must be strings!')
        if len(options) > 0 and element not in options: raise ValueError(f'Invalid input for {var_name}. Expecting all elements to be values from {options}. This "{element}" is NOT in options!')
    return True



from config.personals import *
def validate_personals() -> None | ValueError | TypeError:
    '''
    Validates all variables in the `/config/personals.py` file.
    '''
    global __validation_file_path
    __validation_file_path = "config/personals.py"

    check_string(first_name, "first_name", min_length=1)
    check_string(middle_name, "middle_name")
    check_string(last_name, "last_name", min_length=1)

    check_string(phone_number, "phone_number", min_length=10)

    check_string(current_city, "current_city")
    
    check_string(street, "street")
    check_string(state, "state")
    check_string(zipcode, "zipcode")
    check_string(country, "country")
    
    check_string(ethnicity, "ethnicity", ["Decline", "Hispanic/Latino", "American Indian or Alaska Native", "Asian", "Black or African American", "Native Hawaiian or Other Pacific Islander", "White", "Other"],  min_length=0)
    check_string(gender, "gender", ["Male", "Female", "Other", "Decline", ""])
    check_string(disability_status, "disability_status", ["Yes", "No", "Decline"])
    check_string(veteran_status, "veteran_status", ["Yes", "No", "Decline"])



from config.questions import *
def validate_questions() -> None | ValueError | TypeError:
    '''
    Validates all variables in the `/config/questions.py` file.
    '''
    global __validation_file_path
    __validation_file_path = "config/questions.py"

    check_string(default_resume_path, "default_resume_path")
    check_string(years_of_experience, "years_of_experience")
    check_string(require_visa, "require_visa", ["Yes", "No"])
    check_string(website, "website")
    check_string(linkedIn, "linkedIn")
    check_int(desired_salary, "desired_salary")
    check_string(us_citizenship, "us_citizenship", ["U.S. Citizen/Permanent Resident", "Non-citizen allowed to work for any employer", "Non-citizen allowed to work for current employer", "Non-citizen seeking work authorization", "Canadian Citizen/Permanent Resident", "Other"])
    check_string(linkedin_headline, "linkedin_headline")
    check_int(notice_period, "notice_period")
    check_int(current_ctc, "current_ctc")
    check_string(linkedin_summary, "linkedin_summary")
    check_string(cover_letter, "cover_letter")
    check_string(recent_employer, "recent_employer")
    check_string(confidence_level, "confidence_level")

    check_boolean(pause_before_submit, "pause_before_submit")
    check_boolean(pause_at_failed_question, "pause_at_failed_question")
    check_boolean(overwrite_previous_answers, "overwrite_previous_answers")


from config.search import *
def validate_search() -> None | ValueError | TypeError:
    '''
    Validates all variables in the `/config/search.py` file.
    '''
    global __validation_file_path
    __validation_file_path = "config/search.py"

    check_list(search_terms, "search_terms", min_length=1)
    check_string(search_location, "search_location")
    check_int(switch_number, "switch_number", 1)
    check_boolean(randomize_search_order, "randomize_search_order")

    check_string(sort_by, "sort_by", ["", "Most recent", "Most relevant"])
    check_string(date_posted, "date_posted", ["", "Any time", "Past month", "Past week", "Past 24 hours"])
    check_string(salary, "salary")

    check_boolean(easy_apply_only, "easy_apply_only")

    check_list(experience_level, "experience_level", ["Internship", "Entry level", "Associate", "Mid-Senior level", "Director", "Executive"])
    check_list(job_type, "job_type", ["Full-time", "Part-time", "Contract", "Temporary", "Volunteer", "Internship", "Other"])
    check_list(on_site, "on_site", ["On-site", "Remote", "Hybrid"])

    check_list(companies, "companies")
    check_list(location, "location")
    check_list(industry, "industry")
    check_list(job_function, "job_function")
    check_list(job_titles, "job_titles")
    check_list(benefits, "benefits")
    check_list(commitments, "commitments")

    check_boolean(under_10_applicants, "under_10_applicants")
    check_boolean(in_your_network, "in_your_network")
    check_boolean(fair_chance_employer, "fair_chance_employer")

    check_boolean(pause_after_filters, "pause_after_filters")

    check_list(about_company_bad_words, "about_company_bad_words")
    check_list(about_company_good_words, "about_company_good_words")
    check_list(bad_words, "bad_words")
    check_boolean(security_clearance, "security_clearance")
    check_boolean(did_masters, "did_masters")
    check_int(current_experience, "current_experience", -1)




from config.secrets import *
import os

def check_llm_env_vars() -> dict | None:
    '''
    Checks if required LLM environment variables are set when use_AI is True.
    Returns a dict with status information, or None if AI is disabled.
    Raises ValueError if required vars are missing when AI is enabled.
    '''
    if not use_AI:
        return None  # Skip LLM validation if AI is not enabled
    
    # Check required environment variables for LLM usage
    env_vars = {
        "USE_AI": os.getenv("USE_AI", "False"),
        "AI_PROVIDER": os.getenv("AI_PROVIDER", "openai"),
        "LLM_API_URL": os.getenv("LLM_API_URL"),
        "LLM_MODEL": os.getenv("LLM_MODEL"),
        "LLM_API_KEY": os.getenv("LLM_API_KEY", "not-needed"),
        "LLM_SPEC": os.getenv("LLM_SPEC", "openai"),
        "STREAM_OUTPUT": os.getenv("STREAM_OUTPUT", "False"),
    }
    
    # Check which variables are set
    missing_vars = []
    for var_name, var_value in env_vars.items():
        if var_name in ["LLM_API_URL", "LLM_MODEL"]:
            if not var_value or (isinstance(var_value, str) and var_value.strip() == ""):
                missing_vars.append(var_name)
    
    if missing_vars:
        raise ValueError(
            f'LLM tool is enabled (USE_AI=True) but required environment variables are missing: {", ".join(missing_vars)}\n\n'
            f'Please set these in your .env file or as environment variables:\n'
            f'  - LLM_API_URL: Your AI API endpoint URL\n'
            f'  - LLM_MODEL: Your AI model name\n'
            f'  - LLM_API_KEY: Your API key (or "not-needed" for local LLMs like Ollama)\n'
            f'  - AI_PROVIDER: "openai", "deepseek", or "gemini"\n\n'
            f'Example for OpenAI:\n'
            f'  USE_AI=True\n'
            f'  LLM_API_URL=https://api.openai.com/v1/\n'
            f'  LLM_MODEL=gpt-3.5-turbo\n'
            f'  LLM_API_KEY=sk-your-key-here\n'
            f'  AI_PROVIDER=openai\n\n'
            f'Example for GPT-OSS (OpenAI-compatible):\n'
            f'  USE_AI=True\n'
            f'  LLM_API_URL=http://127.0.0.1:1234/v1/\n'
            f'  LLM_MODEL=your-model-name\n'
            f'  LLM_API_KEY=not-needed\n'
            f'  AI_PROVIDER=openai'
        )
    
    # Validate AI_PROVIDER if set
    ai_provider_env = env_vars.get("AI_PROVIDER", "").lower()
    if ai_provider_env and ai_provider_env not in ["openai", "deepseek", "gemini"]:
        raise ValueError(
            f'Invalid AI_PROVIDER value: "{ai_provider_env}". Must be one of: "openai", "deepseek", "gemini"'
        )
    
    # Return status information
    return {
        "enabled": True,
        "provider": ai_provider_env,
        "api_url": env_vars.get("LLM_API_URL", "Not set"),
        "model": env_vars.get("LLM_MODEL", "Not set"),
        "api_key_set": bool(env_vars.get("LLM_API_KEY") and env_vars.get("LLM_API_KEY") != "not-needed"),
        "stream_output": env_vars.get("STREAM_OUTPUT", "False").lower() == "true",
    }

def validate_secrets() -> None | ValueError | TypeError:
    '''
    Validates all variables in the `/config/secrets.py` file.
    Also checks environment variables for LLM tool usage.
    '''
    global __validation_file_path
    __validation_file_path = "config/secrets.py"

    check_string(username, "username", min_length=5)
    check_string(password, "password", min_length=5)

    check_boolean(use_AI, "use_AI")
    
    # Check LLM environment variables if AI is enabled
    if use_AI:
        check_llm_env_vars()
    
    check_string(llm_api_url, "llm_api_url", min_length=5)
    check_string(llm_api_key, "llm_api_key")
    # check_string(llm_embedding_model, "llm_embedding_model")
    check_boolean(stream_output, "stream_output")
    
    ##> ------ Yang Li : MARKYangL - Feature ------
    # Validate AI provider configuration
    check_string(ai_provider, "ai_provider", ["openai", "deepseek", "gemini"])

    ##> ------ Tim L : tulxoro - Refactor ------
    if ai_provider == "deepseek":
        check_string(llm_model, "deepseek_model", ["deepseek-chat", "deepseek-reasoner"])
    elif ai_provider == "gemini":
        # Gemini models are validated in gemini_create_client()
        check_string(llm_model, "llm_model")
    else:
        # OpenAI or OpenAI-compatible (like GPT-OSS, Ollama, etc.)
        check_string(llm_model, "llm_model")
    ##<

    ##<



from config.settings import *
def validate_settings() -> None | ValueError | TypeError:
    '''
    Validates all variables in the `/config/settings.py` file.
    '''
    global __validation_file_path
    __validation_file_path = "config/settings.py"

    check_boolean(close_tabs, "close_tabs")
    check_boolean(follow_companies, "follow_companies")
    # check_boolean(connect_hr, "connect_hr")
    # check_string(connect_request_message, "connect_request_message", min_length=10)

    check_boolean(run_non_stop, "run_non_stop")
    check_boolean(alternate_sortby, "alternate_sortby")
    check_boolean(cycle_date_posted, "cycle_date_posted")
    check_boolean(stop_date_cycle_at_24hr, "stop_date_cycle_at_24hr")
    
    # check_string(generated_resume_path, "generated_resume_path", min_length=1)

    check_string(file_name, "file_name", min_length=1)
    check_string(failed_file_name, "failed_file_name", min_length=1)
    check_string(logs_folder_path, "logs_folder_path", min_length=1)

    check_int(click_gap, "click_gap", 0)

    check_boolean(run_in_background, "run_in_background")
    check_boolean(disable_extensions, "disable_extensions")
    check_boolean(safe_mode, "safe_mode")
    check_boolean(smooth_scroll, "smooth_scroll")
    check_boolean(keep_screen_awake, "keep_screen_awake")
    check_boolean(stealth_mode, "stealth_mode")




def validate_config() -> bool | ValueError | TypeError:
    '''
    Runs all validation functions to validate all variables in the config files.
    '''
    validate_personals()
    validate_questions()
    validate_search()
    validate_secrets()
    validate_settings()

    # validate_String(chatGPT_username, "chatGPT_username")
    # validate_String(chatGPT_password, "chatGPT_password")
    # validate_String(chatGPT_resume_chat_title, "chatGPT_resume_chat_title")
    return True

