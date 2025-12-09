'''
Author:     Sai Vignesh Golla
LinkedIn:   https://www.linkedin.com/in/saivigneshgolla/

Copyright (C) 2024 Sai Vignesh Golla

License:    GNU Affero General Public License
            https://www.gnu.org/licenses/agpl-3.0.en.html
            
GitHub:     https://github.com/GodsScion/Auto_job_applier_linkedIn

version:    24.12.29.12.30
'''


# Imports

import os
import json

from time import sleep
from random import randint
from datetime import datetime, timedelta
from pprint import pprint
from typing import Optional, Union, List

from config.settings import logs_folder_path



#### Common functions ####

#< Directories related
def make_directories(paths: List[str]) -> None:
    '''
    Function to create missing directories
    '''
    for path in paths:
        path = os.path.expanduser(path) # Expands ~ to user's home directory
        path = path.replace("//","/")
        
        # If path looks like a file path, get the directory part
        if '.' in os.path.basename(path):
            path = os.path.dirname(path)

        if not path: # Handle cases where path is empty after dirname
            continue

        try:
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True) # exist_ok=True avoids race condition
        except Exception as e:
            print(f'Error while creating directory "{path}": ', e)


def find_default_profile_directory() -> Optional[str]:
    '''
    Function to search for Chrome Profiles within default locations
    '''
    default_locations = [
        r"%LOCALAPPDATA%\Google\Chrome\User Data",
        r"%USERPROFILE%\AppData\Local\Google\Chrome\User Data",
        r"%USERPROFILE%\Local Settings\Application Data\Google\Chrome\User Data"
    ]
    for location in default_locations:
        profile_dir = os.path.expandvars(location)
        if os.path.exists(profile_dir):
            return profile_dir
    return None
#>


#< Logging related
def critical_error_log(possible_reason: str, stack_trace: Exception) -> None:
    '''
    Function to log and print critical errors along with datetime stamp
    '''
    print_lg(possible_reason, stack_trace, datetime.now(), from_critical=True)


def get_log_path():
    '''
    Function to replace '//' with '/' for logs path
    '''
    try:
        path = logs_folder_path+"/log.txt"
        return path.replace("//","/")
    except Exception as e:
        critical_error_log("Failed getting log path! So assigning default logs path: './logs/log.txt'", e)
        return "logs/log.txt"


__logs_file_path = get_log_path()


def print_lg(*msgs: Union[str, dict], end: str = "\n", pretty: bool = False, flush: bool = False, from_critical: bool = False) -> None:
    '''
    Function to log and print. **Note that, `end` and `flush` parameters are ignored if `pretty = True`**
    '''
    try:
        for message in msgs:
            pprint(message) if pretty else print(message, end=end, flush=flush)
            with open(__logs_file_path, 'a+', encoding="utf-8") as file:
                file.write(str(message) + end)
    except Exception as e:
        trail = f'Skipped saving this message: "{message}" to log.txt!' if from_critical else "We'll try one more time to log..."
        print_lg(f"log.txt in {logs_folder_path} is open or is occupied by another program! {trail}")
        if not from_critical:
            critical_error_log("Log.txt is open or is occupied by another program!", e)
#>


def buffer(speed: int=0) -> None:
    '''
    Function to wait within a period of selected random range.
    * Will not wait if input `speed <= 0`
    * Will wait within a random range of 
      - `0.6 to 1.0 secs` if `1 <= speed < 2`
      - `1.0 to 1.8 secs` if `2 <= speed < 3`
      - `1.8 to speed secs` if `3 <= speed`
    '''
    if speed<=0:
        return
    elif speed <= 1 and speed < 2:
        return sleep(randint(6,10)*0.1)
    elif speed <= 2 and speed < 3:
        return sleep(randint(10,18)*0.1)
    else:
        return sleep(randint(18,round(speed)*10)*0.1)
    

def cross_platform_alert(text: str, title: str = "Alert", button: str = "OK") -> str:
    """
    Show an alert dialog using wxPython (cross-platform, no Tkinter required).
    Falls back to console output if wxPython fails.
    """
    try:
        import wx
        
        # Use wx.MessageBox which handles app creation automatically
        wx.MessageBox(text, title, wx.OK | wx.ICON_INFORMATION)
        return button
    except (ImportError, Exception):
        # Console fallback if wxPython fails
        print(f"\n{'='*60}")
        print(f"{title}")
        print(f"{'='*60}")
        print(text)
        print(f"{'='*60}\n")
        input(f"Press Enter to continue...")
        return button

def cross_platform_confirm(text: str, title: str = "Confirm", buttons: list = None, default_button: str = None, debug_mode: bool = True) -> str:
    """
    Show a confirmation dialog using wxPython (cross-platform, no Tkinter required).
    Falls back to console input if wxPython fails.
    
    Args:
        text: Message to display
        title: Dialog title
        buttons: List of button labels (defaults to ["OK", "Cancel"] if None)
        default_button: Button to return by default (defaults to last button if None)
        debug_mode: If False, automatically returns default_button without showing dialog
    
    Returns:
        Selected button label
    """
    import os
    
    if buttons is None:
        buttons = ["OK", "Cancel"]
    
    # Check DEBUG_MODE from environment if not explicitly provided
    if debug_mode is None:
        debug_mode_str = os.getenv('DEBUG_MODE', 'True').lower()
        debug_mode = debug_mode_str == 'true'
    
    if not debug_mode:
        # Return default button or last button (usually "Proceed", "Next", "Submit", etc.)
        if default_button and default_button in buttons:
            return default_button
        # Default to last button (usually the "proceed" option)
        return buttons[-1] if buttons else "OK"
    
    try:
        import wx
        
        # Check if wx.App already exists
        app = wx.GetApp()
        if app is None:
            app = wx.App(False)  # Don't redirect stdout/stderr
        
        if len(buttons) == 2:
            # Use standard YES/NO dialog for 2 buttons
            # In wxPython MessageBox: Yes button (right/primary) = wx.ID_YES, No button (left/secondary) = wx.ID_NO
            # We map: buttons[0] = No/Skip (secondary), buttons[1] = Yes/Proceed (primary)
            style = wx.YES_NO | wx.ICON_QUESTION
            dlg = wx.MessageDialog(None, text, title, style)
            result = dlg.ShowModal()
            dlg.Destroy()
            # Only exit main loop if we created the app
            if wx.GetApp() == app:
                app.ExitMainLoop()
            # wx.ID_YES = 5103 (Yes/Proceed button), wx.ID_NO = 5104 (No/Skip button)
            # Map: YES -> buttons[1] (Proceed), NO -> buttons[0] (Skip)
            return buttons[1] if result == wx.ID_YES else buttons[0]
        else:
            # For multiple buttons, use a custom dialog
            # Make "Confirm your information" dialog bigger
            # Check for various confirm dialog titles
            title_lower = title.lower()
            if ("confirm your information" in title_lower or 
                "confirm" in title_lower and "information" in title_lower):
                dialog_size = (750, 550)
                text_min_size = (720, 400)
            else:
                dialog_size = (550, 350)
                text_min_size = (520, 200)
            
            dlg = wx.Dialog(None, title=title, size=dialog_size, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
            panel = wx.Panel(dlg)
            main_sizer = wx.BoxSizer(wx.VERTICAL)
            
            # Add message text with word wrapping in a scrollable text control
            msg_text = wx.TextCtrl(panel, value=text, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP)
            msg_text.SetMinSize(text_min_size)
            main_sizer.Add(msg_text, 1, wx.ALL | wx.EXPAND, 15)
            
            # Add buttons
            button_sizer = wx.BoxSizer(wx.HORIZONTAL)
            button_ids = []
            selected_button = [None]  # Use list to allow modification in nested function
            
            def on_button(event):
                btn_id = event.GetId()
                for bid, btn_text in button_ids:
                    if bid == btn_id:
                        selected_button[0] = btn_text
                        dlg.EndModal(wx.ID_OK)
                        return
            
            for i, btn_text in enumerate(buttons):
                btn = wx.Button(panel, label=btn_text, id=wx.ID_ANY)
                button_ids.append((btn.GetId(), btn_text))
                button_sizer.Add(btn, 0, wx.ALL, 5)
                if btn_text == default_button:
                    btn.SetDefault()
                    btn.SetFocus()
                # Bind each button individually
                btn.Bind(wx.EVT_BUTTON, on_button)
            
            main_sizer.Add(button_sizer, 0, wx.ALL | wx.CENTER, 10)
            panel.SetSizer(main_sizer)
            # Set minimum size to prevent shrinking, then set actual size
            dlg.SetMinSize(dialog_size)
            dlg.SetSize(dialog_size)
            dlg.Center()
            dlg.SetFocus()
            
            # Ensure the dialog is shown and can receive events
            result = dlg.ShowModal()
            selected = selected_button[0] if selected_button[0] else (default_button or buttons[-1])
            dlg.Destroy()
            
            # Only exit main loop if we created the app
            if wx.GetApp() == app:
                app.ExitMainLoop()
            
            return selected
            
    except (ImportError, Exception) as e:
        # Console fallback if wxPython fails
        print(f"\n{'='*60}")
        print(f"{title}")
        print(f"{'='*60}")
        print(text)
        print(f"{'='*60}")
        print("\nOptions:")
        for i, btn in enumerate(buttons, 1):
            marker = " [DEFAULT]" if btn == default_button else ""
            print(f"  {i}. {btn}{marker}")
        
        while True:
            try:
                choice = input(f"\nEnter choice (1-{len(buttons)}) or press Enter for default: ").strip()
                if not choice and default_button:
                    return default_button
                idx = int(choice) - 1
                if 0 <= idx < len(buttons):
                    return buttons[idx]
                print(f"Please enter a number between 1 and {len(buttons)}")
            except ValueError:
                print("Please enter a valid number")
            except KeyboardInterrupt:
                return buttons[-1]  # Return last button on Ctrl+C

def manual_login_retry(is_logged_in: callable, limit: int = 2) -> None:
    '''
    Function to ask and validate manual login
    '''
    count = 0
    while not is_logged_in():
        print_lg("Seems like you're not logged in!")
        button = "Confirm Login"
        message = 'After you successfully Log In, please click "{}" button below.'.format(button)
        if count > limit:
            button = "Skip Confirmation"
            message = 'If you\'re seeing this message even after you logged in, Click "{}". Seems like auto login confirmation failed!'.format(button)
        count += 1
        # Login confirmation removed - user should login manually
        if count > limit: return



def calculate_date_posted(time_string: str) -> Union[datetime, None, ValueError]:
    '''
    Function to calculate date posted from string.
    Returns datetime object | None if unable to calculate | ValueError if time_string is invalid
    Valid time string examples:
    * 10 seconds ago
    * 15 minutes ago
    * 2 hours ago
    * 1 hour ago
    * 1 day ago
    * 10 days ago
    * 1 week ago
    * 1 month ago
    * 1 year ago
    '''
    import re
    time_string = time_string.strip()
    now = datetime.now()

    match = re.search(r'(\d+)\s+(second|minute|hour|day|week|month|year)s?\s+ago', time_string, re.IGNORECASE)

    if match:
        try:
            value = int(match.group(1))
            unit = match.group(2).lower()

            if 'second' in unit:
                return now - timedelta(seconds=value)
            elif 'minute' in unit:
                return now - timedelta(minutes=value)
            elif 'hour' in unit:
                return now - timedelta(hours=value)
            elif 'day' in unit:
                return now - timedelta(days=value)
            elif 'week' in unit:
                return now - timedelta(weeks=value)
            elif 'month' in unit:
                return now - timedelta(days=value * 30)  # Approximation
            elif 'year' in unit:
                return now - timedelta(days=value * 365)  # Approximation
        except (ValueError, IndexError):
            # Fallback for cases where parsing fails
            pass
    
    # If regex doesn't match, or parsing failed, return None.
    # This will skip jobs where the date can't be determined, preventing crashes.
    return None


def convert_to_lakhs(value: str) -> str:
    '''
    Converts str value to lakhs, no validations are done except for length and stripping.
    Examples:
    * "100000" -> "1.00"
    * "101,000" -> "10.1," Notice ',' is not removed 
    * "50" -> "0.00"
    * "5000" -> "0.05" 
    '''
    value = value.strip()
    l = len(value)
    if l > 0:
        if l > 5:
            value = value[:l-5] + "." + value[l-5:l-3]
        else:
            value = "0." + "0"*(5-l) + value[:2]
    return value


def convert_to_json(data) -> dict:
    '''
    Function to convert data to JSON, if unsuccessful, returns `{"error": "Unable to parse the response as JSON", "data": data}`
    '''
    try:
        result_json = json.loads(data)
        return result_json
    except json.JSONDecodeError:
        return {"error": "Unable to parse the response as JSON", "data": data}


def truncate_for_csv(data, max_length: int = 131000, suffix: str = "...[TRUNCATED]") -> str:
    '''
    Function to truncate data for CSV writing to avoid field size limit errors.
    * Takes in `data` of any type and converts to string
    * Takes in `max_length` of type `int` - maximum allowed length (default: 131000, leaving room for suffix)
    * Takes in `suffix` of type `str` - text to append when truncated
    * Returns truncated string if data exceeds max_length
    '''
    try:
        # Convert data to string
        str_data = str(data) if data is not None else ""
        
        # If within limit, return as-is
        if len(str_data) <= max_length:
            return str_data
        
        # Truncate and add suffix
        truncated = str_data[:max_length - len(suffix)] + suffix
        return truncated
    except Exception as e:
        return f"[ERROR CONVERTING DATA: {e}]"