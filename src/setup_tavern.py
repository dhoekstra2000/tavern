import click
from passlib.hash import pbkdf2_sha256

from tavern_db.database import db_session
from tavern_db.models import User, UserGroup


def main():
    username = click.prompt("Username for superuser", type=str)
    password = click.prompt("Password for superuser", type=str)

    superuser_group = UserGroup(name="Superuser", superuser=True)

    user = User(username=username)
    user.password = pbkdf2_sha256.hash(password)
    user.group = superuser_group
    db_session.add(user)
    db_session.commit()

    click.echo("Database configured!")


if __name__ == "__main__":
    main()
