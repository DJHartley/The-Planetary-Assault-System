# -*- coding: utf-8 -*-
'''
Created on Mar 13, 2012

@author: moloch

    Copyright [2012]

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
'''


import os
import logging

from models import User, WeaponSystem
from libs.Dispatch import Dispatch
from libs.SecurityDecorators import authenticated
from tornado.web import RequestHandler
from BaseHandlers import BaseHandler
from recaptcha.client import captcha


class HomeHandler(BaseHandler):

    @authenticated
    def get(self, *args, **kwargs):
        ''' Display the default user page '''
        user = User.by_username(self.session.data['username'])
        dispatch = Dispatch.Instance()
        self.render('user/home.html', 
            user=user, 
            all_weapons=WeaponSystem.get_all(),
        )


class SettingsHandler(BaseHandler):
    ''' User controlled settings '''

    @authenticated
    def get(self, *args, **kwargs):
        ''' Display the user settings '''
        user = User.by_username(self.session.data['username'])
        self.render('user/settings.html', user=user, message=None)

    @authenticated
    def post(self, *args, **kwargs):
        ''' Currently only supports change password '''
        self.change_password(*args, **kwargs)

    def change_password(self, *args, **kwargs):
        ''' Updates a user accounts password '''
        user = User.by_user_name(self.session.data['user_name'])
        try:
            old_password = self.get_argument("old_password")
            new_password = self.get_argument("new_password")
            new_password_two = self.get_argument("new_password2")
        except:
            self.render("user/error.html", 
                operation="Changing Password",
                errors="Please fill out all forms"
            )
        try:
            response = captcha.submit(
                self.get_argument('recaptcha_challenge_field'),
                self.get_argument('recaptcha_response_field'),
                self.application.settings['recaptcha_private_key'],
                self.request.remote_ip
            )
        except:
            self.render("user/error.html", 
                operation="Changing Password",
                errors="Please fill out recaptcha"
            )
        if user.validate_password(old_password):
            if new_password == new_password_two:
                if 12 <= len(new_password):
                    if response.is_valid:
                        user.password = new_password
                        self.dbsession.add(user)
                        self.dbsession.flush()
                        self.render("user/settings.html",
                            message="Succesfully Changed Password!"
                        )
                    else:
                        self.render("user/error.html", 
                            operation="Changing Password",
                            errors="Invalid recaptcha"
                        )
                else:
                    self.render("user/error.html", 
                        operation="Change Password",
                        errors="Password must be at least 12 chars"
                    )
            else:
                self.render("user/error.html", 
                    operation="Changing Password",
                    errors="New password's didn't match"
                )
        else:
            self.render("user/error.html", 
                operation="Changing Password",
                errors="Invalid old password"
            )


class LogoutHandler(BaseHandler):

    def get(self, *args, **kwargs):
        ''' Clears cookies and session data '''
        self.clear_all_cookies()
        if self.session is not None:
            self.session.delete()
        self.redirect("/")
