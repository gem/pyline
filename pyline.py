#!/usr/bin/env python
import sys

class Pyline:
    ST_BEGIN=0
    ST_TRIPLE=1
    ST_QUOTE=2
    ST_COMMENT=3

    def __init__(self, name_in, name_out):
        self.name_in = name_in
        self.name_out = name_out
        with open(self.name_in, "r") as f:
            self.data = f.read()

    def linearize(self):
        s = self.data
        ct = len(s)
        i = 0
        p_pare = 0
        p_brac = 0
        p_curl = 0
        what_quote = ''

        out = ""

        st = self.ST_BEGIN
        while i < ct:
            # print "ST: %d S: [%s] I: %d  CT %d" % (st, s[i], i, ct)
            if st == self.ST_BEGIN:
                if (i + 2) < ct:
                    if ((s[i] == '"' and s[i+1] == '"' and s[i+2] == '"') or
                        (s[i] == "'" and s[i+1] == "'" and s[i+2] == "'")):
                        st = self.ST_TRIPLE
                        what_quote = s[i]
                        out += s[i] *3
                        i += 3
                        continue
                elif (i + 1) < ct:
                    if s[i] == '\\':
                        out += s[i+1]
                        i += 2
                        continue
                if s[i] == '#':
                    st = self.ST_COMMENT
                    out += s[i]

                elif s[i] == '"' or s[i] == "'":
                    what_quote = s[i]
                    out += s[i]
                    st = self.ST_QUOTE

                elif s[i] == '(':
                    out += s[i]
                    p_pare += 1
                elif s[i] == ')':
                    out += s[i]
                    p_pare -= 1

                elif s[i] == '[':
                    out += s[i]
                    p_brac += 1
                elif s[i] == ']':
                    out += s[i]
                    p_brac -= 1

                elif s[i] == '{':
                    out += s[i]
                    p_curl += 1
                elif s[i] == '}':
                    out += s[i]
                    p_curl -= 1

                elif s[i] == '\n':
                    if p_pare == 0 and p_brac == 0 and p_curl == 0:
                        out += s[i]
                    else:
                        out += ' '
                        # remove next line exceeding spaces
                        while i+1 < ct and (s[i+1] == ' ' or s[i+1] == '\t'):
                            i += 1
                else:
                    out += s[i]
            elif st == self.ST_TRIPLE:
                if (i + 2) < ct:
                    if s[i] == what_quote and s[i+1] == what_quote and s[i+2] == what_quote:
                        st = self.ST_BEGIN
                        out += s[i] *3
                        i += 3
                        continue
                elif (i + 1) < ct:
                    if s[i] == '\\':
                        out += s[i+1]
                        i += 2
                        continue
                if s[i] == '\n':
                    out += ' '
                    # remove next line exceeding spaces
                    while i+1 < ct and (s[i+1] == ' ' or s[i+1] == '\t'):
                        i += 1
                else:
                    out += s[i]
            elif st == self.ST_QUOTE:
                if (i + 1) < ct:
                    if s[i] == '\\':
                        out += s[i+1]
                        i += 2
                        continue
                if s[i] == what_quote:
                    out += s[i]
                    st = self.ST_BEGIN
                elif s[i] == '\n':
                    out += ' '
                    # remove next line exceeding spaces
                    while i+1 < ct and (s[i+1] == ' ' or s[i+1] == '\t'):
                        i += 1
                else:
                    out += s[i]
            elif st == self.ST_COMMENT:
                if s[i] == '\n':
                    st = self.ST_BEGIN
                out += s[i]
                
            # end of while i < ct ...
            i += 1

        print out

#
#  MAIN
#

if len(sys.argv) != 2:
    sys.exit(12)

name_in = sys.argv[1]
name_out = "linearized.py"

a = Pyline(name_in, name_out)
a.linearize()
