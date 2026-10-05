#!/bin/bash


clear


.venv/bin/ruff check "v4.0.0/IENA_Client.py"
.venv/bin/ruff check "v4.0.0/IENA_Client_Cache_Cleaner.py"


.venv/bin/ruff check "v4.0.0/TRACK/Option_T1.py"
.venv/bin/ruff check "v4.0.0/TRACK/OSINT_ACTIONS/Osint_Extract.py"
.venv/bin/ruff check "v4.0.0/TRACK/EXIF_ACTIONS/Exif_Extract.py"
.venv/bin/ruff check "v4.0.0/TRACK/COPY_ACTIONS/Copy_Html_Css.py"


.venv/bin/ruff check "v4.0.0/SECURITY/Option_S1.py"
.venv/bin/ruff check "v4.0.0/SECURITY/LINK_ACTIONS/Phishing_Analysis.py"
.venv/bin/ruff check "v4.0.0/SECURITY/DDOS_ACTIONS/DDoS_Analysis.py"
.venv/bin/ruff check "v4.0.0/SECURITY/MEDIA_ACTIONS/Exif_Deleter.py"


.venv/bin/ruff check "v4.0.0/NETHUNTER/Option_N1.py"
.venv/bin/ruff check "v4.0.0/NETHUNTER/PORT_ACTIONS/Port_Extract.py"
.venv/bin/ruff check "v4.0.0/NETHUNTER/IP_ACTIONS/Ip_Extract.py"


read -n 1 -s -r -p "Done"
