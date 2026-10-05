# v4.0.0 ✠
# SECURITY CLASS COMPONENT




import os
import re
import ssl
import sys
import json
import time
import socket
import warnings
import subprocess




from typing import Any
from tqdm import tqdm
from rich.console import Console
from rich.panel import Panel
from rich.align import Align




from urllib.parse import urlparse




warnings.simplefilter('ignore')




Report: dict[str, Any] = {}




Suspicious_Sites = [
    "grabify", "bit.ly", "tinyurl", "ow.ly", "is.gd", "shorturl.at", "adf.ly", "goo.gl",
    "t.co", "v.gd", "lnkd.in", "short.ly", "clkim.com", "iplogger", "blasze.tk", 
    "gyazo.com", "ps3cfw.com", "yip.su", "02ip.ru", "iplis.ru", "cutt.ly", "rb.gy"
]




Phishing_Keywords = [
    "verify", "account", "suspended", "confirm", "secure", "update", "login",
    "banking", "paypal", "amazon", "apple", "microsoft", "netflix", "security",
    "urgent", "alert", "action-required"
]




def Clear_Terminal():
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)




def Loading_Animation(Duration):
    Console().print("[bold blue]Loading...[/bold blue]")
    for _ in tqdm(range(Duration), bar_format="{l_bar}{bar}|", colour='blue'):
        time.sleep(0.010)
    Clear_Terminal()




def Display_Banner():

    Banner_Content = """
    [bold white]
╺┓ ┏━┓┏━┓┏━┓   ╻ ┏━╸ ┏┓╻ ┏━┓
 ┃ ┣━┫┣━┫┗━┫   ┃ ┣╸  ┃┗┫ ┣━┫
╺┻╸┗━┛┗━┛┗━┛   ╹╹┗━╸╹╹ ╹╹╹ ╹[/bold white]

[bold white]PHISHING ANALYSIS TOOL[/bold white]

[bold white]Owner License : 1889 I.E.N.A |  Author : Vsevolod Yetzen |  Version : v4.0.0[/bold white] [bold blue]✠[/bold blue]"""

    Banner_Panel = Panel(
        Align.center(Banner_Content),
        border_style="blue",
        padding=(1, 2),
        expand=True
    )

    Console().print(Banner_Panel)




def Display_Info():

    Info_Panel = Panel(
        "[bold white]Turn on[/bold white] [bold blue]VPN[/bold blue] [bold white]or[/bold white] [bold blue]TOR[/bold blue] [bold white]for anonymity[/bold white]\n\n"
        "[bold white]ABILITY[/bold white]\n\n"
        "[bold blue]+[/bold blue] [bold white]Detect IP loggers[/bold white]\n"
        "[bold blue]+[/bold blue] [bold white]Analyze SSL certificates[/bold white]\n"
        "[bold blue]+[/bold blue] [bold white]Check suspicious keywords[/bold white]\n\n"
        "[bold white]DEVICE PERMISSION -[/bold white] [bold blue]Normal[/bold blue]",
        title="[bold blue]INFORMATION[/bold blue]",
        border_style="blue",
        padding=(1, 2),
        expand=True
    )

    Console().print(Info_Panel)




def Display_Menu():

    System_Panel = Panel(
        "[bold blue][ B ][/bold blue]  [bold white]Back[/bold white]\n"
        "[bold blue][ E ][/bold blue]  [bold white]Exit[/bold white]",
        title="[bold blue]SYSTEM COMMANDS[/bold blue]",
        border_style="blue",
        padding=(1, 2),
        expand=True
    )

    Console().print(System_Panel)




def Get_Input():
    
    Input_Panel = Panel(
        "[bold blue]══[/bold blue] [bold white]Enter URL[/bold white]",
        border_style="blue",
        padding=(0, 2),
        expand=True
    )

    Console().print(Input_Panel)
    
    Choice = Console().input("").strip()
    
    return Choice




def Reset_Report():

    global Report

    Report = {
        "Input": "",
        "Found Data": {},
        "Not Found Data": [],
        "Errors": []
    }




def Make_Directory(Directory_Name):
    if not os.path.exists(Directory_Name):
        os.makedirs(Directory_Name)




def Process(Url):

    Found_Data = {}
    Not_Found = []
    Errors = []

    try:

        Parsed_Url = urlparse(Url)
        Domain = (Parsed_Url.hostname or "").lower()

        try:
            Port = Parsed_Url.port or 443
        except ValueError:
            Port = 443
        
        if not Domain:
            Errors.append("Invalid Domain")
            return None, {}, [], Errors

        Found_Data["Domain"] = Domain

        if Parsed_Url.username is not None:
            Found_Data["Credential Trick"] = "Suspicious (URL contains '@', real host is " + Domain + ")"
        Found_Data["Protocol"] = Parsed_Url.scheme.upper()

        try:
            IP_Address = socket.gethostbyname(Domain)
            Found_Data["IP Address"] = IP_Address
        except Exception:
            Not_Found.append("IP Address")

        Found_Data["IP Logger Check"] = "Safe"

        for Suspicious in Suspicious_Sites:
            if "." in Suspicious:
                Is_Match = Domain == Suspicious or Domain.endswith("." + Suspicious)
            else:
                Is_Match = Suspicious in Domain

            if Is_Match:
                Found_Data["IP Logger Check"] = f"Suspicious ({Suspicious})"
                break

        Matches = [Word for Word in Phishing_Keywords if Word in Url.lower()]

        if Matches:
            Found_Data["Phishing Keywords"] = ", ".join(Matches)
        else:
            Not_Found.append("Phishing Keywords")

        if Parsed_Url.scheme == "https":
            try:
                Context = ssl.create_default_context()

                with socket.create_connection((Domain, Port), timeout=5) as Sock:

                    with Context.wrap_socket(Sock, server_hostname=Domain) as Ssock:

                        Cert = Ssock.getpeercert()

                        if Cert and isinstance(Cert, dict):
                            
                            Issuer_Raw = Cert.get('issuer', ())
                            Issuer_Dict = {}
                            
                            for Rdn in Issuer_Raw:
                                if Rdn and isinstance(Rdn, tuple) and len(Rdn) > 0:

                                    Entry = Rdn[0]
                                    Issuer_Dict[str(Entry[0])] = str(Entry[1])

                            Found_Data["SSL Issuer"] = Issuer_Dict.get('commonName', 'Unknown')
                            Found_Data["SSL Expiry"] = str(Cert.get('notAfter', 'Unknown'))
                        else:
                            Not_Found.append("SSL Certificate Details")

            except Exception:
                Not_Found.append("SSL Certificate Details")
        else:
            Found_Data["SSL Status"] = "No HTTPS (Insecure)"

        Domain_Slug = re.sub(r'[^a-zA-Z0-9]', '_', Domain)
        
        Analysis_Folder = f"PHISHING_{Domain_Slug}"

        Root_Directory = os.path.join("Report", "PHISHING_REPORT")

        Full_Path = os.path.join(Root_Directory, Analysis_Folder)

        Make_Directory(Full_Path)

        return Analysis_Folder, Found_Data, Not_Found, Errors

    except Exception:
        return None, {}, [], Errors




def Create_Report(Found_Data, Not_Found, Errors):
    
    if Found_Data:

        Found_Content = ""

        for Key, Value in Found_Data.items():
            Found_Content += f"[bold blue]{Key}[/bold blue]\n[bold white]{Value}[/bold white]\n\n"
        
        Found_Panel = Panel(
            Found_Content.strip(),
            title="[bold blue]FOUND DATA[/bold blue]",
            border_style="blue",
            padding=(1, 2),
            expand=True
        )

        Console().print(Found_Panel)

    if Not_Found:

        Not_Found_Content = ""

        for Item in Not_Found:
            Not_Found_Content += f"[bold white]{Item}[/bold white]\n"
        
        Not_Found_Panel = Panel(
            Not_Found_Content.strip(),
            title="[bold blue]NOT FOUND DATA[/bold blue]",
            border_style="blue",
            padding=(1, 2),
            expand=True
        )

        Console().print(Not_Found_Panel)

    if Errors:

        Errors_Content = ""

        for Error in Errors:
            Errors_Content += f"[bold white]{Error}[/bold white]\n"
        
        Errors_Panel = Panel(
            Errors_Content.strip(),
            title="[bold blue]ERRORS[/bold blue]",
            border_style="blue",
            padding=(1, 2),
            expand=True
        )

        Console().print(Errors_Panel)

    time.sleep(2)




def Save_Report(Analysis_Folder):

    try:
        
        Root_Directory = os.path.join("Report", "PHISHING_REPORT") 

        Report_Directory = os.path.join(Root_Directory, Analysis_Folder)

        Filename = "Phishing_Results.json"
        
        Make_Directory(Report_Directory)

        Filepath = os.path.join(Report_Directory, Filename)
        
        Report["Timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
        
        with open(Filepath, 'w', encoding='utf-8') as Output_File:
            json.dump(Report, Output_File, ensure_ascii=False, indent=4)
            
        Console().print(f"\n[bold blue]Report Saved[/bold blue] - [bold white]{Filepath}[/bold white]")

    except Exception:
        pass




def Main():

    while True:

        Clear_Terminal()

        Loading_Animation(100)

        Clear_Terminal()

        Display_Banner()

        Display_Info()

        Display_Menu()

        Input_Url = Get_Input()

        if Input_Url.lower() == 'b':
            return
    
        if Input_Url.lower() == 'e':
            Clear_Terminal()
            Console().print("[bold blue]Exited[/bold blue]")
            sys.exit(0)

        if not Input_Url:
            Console().print("\n[bold blue]Invalid URL[/bold blue]")
            time.sleep(1)
            continue     
        
        if not Input_Url.lower().startswith(('http://', 'https://')):
            Console().print("\n[bold yellow]Invalid URL format[/bold yellow]")
            time.sleep(1)
            continue

        Reset_Report()

        Report["Input"] = Input_Url
 
        Clear_Terminal()

        Display_Banner()

        Analysis_Folder, Found_Data, Not_Found, Errors = Process(Input_Url)

        if not Analysis_Folder and Errors:
            Console().print(f"\n[bold blue]{Errors[0]}[/bold blue] - [bold white]Press Enter to continue[/bold white]")
            Console().input()
            continue

        Report["Found Data"] = Found_Data or {}
        Report["Not Found Data"] = Not_Found
        Report["Errors"] = Errors

        Create_Report(Found_Data or {}, Not_Found, Errors)
        Save_Report(Analysis_Folder)

        Console().input("\n[bold blue]Check reports[/bold blue] - [bold white]Press Enter[/bold white]")




if __name__ == "__main__":
    Main()
