# v4.0.0 ✠
# SECURITY CLASS COMPONENT




import os
import subprocess
import sys
import time




from tqdm import tqdm
from rich.console import Console
from rich.panel import Panel
from rich.align import Align




from SECURITY.LINK_ACTIONS import Phishing_Analysis
from SECURITY.DDOS_ACTIONS import DDoS_Analysis
from SECURITY.MEDIA_ACTIONS import Exif_Deleter




def Clear_Terminal():
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)




def Loading_Animation(Duration):
    Console().print("[bold red]Loading...[/bold red]")
    for _ in tqdm(range(Duration), bar_format="{l_bar}{bar}|", colour='red'):
        time.sleep(0.010)
    Clear_Terminal()




def Display_Banner():
    
    Banner_Content = """
    [bold white]
╺┓ ┏━┓┏━┓┏━┓   ╻ ┏━╸ ┏┓╻ ┏━┓
 ┃ ┣━┫┣━┫┗━┫   ┃ ┣╸  ┃┗┫ ┣━┫
╺┻╸┗━┛┗━┛┗━┛   ╹╹┗━╸╹╹ ╹╹╹ ╹[/bold white]

[bold white]SECURITY CENTER[/bold white]

[bold white]Owner License : 1889 I.E.N.A |  Author : Vsevolod Yetzen |  Version : v4.0.0[/bold white] [bold red]✠[/bold red]"""

    Banner_Panel = Panel(
        Align.center(Banner_Content),
        border_style="red",
        padding=(1, 2),
        expand=True
    )

    Console().print(Banner_Panel)




def Display_Menu():

    Panel_1 = Panel(
        "[bold blue][ S1 ][/bold blue] [bold white]PHISHING ANALYSIS TOOL[/bold white]\n"
        "[bold blue][ S2 ][/bold blue] [bold white]DDoS ANALYSIS TOOL[/bold white]\n"
        "[bold blue][ S3 ][/bold blue] [bold white]EXIF DELETER[/bold white]\n\n"
        "[bold white]v4.0.0[/bold white]",
        title="[bold blue]SECURITY TOOLS[/bold blue]",
        border_style="blue",
        padding=(1, 2),
        expand=True
    )

    Console().print(Panel_1)

    System_Panel = Panel(
        "[bold red][ B ][/bold red]  [bold white]Back Main Menu[/bold white]\n"
        "[bold red][ E ][/bold red]  [bold white]Exit Client[/bold white]",
        title="[bold red]SYSTEM COMMANDS[/bold red]",
        border_style="red",
        padding=(1, 2),
        expand=True
    )

    Console().print(System_Panel)




def Get_Input():
    
    Input_Panel = Panel(
        "[bold red]══[/bold red] [bold white]Enter Command[/bold white]",
        border_style="red",
        padding=(0, 2),
        expand=True
    )

    Console().print(Input_Panel)
    
    Choice = Console().input("").strip().lower()
    
    return Choice




def Main():

    while True:
        
        Clear_Terminal()

        Loading_Animation(100)

        Clear_Terminal()

        Display_Banner()

        Display_Menu()

        Choice = Get_Input()

        if Choice == 's1':
            Phishing_Analysis.Main()
            continue  

        if Choice == 's2':
            DDoS_Analysis.Main()
            continue 

        if Choice == 's3':
            Exif_Deleter.Main()
            continue

        if Choice == 'b':
            return

        if Choice == 'e':
            Clear_Terminal()
            Console().print("[bold red]Exited[/bold red]")
            sys.exit(0)




if __name__ == "__main__":
    Main()
