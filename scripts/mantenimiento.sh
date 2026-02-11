#!/bin/bash

# Varibles de color
VERDE='\033[0;32m'
SINCOLOR='\033[0m'

echo -e "${VERDE}--- 🚀 INICIANDO MANTENIMIENTO SRE ---${SINCOLOR}"

echo -e "${VERDE}[1/3] Actualizando Sistema Operativo...${SINCOLOR}"

sudo apt update && sudo apt upgrade -y

echo -e "${VERDE}[2/3] Limpiando Basura de Docker...${SINCOLOR}"

# Eliminamos todo lo que no se esté usando actualmente
docker system prune -af

echo -e "${VERDE}[3/3] Verificando espacio final en disco...${SINCOLOR}"

# Filtramos para ver solo el disco de datos
df -h /mnt/datos | grep /mnt/datos

echo -e "${VERDE}--- ✅ MANTENIMIENTO COMPLETADO ---${SINCOLOR}"