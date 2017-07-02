from flask_principal import Permission, RoleNeed, UserNeed

from app.constants import *


# Roles Needed
root_role    = RoleNeed("root")
admin_role   = RoleNeed("admin")
doctor_role  = RoleNeed("doctor")
officer_role = RoleNeed("officer")

# Permissions
admin_permission            = Permission(admin_role)
root_permission             = Permission(root_role)
administrators_permission   = Permission(root_role, admin_role)

doctor_permission           = Permission(doctor_role)
officer_permission          = Permission(officer_role)
medical_staff_permission    = Permission(doctor_role, officer_role)
