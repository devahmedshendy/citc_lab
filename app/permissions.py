from flask_principal  import Permission, RoleNeed, UserNeed

from app.constants import *


# Roles Needed
root_role    = RoleNeed(ROLES["root"][1])
admin_role   = RoleNeed(ROLES["admin"][1])
doctor_role  = RoleNeed(ROLES["doctor"][1])
officer_role = RoleNeed(ROLES["officer"][1])

# Permissions
doctor_permission = Permission(doctor_role)
officer_permission = Permission(officer_role)
admin_permission   = Permission(admin_role)
root_permission = Permission(root_role)
root_admin_permission = Permission(root_role, admin_role)
