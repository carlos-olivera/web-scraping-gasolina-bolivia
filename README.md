
# Proyecto de Obtención y Almacenamiento de Datos de Gasolineras Biopetrol Bolivia

## Objetivo del Proyecto

El objetivo de este proyecto es desarrollar una aplicación en Python que obtenga información sobre la disponibilidad de gasolina en diferentes gasolineras desde una página web específica. La información obtenida se almacena en una base de datos MongoDB para su posterior consulta y análisis.

## Componentes del Proyecto

El proyecto está compuesto por los siguientes componentes:

1. **Script de Python (`app.py`)**: Encapsula la lógica para obtener, procesar y almacenar los datos de las gasolineras.
2. **Dockerfile**: Archivo de configuración para construir una imagen de Docker del script de Python.
3. **Docker Compose (`docker-compose.yml`)**: Archivo de configuración para orquestar la ejecución del contenedor de Python y el contenedor de MongoDB.
4. **Archivo de Requerimientos (`requirements.txt`)**: Lista de dependencias de Python necesarias para ejecutar el script.
5. **Archivo de Entorno (`.env`)**: Archivo para definir las variables de entorno necesarias para configurar MongoDB.

## Estructura de Directorios

El proyecto tiene la siguiente estructura de directorios:

```plaintext
.
├── database
│   └── data
├── .env
├── app.py
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

- `database`: Directorio para almacenar los datos persistentes de MongoDB.
- `.env`: Archivo para configurar las variables de entorno.
- `app.py`: Script de Python principal.
- `docker-compose.yml`: Archivo de configuración para Docker Compose.
- `Dockerfile`: Archivo de configuración para la imagen de Docker.
- `requirements.txt`: Lista de dependencias de Python.

## Lógica del Código de Python (`app.py`)

El código de Python está encapsulado en la clase `GetGasStations`, que tiene los siguientes métodos principales:

- `__init__`: Inicializa la clase, configurando la URL de la página web y estableciendo la conexión a la base de datos MongoDB.
- `updateGasStations`: Obtiene y procesa los datos de las gasolineras desde la página web, y los almacena en MongoDB.
- `start`: Ejecuta el método `updateGasStations` cada 15 minutos de forma indefinida.

El script sigue estos pasos:

1. Obtiene el contenido HTML de la página web.
2. Analiza el contenido HTML para encontrar la información de las gasolineras.
3. Extrae los datos relevantes (descripción, cantidad de litros disponibles, fecha y hora de la medición, y ubicación).
4. Almacena los datos en la base de datos MongoDB en la colección `surtidores`.

## Guía para Ejecutar el Proyecto

Sigue estos pasos para ejecutar el proyecto:

1. Clona el repositorio del proyecto en tu máquina local.
2. Navega al directorio del proyecto.

```bash
cd nombre-del-directorio-del-proyecto
```

3. Crea un archivo `.env` en el directorio raíz del proyecto con el siguiente contenido:

```plaintext
MONGO_INITDB_ROOT_USERNAME=root
MONGO_INITDB_ROOT_PASSWORD=example
MONGO_INITDB_DATABASE=gasolinedb
```

4. Construye y levanta los servicios de Docker usando Docker Compose:

```bash
docker-compose up --build
```

Este comando construirá las imágenes de Docker y levantará los contenedores definidos en el archivo `docker-compose.yml`.

5. El script de Python (`app.py`) se ejecutará automáticamente y comenzará a actualizar los datos de las gasolineras cada 15 minutos, almacenándolos en MongoDB.

6. Para detener los servicios, presiona `Ctrl+C` en la terminal donde se está ejecutando Docker Compose y luego ejecuta:

```bash
docker-compose down
```

Esto detendrá y eliminará los contenedores levantados por Docker Compose.

## Notas

- Asegúrate de tener Docker y Docker Compose instalados en tu máquina.
- Verifica que las variables de entorno en el archivo `.env` estén configuradas correctamente.

## Licencia
Este proyecto está licenciado bajo la Licencia Pública General de GNU versión 3 (GPL-3.0). Esto significa que puedes distribuir, modificar y usar libremente este software bajo los términos de esta licencia. La GPL-3.0 garantiza que los derechos de los usuarios estén protegidos y que las modificaciones y versiones derivadas del proyecto también estén cubiertas por la misma licencia.