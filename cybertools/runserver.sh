#!/bin/bash
nombre_del_entorno="cybertools"
service_port=8000

echo "### Creando entorno virtual $nombre_del_entorno..."
if [ -d "venv" ]; then
    echo "El entorno virtual $nombre_del_entorno ya existe!"
else
    python -m venv $nombre_del_entorno
fi

echo "### Activando entorno virtual $nombre_del_entorno..."
source $nombre_del_entorno/bin/activate

echo "### Instalando dependencias..."
pip install -r requirements.txt

echo "### Actualizando base de datos..."
python manage.py makemigrations
python manage.py migrate

echo "### Iniciando el servicio en http://localhost:$service_port/..."
python manage.py runserver $service_port