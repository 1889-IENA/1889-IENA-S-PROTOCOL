# v4.0.0 ✠
# MAIN COMPONENT




import os
import subprocess
import shutil




from rich.console import Console
from rich.panel import Panel
from rich.align import Align




def Clear_Terminal():
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)




def Clear_Reports(Path="Report"):

    if not os.path.exists(Path):
        return

    for Filename in os.listdir(Path):

        Filepath = os.path.join(Path, Filename)
        
        try:

            if os.path.isfile(Filepath) and Filename != "Null.txt":
                os.unlink(Filepath)
            
            elif os.path.isdir(Filepath):
                shutil.rmtree(Filepath)
            
        except Exception:
            pass




def Clear_Pycache():

    for Dirpath, Dirnames, Filenames in os.walk('.'):

        if '__pycache__' in Dirnames:

            Pycache_Path = os.path.join(Dirpath, '__pycache__')

            try:
                shutil.rmtree(Pycache_Path)
            except Exception:
                pass




def Display_Banner():
    
    Banner_Content = """[bold white]Cache Cleaned[/bold white]"""
    Banner_Panel = Panel(
        Align.center(Banner_Content),
        border_style="red",
        padding=(1, 2),
        expand=True
    )

    Console().print(Banner_Panel)




if __name__ == "__main__":

    Clear_Terminal()

    Clear_Pycache()

    Display_Banner()
