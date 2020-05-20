# PingUntil
Tool will ping an address until it misses a certain number of pings.

How to configure your environment:
    1. Run PowerShell as administrator
        a. Execute the following command(s):
            Set-ExecutionPolicy Remote-Signed -Force 
    2. Change to the root folder where you would like the repo to exist.
        # NOTE: Do not run this as a script. Once your venv is launched the remaining commands don't run within the venv. 
        a. Execute the following commands(s):
            git clone https://github.com/xander-petty/PingUntil.git
            python -m venv .
            .\Scripts\Activate.ps1
            pip install --upgrade pip 
            pip install wheel 
            pip install --upgrade wheel setuptools 
            pip install scapy flask flask_wtf wtforms
