#!/usr/bin/env python3

import os
import re
from pprint import pprint as pp
import requests
import json
import argparse
import pyterprise


def get_token(tfe_host):
    home = os.getenv('HOME')
    tfrc_path = home + '/.terraformrc'
    try:
        with open(tfrc_path, 'r') as file:
            tfrc_content = file.read()
        token_block_regex = '^\s*(?!#)\s*credentials\s\"' + tfe_host + '\"\s\{\s*token\s=\s\"[a-zA-Z0-9\.]+\"\s*\}'
        p = re.compile(token_block_regex, re.MULTILINE)
        matches = p.findall(tfrc_content)
        token = re.sub('^\s*(?!#)\s*credentials\s\"' + tfe_host + '\"\s\{\s*token\s=\s\"', '', matches[0])
        token = re.sub('\"\s*\}', '', token)
        return token
    except:
        print('could not open ~/.terraformrc')
        raise


def get_env_config(env):
    try:
        with open('env_configs.json', mode='rt', encoding='UTF-8') as f:
            env_confs = json.load(f)
        if env == 'default':
            env = env_confs['default']
        env_conf = env_confs['envs'][env]
        return env_conf
    except:
        print('could not open env_configs.json in the current directory')
        raise


def main():
    parser = argparse.ArgumentParser(description='Do a bunch of cool stuff to TFE.')
    parser.add_argument('--env', metavar='Environment', type=str, default='default',
                        help='Environment you want to use defined in env_configs.json')
    args = parser.parse_args()
    #print(args.env)

    env_conf = get_env_config(args.env)
    pp(env_conf)
    tfe_host = env_conf['tfe_host']
    tfe_org = env_conf['tfe_org']
    tfe_vcs_oauth_token_id = env_conf['tfe_vcs_oauth_token_id']

    # your secret tfe api token
    tfe_token = get_token(tfe_host)
    #print(tfe_token)


if __name__ == '__main__':
    main()
