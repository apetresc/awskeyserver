import cgi
import uuid

import credentials
import permissions

from boto.iam import IAMConnection
from boto.exception import BotoServerError

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class CreateUser(webapp.RequestHandler):
    def get(self):
        group = self.request.get('group')

        if not group:
            self.response.out.write("ERROR: Must specify a group")
        elif group not in permissions.allowed_groups:
            self.response.out.write("ERROR: Not an allowed group")
        else:
            user_name = uuid.uuid4().hex
            try:
                conn.create_user(user_name)
                conn.add_user_to_group(group, user_name)
                create_access_key_res = conn.create_access_key(user_name)
                self.response.out.write("%s:%s" % (
                        create_access_key_res.access_key_id,
                        create_access_key_res.secret_access_key))
            except BotoServerError, e:
                self.response.out.write("ERROR: %s" % e.reason)

conn = IAMConnection(credentials.aws_access_key_id, credentials.aws_secret_access_key)
application = webapp.WSGIApplication([('/create_user', CreateUser)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
