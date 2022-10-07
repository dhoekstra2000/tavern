import click
from passlib.hash import pbkdf2_sha256

from tavern_db.database import db_session
from tavern_db.models import Permission, User, UserGroup


@click.group()
def cli():
    pass


@click.command(help="Initialize server with superuser")
def init():
    username = click.prompt("Username for superuser", type=str)
    password = click.prompt("Password for superuser", type=str)

    superuser_group = UserGroup(name="Superuser", superuser=True)

    user = User(username=username)
    user.password = pbkdf2_sha256.hash(password)
    user.group = superuser_group
    db_session.add(user)
    db_session.commit()

    click.echo("Database configured!")


@click.command(help="Remove all records from the database")
def cleardb():
    User.query.delete()
    UserGroup.query.delete()
    Permission.query.delete()
    db_session.commit()


cli.add_command(init)
cli.add_command(cleardb)

if __name__ == "__main__":
    cli()
