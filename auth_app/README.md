# DEVELOPMENT SETUP

## VIRTUAL ENVIRONMENT:
* To activate the virtual environment through poetry, type:
```shell
poetry shell
```
* To deactivate the virtual environment, type:
```shell
exit
```

## DEPENDENCIES
* To install the defined dependencies for your project, run:
```shell
poetry install
```

## RUNNING
To run your script simply use:
```shell
poetry run python auth_app.py
```
To run pytest, type:
```shell
poetry run pytest
```
Custom command to create superuser
```shell
poetry run flask createsuperuser <username> <password> <email>
```
