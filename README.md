Introduction
============

This service will allow applications to create and manage AWS IAM accounts without ever having access to the main account's credentials. This opens up new possibilities for mobile and client-side applications to use AWS services on the author's behalf, without having to register or be charged separately. Without some sort of third-party service hosting and serving the keys, this is not possible in many situations.

Installation
============

1. Open `app.yaml` and change the value of the `application` field to a Google App Engine application id registered to you.
2. Open `credentials.py` and fill in your main AWS credentials.
3. Open `permissions.py` and fill in the groups you want the service to be able to add users to.
3. Run `appcfg.py update .` to upload the application to the Google App Engine servers.

Usage
=====

At the moment, only the following operation(s) are supported:
    
* `/create_user?group=group_name` - Creates a new user in the group `group_name`. If there are no errors, the response will be a string of the form `aws_access_key_id:aws_secret_access_key` which can be used immediately.

TODO
====

At the moment, the created account has no permissions. Eventually, `permissions.py` will be expanded to define rules for groups based on various factors.

Author
======

awskeyserver was thought up and written by Adrian Petrescu (apetresc@gmail.com). Please contact me with any questions or suggestions.
