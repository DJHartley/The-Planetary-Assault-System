# -*- coding: utf-8 -*-
'''
Created on Mar 13, 2012

@author: moloch

    Copyright [2012] [Redacted Labs]

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

from tornado.web import RequestHandler

class NotFoundHandler(RequestHandler):

    def get(self, *args, **kwargs):
        ''' Renders the "404" page (returns 200 status) '''
        self.render("public/404.html")

    def post(self, *args, **kwargs):
        ''' Renders the "404" page (returns 200 status) '''
        self.render("public/404.html")

class PasswdHandler(RequestHandler):

    def get(self, *args, **kwargs):
        ''' Renders a fake /etc/passwd file '''
        self.render("public/passwd.html")

    def post(self, *args, **kwargs):
        ''' Renders a fake /etc/passwd file '''
        self.render("public/passwd.html")
        
class UnauthorizedHandler(RequestHandler):
    
    def get(self, *args, **kwargs):
        ''' Renders the 403 page '''
        self.render("public/403.html")

    def post(self, *args, **kwargs):
        ''' Renders the 403 page '''
        self.render("public/403.html")
        
class PhpHandler(RequestHandler):
    
    def get(self, *args, **kwargs):
        ''' Renders the php page '''
        self.render("public/php.html")

    def post(self, *args, **kwargs):
        self.render("public/php.html")