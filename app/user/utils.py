from datetime import datetime

from app import (
    celery,
    db
)
from app.constants import (bulk_updates, event_type, role_name, user_type_request)
from app.lib.email_utils import send_email
from app.models import (Events, Requests, Roles, UserRequests, Users)


@celery.task(bind=True, name='app.user.utils.make_user_admin')
def make_user_admin(self, modified_user_guid: str, current_user_guid: str, agency_ein: str):
    """
    Make the specified user an admin for the agency.

    Args:
        user (Users): User to be modified
        agency_ein (str): Agency the user is being added to

    Returns:

    """
    permissions = Roles.query.filter_by(name=role_name.AGENCY_ADMIN).one().permissions
    user = Users.query.filter_by(guid=modified_user_guid).one()
    requests = [request.id for request in user.agencies.filter_by(ein=agency_ein).one().requests]

    new_user_requests = []
    new_user_requests_events = []

    update_user_requests = []
    update_user_requests_events = []

    for request in requests:
        existing_value = UserRequests.query.filter_by(request_id=request, user_guid=user.guid).one_or_none()

        if existing_value:
            user_request = bulk_updates.UserRequestsDict(
                user_guid=user.guid,
                request_id=request,
                request_user_type=user_type_request.AGENCY,
                permissions=permissions,
                point_of_contact=existing_value.point_of_contact
            )
            update_user_requests.append(user_request)
            previous_value = {
                'permissions': existing_value.permissions
            }
            new_value = {
                'permissions': permissions
            }
            user_request_event = bulk_updates.UserRequestsEventDict(
                request_id=request,
                user_guid=user.guid,
                response_id=None,
                type=event_type.USER_PERM_CHANGED,
                timestamp=datetime.utcnow(),
                previous_value=previous_value,
                new_value=new_value,
            )
            update_user_requests_events.append(user_request_event)

        else:
            user_request = bulk_updates.UserRequestsDict(
                user_guid=user.guid,
                request_id=request,
                request_user_type=user_type_request.AGENCY,
                permissions=permissions,
                point_of_contact=None
            )
            new_user_requests.append(user_request)

            new_value = {
                'user_guid': user.guid,
                'request_id': request,
                'request_user_type': user_type_request.AGENCY,
                'permissions': permissions,
                'point_of_contact': None
            }
            user_request_event = bulk_updates.UserRequestsEventDict(
                request_id=request,
                user_guid=current_user_guid,
                response_id=None,
                type=event_type.USER_ADDED,
                timestamp=datetime.utcnow(),
                previous_value=None,
                new_value=new_value
            )
            new_user_requests_events.append(user_request_event)
    try:
        UserRequests.query.filter(UserRequests.user_guid == user.guid).update([('permissions', permissions)])

        db.session.bulk_insert_mappings(Events, update_user_requests_events)
        db.session.bulk_insert_mappings(UserRequests, new_user_requests)
        db.session.bulk_insert_mappings(Events, new_user_requests_events)
        db.session.commit()

        admin_user = Users.query.filter_by(guid=current_user_guid).one()

        send_email(
            subject='User {user_name} Made Admin',
            to=admin_user.email,
            email_content='Finished making changes.'
        )
    except:
        db.session.rollback()


@celery.task(bind=True, name='app.user.utils.remove_user_permissions')
def remove_user_permissions(self, modified_user_guid: str, current_user_guid: str, agency_ein: str):
    """
    Make the specified user an admin for the agency.

    Args:
        user (Users): User to be modified
        agency_ein (str): Agency the user is being removed from

    Returns:

    """
    user = Users.query.filter_by(guid=modified_user_guid).one()
    permissions = 0

    user_requests = db.session.query(UserRequests, Requests).join(Requests).with_entities(UserRequests.request_id,
                                                                                          UserRequests.permissions,
                                                                                          UserRequests.point_of_contact).filter(
        Requests.agency_ein == agency_ein, UserRequests.user_guid == user.guid).all()

    update_user_requests = []
    update_user_requests_events = []

    for user_request in user_requests:
        user_request_dict = bulk_updates.UserRequestsDict(
            guid=user.guid,
            request_id=user_request.request_id,
            request_user_type=user_type_request.AGENCY,
            permissions=permissions,
            point_of_contact=user_request.point_of_contact
        )
        update_user_requests.append(user_request_dict)
        previous_value = {
            'permissions': user_request.permissions
        }
        new_value = {
            'permissions': permissions
        }
        user_request_event = bulk_updates.UserRequestsEventDict(
            request_id=user_request.request_id,
            user_id=current_user_guid,
            response_id=None,
            type=event_type.USER_PERM_CHANGED,
            timestamp=datetime.utcnow(),
            previous_value=previous_value,
            new_value=new_value,
        )
        update_user_requests_events.append(user_request_event)

    try:
        UserRequests.query.filter(UserRequests.user_guid == user.guid).update([('permissions', permissions)])
        db.session.bulk_insert_mappings(Events, update_user_requests_events)
        db.session.commit()

        admin_user = Users.query.filter_by(guid=current_user_guid).one()

        send_email(
            subject='User {user_name} Permissions Removed',
            to=admin_user.email,
            email_content='Finished making changes.'
        )

    except:
        db.session.rollback()
