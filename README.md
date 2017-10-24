# Comandes utils

Activa el enviroment de python (necessari per correr python dins del projecte)
`$source ~/meetNRun/restEnv/bin/activate`

Desactivar enviroment actiu
`$deactivate`

Inicia servidor de proves (dins el directori del repo)
`$python manage.py runserver 0.0.0.0:8000`

Inicia servidor de proves i mantent-lo actiu inclus després de fer logout
Crea un fixer nohup.out amb la sortida per debugar
`$nohup python manage.py runserver 0.0.0.0:8000`

Busca canvis en la capa de dades
`$python manage.py makemigrations`

Applica canvis pendents a la base de dades
`$python manage.py migrate`

Mata qualsevol procés de python en background
`$killall python`

# Setup

`virtualenv -p python3 djangoRest`
`source djangoRest/bin/activate`
`pip install django djangorestframework coreapi`
`python manage.py createsuperuser`