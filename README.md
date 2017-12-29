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

Cron per comprovar challenges finalitzats
Afegir a "sudo crontab -e":


`*/5 * * * * /path/to/python_interpreter /path/to/project/manage.py checkchallenges
`*/5 * * * * /home/alumne/.virtualenvs/development/bin/python3 /home/alumne/development/manage.py checkchallenges'
# Doker (noy yet working)

## Ubuntu install
```
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu  $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install docker-ce

url -L https://github.com/docker/machine/releases/download/v0.13.0/docker-machine-`uname -s`-`uname -m` >/tmp/docker-machine &&
chmod +x /tmp/docker-machine &&
sudo cp /tmp/docker-machine /usr/local/bin/docker-machine
docker-machine version
```
