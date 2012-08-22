#!/usr/bin/env python
'''
Created on Aug 22, 2012

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


import os
import cmd
import sys
import getpass

from libs.ConsoleColors import *
from libs.ConfigManager import ConfigManager
from models import dbsession, User, Permission


class RecoveryConsole(cmd.Cmd):
    ''' Recovery console for user/passwords '''

    intro  = "\n ===========================================\n" + \
             "  Planetary Assault System Recovery Console \n" + \
             " ===========================================\n\n" + \
             "Type 'help' for a list of available commands"
    prompt = underline + "Recovery" + W + " > "

    def do_reset(self, username):
        ''' 
        Reset a user's password
        Usage: reset <user name>
        '''
        user = User.by_user_name(username)
        if user == None:
            print WARN + str("%s user not found in database." % username)
        else:
            print INFO + str("Loaded %s from database" % user.user_name)
            sys.stdout.write(PROMPT + "New ")
            sys.stdout.flush()
            user.password = getpass.getpass()
            dbsession.add(user)
            dbsession.flush()
            print INFO + str("Updated %s password successfully." % user.user_name)

    def do_ls(self, partial):
        ''' 
        List all users in the database 
        Usage: ls
        '''
        users = User.all()
        for user in users:
            print INFO + user.user_name

    def do_delete(self, username):
        '''
        Delete a user from the database
        Usage: delete <user name>
        '''
        user = User.by_user_name(username)
        if user == None:
            print WARN + str("%s user not found in database." % username)
        else:
            username = user.user_name
            print WARN + str("Are you sure you want to delete %s?" % username)
            if raw_input(PROMPT + "Delete [y/n]: ").lower() == 'y':
                dbsession.delete(user)
                dbsession.flush()
                print INFO + str("Successfully deleted %s from database." % username)

    def do_create(self, username):
        '''
        Create a new user account
        Usage: create <user name> 
        '''
        user = User(
            user_name=unicode(username),
        )
        dbsession.add(user)
        dbsession.flush()
        sys.stdout.write(PROMPT + "New ")
        sys.stdout.flush()
        user.password = getpass.getpass()
        user.approved = True
        dbsession.add(user)
        dbsession.flush()
        print INFO + "Successfully created, and approved new account."

    def do_approve(self, username):
        '''
        Approve a user account
        Usage: approve <user name>
        '''
        user = User.by_user_name(username)
        if user == None:
            print WARN + str("%s user not found in database." % username)
        else:
            user.approved = True
            dbsession.add(user)
            dbsession.flush()
            print INFO + str("Successfully approved %s's account." % user.user_name)

    def do_exit(self, *args, **kwargs):
        ''' 
        Exit recovery console
        Usage: exit
        '''
        print INFO + "Have a nice day!"
        os._exit(0)