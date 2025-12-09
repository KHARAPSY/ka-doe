from app.services import ServiceUser
from app.core import Settings

def create_admin_user():
    ServiceUser.create_user(
        Settings.ADMIN_USER,
        Settings.ADMIN_PASS,
        Settings.ADMIN_EMAIL,
        Settings.ADMIN_NAME,
        Settings.IS_ADMIN
    )
