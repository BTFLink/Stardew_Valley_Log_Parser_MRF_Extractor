import os
import platform
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field


#BASIC CONFIGURATION

    #Constantes de archivos de StardewValley
SV = "StardewValley"
ERRLOG = "ErrorLogs"
SMAPILOGFILE= "SMAPI-latest.txt"
SMAPICRHFILE= "SMAPI-crash.txt"
SMAPILOG    = "SMAPI-latest"
SMAPICRH    = "SMAPI-crash"

    #Archivos de lectura
REDFILE = "flags_to_read.txt"
FINFILE = "finish_flag.txt"
IGNFILE = "flags_to_ignore.txt"


    #Determina que plataforma esta usando el script
system = platform.system().lower()

    #Sistema para nombrar el archivo de guardado
ahora   = datetime.now()
formato = ahora.strftime("%Y-%m-%d_%H-%M")
savename = lambda file_name:f"{formato}-MRF-{file_name}.txt"


#XBOX File Sistem
#No estoy seguro de la ruta. Se obtuvo de smapi.io/log
XBOX_DEFAULT_PATH = Path(r"Packages\ConcernedApe.StardewValleyPC_0c8vynj4cqe4e\LocalCache\Roaming")

#ANDROID OS
    #Ruta de trabajo de Android
ANDROIDPATH = Path("/storage/emulated/0")

#----------------------------------------------------------------------------------

    #Clase de las rutas
@dataclass
class Routes:
    #Variables de Bandera
    read_flags_path:    Path
    finish_flags_path:  Path
    ignore_flags_path:  Path
    
    #Variables de Lugares de SMAPI (Donde pueden estar los logs)
    smapi_log_path:     Path
    alter_log_path:     Path
    xbox_path:          Path

    #Variables 
    work_path:          Path
    exit_log_path:      Path

    #Bandera de uso de ruta alternativa
    use_alt_path:       bool


    #Clase de las flags
@dataclass
class Flags:
    #flags que el programa leera y transcribira
    read:   list[str] = field(default_factory=list)
    #flags que el programa detecta como final de lectura (Evita transcribir un rato)
    finish: list[str] = field(default_factory=list)
    #flags que permiten ignorar lineas del Log (Lineas intermedias entre inicio y fin)
    ignore: list[str] = field(default_factory=list)

#----------------------------------------------------------------------------------
#   SYSTEM START (INICIO DEL SISTEMA)
def starSystem():
    
    print("System in use: "+system);
    if system not in ("windows","linux","darwin","android"):
        print("Unsupported System.\nClosing Script")
        return
    
    routes = routes_loader()

    flags = cargar_flags(routes)
    
    print("Bienvenido a StarDew Valley Log Praser\n")

    print(f"Cantidad de Flags para iniciar:   {len(flags.read)}")
    print(f"Cantidad de Flags para finalizar: {len(flags.finish)}")
    print(f"Cantidad de Flags a ignorar:      {len(flags.ignore)}")
    filtrable = len(flags.read)>0
    print()

    if system in ("windows","android"):
        message = "Windows detectado\n¿Usas Xbox APP?"
        if system == "android": message ="Android detectado\n¿Quieres usar la carpeta \"SV_Log_Parser/SV\" para leer el log?"
        while True:
            print(message)
            opcion = input("1) SI \n2) NO\n>")
            if opcion in ("1", "2"):
                routes.use_alt_path = opcion == "1"
                break
            print("Opción inválida, intenta de nuevo")
    no_copiable= system == "android" and routes.use_alt_path
    if no_copiable:
        print(f"""
              Si es la primera vez que usas el script,
              se han creado creado carpetas nuevas en tu dispositivo
              cierra el script, copia el log en:
              {routes.alter_log_path}
              (Android no le ha dado permiso para leer fuera de esa carpeta)
              """)
    
    while True:
        menu= f"""
            Menu de opciones
    1) Filtrar Log de StarDew Valley SMAPI (Disponible: {filtrable})
    2) Copiar Log de StarDew Valley (Disponible: {not no_copiable})
    3) Recargar Flags
    4) Salir
        """
        print(menu)
        opcion = input(">")
        print()
        if opcion not in ("1","2","3","4"):
            print("Opcion Invalida")
            continue
        match opcion:
            case "1":
                if filtrable:
                    sv_log_parser(routes,flags)
                else:
                    print("Imposible filtrar sin flags de inicio\nSi quieres copiar el archivo usa la opcion 2\n")
            case "2":
                if no_copiable:
                    print("Bajo las configuraciones actuales no dispones de copiar el archivo\nYa posees el archivo")
                else:
                    sv_log_parser(routes,flags,copy=True)
                
            case "3":
                flags = cargar_flags(routes)
                print(f"Cantidad de Flags para iniciar:   {len(flags.read)}")
                print(f"Cantidad de Flags para finalizar: {len(flags.finish)}")
                print(f"Cantidad de Flags a ignorar:      {len(flags.ignore)}")
                filtrable = len(flags.read)>0
            case "4":
                print("Gracias por usar, Adios.")
                break
    pass

#Cargador de Rutas
def routes_loader() -> Routes:
    use_alt_path=False
    routes_count = 0

    if system == "android":
        
        android_work_path   = ANDROIDPATH / "SV_Log_Parser"
        read_flags_path     = android_work_path / REDFILE
        finish_flags_path   = android_work_path / FINFILE
        ignore_flags_path   = android_work_path / IGNFILE
        smapi_log_path      = ANDROIDPATH
        newRoute            = smapi_log_path
        for p in smapi_log_path.rglob("ErrorLogs"):
            if "stardew" in str(p).lower():
                print(p)
                routes_count+=1
                newRoute = p
        if routes_count!=1 :
            use_alt_path=True
        smapi_log_path  = newRoute
        alter_log_path  = android_work_path / SV
        alter_log_path.mkdir(parents=True, exist_ok=True)
        exit_log_path   = android_work_path
        work_path       = android_work_path
        
    else:
        work_path   = Path(__file__).resolve().parent
        read_flags_path     = work_path / REDFILE
        finish_flags_path   = work_path / FINFILE
        ignore_flags_path   = work_path / IGNFILE
        exit_log_path       = work_path
        
        if system == "windows":
            smapi_log_path  = Path(os.environ["APPDATA"])/SV/ERRLOG
            alter_log_path  = Path(os.environ["LOCALAPPDATA"])/XBOX_DEFAULT_PATH/SV/ERRLOG
        else:
            smapi_log_path  = Path.home()/".config"/SV/ERRLOG
            alter_log_path  = smapi_log_path
    

    return Routes(read_flags_path,finish_flags_path,ignore_flags_path,
        smapi_log_path,alter_log_path,XBOX_DEFAULT_PATH,work_path,exit_log_path,use_alt_path)

#Creacion de archivos base si no existen
def create_flag_files(routes: Routes):
    routes.read_flags_path.touch()
    routes.finish_flags_path.touch()
    routes.ignore_flags_path.touch()

#Cargador de Banderas
def cargar_flags(routes: Routes):
    create_flag_files(routes)
    return Flags(
        read=flags_path_reader(routes.read_flags_path),
        finish=flags_path_reader(routes.finish_flags_path),
        ignore=flags_path_reader(routes.ignore_flags_path),
    )

#Lector del Archivo Banderas
def flags_path_reader(path_flags: Path) ->list[str]:
    try:
        if path_flags.is_file():
            with open(path_flags, "r") as f:
                return [line.strip() for line in f if line.strip()]
        return []
    except OSError as e:
        print(f"Error leyendo {path_flags}: {e}")
        return []

#Funcion encargada de preparar los archivos de salida y mandarlos al write_files
def sv_log_parser(routes: Routes,flags: Flags,copy: bool = False):
    
    file_path_to_read = (
        routes.alter_log_path
        if routes.use_alt_path
        else routes.smapi_log_path
    )

    latest_log_file = file_path_to_read / SMAPILOGFILE
    crash_log_file  = file_path_to_read / SMAPICRHFILE

    exit_name_1 = SMAPILOG+"-COPIA" if copy else SMAPILOG
    exit_name_2 = SMAPICRH+"-COPIA" if copy else SMAPICRH
    
    exit_file_Path_1 = routes.exit_log_path / savename(exit_name_1);
    exit_file_Path_2 = routes.exit_log_path / savename(exit_name_2);
    file_1_FLAG = False;
    file_2_FLAG = False;

    try:
        
        #Verificar si el archivo existe en la ruta especificada
        if latest_log_file.is_file():
            file_1_FLAG=True;
            write_files(latest_log_file,exit_file_Path_1,flags,copy)
        
        if crash_log_file.is_file():
            file_2_FLAG = True;
            write_files(crash_log_file,exit_file_Path_2,flags,copy)
    
    except FileNotFoundError as fnf:
        print(fnf);
    except PermissionError as pe:
        print(pe);
    except OSError as e:
        print(e);
    else:
        if file_1_FLAG or file_2_FLAG:
            print("Salida de los archivos en:")
            if file_1_FLAG:
                print(str(exit_file_Path_1))
            if file_2_FLAG:
                print(str(exit_file_Path_2))
        else:
            print("Archivos logs no encontrados")

#Seccion encargada de escribir los archivos
def write_files(file_to_read: Path, exit_file_Path: Path, flags: Flags, copy: bool):
    try:
        with open(file_to_read, "r", encoding="utf-8") as infile, \
             open(exit_file_Path, "w", encoding="utf-8") as outfile:

            if copy:
                for linea in infile:
                    outfile.write(linea)
                return

            writing = False

            finish_special = [f.replace("<<!>>", "") for f in flags.finish if "<<!>>" in f]
            finish_normal  = [f for f in flags.finish if "<<!>>" not in f]

            for linea in infile:
                linea = linea.rstrip("\n")

                is_read    = any(flag in linea for flag in flags.read)
                is_ignore  = any(flag in linea for flag in flags.ignore)
                is_special = any(flag in linea for flag in finish_special)
                is_finish  = any(flag in linea for flag in finish_normal)

                if is_read: writing = True

                if writing:
                    if is_ignore: continue

                    if is_special:
                        writing = False
                        continue

                    outfile.write(linea + "\n")

                    if is_finish: writing = False

    except OSError as e:
        print(e)

starSystem()
