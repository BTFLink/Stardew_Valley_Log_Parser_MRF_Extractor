📄 Stardew Valley SMAPI Log Parser By BTF
🇬🇧 English
📌 Overview

This script is a log parser for Stardew Valley SMAPI logs. It allows you to:

Filter relevant log sections using custom flags
Copy full log files
Work across multiple platforms (Windows, Linux, macOS, Android)
Handle different log locations (including Xbox App environments)
⚙️ Features
🔍 Filter logs based on:
Start flags (flags_to_read.txt)
End flags (finish_flag.txt)
Ignore flags (flags_to_ignore.txt)
📄 Copy full logs without filtering
📱 Android-compatible (with sandbox limitations handled)
🖥️ Cross-platform support
🕒 Automatically timestamped output files
📂 File Structure

The script uses the following configuration files:

flags_to_read.txt → Defines when to start capturing logs
finish_flag.txt → Defines when to stop capturing logs
flags_to_ignore.txt → Defines lines to ignore during capture

These files are automatically created if they do not exist.

🚀 Usage

Run the script:

python script.py

You will see an interactive menu:

1) Filter SMAPI log
2) Copy full log
3) Reload flags
4) Exit
🧠 How It Works

The parser reads log files:

SMAPI-latest.txt
SMAPI-crash.txt
Filtering Logic:
Starts writing when a read flag is detected
Stops when a finish flag is detected
Ignores lines containing ignore flags
Special Finish Flag:

If a finish flag contains <<!>>, it:

Stops writing without including that line
📍 Platform Notes
Windows

Default log path:

%APPDATA%/StardewValley/ErrorLogs
Xbox App alternative path supported
Linux / macOS
~/.config/StardewValley/ErrorLogs
Android

Uses:

/storage/emulated/0
Due to permission restrictions:

Logs may need to be manually copied to:

SV_Log_Parser/SV
📤 Output

Generated files include timestamps:

YYYY-MM-DD_HH-MM-MRF-SMAPI-latest.txt
YYYY-MM-DD_HH-MM-MRF-SMAPI-crash.txt
⚠️ Requirements
Python 3.10+ (for match-case)
Read/write permissions for log directories
🛠️ Customization

Edit the flag files to adjust filtering behavior:

Add keywords to track important events
Ignore noisy log entries
Define custom stop conditions
📜 License

Free to use and modify.

🇪🇸 Español
📌 Descripción

Este script es un parser de logs de SMAPI para Stardew Valley. Permite:

Filtrar partes relevantes del log mediante banderas (flags)
Copiar logs completos
Funcionar en múltiples plataformas (Windows, Linux, macOS, Android)
Manejar distintas rutas de logs (incluyendo Xbox App)
⚙️ Características
🔍 Filtrado de logs basado en:
Banderas de inicio (flags_to_read.txt)
Banderas de finalización (finish_flag.txt)
Banderas de ignorar (flags_to_ignore.txt)
📄 Copia completa de logs
📱 Compatible con Android (considerando restricciones)
🖥️ Soporte multiplataforma
🕒 Archivos de salida con timestamp automático
📂 Estructura de Archivos

El script utiliza:

flags_to_read.txt → Define cuándo empezar a leer
finish_flag.txt → Define cuándo detener la lectura
flags_to_ignore.txt → Define líneas a ignorar

Si no existen, el script los crea automáticamente.

🚀 Uso

Ejecuta el script:

python script.py

Menú interactivo:

1) Filtrar Log SMAPI
2) Copiar Log completo
3) Recargar Flags
4) Salir
🧠 Cómo Funciona

El parser lee los archivos:

SMAPI-latest.txt
SMAPI-crash.txt
Lógica de filtrado:
Empieza a escribir cuando detecta una flag de inicio
Termina cuando detecta una flag de fin
Ignora líneas con flags de ignorar
Flag especial:

Si una flag de final contiene <<!>>:

Detiene la escritura sin incluir esa línea
📍 Notas por Plataforma
Windows

Ruta por defecto:

%APPDATA%/StardewValley/ErrorLogs

Compatible con ruta alternativa de Xbox App

Linux / macOS
~/.config/StardewValley/ErrorLogs
Android

Ruta base:

/storage/emulated/0

Debido a restricciones:

Puede ser necesario copiar manualmente los logs a:
SV_Log_Parser/SV
📤 Salida

Archivos generados:

YYYY-MM-DD_HH-MM-MRF-SMAPI-latest.txt
YYYY-MM-DD_HH-MM-MRF-SMAPI-crash.txt
⚠️ Requisitos
Python 3.10+ (uso de match-case)
Permisos de lectura/escritura
🛠️ Personalización

Puedes editar los archivos de flags para:

Detectar eventos importantes
Ignar ruido del log
Definir condiciones de corte
📜 Licencia

Libre uso y modificación.