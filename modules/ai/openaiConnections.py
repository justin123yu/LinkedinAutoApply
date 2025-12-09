'''
Author:     Sai Vignesh Golla
LinkedIn:   https://www.linkedin.com/in/saivigneshgolla/

Copyright (C) 2024 Sai Vignesh Golla

License:    GNU Affero General Public License
            https://www.gnu.org/licenses/agpl-3.0.en.html
            
GitHub:     https://github.com/GodsScion/Auto_job_applier_linkedIn

version:    24.12.29.12.30
'''


from config.secrets import *
from config.settings import showAiErrorAlerts
from config.personals import ethnicity, gender, disability_status, veteran_status
from config.questions import *
from config.search import security_clearance, did_masters

from modules.helpers import print_lg, critical_error_log, convert_to_json, cross_platform_confirm
from modules.ai.prompts import *
from openai import OpenAI
from openai.types.model import Model
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from typing import Iterator, Literal, Optional, Union, List


apiCheckInstructions = """

1. Make sure your AI API connection details like url, key, model names, etc are correct.
2. If you're using an local LLM, please check if the server is running.
3. Check if appropriate LLM and Embedding models are loaded and running.

Open `secret.py` in `/config` folder to configure your AI API connections.

ERROR:
"""

# Function to show an AI error alert
def ai_error_alert(message: str, stackTrace: str, title: str = "AI Connection Error") -> None:
    """
    Function to show an AI error alert and log it.
    """
    global showAiErrorAlerts
    if showAiErrorAlerts:
        if "Pause AI error alerts" == cross_platform_confirm(f"{message}{stackTrace}\n", title, ["Pause AI error alerts", "Okay Continue"]):
            showAiErrorAlerts = False
    critical_error_log(message, stackTrace)


# Function to check if an error occurred
def ai_check_error(response: Union[ChatCompletion, ChatCompletionChunk]) -> None:
    """
    Function to check if an error occurred.
    * Takes in `response` of type `ChatCompletion` or `ChatCompletionChunk`
    * Raises a `ValueError` if an error is found
    * Works with both official OpenAI API and OpenAI-compatible APIs (like GPT-OSS)
    """
    # Check if model_extra exists and has an error (some APIs may not have this attribute)
    if hasattr(response, 'model_extra') and response.model_extra and response.model_extra.get("error"):
        raise ValueError(
            f'Error occurred with API: "{response.model_extra.get("error")}"'
        )


# Function to create an OpenAI client
def ai_create_openai_client() -> OpenAI:
    """
    Function to create an OpenAI client.
    * Works with official OpenAI API and OpenAI-compatible APIs (like GPT-OSS, Ollama, etc.)
    * Takes no arguments
    * Returns an `OpenAI` object
    """
    try:
        print_lg("Creating OpenAI client...")
        if not use_AI:
            raise ValueError("AI is not enabled! Please enable it by setting `use_AI = True` in `secrets.py` in `config` folder.")
        
        client = OpenAI(base_url=llm_api_url, api_key=llm_api_key)

        # Try to get models list - some OpenAI-compatible APIs may not support this endpoint
        models = ai_get_models_list(client)
        if "error" in models:
            # If models list fails, it might be an OpenAI-compatible API that doesn't support /models endpoint
            # Log warning but continue - we'll validate the model when we try to use it
            print_lg(f"Warning: Could not retrieve models list. This is normal for some OpenAI-compatible APIs (like GPT-OSS, Ollama, etc.).")
            print_lg(f"Will attempt to use model '{llm_model}' directly.")
        elif len(models) == 0:
            raise ValueError("No models are available!")
        elif llm_model not in [model.id for model in models]:
            # Check if it's a partial match (some APIs return model names differently)
            model_ids = [model.id for model in models]
            if not any(llm_model.lower() in model_id.lower() or model_id.lower() in llm_model.lower() for model_id in model_ids):
                print_lg(f"Warning: Model `{llm_model}` not found in available models list.")
                print_lg(f"Available models: {model_ids}")
                print_lg(f"Will attempt to use model '{llm_model}' anyway (this may work with OpenAI-compatible APIs).")
        
        print_lg("---- SUCCESSFULLY CREATED OPENAI CLIENT! ----")
        print_lg(f"Using API URL: {llm_api_url}")
        print_lg(f"Using Model: {llm_model}")
        print_lg("Check './config/secrets.py' for more details.\n")
        print_lg("---------------------------------------------")

        return client
    except Exception as e:
        ai_error_alert(f"Error occurred while creating OpenAI client. {apiCheckInstructions}", e)


# Function to close an OpenAI client
def ai_close_openai_client(client: OpenAI) -> None:
    """
    Function to close an OpenAI client.
    * Takes in `client` of type `OpenAI`
    * Returns no value
    """
    try:
        if client:
            print_lg("Closing OpenAI client...")
            client.close()
    except Exception as e:
        ai_error_alert("Error occurred while closing OpenAI client.", e)



# Function to get list of models available in OpenAI API
def ai_get_models_list(client: OpenAI) -> List[Union[Model, str]]:
    """
    Function to get list of models available in OpenAI API.
    * Works with both official OpenAI API and OpenAI-compatible APIs (like GPT-OSS, Ollama, etc.)
    * Takes in `client` of type `OpenAI`
    * Returns a `list` object or ["error", exception] if the endpoint is not supported
    """
    try:
        print_lg("Getting AI models list...")
        if not client: raise ValueError("Client is not available!")
        models = client.models.list()
        # Only check for errors if model_extra exists (some APIs may not have this)
        if hasattr(models, 'model_extra') and models.model_extra:
            ai_check_error(models)
        print_lg("Available models:")
        print_lg(models.data, pretty=True)
        return models.data
    except Exception as e:
        # Some OpenAI-compatible APIs (like GPT-OSS, Ollama) may not support the /models endpoint
        # This is not necessarily an error - we'll continue and validate when we try to use the model
        critical_error_log("Could not retrieve models list (this is normal for some OpenAI-compatible APIs).", e)
        return ["error", e]

def model_supports_temperature(model_name: str) -> bool:
    """
    Checks if the specified model supports the temperature parameter.
    
    Args:
        model_name (str): The name of the AI model.
    
    Returns:
        bool: True if the model supports temperature adjustments, otherwise False.
    """
    return model_name in ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o", "gpt-4o-mini"]

def model_supports_json_schema(model_name: str) -> bool:
    """
    Checks if the specified model supports json_schema response format.
    Only GPT-4o and newer models support json_schema.
    GPT-3.5-turbo and older models only support json_object.
    
    Args:
        model_name (str): The name of the AI model.
    
    Returns:
        bool: True if the model supports json_schema, False otherwise.
    """
    # Only GPT-4o and newer models support json_schema
    # GPT-3.5-turbo and GPT-4 (non-o) only support json_object
    json_schema_models = [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",  # Some versions may support it
    ]
    
    # Check if model name contains any of the supported models
    model_lower = model_name.lower()
    for supported_model in json_schema_models:
        if supported_model in model_lower:
            return True
    
    return False

# Function to get chat completion from OpenAI API
def ai_completion(client: OpenAI, messages: List[dict], response_format: Optional[dict] = None, temperature: float = 0, stream: bool = stream_output) -> Union[dict, ValueError]:
    """
    Function that completes a chat and prints and formats the results of the OpenAI API calls.
    * Takes in `client` of type `OpenAI`
    * Takes in `messages` of type `list[dict]`. Example: `[{"role": "user", "content": "Hello"}]`
    * Takes in `response_format` of type `dict` for JSON representation, default is `None`
    * Takes in `temperature` of type `float` for temperature, default is `0`
    * Takes in `stream` of type `bool` to indicate if it's a streaming call or not
    * Returns a `dict` object representing JSON response, will try to convert to JSON if `response_format` is given
    """
    if not client: raise ValueError("Client is not available!")

    params = {"model": llm_model, "messages": messages, "stream": stream}

    if model_supports_temperature(llm_model):
        params["temperature"] = temperature
    if response_format and llm_spec in ["openai", "openai-like"]:
        # Only add response_format if it's a simple dict (not json_schema which may not be supported)
        # json_schema is only supported by certain models, so we'll handle it in the calling function
        if isinstance(response_format, dict):
            params["response_format"] = response_format

    completion = client.chat.completions.create(**params)

    result = ""
    
    # Log response
    if stream:
        print_lg("--STREAMING STARTED")
        for chunk in completion:
            ai_check_error(chunk)
            # Handle cases where delta might not have content attribute
            if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                chunkMessage = chunk.choices[0].delta.content if hasattr(chunk.choices[0].delta, 'content') else None
                if chunkMessage != None:
                    result += chunkMessage
                print_lg(chunkMessage or "", end="", flush=True)
        print_lg("\n--STREAMING COMPLETE")
    else:
        ai_check_error(completion)
        # Handle response extraction - works with both OpenAI and OpenAI-compatible APIs
        if hasattr(completion, 'choices') and len(completion.choices) > 0:
            if hasattr(completion.choices[0], 'message') and hasattr(completion.choices[0].message, 'content'):
                result = completion.choices[0].message.content
            else:
                raise ValueError("Unexpected response format from API. The response does not contain the expected structure.")
        else:
            raise ValueError("Unexpected response format from API. No choices found in response.")
    
    if response_format:
        result = convert_to_json(result)
    
    print_lg("\nAI Answer to Question:\n")
    print_lg(result, pretty=response_format)
    return result


def ai_extract_skills(client: OpenAI, job_description: str, stream: bool = stream_output) -> Union[dict, ValueError]:
    """
    Function to extract skills from job description using OpenAI API.
    * Takes in `client` of type `OpenAI`
    * Takes in `job_description` of type `str`
    * Takes in `stream` of type `bool` to indicate if it's a streaming call
    * Returns a `dict` object representing JSON response
    * Handles models that don't support json_schema by falling back to json_object or text mode
    * GPT-3.5-turbo uses json_object directly (doesn't support json_schema)
    """
    print_lg("-- EXTRACTING SKILLS FROM JOB DESCRIPTION")
    try:        
        prompt = extract_skills_prompt.format(job_description)
        messages = [{"role": "user", "content": prompt}]
        
        # Check if model supports json_schema (GPT-4o, GPT-4 Turbo) or only json_object (GPT-3.5-turbo)
        if model_supports_json_schema(llm_model):
            # Try json_schema first (supported by GPT-4o, GPT-4 Turbo, etc.)
            try:
                return ai_completion(client, messages, response_format=extract_skills_response_format, stream=stream)
            except Exception as json_schema_error:
                error_str = str(json_schema_error).lower()
                # Check if it's the json_schema not supported error (common with GPT-OSS and local models)
                is_json_schema_error = (
                    "json_schema" in error_str or 
                    "response_format" in error_str or 
                    "400" in error_str or
                    "not supported" in error_str or
                    "invalid parameter" in error_str
                )
                
                if is_json_schema_error:
                    print_lg("Warning: Model doesn't support json_schema format. Falling back to json_object format...")
                    # Fall back to json_object format (more widely supported)
                    try:
                        json_object_format = {"type": "json_object"}
                        return ai_completion(client, messages, response_format=json_object_format, stream=stream)
                    except Exception as json_object_error:
                        error_str_obj = str(json_object_error).lower()
                        is_json_object_error = (
                            "json_object" in error_str_obj or 
                            "response_format" in error_str_obj or 
                            "400" in error_str_obj or
                            "not supported" in error_str_obj
                        )
                        if is_json_object_error:
                            print_lg("Warning: Model doesn't support json_object format. Falling back to text mode...")
                            # Final fallback: use text mode and parse JSON from response
                            prompt_with_json_instruction = prompt + "\n\nIMPORTANT: Respond with ONLY a valid JSON object in the exact format specified above. Do not include any markdown formatting, explanations, or additional text."
                            messages_fallback = [{"role": "user", "content": prompt_with_json_instruction}]
                            result = ai_completion(client, messages_fallback, response_format=None, stream=stream)
                            # Try to parse as JSON
                            if isinstance(result, str):
                                return convert_to_json(result)
                            return result
                        else:
                            # Different error, re-raise
                            raise json_object_error
                else:
                    # Re-raise if it's a different error
                    raise json_schema_error
        else:
            # GPT-3.5-turbo and models that don't support json_schema - use json_object directly
            print_lg(f"Using json_object format for {llm_model} (json_schema not supported)...")
            try:
                json_object_format = {"type": "json_object"}
                return ai_completion(client, messages, response_format=json_object_format, stream=stream)
            except Exception as json_object_error:
                error_str_obj = str(json_object_error).lower()
                is_json_object_error = (
                    "json_object" in error_str_obj or 
                    "response_format" in error_str_obj or 
                    "400" in error_str_obj or
                    "not supported" in error_str_obj
                )
                if is_json_object_error:
                    print_lg("Warning: Model doesn't support json_object format. Falling back to text mode...")
                    # Final fallback: use text mode and parse JSON from response
                    prompt_with_json_instruction = prompt + "\n\nIMPORTANT: Respond with ONLY a valid JSON object in the exact format specified above. Do not include any markdown formatting, explanations, or additional text."
                    messages_fallback = [{"role": "user", "content": prompt_with_json_instruction}]
                    result = ai_completion(client, messages_fallback, response_format=None, stream=stream)
                    # Try to parse as JSON
                    if isinstance(result, str):
                        return convert_to_json(result)
                    return result
                else:
                    # Different error, re-raise
                    raise json_object_error
    except Exception as e:
        ai_error_alert(f"Error occurred while extracting skills from job description. {apiCheckInstructions}", e)


##> ------ Dheeraj Deshwal : dheeraj9811 Email:dheeraj20194@iiitd.ac.in/dheerajdeshwal9811@gmail.com - Feature ------
def ai_answer_question(
    client: OpenAI, 
    question: str, options: Optional[List[str]] = None, question_type: Literal['text', 'textarea', 'single_select', 'multiple_select'] = 'text', 
    job_description: str = None, about_company: str = None, user_information_all: str = None,
    stream: bool = stream_output
) -> Union[dict, ValueError]:
    """
    Function to generate AI-based answers for questions in a form.
    
    Parameters:
    - `client`: OpenAI client instance.
    - `question`: The question being answered.
    - `options`: List of options (for `single_select` or `multiple_select` questions).
    - `question_type`: Type of question (text, textarea, single_select, multiple_select) It is restricted to one of four possible values.
    - `job_description`: Optional job description for context.
    - `about_company`: Optional company details for context.
    - `user_information_all`: information about you, AI cna use to answer question eg: Resume-like user information.
    - `stream`: Whether to use streaming AI completion.
    
    Returns:
    - `str`: The AI-generated answer.
    """

    print_lg("-- ANSWERING QUESTION using AI")
    try:
        prompt = ai_answer_prompt.format(user_information_all or "N/A", question)
         # Append optional details if provided
        if job_description and job_description != "Unknown":
            prompt += f"\nJob Description:\n{job_description}"
        if about_company and about_company != "Unknown":
            prompt += f"\nAbout the Company:\n{about_company}"

        messages = [{"role": "user", "content": prompt}]
        print_lg("Prompt we are passing to AI: ", prompt)
        response =  ai_completion(client, messages, stream=stream)
        # print_lg("Response from AI: ", response)
        return response
    except Exception as e:
        ai_error_alert(f"Error occurred while answering question. {apiCheckInstructions}", e)
##<


def ai_gen_experience(
    client: OpenAI, 
    job_description: str, about_company: str, 
    required_skills: dict, user_experience: dict,
    stream: bool = stream_output
) -> Union[dict, ValueError]:
    pass



def ai_generate_resume(
    client: OpenAI, 
    job_description: str, about_company: str, required_skills: dict,
    stream: bool = stream_output
) -> Union[dict, ValueError]:
    '''
    Function to generate resume. Takes in user experience and template info from config.
    '''
    pass



def ai_generate_coverletter(
    client: OpenAI, 
    job_description: str, about_company: str, required_skills: dict,
    stream: bool = stream_output
) -> Union[dict, ValueError]:
    '''
    Function to generate resume. Takes in user experience and template info from config.
    '''
    pass



##< Evaluation Agents
def ai_evaluate_resume(
    client: OpenAI, 
    job_description: str, about_company: str, required_skills: dict,
    resume: str,
    stream: bool = stream_output
) -> Union[dict, ValueError]:
    pass



def ai_evaluate_resume(
    client: OpenAI, 
    job_description: str, about_company: str, required_skills: dict,
    resume: str,
    stream: bool = stream_output
) -> Union[dict, ValueError]:
    pass



def ai_check_job_relevance(
    client: OpenAI, 
    job_description: str, about_company: str,
    stream: bool = stream_output
) -> dict:
    pass
#>