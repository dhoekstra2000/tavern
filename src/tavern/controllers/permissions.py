from tavern.security import needs_permission
from tavern_db.models import Permission
from tavern_db.schemas import PermissionSchema


@needs_permission("Permissions | can list permissions")
def read_all():
    perms = Permission.query.all()

    schema = PermissionSchema(
        only=["id", "name", "date_created", "date_updated"], many=True
    )
    return schema.dump(perms)
