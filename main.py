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
import webapp2
import jinja2
import os
from google.appengine.api import users
import logging

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
            # greeting = '<a href="{}">Sign in</a'.format(login_url)
            greeting = ''.format(login_url)

        self.response.write('<html><body>{}</body></html>'.format(greeting))
        template = jinja_environment.get_template('templates/log_in_results.html')
        self.response.write(template.render())
        template = jinja_environment.get_template('templates/log_in.html')
        # user = users.get_current_user()
        # if user:
        #     nickname = user.nickname()
        #     logout_url = users.create_logout_url('/')
        #     greeting = """Welcome, {}! (<a href='{}'>sign out</a>)""".format(
        #         nickname, logout_url)
        # else:
        #     login_url = users.create_login_url('/')
        #     greeting = """<a href="{}">Sign in</a>""".format(login_url)
        #
        # self.response.write(
        #     '<html><body>{}</body></html>'.format(greeting))
        self.response.write(template.render())

class SecondHandler (webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/final_calculator.html')
        self.response.out.write(template.render())

    def post(self):
        r_template = jinja_environment.get_template('templates/final_result.html')
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

#
class ThirdHandler (webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/grade_calculator.html')
        self.response.out.write(template.render())

    def post(self):
        a_template = jinja_environment.get_template('templates/grade_results.html')
        semester_grade = float(self.request.get('semester_grade')) * .01
        semester_worth = float(self.request.get('semester_worth')) * .01
        semester_score = semester_grade * semester_worth
        final_worth = 1 - semester_worth
        final = float(self.request.get('final')) * .01
        final_score = final * final_worth
        final_grade = (final_score + semester_score) * 100

        variables = {
            'answer' : final_grade
        }
        self.response.write(a_template.render(variables))

class FourthHandler (webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/grade_results.html')
        self.response.out.write(template.render())
class FifthHandler (webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/expenses.html')
        self.response.out.write(template.render())
    def post(self):
        expenses_template = jinja_environment.get_template('templates/expenses_result.html')
        # weekly = self.request.get('weekly')
        # bi_weekly = self.request.get('bi_weekly')
        # monthly = self.request.get('monthly')
        # yearly = self.request.get('yearly')
        # save_time = self.request.form['cars']
        save_time = str(self.request.get('save_time'))
        #print(save_time)

        if save_time == 'weekly':
            # print("How much do you want to save?")
            save = int(self.request.get('save'))
            # print("What is your income? (based on how often you want to save)")
            income = int(self.request.get('income'))
            #weekly
            weekly = save
            print(weekly)
            weekly_day = save / 7
            weekly_spend = income - save
            weekly_spend_day = weekly_spend / 7
            #weekly = save_time
            variables = {
                'weekly' : weekly,
                'weekly_day' : weekly_day,
                'weekly_spend' : weekly_spend,
                'weekly_spend_day' : weekly_spend_day
            }
            self.response.write(expenses_template.render(variables))
        elif save_time == 'bi_weekly':
            save = int(self.request.get('save'))
            # print("What is your income? (based on how often you want to save)")
            income = int(self.request.get('income'))
            weekly = save / 2
            weekly_day = save / 14
            weekly_spend = (income - save) / 2
            weekly_spend_day = weekly_spend / 7
            variables = {
                'weekly' : weekly,
                'weekly_day' : weekly_day,
                'weekly_spend' : weekly_spend,
                'weekly_spend_day' : weekly_spend_day
            }
            self.response.write(expenses_template.render(variables))
            # print("You need to save $" + str(weekly) + " per day. You can spend $"
            # +  str(weekly_spend) + " per week or you can spend $" + str(weekly_spend_day) + " per day.")
        elif save_time == 'monthly':
            save = int(self.request.get('save'))
            # print("What is your income? (based on how often you want to save)")
            income = int(self.request.get('income'))
            weekly = save / 4
            weekly_day = save / 30
            weekly_spend = (income - save) / 4
            weekly_spend_day = weekly_spend / 7
            variables = {
                'weekly' : weekly,
                'weekly_day' : weekly_day,
                'weekly_spend' : weekly_spend,
                'weekly_spend_day' : weekly_spend_day
            }
            self.response.write(expenses_template.render(variables))
        elif save_time == 'yearly':
            save = int(self.request.get('save'))
            # print("What is your income? (based on how often you want to save)")
            income = int(self.request.get('income'))
            weekly = save / 52
            weekly_day = save / 365
            weekly_spend = (income - save) / 52
            weekly_spend_day = weekly_spend / 7
            variables = {
                'weekly' : weekly,
                'weekly_day' : weekly_day,
                'weekly_spend' : weekly_spend,
                'weekly_spend_day' : weekly_spend_day
            }
            self.response.write(expenses_template.render(variables))
class SixthHandler (webapp2.RequestHandler):
        def get(self):
            template = jinja_environment.get_template('templates/about_us.html')
            self.response.out.write(template.render())


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/final_calculator', SecondHandler),
    ('/grade_calculator', ThirdHandler),
    ('/grade_results', FourthHandler),
    ('/expenses', FifthHandler),
    ('/about_us', SixthHandler),
], debug=True)
