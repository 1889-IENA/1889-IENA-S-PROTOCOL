# v4.0.0 ✠
# NETHUNTER CLASS COMPONENT




import os
import sys
import time
import json
import warnings
import requests
import subprocess




from typing import Any
from tqdm import tqdm
from collections import Counter
from rich.console import Console
from rich.panel import Panel
from rich.align import Align




warnings.simplefilter('ignore')




Report: dict[str, Any] = {}




def Clear_Terminal():
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)




def Loading_Animation(Duration):
    Console().print("[bold green]Loading...[/bold green]")
    for _ in tqdm(range(Duration), bar_format="{l_bar}{bar}|", colour='green'):
        time.sleep(0.010)
    Clear_Terminal()




def Display_Banner():
    
    Banner_Content = """
    [bold white]
╺┓ ┏━┓┏━┓┏━┓   ╻ ┏━╸ ┏┓╻ ┏━┓
 ┃ ┣━┫┣━┫┗━┫   ┃ ┣╸  ┃┗┫ ┣━┫
╺┻╸┗━┛┗━┛┗━┛   ╹╹┗━╸╹╹ ╹╹╹ ╹[/bold white]

[bold white]IP EXTRACT TOOL[/bold white]

[bold white]Owner License : 1889 I.E.N.A |  Author : Vsevolod Yetzen |  Version : v4.0.0[/bold white] [bold green]✠[/bold green]"""

    Banner_Panel = Panel(
        Align.center(Banner_Content),
        border_style="green",
        padding=(1, 2),
        expand=True
    )

    Console().print(Banner_Panel)




def Display_Info():

    Info_Panel = Panel(
        "[bold white]Turn on[/bold white] [bold green]VPN[/bold green] [bold white]or[/bold white] [bold green]TOR[/bold green] [bold white]for anonymity[/bold white]\n\n"
        "[bold white]ABILITY[/bold white]\n\n"
        "[bold green]+[/bold green] [bold white]IP Geo-Location Analysis[/bold white]\n"
        "[bold green]+[/bold green] [bold white]ISP and Organization Info[/bold white]\n"
        "[bold green]+[/bold green] [bold white]Region and Timezone Detection[/bold white]\n\n"
        "[bold white]DEVICE PERMISSION -[/bold white] [bold green]Normal[/bold green]",
        title="[bold green]INFORMATION[/bold green]",
        border_style="green",
        padding=(1, 2),
        expand=True
    )

    Console().print(Info_Panel)




def Display_Menu():

    System_Panel = Panel(
        "[bold green][ B ][/bold green]  [bold white]Back[/bold white]\n"
        "[bold green][ E ][/bold green]  [bold white]Exit[/bold white]",
        title="[bold green]SYSTEM COMMANDS[/bold green]",
        border_style="green",
        padding=(1, 2),
        expand=True
    )

    Console().print(System_Panel)




def Get_Input():
    
    Input_Panel = Panel(
        "[bold green]══[/bold green] [bold white]Enter Target IP Address[/bold white]",
        border_style="green",
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




def Process(Target_Ip):

    Found_Data = {}
    Not_Found = []
    Errors = []
    Datas = []
    
    Session = requests.Session()
    
    try:

        Url = f"http://ip-api.com/json/{Target_Ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as"
        
        Response = Session.get(Url, timeout=10)
        Data = Response.json()

        if Data["status"] == "success":
            Datas.append({
                "Country": Data.get('country'),
                "Country Code": Data.get('countryCode'),
                "Region": Data.get('regionName'),
                "Region Code": Data.get('region'),
                "City": Data.get('city'),
                "Zip Code": Data.get('zip'),
                "Timezone": Data.get('timezone'),
                "ISP": Data.get('isp'),
                "Organization": Data.get('org'),
                "ASN": Data.get('as'),
                "Latitude": str(Data.get('lat')) if Data.get('lat') is not None else None,
                "Longitude": str(Data.get('lon')) if Data.get('lon') is not None else None
            })

        else:
            Errors.append(f"IP query failed on ip-api.com: {Data.get('message', 'Unknown error')}")

    except requests.exceptions.RequestException:
        Errors.append("Network error on ip-api.com")
    
    except Exception:
        Errors.append("Failed to retrieve IP data from ip-api.com")

    try:

        Url = f"https://ipinfo.io/{Target_Ip}/json"
        
        Response = Session.get(Url, timeout=10)
        Data = Response.json()

        if 'error' not in Data:
            Loc_Parts = Data.get('loc', '').split(',')
            Lat = Loc_Parts[0].strip() if Loc_Parts else None
            Lon = Loc_Parts[1].strip() if len(Loc_Parts) > 1 else None
            Asn = Data.get('asn', {}).get('asn') if 'asn' in Data else None
            Datas.append({
                "Country": Data.get('country'),
                "Region": Data.get('region'),
                "City": Data.get('city'),
                "Zip Code": Data.get('postal'),
                "Timezone": Data.get('timezone'),
                "ISP": Data.get('org'),
                "Organization": Data.get('org'),
                "ASN": Asn,
                "Latitude": Lat,
                "Longitude": Lon
            })

        else:
            Errors.append(f"IP query failed on ipinfo.io {Data.get('title', 'Unknown error')}")

    except requests.exceptions.RequestException:
        Errors.append("Network error on ipinfo.io")
    
    except Exception:
        Errors.append("Failed to retrieve IP data from ipinfo.io")

    try:

        Url = f"http://ipwhois.app/json/{Target_Ip}"

        Response = Session.get(Url, timeout=10)
        Data = Response.json()

        if Data.get('success'):
            Datas.append({
                "Country": Data.get('country'),
                "Country Code": Data.get('country_code'),
                "Region": Data.get('region'),
                "City": Data.get('city'),
                "Zip Code": Data.get('zip'),
                "Timezone": Data.get('timezone'),
                "ISP": Data.get('isp'),
                "Organization": Data.get('org'),
                "ASN": Data.get('asn'),
                "Latitude": str(Data.get('latitude')) if Data.get('latitude') is not None else None,
                "Longitude": str(Data.get('longitude')) if Data.get('longitude') is not None else None
            })

        else:
            Errors.append(f"IP query failed on ipwhois.app {Data.get('message', 'Unknown error')}")

    except requests.exceptions.RequestException:
        Errors.append("Network error on ipwhois.app")
    
    except Exception:
        Errors.append("Failed to retrieve IP data from ipwhois.app")

    try:

        Url = f"https://freegeoip.app/json/{Target_Ip}"

        Response = Session.get(Url, timeout=10)
        Data = Response.json()

        Datas.append({
            "Country": Data.get('country_name'),
            "Country Code": Data.get('country_code'),
            "Region": Data.get('region_name'),
            "Region Code": Data.get('region_code'),
            "City": Data.get('city'),
            "Zip Code": Data.get('zip_code'),
            "Timezone": Data.get('time_zone'),
            "Latitude": str(Data.get('latitude')) if Data.get('latitude') is not None else None,
            "Longitude": str(Data.get('longitude')) if Data.get('longitude') is not None else None
        })

    except requests.exceptions.RequestException:
        Errors.append("Network error on freegeoip.app")
    
    except Exception:
        Errors.append("Failed to retrieve IP data from freegeoip.app")

    if not Datas:
        Errors.append("No data retrieved from any API")
        return None, {}, Not_Found, Errors

    Fields = ["Country", "Country Code", "Region", "Region Code", "City", "Zip Code", "Timezone", "ISP", "Organization", "ASN", "Latitude", "Longitude"]

    for Field in Fields:
        
        Values = [D[Field] for D in Datas if D.get(Field) and D[Field] != 'Unknown' and D[Field] != 'N/A' and D[Field] is not None]
        
        if Values:
            Found_Data[Field] = Counter(Values).most_common(1)[0][0]
        else:
            Not_Found.append(Field)

    Found_Data["IP Address"] = Target_Ip

    if Found_Data.get("Latitude") and Found_Data.get("Longitude"):
        Found_Data["Location"] = f"{Found_Data['Latitude']}, {Found_Data['Longitude']}"
    
    else:
        Not_Found.append("Location")

    Ip_Folder = f"IP_{Target_Ip.replace('.', '_')}"

    Root_Directory = os.path.join("Report", "IP_REPORT")

    Full_Path = os.path.join(Root_Directory, Ip_Folder)

    Make_Directory(Full_Path)

    return Ip_Folder, Found_Data, Not_Found, Errors




def Create_Report(Found_Data, Not_Found, Errors):

    if Found_Data:

        Found_Content = ""

        for Key, Value in Found_Data.items():
            Found_Content += f"[bold green]{Key}[/bold green]\n[bold white]{Value}[/bold white]\n\n"
        
        Found_Panel = Panel(
            Found_Content.strip(),
            title="[bold green]FOUND DATA[/bold green]",
            border_style="green",
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
            title="[bold green]NOT FOUND DATA[/bold green]",
            border_style="green",
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
            title="[bold green]ERRORS[/bold green]",
            border_style="green",
            padding=(1, 2),
            expand=True
        )
        
        Console().print(Errors_Panel)

    time.sleep(1)




def Save_Report(Ip_Folder):

    try:
        
        Root_Directory = os.path.join("Report", "IP_REPORT")

        Report_Directory = os.path.join(Root_Directory, Ip_Folder)

        Filename = "Ip_Results.json"
        
        Make_Directory(Report_Directory)

        Filepath = os.path.join(Report_Directory, Filename)
        
        Report["Timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
        
        with open(Filepath, 'w', encoding='utf-8') as Output_File:
            json.dump(Report, Output_File, ensure_ascii=False, indent=4)
            
        Console().print(f"\n[bold green]Report Saved[/bold green] - [bold white]{Filepath}[/bold white]")

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

        Input_Ip = Get_Input()

        if Input_Ip.lower() == 'b':
            return
        
        if Input_Ip.lower() == 'e':
            Clear_Terminal()
            Console().print("[bold green]Exited[/bold green]")
            sys.exit(0)

        if not Input_Ip:
            Console().print("\n[bold green]Invalid IP address[/bold green]")
            time.sleep(1)
            continue

        Reset_Report()

        Report["Input"] = Input_Ip

        Clear_Terminal()

        Display_Banner()

        Ip_Folder, Found_Data, Not_Found, Errors = Process(Input_Ip)

        if not Ip_Folder and Errors:
            Console().print(f"\n[bold green]{Errors[0]}[/bold green] - [bold white]Press Enter to continue[/bold white]")
            Console().input()
            continue

        Report["Found Data"] = Found_Data or {}
        Report["Not Found Data"] = Not_Found
        Report["Errors"] = Errors

        Create_Report(Found_Data or {}, Not_Found, Errors)
        Save_Report(Ip_Folder)

        Console().input("\n[bold green]Check reports[/bold green] - [bold white]Press Enter[/bold white]")




if __name__ == "__main__":
    Main()
