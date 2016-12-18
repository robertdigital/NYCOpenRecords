# Request Information Permissions
CHANGE_PRIVACY_TITLE = 0x00000001
CHANGE_PRIVACY_AGENCY_DESCRIPTION = 0x00000002
EDIT_TITLE = 0x00000004
EDIT_AGENCY_DESCRIPTION = 0x00000008
EDIT_REQUESTER_INFO = 0x00000010
REQUEST_INFO_PERMISSIONS = frozenset((
    CHANGE_PRIVACY_TITLE,
    CHANGE_PRIVACY_AGENCY_DESCRIPTION,
    EDIT_TITLE,
    EDIT_AGENCY_DESCRIPTION,
    EDIT_REQUESTER_INFO
))

# Response Permissions
ADD_FILE = 0x00000020
ADD_LINK = 0x00000040
ADD_OFFLINE_INSTRUCTIONS = 0x00000080
ADD_NOTE = 0x00000100
ADD_RESPONSE_PERMISSIONS = frozenset((
    ADD_FILE,
    ADD_LINK,
    ADD_OFFLINE_INSTRUCTIONS,
    ADD_NOTE,
))
EDIT_FILE = 0x00000200
EDIT_FILE_PRIVACY = 0x00000400
EDIT_LINK = 0x00000800
EDIT_LINK_PRIVACY = 0x000001000
EDIT_OFFLINE_INSTRUCTIONS = 0x00002000
EDIT_OFFLINE_INSTRUCTIONS_PRIVACY = 0x00004000
EDIT_NOTE = 0x00008000
EDIT_NOTE_PRIVACY = 0x00010000
EDIT_RESPONSE_PERMISSIONS = frozenset((
    EDIT_FILE,
    EDIT_FILE_PRIVACY,
    EDIT_LINK,
    EDIT_LINK_PRIVACY,
    EDIT_OFFLINE_INSTRUCTIONS,
    EDIT_OFFLINE_INSTRUCTIONS_PRIVACY,
    EDIT_NOTE,
    EDIT_NOTE_PRIVACY
))
DELETE_FILE = 0x00020000
DELETE_LINK = 0x00040000
DELETE_OFFLINE_INSTRUCTIONS = 0x00080000
DELETE_NOTE = 0x00100000
DELETE_RESPONSE_PERMISSIONS = frozenset((
    DELETE_FILE,
    DELETE_LINK,
    DELETE_OFFLINE_INSTRUCTIONS,
    DELETE_NOTE,
))
RESPONSE_PERMISSIONS = frozenset((
    ADD_FILE,
    ADD_LINK,
    ADD_OFFLINE_INSTRUCTIONS,
    ADD_NOTE,
    EDIT_FILE,
    EDIT_FILE_PRIVACY,
    EDIT_LINK,
    EDIT_LINK_PRIVACY,
    EDIT_OFFLINE_INSTRUCTIONS,
    EDIT_OFFLINE_INSTRUCTIONS_PRIVACY,
    EDIT_NOTE,
    EDIT_NOTE_PRIVACY,
    DELETE_FILE,
    DELETE_LINK,
    DELETE_OFFLINE_INSTRUCTIONS,
    DELETE_NOTE,
))

# Determination Permissions
ACKNOWLEDGE = 0x00200000
DENY = 0x00400000
EXTEND = 0x00800000
CLOSE = 0x01000000
RE_OPEN = 0x02000000
DETERMINATION_PERMISSIONS = frozenset((
    ACKNOWLEDGE,
    DENY,
    EXTEND,
    CLOSE,
    RE_OPEN,
))

# User Management Functionality
ADD_USER_TO_REQUEST = 0x04000000
REMOVE_USER_FROM_REQUEST = 0x08000000
EDIT_USER_REQUEST_PERMISSIONS = 0x10000000
ADD_USER_TO_AGENCY = 0x20000000
REMOVE_USER_FROM_AGENCY = 0x40000000
CHANGE_USER_ADMIN_PRIVILEGE = 0x80000000
USER_MANAGEMENT_PERMISSIONS = frozenset((
    ADD_USER_TO_REQUEST,
    REMOVE_USER_FROM_REQUEST,
    EDIT_USER_REQUEST_PERMISSIONS,
    ADD_USER_TO_AGENCY,
    REMOVE_USER_FROM_AGENCY,
    CHANGE_USER_ADMIN_PRIVILEGE,
))

PERMISSIONS = [
    (ACKNOWLEDGE, "Acknowledge Request"),
    (DENY, "Deny Request"),
    (EXTEND, "Extend Request"),
    (CLOSE, "Close Request"),
    (RE_OPEN, "Re-Open Request"),
    (CHANGE_PRIVACY_TITLE, "Change Title Privacy"),
    (CHANGE_PRIVACY_AGENCY_DESCRIPTION, "Change Agency Description Privacy"),
    (EDIT_TITLE, "Edit Title"),
    (EDIT_AGENCY_DESCRIPTION, "Edit Agency Description"),
    (ADD_FILE, "Add Files"),
    (ADD_LINK, "Add Links"),
    (ADD_OFFLINE_INSTRUCTIONS, "Add Offline Instructions"),
    (ADD_NOTE, "Add Notes"),
    (EDIT_FILE, "Edit Files"),
    (EDIT_FILE_PRIVACY, "Change File Privacy"),
    (EDIT_LINK, "Edit Links"),
    (EDIT_LINK_PRIVACY, "Change Link Privacy"),
    (EDIT_OFFLINE_INSTRUCTIONS, "Edit Offline Instructions"),
    (EDIT_OFFLINE_INSTRUCTIONS_PRIVACY, "Change Offline Instructions Privacy"),
    (EDIT_NOTE, "Edit Notes"),
    (EDIT_NOTE_PRIVACY, "Change Note Privacy"),
    (DELETE_FILE, "Delete File"),
    (DELETE_LINK, "Delete Link"),
    (DELETE_OFFLINE_INSTRUCTIONS, "Delete Offline Instructions"),
    (DELETE_NOTE, "Delete Note"),
    (ADD_USER_TO_REQUEST, "Add User"),
    (REMOVE_USER_FROM_REQUEST, "Remove User"),
    (EDIT_USER_REQUEST_PERMISSIONS, "Edit User Request Permissions"),
    (EDIT_REQUESTER_INFO, "Edit Requester Information")
]
