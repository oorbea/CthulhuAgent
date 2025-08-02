# Artificial Intelligence Agent for Cthulhu Dark

This project is an artificial intelligence agent designed to assist players and game masters during sessions of the **Cthulhu Dark** role-playing game. It leverages AI to generate content, answer questions, and help advance the storyline.

## What can this assistant do?

1. **Create custom Cthulhu Dark stories**
2. **Help the game master or players get unstuck** if they don’t know what to do in a situation
3. **Create characters for your sessions**
4. **Explain the game’s rules and mechanics**

---

## Requirements

- Python 3.8 or higher
- Gemini API Key (required)

> **Note:** To use the AI features, you need a Gemini API key. Set it as an environment variable called `GEMINI_API_KEY`.

### How to set the environment variable

**On Windows (cmd):**
```cmd
set GEMINI_API_KEY=YOUR_API_KEY_HERE
```

**On Linux/MacOS (bash/zsh):**
```bash
export GEMINI_API_KEY=YOUR_API_KEY_HERE
```

## Installation and Usage

### First time setup
Use the script for your operating system to install dependencies and set up the environment:

- **Windows:**  
  Run `build.bat`
- **Linux/MacOS:**  
  Run `build.sh`

 **Note for Linux/MacOS users:**  
 You may need to grant execution permissions to the scripts. Do this by running:

 ```bash
 chmod +x build.sh run.sh
 ```

This will create the virtual environment and automatically install all necessary dependencies.

### Regular usage
After the initial setup, simply use the run script:

- **Windows:**  
  Run `run.bat`
- **Linux/MacOS:**  
  Run `run.sh`

---

## Credits

Project developed by **Oriol Orbea Suari**.

- Author of the rules system: **Graham Walmsley (2010)**
- Spanish PDF translation: **Alexandre Pereira**
- Authors of stories used as context for the AI: **Oriol Orbea**, **Alejandro Stratta**, **Orgullo Freak**, and **@solowho**

Inspired by the **Cthulhu Dark** game system.

---

Questions or problems? Please open an issue in this repository!
