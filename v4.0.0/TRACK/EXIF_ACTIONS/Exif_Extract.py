# v4.0.0 ✠
# TRACK CLASS COMPONENT




import os
import sys
import json
import time
import requests
import exifread
import warnings
import subprocess




from typing import Any
from tqdm import tqdm
from io import StringIO
from contextlib import redirect_stderr
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

[bold white]EXIF EXTRACT TOOL[/bold white]

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
        "[bold yellow]+[/bold yellow] [bold white]Detect time from photo[/bold white]\n"
        "[bold yellow]+[/bold yellow] [bold white]Detect location from photo[/bold white]\n"
        "[bold yellow]+[/bold yellow] [bold white]Detect device from photo[/bold white]\n\n"
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
        "[bold yellow]══[/bold yellow] [bold white]Enter Photo Path[/bold white]",
        border_style="yellow",
        padding=(0, 2),
        expand=True
    )

    Console().print(Input_Panel)
    
    Choice = Console().input("").strip().strip('"').strip("'")
    
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




def Convert_To_Degrees(Value):
    Degree = float(Value.values[0].num) / float(Value.values[0].den)
    Minute = float(Value.values[1].num) / float(Value.values[1].den)
    Second = float(Value.values[2].num) / float(Value.values[2].den)
    return Degree + (Minute / 60.0) + (Second / 3600.0)




def Get_Location_From_Coords(Latitude, Longitude):

    try:
        
        Url = f"https://nominatim.openstreetmap.org/reverse?lat={Latitude}&lon={Longitude}&format=json"

        Response = requests.get(Url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) 1889-IENA/1.0'}, timeout=5)

        if Response.status_code == 200:
            Address = Response.json().get('display_name')
            return Address if Address else None
        return None
    
    except Exception:
        return None




def Process(Image_Path):

    Found_Data = {}
    Not_Found = []
    Errors = []

    try:

        Fake_Stderr = StringIO()
        
        with redirect_stderr(Fake_Stderr):
            with open(Image_Path, 'rb') as File:
                Tags = exifread.process_file(File, details=False, debug=False)

        if not Tags:
            Errors.append("EXIF data not found")
            return None, {}, [], Errors

        Found_Data["File name"] = os.path.basename(Image_Path)
        Found_Data["File size"] = f"{os.path.getsize(Image_Path)/1024:.2f} KB"
        Found_Data["File path"] = Image_Path

        GPS_Latitude = Tags.get('GPS GPSLatitude')
        GPS_Longitude = Tags.get('GPS GPSLongitude')

        Latitude_Ref = Tags.get('GPS GPSLatitudeRef')
        Longitude_Ref = Tags.get('GPS GPSLongitudeRef')

        if GPS_Latitude and GPS_Longitude and Latitude_Ref and Longitude_Ref:

            Latitude = Convert_To_Degrees(GPS_Latitude)
            Longitude = Convert_To_Degrees(GPS_Longitude)
            
            if Latitude_Ref.values[0] == 'S':
                Latitude = -Latitude
            
            if Longitude_Ref.values[0] == 'W':
                Longitude = -Longitude
                
            Location = Get_Location_From_Coords(Latitude, Longitude)

            Found_Data["GPS Coordinates"] = f"{Latitude:.6f}, {Longitude:.6f}"
            
            if Location:
                Found_Data["Location"] = Location
            else:
                Not_Found.append("Address not found for coordinates")

        else:
            Not_Found.append("GPS information")

        for Tag in Tags:
            
            Key = str(Tag)
            Value = str(Tags[Tag])

            if Key not in ['MakerNote', 'Thumbnail', 'JPEGThumbnail']:
                if Key.startswith('GPS'):
                    continue
                Found_Data[Key] = Value

        Image_Name_Clean = os.path.splitext(os.path.basename(Image_Path))[0]
        
        Exif_Folder = f"EXIF_{Image_Name_Clean}"

        Root_Directory = os.path.join("Report", "EXIF_REPORT")

        Full_Path = os.path.join(Root_Directory, Exif_Folder)

        Make_Directory(Full_Path)

        return Exif_Folder, Found_Data, Not_Found, Errors

    except Exception:
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




def Save_Report(Exif_Folder):

    try:
        
        Root_Directory = os.path.join("Report", "EXIF_REPORT") 

        Report_Directory = os.path.join(Root_Directory, Exif_Folder)

        Filename = "Exif_Results.json"
        
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

        Input_Path = Get_Input()

        if Input_Path.lower() == 'b':
            return
            
        if Input_Path.lower() == 'e':
            Clear_Terminal()
            Console().print("[bold yellow]Exited[/bold yellow]")
            sys.exit(0)

        if not Input_Path or not os.path.isfile(Input_Path):
            Console().print("\n[bold yellow]Invalid file path[/bold yellow]")
            continue

        Reset_Report()

        Report["Input"] = Input_Path

        Clear_Terminal()

        Display_Banner()

        Exif_Folder, Found_Data, Not_Found, Errors = Process(Input_Path)

        if not Exif_Folder and Errors:
            Console().print(f"\n[bold yellow]{Errors[0]}[/bold yellow] - [bold white]Press Enter to continue[/bold white]")
            Console().input()
            continue

        Report["Found Data"] = Found_Data or {}
        Report["Not Found Data"] = Not_Found
        Report["Errors"] = Errors

        Create_Report(Found_Data or {}, Not_Found, Errors)
        Save_Report(Exif_Folder)

        Console().input("\n[bold yellow]Check reports[/bold yellow] - [bold white]Press Enter[/bold white]")




if __name__ == "__main__":
    Main()
