"""Demo of a python client generated for this api.

Produce the client from the project-root with:

```shell
# Generate schema
tutorial/manage.py spectacular --file schema.yml
mv schema.yml client/

# Generate client
docker run \
    --rm \
    -v "$PWD:/local" \
    openapitools/openapi-generator-cli \
    generate \
    -i /local/templates/openapi-schema.yml \
    -g python \
    -o /local/client/python

# Install client
python -m pip install -e client/python

# Run demo
python demo.py
```

"""
# python setup.py install --user
import sys
import time
from pprint import pprint
from typing import List

import openapi_client
from openapi_client.api import groups_api
from openapi_client.model.group import Group
from openapi_client.model.group_request import GroupRequest
from openapi_client.model.paginated_group_list import PaginatedGroupList
from openapi_client.model.patched_group_request import PatchedGroupRequest

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = openapi_client.Configuration(
    host="http://localhost:5000", username="admin", password="Pass1234"
)

# Configure API key authorization: cookieAuth
# configuration.api_key['cookieAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'


def main(args: List[str]) -> None:
    if len(args) > 1:
        group_name = args[1]
    else:
        group_name = f"name_example_{int(time.time())}"

    # Enter a context with an instance of the API client
    with openapi_client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = groups_api.GroupsApi(api_client)
        group_request = GroupRequest(
            name=group_name,
        )  # GroupRequest |

        try:
            api_response = api_instance.groups_create(group_request)
            pprint(api_response)
        except openapi_client.ApiException as e:
            print("Exception when calling GroupsApi->groups_create: %s\n" % e)


if __name__ == "__main__":
    main(sys.argv)
