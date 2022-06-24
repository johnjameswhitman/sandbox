# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from from openapi_client.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from openapi_client.model.group import Group
from openapi_client.model.group_request import GroupRequest
from openapi_client.model.paginated_group_list import PaginatedGroupList
from openapi_client.model.paginated_user_list import PaginatedUserList
from openapi_client.model.patched_group_request import PatchedGroupRequest
from openapi_client.model.patched_user_request import PatchedUserRequest
from openapi_client.model.user import User
from openapi_client.model.user_request import UserRequest
