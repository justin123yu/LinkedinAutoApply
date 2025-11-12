# LinkedIn Auto Apply Bot - Windows 11 Setup

## Prerequisites
- Windows 11
- Python 3.12 or later
- Google Chrome browser installed

## Step 1: Install Python (if not already installed)
1. Download Python from https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Verify installation:
   ```cmd
   python --version
   ```

## Step 2: Navigate to project directory
```cmd
cd path\to\your\project\directory
```
Replace `path\to\your\project\directory` with your actual project path.

## Step 3: Create virtual environment
```cmd
python -m venv venv
```

## Step 4: Activate virtual environment
```cmd
venv\Scripts\activate
```

## Step 5: Upgrade pip
```cmd
python -m pip install --upgrade pip
```

## Step 6: Install dependencies
```cmd
py -m pip install -r requirements.txt
```

## Step 7: Set up .env file
```cmd
copy .env.example .env
notepad .env
```

Edit `.env` with your credentials:
- `LINKEDIN_USERNAME` - Your LinkedIn email
- `LINKEDIN_PASSWORD` - Your LinkedIn password
- `USE_AI` - Set to `True` or `False`
- `AI_PROVIDER` - `openai`, `deepseek`, or `gemini`
- `LLM_API_URL` - Your AI API URL
- `LLM_API_KEY` - Your AI API key
- `LLM_MODEL` - Model name (e.g., `gpt-3.5-turbo`)
- `TCL_LIBRARY` - (Optional) Path to Tcl library directory (e.g., `C:\Users\YourName\AppData\Local\Programs\Python\Python313\tcl\tcl8.6`)
- `TK_LIBRARY` - (Optional) Path to Tk library directory (e.g., `C:\Users\YourName\AppData\Local\Programs\Python\Python313\tcl\tk8.6`)

**Note:** TCL_LIBRARY and TK_LIBRARY are only needed if you encounter "Can't find a usable init.tcl" errors. Find your Python installation directory and locate the `tcl\tcl8.6` and `tcl\tk8.6` folders.

## Step 8: Set up personal information

### Option A: Migrate from existing configuration (if upgrading)
If you have existing personal information in `config/personals.py` and `config/questions.py`, run the migration script:

```cmd
py config\migrate_to_json.py
```

This will:
- Export your current personal information to `config/personal_config.json`
- Preserve all your existing settings
- Create a JSON file that is automatically gitignored (won't be committed to GitHub)

**Note:** If `personal_config.json` already exists, the script will ask for confirmation before overwriting.

### Option B: Create from template (if new installation)
If you're setting up for the first time:

```cmd
copy config\personal_config.json.example config\personal_config.json
notepad config\personal_config.json
```

Edit `config/personal_config.json` with your personal information:
- **personal_info**: Your name, phone, address, etc.
- **demographic_info**: Optional demographic information
- **application_info**: Years of experience, salary, LinkedIn profile, cover letter, etc.

**Important:** 
- The `personal_config.json` file is gitignored and will not be committed to GitHub
- Review all values and replace any placeholder text with your actual information
- Leave fields blank (`""`) if you don't want to provide that information

## Step 9: Verify resume file exists
Make sure your resume is at: `all resumes\default\resume.pdf`

## Step 10: Run the bot
```cmd
python runAiBot.py
```

## Notes for Windows:
- No need for DISPLAY environment variable
- No X11/display server needed
- GUI dialogs will work natively
- Chrome will open automatically
- All dependencies should install without issues

## Troubleshooting

### If Chrome doesn't open:
- Make sure Google Chrome is installed
- Check if Chrome is already running (close all Chrome windows)
- Try setting `safe_mode = True` in `config/settings.py`

### If you get import errors:
- Make sure venv is activated (you should see `(venv)` in your prompt)
- Reinstall requirements: `py -m pip install -r requirements.txt`

### If you get "Can't find a usable init.tcl" error:
- This is a Windows-specific Tcl/Tk library path issue
- Find your Python installation directory (usually in `C:\Users\YourName\AppData\Local\Programs\Python\Python3XX\`)
- Locate the `tcl\tcl8.6` and `tcl\tk8.6` folders
- Add these paths to your `.env` file:
  - `TCL_LIBRARY=C:\Users\YourName\AppData\Local\Programs\Python\Python3XX\tcl\tcl8.6`
  - `TK_LIBRARY=C:\Users\YourName\AppData\Local\Programs\Python\Python3XX\tcl\tk8.6`
- Replace `YourName` and `Python3XX` with your actual username and Python version
- If the error persists, you can also set these as system environment variables

### To deactivate virtual environment:
```cmd
deactivate
```

### To reactivate later:
```cmd
cd D:\Coding\LinkedinAutoApply
venv\Scripts\activate
python runAiBot.py
```

