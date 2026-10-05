# v4.0.0 ✠
# TRACK CLASS COMPONENT




import os
import sys
import time
import json
import random
import warnings
import subprocess




from typing import Any
from tqdm import tqdm
from rich.console import Console
from rich.panel import Panel
from rich.align import Align




from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from curl_cffi import requests as cffi_requests




warnings.simplefilter('ignore')




Report: dict[str, Any] = {}




def Clear_Terminal():
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)




def Loading_Animation(Duration):
    Console().print("[bold yellow]Loading...[/bold yellow]")
    for _ in tqdm(range(Duration), bar_format="{l_bar}{bar}|", colour='yellow'):
        time.sleep(0.010)
    Clear_Terminal()




def Display_Banner():

    Banner_Content = """
    [bold white]
╺┓ ┏━┓┏━┓┏━┓   ╻ ┏━╸ ┏┓╻ ┏━┓
 ┃ ┣━┫┣━┫┗━┫   ┃ ┣╸  ┃┗┫ ┣━┫
╺┻╸┗━┛┗━┛┗━┛   ╹╹┗━╸╹╹ ╹╹╹ ╹[/bold white]

[bold white]WEBSITE COPY TOOL[/bold white]

[bold white]Owner License : 1889 I.E.N.A |  Author : Vsevolod Yetzen |  Version : v4.0.0[/bold white] [bold yellow]✠[/bold yellow]"""

    Banner_Panel = Panel(
        Align.center(Banner_Content),
        border_style="yellow",
        padding=(1, 2),
        expand=True
    )

    Console().print(Banner_Panel)




def Display_Info():

    Info_Panel = Panel(
        "[bold white]Turn on[/bold white] [bold yellow]VPN[/bold yellow] [bold white]or[/bold white] [bold yellow]TOR[/bold yellow] [bold white]for anonymity[/bold white]\n\n"
        "[bold white]ABILITY[/bold white]\n\n"
        "[bold yellow]+[/bold yellow] [bold white]Copy the site exactly from the link[/bold white]\n\n"
        "[bold white]DEVICE PERMISSION -[/bold white] [bold yellow]Normal[/bold yellow]",
        title="[bold yellow]INFORMATION[/bold yellow]",
        border_style="yellow",
        padding=(1, 2),
        expand=True
    )

    Console().print(Info_Panel)




def Display_Menu():

    System_Panel = Panel(
        "[bold yellow][ B ][/bold yellow]  [bold white]Back[/bold white]\n"
        "[bold yellow][ E ][/bold yellow]  [bold white]Exit[/bold white]",
        title="[bold yellow]SYSTEM COMMANDS[/bold yellow]",
        border_style="yellow",
        padding=(1, 2),
        expand=True
    )

    Console().print(System_Panel)




def Get_Input():
    
    Input_Panel = Panel(
        "[bold yellow]══[/bold yellow] [bold white]Paste URL[/bold white]",
        border_style="yellow",
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




def Save_File(Content, Filename):

    try:
        with open(Filename, 'w', encoding='utf-8') as File:
            File.write(Content)
        return True
    
    except Exception:
        return False




def Download_Css_File(Url, Folder, Session=None):
    
    try:

        time.sleep(random.uniform(0.5, 1.5))

        Requester = Session if Session else cffi_requests
        Response = Requester.get(Url, timeout=15, verify=False, impersonate="chrome")

        Response.raise_for_status()

        Filename = os.path.basename(urlparse(Url).path)

        if not Filename or Filename.endswith('/'):
            Filename = "style.css"
        
        if not Filename.endswith('.css'):
            Filename = f"{Filename}.css"

        Full_Path = os.path.join(Folder, Filename)

        with open(Full_Path, 'w', encoding='utf-8') as File:
            File.write(Response.text)
        return Filename
    
    except Exception:
        return None




def Process(Url):

    Found_Data = {}
    Not_Found = []
    Errors = []
    
    try:

        time.sleep(random.uniform(1.0, 2.0))

        Session = cffi_requests.Session()

        Response = Session.get(Url, timeout=20, verify=False, impersonate="chrome", allow_redirects=True)
        Response.raise_for_status()

        Parsed_Url = urlparse(Url)

        Site_Name = Parsed_Url.netloc.replace(':', '_').replace('.', '_')

        Found_Data["Domain"] = Parsed_Url.netloc
        Found_Data["Protocol"] = Parsed_Url.scheme
        Found_Data["Status Code"] = str(Response.status_code)
        Found_Data["Content Type"] = Response.headers.get('Content-Type', 'Unknown')
        Found_Data["HTML Size"] = f"{len(Response.text) / 1024:.2f} KB"

        Root_Directory = os.path.join("Report", "COPIED_WEBSITE_REPORT") 

        Site_Folder_Path = os.path.join(Root_Directory, Site_Name)

        Make_Directory(Site_Folder_Path)

        Soup = BeautifulSoup(Response.text, 'html.parser')

        Html_Filename = os.path.join(Site_Folder_Path, 'index.html')
        
        if Save_File(Response.text, Html_Filename):
            Found_Data["HTML File"] = "Saved"
        else:
            Errors.append("Could not save HTML file")

        Css_Links = Soup.find_all('link', rel='stylesheet')

        Downloaded_Css_List = []
        
        if Css_Links:

            for Link in Css_Links:

                Href = Link.get('href')

                if Href and isinstance(Href, str):

                    Full_Url = urljoin(Url, Href)

                    Saved_Name = Download_Css_File(Full_Url, Site_Folder_Path, Session)

                    if Saved_Name:
                        Downloaded_Css_List.append(Saved_Name)
            
            Found_Data["CSS Count"] = str(len(Downloaded_Css_List))
            Found_Data["CSS List"] = ", ".join(Downloaded_Css_List) if Downloaded_Css_List else "Failed to download"

        else:
            Not_Found.append("External CSS")

        Title = Soup.find('title')
        
        Found_Data["Title"] = Title.get_text().strip()[:50] if Title else "None"
        Found_Data["Meta Tags"] = str(len(Soup.find_all('meta')))
        Found_Data["Scripts"] = str(len(Soup.find_all('script')))
        Found_Data["Images"] = str(len(Soup.find_all('img')))
        Found_Data["Links"] = str(len(Soup.find_all('a')))

        return Site_Name, Found_Data, Not_Found, Errors

    except Exception as Error:
        Errors.append(f"Connection failed: {str(Error)}")
        return None, {}, [], Errors




def Create_Report(Found_Data, Not_Found, Errors):
    
    if Found_Data:

        Found_Content = ""

        for Key, Value in Found_Data.items():
            Found_Content += f"[bold yellow]{Key}[/bold yellow]\n[bold white]{Value}[/bold white]\n\n"
        
        Found_Panel = Panel(
            Found_Content.strip(),
            title="[bold yellow]FOUND DATA[/bold yellow]",
            border_style="yellow",
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
            title="[bold yellow]NOT FOUND DATA[/bold yellow]",
            border_style="yellow",
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
            title="[bold yellow]ERRORS[/bold yellow]",
            border_style="yellow",
            padding=(1, 2),
            expand=True
        )

        Console().print(Errors_Panel)

    time.sleep(1)




def Save_Report(Site_Name):

    try:

        Root_Directory = os.path.join("Report", "COPIED_WEBSITE_REPORT") 

        Report_Directory = os.path.join(Root_Directory, Site_Name)

        Filename = "Copy_Html_Css_Results.json"
        
        Make_Directory(Report_Directory)

        Filepath = os.path.join(Report_Directory, Filename)
        
        Report["Timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
        
        with open(Filepath, 'w', encoding='utf-8') as Output_File:
            json.dump(Report, Output_File, ensure_ascii=False, indent=4)
            
        Console().print(f"\n[bold yellow]Report Saved[/bold yellow] - [bold white]{Filepath}[/bold white]")

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
            Console().print("[bold yellow]Exited[/bold yellow]")
            sys.exit(0)

        if not Input_Url:
            Console().print("\n[bold yellow]Invalid URL[/bold yellow]")
            time.sleep(1)
            continue
        
        if not Input_Url.startswith('http://') and not Input_Url.startswith('https://'):
            Console().print("\n[bold yellow]Invalid URL format[/bold yellow]")
            time.sleep(1)
            continue

        Reset_Report()

        Report["Input"] = Input_Url

        Clear_Terminal()

        Display_Banner()
        
        Site_Name, Found_Data, Not_Found, Errors = Process(Input_Url)

        if not Site_Name and Errors:
            Console().print(f"\n[bold yellow]{Errors[0]}[/bold yellow] - [bold white]Press Enter to continue[/bold white]")
            Console().input()
            continue

        Report["Found Data"] = Found_Data or {}
        Report["Not Found Data"] = Not_Found
        Report["Errors"] = Errors

        Create_Report(Found_Data or {}, Not_Found, Errors)
        Save_Report(Site_Name)

        Console().input("\n[bold yellow]Check reports[/bold yellow] - [bold white]Press Enter[/bold white]")




if __name__ == "__main__":
    Main()
