# v4.0.0 ✠
# SECURITY CLASS COMPONENT




import os
import sys
import time
import json
import warnings
import subprocess




from typing import Any
from tqdm import tqdm
from rich.console import Console
from rich.panel import Panel
from rich.align import Align




from PIL import Image




warnings.simplefilter('ignore')




Report: dict[str, Any] = {}




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

[bold white]EXIF DELETER TOOL[/bold white]

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
        "[bold blue]+[/bold blue] [bold white]Strip all EXIF metadata from photo[/bold white]\n"
        "[bold blue]+[/bold blue] [bold white]Remove GPS, device, timestamp data[/bold white]\n"
        "[bold blue]+[/bold blue] [bold white]Save clean photo with no hidden data[/bold white]\n\n"
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
        "[bold blue]══[/bold blue] [bold white]Enter Photo Path[/bold white]",
        border_style="blue",
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




def Process(Image_Path):

    Found_Data = {}
    Not_Found = []
    Errors = []

    try:

        Original_Size = os.path.getsize(Image_Path)
        File_Name = os.path.basename(Image_Path)
        File_Ext = os.path.splitext(File_Name)[1].lower()
        File_Name_Clean = os.path.splitext(File_Name)[0]

        Allowed_Extensions = [".jpg", ".jpeg", ".png", ".tiff", ".tif", ".webp", ".bmp"]

        if File_Ext not in Allowed_Extensions:
            Errors.append("Unsupported file format")
            return None, {}, [], Errors

        Original_Image = Image.open(Image_Path)

        Clean_Image = Image.new(Original_Image.mode, Original_Image.size)
        Clean_Image.putdata(Original_Image.getdata())

        Clean_Folder = f"EXIF_DELETED_{File_Name_Clean}"

        Root_Directory = os.path.join("Report", "EXIF_DELETED_REPORT")

        Full_Path = os.path.join(Root_Directory, Clean_Folder)

        Make_Directory(Full_Path)

        Output_Filename = f"CLEAN_{File_Name}"
        Output_Path = os.path.join(Full_Path, Output_Filename)

        Save_Format = Original_Image.format if Original_Image.format else "JPEG"

        Clean_Image.save(Output_Path, quality=100, format=Save_Format)

        Clean_Size = os.path.getsize(Output_Path)

        Found_Data["Original File"] = File_Name
        Found_Data["Clean File"] = Output_Filename
        Found_Data["Format"] = Save_Format
        Found_Data["Original Size"] = f"{Original_Size / 1024:.2f} KB"
        Found_Data["Clean Size"] = f"{Clean_Size / 1024:.2f} KB"
        Found_Data["Metadata Status"] = "All EXIF data removed"
        Found_Data["Output Path"] = Output_Path

        return Clean_Folder, Found_Data, Not_Found, Errors

    except Exception as Error:
        Errors.append(f"Process failed: {str(Error)}")
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




def Save_Report(Clean_Folder):

    try:

        Root_Directory = os.path.join("Report", "EXIF_DELETED_REPORT")

        Report_Directory = os.path.join(Root_Directory, Clean_Folder)

        Filename = "Exif_Deleter_Results.json"

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

        Input_Path = Get_Input()

        if Input_Path.lower() == 'b':
            return

        if Input_Path.lower() == 'e':
            Clear_Terminal()
            Console().print("[bold blue]Exited[/bold blue]")
            sys.exit(0)

        if not Input_Path or not os.path.isfile(Input_Path):
            Console().print("\n[bold blue]Invalid file path[/bold blue]")
            time.sleep(1)
            continue

        Reset_Report()

        Report["Input"] = Input_Path

        Clear_Terminal()

        Display_Banner()

        Clean_Folder, Found_Data, Not_Found, Errors = Process(Input_Path)

        if not Clean_Folder and Errors:
            Console().print(f"\n[bold blue]{Errors[0]}[/bold blue] - [bold white]Press Enter to continue[/bold white]")
            Console().input()
            continue

        Report["Found Data"] = Found_Data or {}
        Report["Not Found Data"] = Not_Found
        Report["Errors"] = Errors

        Create_Report(Found_Data or {}, Not_Found, Errors)
        Save_Report(Clean_Folder)

        Console().input("\n[bold blue]Check reports[/bold blue] - [bold white]Press Enter[/bold white]")




if __name__ == "__main__":
    Main()
