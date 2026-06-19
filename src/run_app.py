import os
import sys
import streamlit.web.cli as stcli

def get_base_path():
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def get_project_root():
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    base_path = get_base_path()
    script_path = os.path.join(base_path, "app.py")
    sys.argv = [
        "streamlit",
        "run",
        script_path,
        "--global.developmentMode=false",
    ]
    
    os.chdir(get_project_root())
    
    sys.exit(stcli.main())
