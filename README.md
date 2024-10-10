Django Starter Template

Este es un proyecto base de Django configurado siguiendo la guía oficial de Django: https://docs.djangoproject.com/en/5.0/intro/tutorial01/

Requisitos Previos

Antes de comenzar, asegúrate de tener instalados los siguientes programas en tu sistema:

1. Python (versión 3.8 o superior)
2. Django (versión 5.0 o superior)
3. Node.js (versión 14.x o superior) y npm (Node Package Manager)

Configuración del Entorno de Desarrollo

Sigue estos pasos para configurar y ejecutar el proyecto:

1. Clonar el Repositorio

   Clona este repositorio en tu máquina local:

   git clone https://github.com/tu_usuario/tu_repositorio.git
   cd tu_repositorio

2. Crear y Activar un Entorno Virtual de Python

   Es recomendable utilizar un entorno virtual para gestionar las dependencias de Python:

   python3 -m venv venv
   source venv/bin/activate  # En Windows usa: venv\Scripts\activate

3. Instalar las Dependencias de Python

   Una vez activado el entorno virtual, instala las dependencias necesarias para el proyecto:

   pip install -r requirements.txt

4. Instalar Dependencias de Node.js

   El proyecto incluye una configuración para gestionar las dependencias de Node.js, como Bootstrap, jQuery, y otros módulos de JavaScript que se utilizarán en el frontend del proyecto.

   Para instalar estas dependencias, sigue estos pasos:

   4.1 Navegar al Directorio de tu Proyecto

   Asegúrate de estar en el directorio raíz de tu proyecto Django:

   cd mysite

   4.2 Ejecutar npm install

   Ejecuta el siguiente comando para descargar e instalar todos los módulos listados en el archivo package.json:

   npm install

   Este comando descargará todas las dependencias necesarias y las guardará en el directorio node_modules.

5. Configuración de Archivos Estáticos

   Django maneja los archivos estáticos (como CSS, JavaScript, imágenes, etc.) de forma particular. Asegúrate de tener configurada la ruta correcta en tu archivo de configuración settings.py para incluir los archivos de Node.js.

   En tu archivo settings.py, asegúrate de tener algo como esto:

   import os

   # Ruta donde se encuentran los módulos de Node.js
   BOOSTRAP_ROOT = Path(__file__).resolve().parent.parent.parent / 'node_modules/'

   # Configura los archivos estáticos
   STATICFILES_DIRS = [
        f'{BASE_DIR}/static',
        f'{BOOSTRAP_ROOT}/bootstrap',
        f'{BOOSTRAP_ROOT}/flatpickr',
        f'{BOOSTRAP_ROOT}/@popperjs/core',
        f'{BOOSTRAP_ROOT}/jquery',
    # Agrega más rutas según sea necesario
    ]

6. Ejecutar la Aplicación Django

   Finalmente, puedes ejecutar el servidor de desarrollo de Django:

   pyton manage.py makemigrations

   python manage.py migrate

   python manage.py runserver

   Visita http://127.0.0.1:8000 en tu navegador para ver la aplicación en funcionamiento.

Recursos Adicionales

- Documentación oficial de Django: https://docs.djangoproject.com/en/5.0/
- Documentación oficial de Node.js: https://nodejs.org/en/docs/
- Archivo devserver para linux y windows en la root del proyecto (El proyecto no el proyecto Django, ok?)

Si tienes alguna pregunta o problema, no dudes en crear un issue en el repositorio o consultar la documentación oficial.

---

¡Gracias por usar este proyecto Django!
