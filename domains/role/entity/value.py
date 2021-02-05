from enum import Enum


class RoleType(Enum):
    normal = 0


class RoleDisable(Enum):
    able = 0
    disable = 1


TreeKey = 'roleMember.key.'
BelongTreeKey = 'belongRoleMember.key'
RoleMemberRoleKey = 'role_keys'
RoleMemberUserKey = 'user_keys'
