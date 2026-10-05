# v4.0.0 ✠
# SECURITY CLASS COMPONENT




import os
import sys
import time
import json
import warnings
import subprocess
import collections




from typing import Any
from tqdm import tqdm
from rich.console import Console
from rich.panel import Panel
from rich.align import Align




from scapy.all import sniff
from scapy.layers.inet import TCP, UDP, ICMP, IP




warnings.simplefilter('ignore')




Suspicious_Protocols = ["ICMP", "UDP"]




Known_Attack_Ports = [
    80, 443, 53, 22, 21, 25, 3389, 5060, 123, 161, 
    1900, 111, 137, 138, 139, 445, 69, 520, 1434
]




Traffic_Data: list[Any] = []
Report: dict[str, Any] = {}




def Clear_Terminal():
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)




def Check_Root_Privileges():

    if os.name == 'posix':

        try:

            if os.geteuid() != 0:
                Console().print("\n[bold blue]This code requires Root privileges[/bold blue]")
                time.sleep(3)
                return False
            
            else:
                return True
            
        except AttributeError:
            return True
        
    return True




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

[bold white]DDoS ANALYSIS TOOL[/bold white]

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
        "[bold blue]+[/bold blue] [bold white]Monitor network traffic[/bold white]\n"
        "[bold blue]+[/bold blue] [bold white]Analyze protocol distribution[/bold white]\n"
        "[bold blue]+[/bold blue] [bold white]Detect port activity[/bold white]\n"
        "[bold blue]+[/bold blue] [bold white]Examine source IP behavior[/bold white]\n\n"
        "[bold white]DEVICE PERMISSION -[/bold white] [bold blue]Root[/bold blue]",
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
        "[bold blue]══[/bold blue] [bold white]Analysis Duration (Seconds)[/bold white]",
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




def Analyze_Packet(Packet):

    global Traffic_Data

    if IP in Packet:

        Source_Ip = Packet[IP].src
        Destination_Ip = Packet[IP].dst
        Protocol = Packet[IP].proto
        Length = len(Packet)
        
        Source_Port = None
        Destination_Port = None
        
        Protocol_Name = "Unknown"
        
        if TCP in Packet:
            Protocol_Name = "TCP"
            Source_Port = Packet[TCP].sport
            Destination_Port = Packet[TCP].dport
        
        elif UDP in Packet:
            Protocol_Name = "UDP"
            Source_Port = Packet[UDP].sport
            Destination_Port = Packet[UDP].dport
        
        elif ICMP in Packet:
            Protocol_Name = "ICMP"
        
        else:
            Protocol_Name = str(Protocol)

        Traffic_Data.append({
            "Source_Ip": Source_Ip,
            "Destination_Ip": Destination_Ip,
            "Protocol": Protocol_Name,
            "Length": Length,
            "Source_Port": Source_Port,
            "Destination_Port": Destination_Port
        })




def Process(Duration):

    Found_Data = {}
    Not_Found = []
    Errors = []
    
    try:

        sniff(prn=Analyze_Packet, timeout=Duration, store=0)
        
        if not Traffic_Data:
            Errors.append("No network traffic captured in specified duration")
            return None, Not_Found, Errors
        
        Total_Packets = len(Traffic_Data)
        Total_Bytes = sum(P["Length"] for P in Traffic_Data)
        
        Found_Data["Total packets"] = str(Total_Packets)

        Found_Data["Total duration"] = f"{Duration} seconds"

        Found_Data["Average packets/sec"] = f"{Total_Packets / Duration:.2f}" if Duration > 0 else "0.00"

        Found_Data["Total data"] = f"{Total_Bytes / 1024:.2f} KB"
        

        Protocol_Counts = collections.Counter(P["Protocol"] for P in Traffic_Data)

        for Proto, Count in Protocol_Counts.items():
            Percentage = (Count / Total_Packets) * 100 if Total_Packets > 0 else 0
            Found_Data[f"Protocol {Proto}"] = f"{Count} packets ({Percentage:.2f}%)"
        
        Target_Ports = collections.Counter(P["Destination_Port"] for P in Traffic_Data if P["Destination_Port"] is not None)

        Top_Ports = dict(Target_Ports.most_common(10))
        
        for Port, Count in Top_Ports.items():
            Found_Data[f"Port {Port}"] = f"{Count} connections"
        
        if not Top_Ports:
            Not_Found.append("Port activity")
        
        Source_Counts = collections.Counter(P["Source_Ip"] for P in Traffic_Data)

        Total_Sources = len(Source_Counts)
        
        Found_Data["Total source IPs"] = str(Total_Sources)
        
        Top_Sources = dict(Source_Counts.most_common(5))

        for Ip, Count in Top_Sources.items():
            Pps = Count / Duration if Duration > 0 else 0
            Found_Data[f"Source IP {Ip}"] = f"{Count} packets ({Pps:.2f} P/S)"
        
        return Found_Data, Not_Found, Errors
        
    except PermissionError:
        return None, Not_Found, Errors

    except Exception:
        return None, Not_Found, Errors




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




def Save_Report(Duration):

    try:
        
        Root_Directory = os.path.join("Report", "DDOS_REPORT")
        
        Folder_Name = f"Analysis_{Duration}s_{int(time.time())}"
        
        Report_Directory = os.path.join(Root_Directory, Folder_Name)

        Filename = "DDoS_Results.json"
        
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

        if not Check_Root_Privileges():
            return

        Loading_Animation(100)

        Clear_Terminal()

        Display_Banner()

        Display_Info()

        Display_Menu()

        Input_Duration = Get_Input()

        if Input_Duration.lower() == 'b':
            return
    
        if Input_Duration.lower() == 'e':
            Clear_Terminal()
            Console().print("[bold blue]Exited[/bold blue]")
            sys.exit(0)

        if not Input_Duration:
            Console().print("\n[bold blue]Invalid input[/bold blue]")
            time.sleep(1)
            continue
            
        try:
            Duration = int(Input_Duration)
            if Duration <= 0:
                Console().print("\n[bold blue]Analysis duration must be greater than 0[/bold blue]")
                time.sleep(1)
                continue
        
        except ValueError:
            Console().print("\n[bold blue]Enter numbers only[/bold blue]")
            time.sleep(1)
            continue

        global Traffic_Data
        
        Traffic_Data = []

        Reset_Report()
    
        Report["Input"] = f"{Duration} seconds"

        Clear_Terminal()

        Display_Banner()

        Found_Data, Not_Found, Errors = Process(Duration)

        if Found_Data is None and Errors:
            Console().print(f"\n[bold blue]{Errors[0]}[/bold blue] - [bold white]Press Enter to continue[/bold white]")
            Console().input()
            continue

        Report["Found Data"] = Found_Data or {}
        Report["Not Found Data"] = Not_Found
        Report["Errors"] = Errors

        Create_Report(Found_Data or {}, Not_Found, Errors)
        Save_Report(Duration)

        Console().input("\n[bold blue]Check reports[/bold blue] - [bold white]Press Enter[/bold white]")




if __name__ == "__main__":
    Main()
