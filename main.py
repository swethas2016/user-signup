#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

form="""
    <form method='post'>
        <h2>Signup</h2>
    <table>
        <tr>
        <td><label>Username</td>
        <td><input type='text' name='username' value="%(username)s"></label></td>
        <td style="color:red">%(error_username)s</td>
        </tr>
        <tr>
        <td><label>Password</td>
        <td><input type='password' name='password' value=""></label></td>
        <td style="color:red">%(error_password)s</td>
        </tr>
        <tr>
        <td><label>Verify Password</td>
        <td><input type='password' name='verify_password' value=""></label></td>
        <td style="color:red">%(errorverify_password)s</td>
        </tr>
        <tr>
        <td><label>Email (optional)</td>
        <td><input type='email' name='email' value="%(email)s"></label></td>
        <td style="color:red">%(error_email)s</td>
        </tr>
    </table>
        <br>
        <input type='submit' />

    </form>
    """
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)


class MainHandler(webapp2.RequestHandler):
    def write_form(self, error_username="", error_password="", errorverify_password="",
                    error_email="", username="", email=""):
        self.response.write(form % {"error_username": error_username,
                                    "error_password": error_password,
                                    "errorverify_password": errorverify_password,
                                    "error_email": error_email,
                                    "username": username,
                                    "email": email})
    def get(self):
        self.write_form()
    def post(self):
        have_error = False
        user_name = self.request.get('username')
        user_password = self.request.get('password')
        user_verify = self.request.get('verify_password')
        user_email = self.request.get('email')


        error_username = ""
        error_password = ""
        errorverify_password = ""
        error_email = ""

        if not valid_username(user_name):
            error_username = "That's not a valid username"
            have_error = True

        if not valid_password(user_password):
            error_password = "That's not a valid password"
            have_error = True

        elif user_verify != user_password:
            errorverify_password = "Passwords didn't match"
            have_error = True

        if not valid_email(user_email):
            error_email = "That's not a valid email"
            have_error = True

        if have_error:
            self.write_form(error_username, error_password,
                            errorverify_password, error_email,
                            user_name, user_email)
        else:
            username = self.request.get('username')
            self.redirect('/welcome?username=%s'%username)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        self.response.write("Welcome, " + username + '!')

app = webapp2.WSGIApplication([
    ('/', MainHandler),('/welcome', WelcomeHandler)
], debug=True)
