from flask_principal  import Permission, RoleNeed, UserNeed

from app.constants import *


# Roles Needed
root_role    = RoleNeed(ROLE_NAME_TO_CODE["Super User"])
admin_role   = RoleNeed(ROLE_NAME_TO_CODE["Users Admin"])
doctor_role  = RoleNeed(ROLE_NAME_TO_CODE["Investigation Doctor"])
officer_role = RoleNeed(ROLE_NAME_TO_CODE["Registration Officer"])

# Permissions
doctor_permission = Permission(doctor_role)
officer_permission = Permission(officer_role)
admin_permission   = Permission(admin_role)
root_permission = Permission(root_role)
root_admin_permission = Permission(root_role, admin_role)
