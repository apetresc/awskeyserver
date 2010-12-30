import credentials

from policy import PolicyHandler
from policy import PolicyResponseCode

import urllib

from google.appengine.api.urlfetch import fetch

API_SERVER = "http://api.recaptcha.net"
VERIFY_SERVER = "http://api-verify.recaptcha.net"

# This value is the offset into the response HTML where the challenge field id begins.
# This may change, so in the future this should definitely be parsed out using some
# sort of regular expression.
RECAPTCHA_CHALLENGE_FIELD_OFFSET = 442

class CaptchaValidator(PolicyHandler):

    def handle(self, request, response):
        if request.get('recaptcha_challenge_field'):
            # Validate response against server

            def encode_if_necessary(s):
                if isinstance(s, unicode):
                    return s.encode('utf-8')
                return s

            captcha_verify_params = urllib.urlencode({
                'privatekey': encode_if_necessary(credentials.RECAPTCHA_PRIV_KEY),
                'remoteip'  : encode_if_necessary(request.remote_addr),
                'challenge' : encode_if_necessary(request.get('recaptcha_challenge_field')),
                'response'  : encode_if_necessary(request.get('recaptcha_response_field')),
                })
            captcha_verify_response = fetch(
                url = "%s/verify" % VERIFY_SERVER,
                payload = captcha_verify_params, 
                headers = {
                    "Content-type" : "application/x-www-form-urlencoded",
                    "User-agent"   : "reCAPTCHA Python"
                    },
                method = "POST")
            captcha_verify_status = captcha_verify_response.content.splitlines()[0]
            if captcha_verify_status == "true":
                return PolicyResponseCode.ACCEPT
            else:
                return PolicyResponseCode.DENY
        else:
            # This is a fresh request, need to get a captcha for them
            captcha_url = "%s/noscript?k=%s" % (API_SERVER, credentials.RECAPTCHA_PUB_KEY)
            captcha_html = fetch(captcha_url).content
            challenge_field_id = captcha_html[
                    RECAPTCHA_CHALLENGE_FIELD_OFFSET:
                    RECAPTCHA_CHALLENGE_FIELD_OFFSET + captcha_html[RECAPTCHA_CHALLENGE_FIELD_OFFSET:].index('"')]
            response.out.write(challenge_field_id) 
            return PolicyResponseCode.CHALLENGE

