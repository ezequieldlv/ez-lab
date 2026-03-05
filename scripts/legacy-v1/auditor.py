import psutil # Herramienta para medir hardware
import shutil # Herramienta para operaciones de archivos (espacio en disco)
import requests
import os
from dotenv import load_dotenv

# --- CONFIGURACION DE RUTAS ---
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, '../.env')

# Cargar variables de entorno
load_dotenv(env_path)

# --- CREDENCIALES ---
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Verificación de seguridad
if not TELEGRAM_TOKEN or not CHAT_ID:
    print(f"ERROR CRITICO: No se encontraron las credenciales en: {env_path}")
    print("Asegurate de agregar TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID en tu archivo .env")
    sys.exit(1)

# --- VARIABLES DE UMBRAL ---
DISCO = "/mnt/datos"
LIMITE_DISCO = 85
LIMITE_RAM = 90
LIMITE_TEMP = 75.0

def enviar_telegram(mensaje):
    # Construimos URL
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    #Empaquetamos los datos (A quien y Que decir)
    datos = {
        "chat_id": CHAT_ID,
        "text": mensaje
    }

    try:
        response = requests.post(url, data=datos)
        print(f"📡 Estado Telegram: {response.status_code}")
        if response.status_code != 200:
            print(f"❌ Error detallado: {response.text}")

    except Exception as e:
        print(f"❌ Error enviando a Telegram: {e}")

def check_disco():
    # shutil.disk_usage nos devuelve estos 3 numeros:
    total, usado, libre = shutil.disk_usage(DISCO)

    # Convertimos bytes a Gigabytes (dividiendo por 1024 tres veces: KB, MB, GB)
    gb_libres = libre // (2**30)

    porcentaje = (usado / total) * 100

    print(f"📂 Disco {DISCO}: {gb_libres} GB libres (Uso: {porcentaje:.1f}%)")

    return porcentaje

def check_ram():
    # psutil.virtual_memory() nos devuelve un objeto con todo: total, usada, libre..
    memoria = psutil.virtual_memory()

    print(f"🧠 RAM: {memoria.percent}% usada")

    return memoria.percent

def check_temp():
    """Lee la temperatura de la CPU de la Raspberry Pi"""
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp_mili = int(f.read())

        # Convertimos a grados normales
        temp_c = temp_mili / 1000.0

        print(f"🌡️ Temperatura CPU: {temp_c:.1f}°C")
        return temp_c
    except Exception as e:
        print(f"❌ Error leyendo temperatura: {e}")
        return 0.0

if __name__ == "__main__":
    print("--- 🕵️ INICIANDO AUDITORÍA SRE ---")

# Auditoria de Disco
uso_disco = check_disco()

if uso_disco > LIMITE_DISCO:
    aviso = f"⚠️ ALERTA: Poco espacio en disco ({uso_disco:.1f}%)"
    print(aviso)
    enviar_telegram(aviso)
else:
    print("✅ Disco Saludable")

# Auditoria de RAM
uso_ram = check_ram()

if uso_ram > LIMITE_RAM:
    aviso = f"⚠️ ALERTA: RAM Critica ({uso_ram})%"
    print(aviso)
    enviar_telegram(aviso)
else:
    print("✅ RAM Saludable")

# Auditoria Temperatura
temp_actual = check_temp()

if temp_actual > LIMITE_TEMP:
    aviso = f"🔥 ALERTA DE FUEGO: CPU a {temp_actual:.1f}°C"
    print(aviso)
    enviar_telegram(aviso)
else:
    print("✅ Temperatura Normal")

print("-" * 20)
