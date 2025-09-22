#!/bin/bash

# Obtener el puerto de la variable de entorno o usar 8000 por defecto
PORT=${PORT:-8000}

# Iniciar la aplicación
uvicorn api:app --host 0.0.0.0 --port $PORT
