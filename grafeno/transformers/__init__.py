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

import glob
from importlib import import_module
from os.path import dirname, basename, isfile

transformers = dict()

for m in glob.glob(dirname(__file__)+"/*.py"):
    f = basename(m)[:-3]
    if isfile(m) is True and not f.startswith('__'):
        transformers[f] = import_module('grafeno.transformers.'+f, __name__).Transformer

def get_pipeline (modules):
    '''Takes a list of transformers and returns a transformer which
    subclasses them all'''
    name = '__'.join(modules)
    if name in transformers:
        return transformers[name]
    else:
        T = type(name, tuple(transformers[m] for m in reversed(modules)), {})
        transformers[name] = T
        return T