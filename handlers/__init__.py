# -*- coding: utf-8 -*-
'''
Created on June 23, 2012

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

import sys
import models
import logging

from os import urandom, path
from base64 import b64encode
from models import dbsession
from modules.Menu import Menu
from libs.ConsoleColors import *
from libs.Session import SessionManager
from libs.HostIpAddress import HostIpAddress
from tornado import netutil, options
from tornado.web import Application, StaticFileHandler 
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop, PeriodicCallback
from handlers.JobHandlers import *
from handlers.UserHandlers import *
from handlers.ErrorHandlers import *
from handlers.AdminHandlers import *
from handlers.PublicHandlers import *


### Logging configuration
logging.basicConfig(format = '[%(levelname)s] %(asctime)s - %(message)s', level = logging.DEBUG)

### Application setup
application = Application([
        # Static Handlers - Serves static CSS, JavaScript and image files
        (r'/static/(.*)', StaticFileHandler, {'path': 'static'}),
        
        # User Handlers - Serves user related pages
        (r'/user', HomeHandler, {'dbsession': dbsession}),
        (r'/settings', SettingsHandler, {'dbsession': dbsession}),
        (r'/logout', LogoutHandler),

        # Job Handlers - Serves job related pages
        (r'/createjob', CreateJobHandler, {'dbsession': dbsession}),
        
        # Admin Handlers - Administration pages
        (r'/manageusers(.*)', ManageUsersHandler, {'dbsession':dbsession}),
        
        # Public handlers - Serves all public pages
        (r'/', WelcomeHandler),
        (r'/login', LoginHandler, {'dbsession': dbsession}),
        (r'/register', RegistrationHandler, {'dbsession': dbsession}),
        (r'/about', AboutHandler),
        
        # Error handlers - Serves error pages
        (r'/403', UnauthorizedHandler),
        (r'/(.*).php', PhpHandler),
        (r'/(.*)', NotFoundHandler)
    ],
                          
    # Randomly generated 64-byte secret key
    cookie_secret = b64encode(urandom(64)),
    
    # Ip addresses that access the admin interface
    admin_ips = ('127.0.0.1'),

    # Rainbow table dictionary
    rainbow_tables = {
        "MD5": "/media/data/RainbowTables/MD5/",
        "NTLM": "/media/data/RainbowTables/NTLM/",
        "LM": "/media/data/RainbowTables/LM/",
    },
    
    # Template directory
    template_path = 'templates',
    
    # Request that does not pass @authorized will be redirected here
    forbidden_url = '/403',
    
    # Requests that does not pass @authenticated  will be redirected here
    login_url = '/login',
    
    # UI Modules
    ui_modules = {"Menu": Menu},
    
    # Enable XSRF forms
    xsrf_cookies = True,
    
    # Recaptcha Key
    recaptcha_private_key = "6LcJJ88SAAAAAPPAN72hppldxema3LI7fkw0jaIa",

    # Milli-Seconds between session clean up
    clean_up_timeout = int(60 * 1000),

    # Debug mode
    debug = True,
    
    # Application version
    version = '0.1'
)

### Settings
LISTEN_PORT = 8888

### Main entry point
def start_server():
    ''' Main entry point for the application '''
    logging.info("Server starting up, please wait ... ")
    sockets = netutil.bind_sockets(LISTEN_PORT)
    server = HTTPServer(application)
    server.add_sockets(sockets)
    io_loop = IOLoop.instance()
    session_manager = SessionManager.Instance()    
    session_clean_up = PeriodicCallback(
        session_manager.clean_up,
        application.settings['clean_up_timeout'],
        io_loop = io_loop
    )
    try:
        logging.info("Server event loop started. ")
        io_loop.start()
        session_clean_up.start()
    except KeyboardInterrupt:
        logging.warn("Keyboard interrupt, shutdown everything!")
        session_clean_up.stop()
        io_loop.stop()