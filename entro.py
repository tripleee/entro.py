#!/usr/bin/python
# -*- encoding: utf-8 -*-
#
# https://github.com/tripleee/entro.py

"""
Simple command-line calculator for variations of Shannon entropy

Try entro.py --help to see a list of options.
"""

import math, sys
from optparse import OptionParser  # ugh


class Str (str):
    def width (self, member):
        return 256

class Utf8 (unicode):
    def __new__ (self, content):
        return unicode.__new__(self, content.decode('utf-8'))
    def width (self, member):
        return 256 * len(member.encode('utf-8'))

class Nybble (str):
    def __iter__ (self):
        for i in xrange(str.__len__(self)):
            yield chr(ord(self[i])>>4)
            yield chr(ord(self[i])&15)
    def __len__ (self):
        return str.__len__(self) * 2
    def width (self, member):
        return 16

class Bit (str):
    def __iter__ (self):
        for i in xrange(str.__len__(self)):
            for b in xrange(8):
                yield chr((ord(self[i])&(2**b)) >> b)
    def __len__ (self):
        return str.__len__(self) * 8
    def width (self, member):
        return 2


def H(data, debug=False):
    entropy = 0
    count = dict()
    for c in data:
        try:
            count[c] += 1
        except KeyError:
            count[c] = 1
    for x in count:
        p_x = float(count[x])/len(data)
        if debug:
            print "# %r: %i/%i = %f => %f" % (
                x, count[x], len(data), p_x, -p_x*math.log(p_x, data.width(x)))
        ######## FIXME: base should be 8 for byte entropy,
        # but unclear what exactly it should be for UTF-8
        entropy += - p_x*math.log(p_x, data.width(x))
    return entropy


def main (args):
    parser = OptionParser()
    parser.add_option('-u', '--unicode', const=Utf8,
                      help='Use UTF-8 code points as the basic input type',
                      dest='objtype', action='store_const')
    parser.add_option('-8', '--byte', const=Str, default=Str,
                      help='Use 8-bit bytes as the basic input type',
                      dest='objtype', action='store_const')
    parser.add_option('-n', '--nybble', const=Nybble,
                      help='Use nybbles as the basic input type',
                      dest='objtype', action='store_const')
    parser.add_option('-b', '--bit', const=Bit,
                      help='Use bits as the basic input type',
                      dest='objtype', action='store_const')
    parser.add_option('-v', '--verbose',
                      help='Verbose diagnostic output',
                      dest='debug', action='store_true')
    (opts, args) = parser.parse_args()

    if args == []:
        args = ['-']
    for file in args:
        if file is '-':
            handle = sys.stdin
        else:
            handle = open(file)
        data = handle.read()
        handle.close()
        print "%s: %f" % (file, H(opts.objtype(data),debug=opts.debug))

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
