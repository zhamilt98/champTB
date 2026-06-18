import os
import sys
import streamlit.web.cli as stcli

def get_base_path():
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    script_path = os.path.join(get_base_path(), "app.py")
    sys.argv = [
        "streamlit",
        "run",
        script_path,
        "--global.developmentMode=false",
    ]
    
    # Change current working directory to the base path so app.py can find the JSON files
    os.chdir(get_base_path())
    
    sys.exit(stcli.main())
