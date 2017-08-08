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
import jinja2
import os
from google.appengine.api import users

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(
                nickname, logout_url)
        else:
            login_url = users.create_login_url('/')
            greeting = '<a href="{}">Sign in</a>'.format(login_url)

        self.response.write(
            '<html><body>{}</body></html>'.format(greeting))
#
class SecondHandler (webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/grading_calculator.html')
        self.response.out.write(template.render())

    def post(self):
        r_template = jinja_environment.get_template('templates/grading_result.html')
        semester_grade = float(self.request.get('semester_grade')) * .01
        semester_worth = float(self.request.get('semester_worth')) * .01
        semester_score = semester_grade * semester_worth
        desired_grade = float(self.request.get('desired_grade'))
        required = (desired_grade * .01) - semester_score
        final_worth = 1 - semester_worth
        final_required = (required / final_worth) * 100

        template_variables = {
            'answer1' : final_required

        }
        self.response.write(r_template.render(template_variables))
#
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/grade_calculator', SecondHandler)#
], debug=True)
