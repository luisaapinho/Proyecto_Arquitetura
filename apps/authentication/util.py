# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
import hashlib
import binascii

# Inspiration -> https://www.vitoshacademy.com/hashing-passwords-in-python/



from werkzeug.security import generate_password_hash, check_password_hash

def hash_pass(password):
    return generate_password_hash(password)

def verify_pass(provided_password, stored_password):
    return check_password_hash(stored_password, provided_password)
