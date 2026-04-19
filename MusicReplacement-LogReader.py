import os
import platform
from pathlib import Path
from datetime import datetime


#Constantes de archivos de StardewValley
SV = "StardewValley"
ERRLOG = "ErrorLogs"
SMAPILOGFILE = "SMAPI-latest.txt"
SMAPICRHFILE = "SMAPI-crash.txt"

#Banderas al momento de leer archivos
STARTFLAG1 = "INFO  Music Replacement Framework] Track="
STARTFLAG2 = "INFO  Music Replacement Framework] Want to replace this music?"
ENDFLAG = "----------------------------------"

#Tambien es una constante pero no estoy seguro. Se obtuvo de smapi.io/log
XBOXPATH = r"Packages\ConcernedApe.StardewValleyPC_0c8vynj4cqe4e\LocalCache\Roaming"

#Path alternativo y de salida de Android (Android jode mucho)
ANDROIDLOGPATH = Path("/storage/emulated/0") / "MusicReplaceFrameWork"

#Sistema para nombrar el archivo de guardado
savename = lambda fileN:f"{formato}-MRF-{fileN}.txt"
ahora = datetime.now()
formato = ahora.strftime("%Y-%m-%d_%H-%M")

#Determina que plataforma esta usando el script
system = platform.system().lower()

#Variables donde se almacena la ruta de archivos
#altLogPath es el alternativo para windows/xboxapp y android
smapiLogPath = "NOFILE";
altLogPath  = "NOFILE";
exitLogPath = Path(__file__).parent;

#Ruta y flags que permiten ignorar lineas del Log, deben ser modificadas por los usuarios
ignoreFlagsPath = Path(__file__).parent / "flags_to_ignore.txt"
ignoreFlags =[];


#Utilizado en Windows por el usuario, automatico en android
useAltPath = False;

#Determina la carpeta de sistema a utilizar
def logPathSelection():
    global smapiLogPath
    global altLogPath
    global useAltPath
    global exitLogPath
    match system:
        case "windows":
            #Windows tiene una ruta alternativa en caso de usar XBOXAPP (NI PTA IDEA)
            smapiLogPath = Path(os.environ["APPDATA"])/SV/ERRLOG
            altLogPath = Path(os.environ["LOCALAPPDATA"])/XBOXPATH/SV/ERRLOG

            #print("windows Case")
            #print(smapiLogPath)
            #print(altLogPath)
            while True:
                userInput = input(""" Windows Detected
                                  is for XBOX APP?
                                  1) Yes
                                  2) No
                                  Answer: """)
                print()
                if(userInput=="1" or userInput=="2"):
                    useAltPath= userInput=="1";
                    break
                print("Invalid entry, let me ask again...\n")

        case "linux","darwin":
            #Tanto Linux como Mac (Darwin) usan la misma ruta
            smapiLogPath = Path.home()/".config"/SV/ERRLOG

        case "android":
            #Android tiene ruta alternativa en caso de error con permisos
            smapiLogPath =Path("/storage/emulated/0")
            routesCount=0;
            for p in smapiLogPath.rglob("ErrorLogs"):
                if "stardew" in str(p).lower():
                    print(p)
                    routesCount+=1;
                    newRoute = p;
            if (routesCount>1 or routesCount==0):
                useAltPath=True;
            smapiLogPath = Path(newRoute);
            altLogPath = ANDROIDLOGPATH / SV
            altLogPath.mkdir(parents=True, exist_ok=True)
            exitLogPath= ANDROIDLOGPATH

        case _:
            #Si no se determina el sistema... Pues valio queso
            print(f"Unable to find a path for {system} system");
    pass

#Lector del Archivo Banderas para ignorar lineas especificas
def cargar_flags(path_flags):
    try:
        if path_flags.is_file():
            with open(path_flags, "r") as f:
                return [line.strip() for line in f if line.strip()]
        else:
            path_flags.touch()
            return []
    except ValueError as ve:
        print(ve);
        return[]


#Seccion encargada de escribir los archivos
def writefiles(fileToRead,exitfilePath):
    writing = False;
    try:
        if fileToRead.is_file():
            with open(fileToRead, "r", encoding="utf-8") as infile, open(exitfilePath, "w", encoding ="utf-8") as outfile:
                for linea in infile:
                    linea = linea.strip()

                    if STARTFLAG1 in linea:
                        writing = True
                    if STARTFLAG2 in linea:
                        writing = True
                    if writing:
                        if any(flag in linea for flag in ignoreFlags):
                            continue
                        outfile.write(linea + "\n")
                    if ENDFLAG in linea:
                        writing = False
    except ValueError as ve:
        print(ve)
    

def readSVLogFile():
    filePathToRead = smapiLogPath;
    exitfilePath1 = Path(exitLogPath)/ savename("1");
    exitfilePath2 = Path(exitLogPath)/ savename("2");
    file1FLAG = False;
    file2FLAG = False;
    match system:
        case "windows":
            if useAltPath:
                filePathToRead = altLogPath;
        case "android":
            if useAltPath:
                filePathToRead = useAltPath;
    fileToRead1= filePathToRead / SMAPILOGFILE
    fileToRead2= filePathToRead / SMAPICRHFILE

    try:
        #Verificar si el archivo existe en la ruta especificada
        if fileToRead1.is_file():
            file1FLAG=True;
            writefiles(fileToRead1,exitfilePath1)
        
        if fileToRead2.is_file():
            file2FLAG = True;
            writefiles(fileToRead2,exitfilePath2)
            
        
    except FileNotFoundError as fnf:
        print(fnf);
    except PermissionError as pe:
        print(pe);
    except ValueError as e:
        print(e);
    else:
        print("Salida de los archivos en:")
        if file1FLAG:
            print(str(exitfilePath1))
        if file2FLAG:
            print(str(exitfilePath2))
    

def starSystem():
    print("System in use: "+system);
    global ignoreFlags
    ignoreFlags = cargar_flags(ignoreFlagsPath);
    print(f"Cantidad de Flags a ignorar: {len(ignoreFlags)}")
    logPathSelection();
    if (altLogPath=="NOFILE" and smapiLogPath=="NOFILE"):
        print("Closing Script")
        return
    readSVLogFile()
    pass

starSystem()