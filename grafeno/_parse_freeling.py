#!/usr/bin/env python3

from subprocess import Popen, PIPE
import subprocess as subp
import json
import re

regex = re.compile('}\s*{')

def parse (sentence):
    '''Calls the freeling process to obtain the dependency parse of a text.'''
    config = "grafeno/freeling_deps_es.cfg"
    proc = Popen(["analyze", "--flush", "-f", config], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    data, err = proc.communicate(sentence.encode('UTF-8'))
    # print('data\n %r' % data)
    # print('sentence\n %r' % sentence)
    return json.loads('['+regex.sub('},{',data.decode('UTF-8'))+']')
