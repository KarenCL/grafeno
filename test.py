#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

# Grafeno -- Python concept graphs library
# Copyright 2016 Antonio F. G. Sevilla <afgs@ucm.es>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import argparse

arrayize = lambda t: t.split(',')

arg_parser = argparse.ArgumentParser(description='Test script')
group = arg_parser.add_mutually_exclusive_group()
group.add_argument('-s','--string')
group.add_argument('-f','--file',type=argparse.FileType('r'))
arg_parser.add_argument('-t','--transformers',type=arrayize,help='transformer pipeline to use')
arg_parser.add_argument('-l','--linearizers',type=arrayize,help='linearizing pipeline to use')
arg_config = arg_parser.add_argument('-c','--config-file',help='use a config file for pipeline options')
arg_parser.add_argument('-d','--display',action='store_true',help='display a drawing of the graph')
arg_parser.add_argument('-p','--print-json',action='store_true',help='print the graph in json')

try:
    print("(./test.py): dentro del try")
    import argcomplete
    import glob
    from os.path import dirname, basename
    def config_completer(prefix, **kwargs):
        print("(./test.py) - config_completer")
        return (basename(c)[:-5] for c in glob.glob(dirname(__file__)+"/configs/*.yaml"))
    arg_config.completer = config_completer
    argcomplete.autocomplete(arg_parser)
except ImportError:
    pass

args = arg_parser.parse_args()

import yaml
#se importa el modulo pipeline de grafeno
from grafeno import pipeline

#si la entrada e sun fichero de texto
if args.file:
    #se lee el contenido del fichero adjunto a transformar
    text = args.file.read()
#leemos el texto de una cadena
else:
    #se lee la cadena transformar
    text = args.string

#si se ha usado la opcion -c
if args.config_file:
    try:
        print("(./test.py): se ha usado la opcion -c")
        print("(./test.py): accediendo a %r.yaml" % args.config_file)
        config_file = open('configs/'+args.config_file+'.yaml')
    except FileNotFoundError:
        print("(./test.py): archivo de configuracion .yaml no encontrado")
        config_file = None
    if not config_file:
        print("(./test.py): accediendo al file_config sin extension")
        config_file = open(args.config_file)
    config = yaml.load(config_file)
#si no se usan los ficheros de configuracion, se opera con los transformadores
else:
    config = {}
    if args.transformers:
        config['transformers'] = args.transformers
        print("(./test.py): args.transformers-> %r" % args.transformers)
    if args.linearizers:
        config['linearizers'] = args.linearizers
        print("(./test.py): args.linearizers-> %r" % args.linearizers)


config['text'] = text

result = pipeline.run(config)
print("(./test.py): resultado del pipeline.run\n")

if args.print_json:
    print(result.to_json())

if args.display:
    result.draw()

if not args.print_json or not args.display:
    print(result)
