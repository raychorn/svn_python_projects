from vyperlogix.enum.Enum import Enum

class MoltenPrivileges(Enum):
    Partners = 0
    Member = 2**0
    Super_User = 2**1
    User_Manager = 2**2
    Support_Admin = 2**3
    Admin = 2**4

def role_from_molten(aRoleName):
    return MoltenPrivileges(aRoleName.replace(' ','_'))

def isValidMoltenRole(role):
    return role in [MoltenPrivileges.Admin, MoltenPrivileges.Member, MoltenPrivileges.Partners, MoltenPrivileges.Super_User, MoltenPrivileges.Support_Admin, MoltenPrivileges.User_Manager]

def isValidMoltenUserRole(role):
    return role in [MoltenPrivileges.Member, MoltenPrivileges.Partners, MoltenPrivileges.Super_User, MoltenPrivileges.User_Manager]

def isMemberMoltenUserRole(role):
    return role == MoltenPrivileges.Member

def isPartnersMoltenUserRole(role):
    return role == MoltenPrivileges.Partners

def isSuperUserMoltenUserRole(role):
    return role == MoltenPrivileges.Super_User

def isUserManagerMoltenUserRole(role):
    return role == MoltenPrivileges.User_Manager
