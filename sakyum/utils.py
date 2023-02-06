# -*- coding: utf-8 -*-

import os
import base64
import random
import hashlib


def static_dir(app):
  """relative path to static files"""
  return os.getcwd() + "/static/" + app

def template_dir():
  """relative path to html page"""
  return os.getcwd() + "/templates"

def readIMG(p):
  """read default alert image and favicon.ico, for sure static file work"""
  with open(p, "rb") as i:
    r = i.read()
  return r

def stylePage(name, _is):
  """function for styling project application description default page"""
  desc = "Your " + name + " " + _is + " default pages"
  desc_center = desc.center(len(desc) + 6)
  border = "=" * len(desc_center)
  return [desc_center, border]

  
class Security:
  """
  Passcode class for suggesting user passcode iteration,
  generating salt, and creating secure passcode for every user
  
  A reqular expression that matches any character that
  should never appear in base 64 encodings would be:
    [^A-Za-z0-9+/=]
    
  we follow the base64 pattern of [^A-Za-z0-9+/=] that should never appear in base64, (in reqex)
  """
  
  token_sm_alpha = 'abcdefghijklmnopqrstuvwxyz'
  token_cap_alpha = token_sm_alpha.upper()
  token_num = '0123456789'
  token_char = '/+='
  token_sum = token_sm_alpha + token_cap_alpha + token_num
  
  """
  We times the above variable (token_sum) by 2 (total length is 124),
  so that we will randomly select from it without any restriction,
  since we make the minimum length of the salt to be 32 and the maximum to be 64,
  and also it will randomly select from that range of (32 - 64)
  """

  token_times = token_sum * 2
  token_list = list(token_times)
  random.shuffle(token_list) # shuffling the above list
  token_generate = ''.join(token_list)
  
  def __init__(self, token_generate = token_generate):
    self.token_generate = "".join(token_generate)
    
  @property
  def passcode_salt(self):
    """
    salting our passcode with this class method
    
    By using the random sample method, where we make:
      population = self.token_generate
      k = random.randint(32, 64)
    """

    salt = "".join(random.sample(self.token_generate, random.randint(32, 64)))
    return salt # return type is string
    
  def passcode_iteration(self, r_min, r_max, r_step):
    """
    Generating a random iteration. The iterations is not static,
    it is dynamic (every user's iteration is randomly choosen),
    by using the random method of randrange
    """

    itter = random.randrange(r_min, r_max, r_step)
    return itter # return type is integer
    
  def get_hash(self, salt: str, itter: int, passwd: str) -> str:
    """
    generating our key using this class method, and also
    the return type of the key is bytes
    """

    key = hashlib.pbkdf2_hmac(
        'sha256', # The hash digest algorithm for HMAC
        passwd.encode('utf-8'), # Convert the password to bytes
        salt.encode('utf-8'), # Convert the salt to bytes
        itter, # iteration type is integer
        dklen=128 # Get a 128 byte key
    )
    
    """
    Base64 encoding convert the binary data (sequence of byte) into text format,
    to avoid data corruption when transfer via only text channel.
    It is Privacy enhanced Electronic Mail (PEM).
    
    We use ascii to encode the (key)
    """
    
    # encodeing the key, type is string
    b64_encode = base64.b64encode(key).decode("ascii").strip()

    # hashing our b64_encode (the second hash), type is string
    hash_result = hashlib.sha256(str.encode(str(b64_encode))).hexdigest()

    # salt + iteration + hash_result, type is string
    secure_ingredient = '%s%d%s' % (salt, itter, hash_result)
    
    # return types of the list is string all, access it by print(self.get_hash.__annotations__)
    return [hash_result, secure_ingredient]
    
  def __str__(self):
    return f"Passcode security class"


def security(_passwd, r_min=260000, r_max=400000, r_step=7):
  """
    :_passwd ==> this is the raw password that you pass as an argument into this function,
    which will later hash it, also it will generate your password hash with a randomly
    generated iteration number and salt combine with your raw password.

    # :min ( r_min ) of 260000,
    # :max ( r_max ) of 400000, and
    # :stepping ( r_step ) of 7

    you can change the `r_min`, `r_max`, and `r_step` values to your desired
    ones, when calling the function, but make sure to pass the value of the password sting
  """
  
  pwd = Security()
  pwd_salt = pwd.passcode_salt
  pwd_itter = pwd.passcode_iteration(r_min=r_min, r_max=r_max, r_step=r_step)
  pwd_hash = pwd.get_hash(pwd_salt, pwd_itter, _passwd)

  #      [salt,     iteration, hashed_pwd,  ingredients]
  return [pwd_salt, pwd_itter, pwd_hash[0], pwd_hash[1]]

# print(security(_passwd="password"))
print(security(_passwd="password", r_min=100, r_max=300, r_step=7))
