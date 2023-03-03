import click
from flask.cli import with_appcontext

from models import User, Role
from enumeration.roles import RolesEnum


@click.command('createsuperuser')
@click.argument('username')
@click.argument('password')
@click.argument('email')
@with_appcontext
def createsuperuser(username, password, email):
    user = User.find_by_username(username=username)
    if user:
        return 'User already exist. Try another username'
    admin_role = Role.find_by_name(name=RolesEnum.ADMIN)
    if not admin_role:
        admin_role = Role(name=RolesEnum.ADMIN, description='Grant All Privileges')
        Role(name=RolesEnum.BASE, description='Base user role').save()
        Role(name=RolesEnum.EXTENDED, description='Extended user role').save()
        Role(name=RolesEnum.MANAGER, description='Manage user role').save()
    superuser = User(username=username, password=password, email=email)
    superuser.roles = [admin_role]
    superuser.save()
    return 'Success create superuser.'
