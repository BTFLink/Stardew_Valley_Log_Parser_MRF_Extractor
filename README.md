🎮 Stardew Valley Log Parser (MRF Extractor)

Este script en Python está diseñado para leer y filtrar logs de SMAPI de Stardew Valley, específicamente relacionados con el mod Music Replacement Framework (MRF), y generar archivos de salida limpios con la información relevante.

📌 ¿Qué hace este script?
Detecta automáticamente el sistema operativo (Windows, Linux, macOS o Android).
Localiza los archivos de log de SMAPI:
SMAPI-latest.txt
SMAPI-crash.txt
Extrae únicamente las secciones relacionadas con el mod MRF.
Filtra líneas según una lista de “flags” ignorados.

Genera archivos de salida con formato:

YYYY-MM-DD_HH-MM-MRF-1.txt
YYYY-MM-DD_HH-MM-MRF-2.txt
Guarda los resultados en la misma carpeta del script o en rutas alternativas según el sistema.
🧠 Cómo funciona

El script busca bloques dentro del log delimitados por:

Inicio del bloque:
INFO Music Replacement Framework] Track=
INFO Music Replacement Framework] Want to replace this music?
Fin del bloque:
----------------------------------

Solo las líneas dentro de esos bloques son procesadas y escritas en los archivos de salida.

🖥️ Compatibilidad

El script soporta múltiples plataformas:

🪟 Windows
Soporta ruta estándar de AppData
Soporte opcional para Xbox App
🐧 Linux
Usa ~/.config/StardewValley/ErrorLogs
🍎 macOS
Misma ruta que Linux (darwin)
🤖 Android
Busca logs en almacenamiento interno
Usa ruta alternativa si hay problemas de permisos
⚙️ Configuración
📄 Archivo de flags ignorados

Puedes crear o editar:

flags_to_ignore.txt

Ubicado en la misma carpeta del script.

Cada línea representa un texto que será ignorado durante el procesamiento del log.

📂 Archivos de entrada

El script espera encontrar:

SMAPI-latest.txt
SMAPI-crash.txt

Dentro de la carpeta de logs de Stardew Valley según el sistema.

📤 Archivos de salida

Los resultados se guardan como:

YYYY-MM-DD_HH-MM-MRF-1.txt
YYYY-MM-DD_HH-MM-MRF-2.txt
-1 → log principal
-2 → crash log (si existe)
🚀 Ejecución

Ejecuta el script con Python:

python script.py

Durante la ejecución:

En Windows se te preguntará si usas Xbox App.
El script detecta automáticamente rutas y sistema operativo.
Muestra la ubicación final de los archivos generados.
⚠️ Notas importantes
Si no se detecta una ruta válida, el script se detendrá.
En Android puede requerir permisos de almacenamiento.
Si no hay logs disponibles, no se generará salida.
El filtrado depende de ignoreFlagsPath.
🧩 Variables clave del script
STARTFLAG1 / STARTFLAG2 → Inicio de extracción
ENDFLAG → Fin de bloque
ignoreFlags → Líneas ignoradas
savename → Generación de nombre de archivo con timestamp
useAltPath → Selección de ruta alternativa
👨‍💻 Autor / Uso

Script creado para facilitar el análisis de logs de Stardew Valley relacionados con el mod Music Replacement Framework.