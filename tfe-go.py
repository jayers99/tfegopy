#!/usr/bin/env python3

import os
import re
import requests
import json

def get_token(tfe_host):
  home = os.getenv('HOME')
  tfrc_path = home + '/.terraformrc'
  try:
    with open(tfrc_path, 'r') as file:
      tfrc_content = file.read()
  except:
    print('could not open ~/.terraformrc')
  token_block_regex = '^\s*(?!#)\s*credentials\s\"' + tfe_host + '\"\s\{\s*token\s=\s\"[a-zA-Z0-9\.]+\"\s*\}'
  p = re.compile(token_block_regex, re.MULTILINE)
  matches = p.findall(tfrc_content)
  token = re.sub('^\s*(?!#)\s*credentials\s\"' + tfe_host + '\"\s\{\s*token\s=\s\"', '', matches[0])
  token = re.sub('\"\s*\}', '', token)
  return token
