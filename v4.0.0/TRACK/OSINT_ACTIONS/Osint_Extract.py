# v4.0.0 ✠
# TRACK CLASS COMPONENT




import os
import re
import sys
import json
import time
import random
import warnings
import subprocess




from tqdm import tqdm
from typing import Any
from rich.console import Console
from rich.panel import Panel
from rich.align import Align




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

[bold white]OSINT EXTRACT TOOL[/bold white]

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
        "[bold yellow]+[/bold yellow] [bold white]Search side profiles[/bold white]\n\n"
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
        "[bold yellow]══[/bold yellow] [bold white]Enter Username[/bold white]",
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




def Format_Input(Input_String: str, Platform: str) -> str:

    try:

        Cleaned_Input = Input_String.strip()

        if Platform == "GitHub":
            Cleaned_Input = Cleaned_Input.lower()
            Cleaned_Input = re.sub(r'[^a-z0-9-]', '', Cleaned_Input)
            Cleaned_Input = re.sub(r'-{2,}', '-', Cleaned_Input).strip('-')
            return Cleaned_Input[:39]
        
        elif Platform in ("Twitter", "X"):
            return re.sub(r'[^A-Za-z0-9_]', '', Cleaned_Input)[:15]
        
        elif Platform == "Instagram":
            Cleaned_Input = re.sub(r'[^A-Za-z0-9._]', '', Cleaned_Input)
            Cleaned_Input = re.sub(r'\.{2,}', '.', Cleaned_Input).strip('.')
            return Cleaned_Input[:30]
        
        elif Platform == "Facebook":
            return re.sub(r'[^A-Za-z0-9.]', '', Cleaned_Input)[:50]
        
        elif Platform == "LinkedIn":
            return re.sub(r'[^A-Za-z0-9-]', '', Cleaned_Input)[:100]
        
        elif Platform == "Reddit":
            return re.sub(r'[^A-Za-z0-9_-]', '', Cleaned_Input)[:20]
        
        elif Platform == "TikTok":
            Cleaned_Input = re.sub(r'[^A-Za-z0-9._]', '', Cleaned_Input)
            if Cleaned_Input.endswith('.'):
                Cleaned_Input = Cleaned_Input[:-1]
            return Cleaned_Input[:24]
        
        elif Platform == "Pinterest":
            return re.sub(r'[^A-Za-z0-9]', '', Cleaned_Input)[:30]
        
        elif Platform == "Snapchat":
            Cleaned_Input = re.sub(r'[^A-Za-z0-9._-]', '', Cleaned_Input)
            Cleaned_Input = re.sub(r'^[^A-Za-z]+|[^A-Za-z0-9]+$', '', Cleaned_Input)
            return Cleaned_Input[:15]
        
        elif Platform == "YouTube":
            Cleaned_Input = re.sub(r'[^0-9A-Za-z_\-\.\·]', '', Cleaned_Input)
            Cleaned_Input = re.sub(r'^[._\-·]+|[._\-·]+$', '', Cleaned_Input)
            return Cleaned_Input[:30]
        
        elif Platform == "Telegram":
            return re.sub(r'[^A-Za-z0-9_]', '', Cleaned_Input)[:32]
        
        elif Platform == "Medium":
            Cleaned_Input = Cleaned_Input.lower()
            return re.sub(r'[^a-z0-9_-]', '', Cleaned_Input)[:50]
        
        else:
            return re.sub(r'[^\w\-\.]', '', Cleaned_Input)
        
    except Exception:
        return Input_String




def Process(Username):

    Possible_Profiles = {}
    Not_Found = []
    Errors = []
    
    Platforms = {
        "Twitter":   "https://twitter.com/{}",
        "Instagram": "https://www.instagram.com/{}",
        "Facebook":  "https://www.facebook.com/{}",
        "LinkedIn":  "https://www.linkedin.com/in/{}",
        "GitHub":    "https://github.com/{}",
        "Reddit":    "https://www.reddit.com/user/{}",
        "TikTok":    "https://www.tiktok.com/@{}",
        "Pinterest": "https://www.pinterest.com/{}",
        "Snapchat":  "https://www.snapchat.com/add/{}",
        "YouTube":   "https://www.youtube.com/user/{}",
        "Telegram":  "https://t.me/{}",
        "Medium":    "https://medium.com/@{}",
        "Flickr":    "https://www.flickr.com/people/{}"
    }

    try:

        time.sleep(random.uniform(1.0, 2.0))

        User_Folder = f"OSINT_{Username}"

        Root_Directory = os.path.join("Report", "OSINT_REPORT")

        Full_Path = os.path.join(Root_Directory, User_Folder)

        Make_Directory(Full_Path)

        for Platform, Template_Url in Platforms.items():
            Formatted_Username = Format_Input(Username, Platform)
            Profile_Url = Template_Url.format(Formatted_Username)
            Possible_Profiles[Platform] = Profile_Url

        return User_Folder, Possible_Profiles, Not_Found, Errors

    except Exception:
        return None, {}, [], Errors




def Create_Report(User_Folder, Possible_Profiles, Not_Found, Errors):
    
    if Possible_Profiles:

        Found_Content = ""

        for Key, Value in Possible_Profiles.items():
            Short_URL = Value if len(Value) <= 80 else Value[:77] + "..."
            Found_Content += f"[bold yellow]{Key}[/bold yellow]\n[bold white]{Short_URL}[/bold white]\n\n"
        
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




def Save_Report(User_Folder):

    try:

        Root_Directory = os.path.join("Report", "OSINT_REPORT") 

        Report_Directory = os.path.join(Root_Directory, User_Folder)

        Filename = "Osint_Results.json"
        
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

        Input_Username = Get_Input()

        if Input_Username.lower() == 'b':
            return
            
        if Input_Username.lower() == 'e':
            Clear_Terminal()
            Console().print("[bold yellow]Exited[/bold yellow]")
            sys.exit(0)

        if not Input_Username:
            Console().print("\n[bold yellow]Invalid username[/bold yellow]")
            time.sleep(1)
            continue

        Reset_Report()

        Report["Input"] = Input_Username

        Clear_Terminal()

        Display_Banner()
        
        User_Folder, Possible_Profiles, Not_Found, Errors = Process(Input_Username)

        if not User_Folder and Errors:
            Console().print(f"\n[bold yellow]{Errors[0]}[/bold yellow] - [bold white]Press Enter to continue[/bold white]")
            Console().input()
            continue

        Report["Found Data"] = Possible_Profiles or {}
        Report["Not Found Data"] = Not_Found
        Report["Errors"] = Errors

        Create_Report(User_Folder, Possible_Profiles or {}, Not_Found, Errors)
        Save_Report(User_Folder)

        Console().input("\n[bold yellow]Check reports[/bold yellow] - [bold white]Press Enter[/bold white]")




if __name__ == "__main__":
    Main()
