@ECHO OFF
REM Activar el entorno virtual
CALL .venv\Scripts\activate

REM Ejecutar makemigrations
py mysite\manage.py makemigrations

REM Ejecutar migrate
py mysite\manage.py migrate

REM Ejecutar el servidor de desarrollo
SET PORT=8000
python mysite\manage.py runserver %PORT%