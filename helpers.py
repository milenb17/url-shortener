
import string
import random

def generate_key():
  res = ''.join(random.choices(string.ascii_letters, k=10))
  return res