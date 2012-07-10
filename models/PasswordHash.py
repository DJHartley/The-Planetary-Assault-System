'''
Created on Mar 12, 2012

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


import re
import logging

from sqlalchemy import and_
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import synonym, relationship, backref
from sqlalchemy.types import Unicode, Integer, Boolean
from models import dbsession
from models.BaseObject import BaseObject

class PasswordHash(BaseObject):

    job_id = Column(Integer, ForeignKey('job.id'), nullable = False)
    algorithm = Column(Unicode(16), nullable = False)
    user_name = Column(Unicode(64))
    digest = Column(Unicode(128), nullable = False)
    solved = Column(Boolean, default = False, nullable = False)
    plain_text = Column(Unicode(64))
    common_passwords = ['123456', '12345', '123456789', 'password', 'iloveyou', 'princess',
        'rockyou', '1234567', '12345678', 'abc123', 'nicole', 'daniel', 'babygirl', 'monkey',
        'jessica', 'lovely', 'michael', 'ashley', '654321', 'qwerty', 'letmein', 'admin', 'fuck',
        'fuckyou', 'love', 'sex', 'secret', 'god',
    ]

    @classmethod
    def by_id(cls, hash_id):
        """ Return the PasswordHash object whose user id is 'hash_id' """
        return dbsession.query(cls).filter_by(id = hash_id).first()

    @classmethod
    def by_digest(cls, digest_value, job_id_value):
        """ Return the digest based on valud and job_id """
        return dbsession.query(cls).filter(and_(digest == digest_value, job_id == job_id_value)).first()

    @property
    def lower_case(self):
        ''' Checks to see if the password is only lower case chars '''
        if not self.solved:
            raise ValueError
        return self.__regex__("^[a-z]*$")

    @property
    def upper_case(self):
        ''' Checks to see if the password is only upper case chars '''
        if not self.solved:
            raise ValueError
        return self.__regex__("^[A-Z]*$")

    @property
    def numeric(self):
        ''' Checks to see if the password is only numeric chars '''
        if not self.solved:
            raise ValueError
        return self.__regex__("^[0-9]*$")

    @property
    def mixed_case(self):
        ''' Checks to see if the password is only lower/upper chars '''
        if not self.solved:
            raise ValueError
        contains_cases = self.__regex__("^(?=.*[a-z])(?=.*[A-Z]).+$")
        only_alpha = self.__regex__("^[a-zA-Z]*$")
        return (contains_cases and only_alpha)

    @property
    def lower_alpha_numeric(self):
        ''' Checks to see if the password is only lower case/numeric chars '''
        if not self.solved:
            raise ValueError
        contains_alph_numeric = self.__regex__("^(?=.*[a-z])(?=.*[0-9]).+$")
        only_alpha_numeric = self.__regex__("^[a-z0-9]*$")
        return (contains_alph_numeric and only_alpha_numeric)

    @property
    def upper_alpha_numeric(self):
        ''' Checks to see if the password is only upper case/numeric chars '''
        if not self.solved:
            raise ValueError
        contains_alph_numeric = self.__regex__("^(?=.*[A-Z])(?=.*[0-9]).+$")
        only_alpha_numeric = self.__regex__("^[A-Z0-9]*$")
        return (contains_alph_numeric and only_alpha_numeric)

    @property
    def mixed_alpha_numeric(self):
        ''' Checks to see if the password is only lower/upper case and numeric chars '''
        if not self.solved:
            raise ValueError
        contains_mixed_alpha_numeric = self.__regex__("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).+$")
        only_mixed_alpha_numeric = self.__regex__("^[a-zA-Z0-9]*$")
        return (contains_mixed_alpha_numeric and only_mixed_alpha_numeric)

    @property
    def is_common(self):
        ''' Checks to see if the password is in the common password list '''
        if not self.solved:
            raise ValueError
        return self.plain_text.lower() in self.common_passwords

    def __regex__(self, expression):
        ''' Runs a regex returns a bool '''
        regex = re.compile(expression)
        return bool(regex.match(self.plain_text))

    def __len__(self):
        ''' Returns the length of the digest '''
        return len(self.digest)
