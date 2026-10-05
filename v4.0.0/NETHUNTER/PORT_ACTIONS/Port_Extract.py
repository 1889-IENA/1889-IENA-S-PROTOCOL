# v4.0.0 ✠
# NETHUNTER CLASS COMPONENT




import os
import sys
import time
import json
import socket
import warnings
import subprocess
import concurrent.futures




from typing import Any
from tqdm import tqdm
from io import StringIO
from rich.console import Console
from rich.panel import Panel
from rich.align import Align




from scapy.layers.inet import IP, TCP, ICMP
from scapy.volatile import RandShort
from scapy.sendrecv import sr1, send
from contextlib import redirect_stderr




warnings.simplefilter('ignore')




Report: dict[str, Any] = {}




def Clear_Terminal():
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)




def Check_Root_Privileges():

    if os.name == 'posix':

        try:

            if os.geteuid() != 0:
                Console().print("\n[bold green]This code requires Root privileges[/bold green]")
                time.sleep(3)
                return False

            else:
                return True
            
        except AttributeError:
            return True
        
    return True




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

[bold white]PORT EXTRACT TOOL[/bold white]

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
        "[bold green]+[/bold green] [bold white]SYN port scanning[/bold white]\n"
        "[bold green]+[/bold green] [bold white]Service banner detection[/bold white]\n"
        "[bold green]+[/bold green] [bold white]Operating system detection[/bold white]\n\n"
        "[bold white]DEVICE PERMISSION -[/bold white] [bold green]Root[/bold green]",
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




def Get_Scan_Type():
    
    Input_Panel = Panel(
        "[bold green]══[/bold green] [bold white]Scan Type ( Fast / All / Manual )[/bold white]",
        border_style="green",
        padding=(0, 2),
        expand=True
    )

    Console().print(Input_Panel)
    
    Choice = Console().input("").strip().lower()
    
    return Choice




def Get_Port_Range():
    
    Input_Panel = Panel(
        "[bold green]══[/bold green] [bold white]Port Range (1-1000)[/bold white]",
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




def Syn_Scan(Target_Ip, Target_Port):

    try:

        Src_Port = RandShort()
        Syn_Packet = IP(dst=Target_Ip)/TCP(sport=Src_Port, dport=Target_Port, flags="S")
        Response = sr1(Syn_Packet, timeout=1, verbose=False)

        if Response and Response.haslayer(TCP):

            Tcp_Layer = Response.getlayer(TCP)

            if Tcp_Layer:

                if Tcp_Layer.flags == 0x12:
                    Rst_Packet = IP(dst=Target_Ip)/TCP(sport=Src_Port, dport=Target_Port, flags="R")
                    send(Rst_Packet, verbose=False)
                    return "open"
                
                elif Tcp_Layer.flags == 0x14:
                    return "closed"
        
        return "filtered"
    
    except (KeyboardInterrupt, SystemExit):
        raise
    
    except Exception:
        return "filtered"




def Get_Banner(Target_Ip, Port):

    try:

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as S:
            
            S.settimeout(2)
            S.connect((Target_Ip, Port))
            S.send(b"HEAD / HTTP/1.1\r\nHost: example.com\r\n\r\n") 

            Banner_Full = S.recv(1024).decode().strip()
            Banner_First_Line = Banner_Full.split('\n')[0].strip()
            return Banner_First_Line
        
    except Exception:
        return None




def Detect_Os(Target_Ip):

    try:

        Response = sr1(IP(dst=Target_Ip)/ICMP(), timeout=1, verbose=False)

        if Response and Response.haslayer(IP):

            Ip_Layer = Response.getlayer(IP)

            if Ip_Layer:

                Ttl = Ip_Layer.ttl

                if Ttl <= 64:
                    return "Linux/Unix"
                
                elif Ttl <= 128:
                    return "Windows"
                
                else:
                    return "Unknown"
                
            return "Unknown"
        
    except Exception:
        return "Unknown"




def Process(Target_Ip, Scan_Type, Custom_Range=None):

    Found_Data = {}
    Not_Found = []
    Errors = []
    
    try:

        Fake_Stderr = StringIO()

        with redirect_stderr(Fake_Stderr):
            
            if Scan_Type == "fast":
                Ports = [22, 80, 443, 3306, 8080, 53, 21, 23, 25, 110, 137, 138, 139, 445]
            
            elif Scan_Type == "all":
                Ports = list(range(1, 65536))
            
            elif Scan_Type == "manual" and Custom_Range:
                try:
                    Start_Port, End_Port = map(int, Custom_Range.split('-'))
                    Ports = list(range(Start_Port, End_Port + 1))
                
                except ValueError:
                    Errors.append("Invalid port range format")
                    return None, {}, Not_Found, Errors
                
            else:
                Errors.append("Invalid scan type")
                return None, {}, Not_Found, Errors

            Os_Detected = Detect_Os(Target_Ip)

            Found_Data["Target IP"] = Target_Ip

            Found_Data["Operating system"] = Os_Detected

            Found_Data["Scanned ports count"] = str(len(Ports))

            Found_Data["Scan type"] = Scan_Type

            Open_Ports = []
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as Executor:

                Futures = {Executor.submit(Syn_Scan, Target_Ip, Port): Port for Port in Ports}

                for Future in tqdm(concurrent.futures.as_completed(Futures), total=len(Futures), bar_format="{l_bar}{bar}|", colour='green'):

                    Port = Futures[Future]
                    Status = Future.result()

                    if Status == "open":
                        Banner = Get_Banner(Target_Ip, Port)
                        Service = str(Banner) if Banner else "Unknown"
                        Open_Ports.append({"port": Port, "service": Service})
                        Found_Data[f"Port {Port}"] = f"Open - Service: {Service}"

            if not Open_Ports:
                Not_Found.append("No open ports found")

        Port_Folder = f"PORT_{Target_Ip.replace('.', '_')}"

        Root_Directory = os.path.join("Report", "PORT_REPORT")

        Full_Path = os.path.join(Root_Directory, Port_Folder)

        Make_Directory(Full_Path)

        return Port_Folder, Found_Data, Not_Found, Errors

    except Exception:
        Errors.append("Port scanning failed")
        return None, {}, Not_Found, Errors




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




def Save_Report(Port_Folder):

    try:
        
        Root_Directory = os.path.join("Report", "PORT_REPORT")

        Report_Directory = os.path.join(Root_Directory, Port_Folder)

        Filename = "Port_Results.json"
        
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

        if not Check_Root_Privileges():
            return

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

        Scan_Type = Get_Scan_Type()

        Custom_Range = None

        if Scan_Type == "manual":
            Custom_Range = Get_Port_Range()

        if Scan_Type not in ["fast", "all", "manual"]:
            Console().print("\n[bold green]Invalid scan type[/bold green]")
            time.sleep(1)
            continue

        Reset_Report()
        
        Report["Input"] = Input_Ip

        Clear_Terminal()

        Display_Banner()

        Port_Folder, Found_Data, Not_Found, Errors = Process(Input_Ip, Scan_Type, Custom_Range)

        if not Port_Folder and Errors:
            Console().print(f"\n[bold green]{Errors[0]}[/bold green] - [bold white]Press Enter to continue[/bold white]")
            Console().input()
            continue

        Report["Found Data"] = Found_Data or {}
        Report["Not Found Data"] = Not_Found
        Report["Errors"] = Errors

        Create_Report(Found_Data or {}, Not_Found, Errors)
        Save_Report(Port_Folder)

        Console().input("\n[bold green]Check reports[/bold green] - [bold white]Press Enter[/bold white]")




if __name__ == "__main__":
    Main()
