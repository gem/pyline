#!/usr/bin/env python

# Copyright (c) 2014, GEM Foundation.
#
# pyline is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyline is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with OpenQuake.  If not, see <http://www.gnu.org/licenses/>.
"""
Join lines of the same python statement.
"""
import sys

class Pyline:
    """
    Class to join lines of the same python statement.
    """
    ST_BEGIN = 0
    ST_TRIPLE = 1
    ST_QUOTE = 2
    ST_COMMENT = 3

    def __init__(self, f_in, name_in):
        self.f_in    = f_in
        self.name_in = name_in
        self.data = f_in.read()

    @staticmethod
    def backslash_newline(cha):
        """
        Manage the character after a backslash.
        """
        if (cha == '\n'):
            return ''
        else:
            return cha

    @staticmethod
    def joinlines(i, s_in, s_len):
        """
        Remove all indentation spaces from joined line.
        """
        while i+1 < s_len and (s_in[i+1] == ' ' or s_in[i+1] == '\t'):
            i += 1
        return i

    def linearize(self):
        """
        Main method to join multi-lines statement.
        """
        s_in = self.data
        s_len = len(s_in)
        c_pos = 0
        i = 0
        p_pare = 0
        p_brac = 0
        p_curl = 0
        what_quote = ''

        out = ""

        status = self.ST_BEGIN
        while i < s_len:
            if c_pos == 0:
                out += ("" if self.name_in == "" else "%s:" % self.name_in)
                c_pos = 1
            #print "ST: %d S: [%s] I: %d  S_LEN %d" % (status,
            #                                          s_in[i], i, s_len)
            if status == self.ST_BEGIN:
                if (i + 2) < s_len:
                    if s_in[i:i+3] == '"""' or s_in[i:i+3] == "'''":
                        status = self.ST_TRIPLE
                        what_quote = s_in[i]
                        out += s_in[i] *3
                        i += 3
                        continue
                elif (i + 1) < s_len:
                    if s_in[i] == '\\':
                        out += self.backslash_newline(s_in[i+1])
                        i += 2
                        continue
                if s_in[i] == '#':
                    status = self.ST_COMMENT
                    out += s_in[i]

                elif s_in[i] == '"' or s_in[i] == "'":
                    what_quote = s_in[i]
                    out += s_in[i]
                    status = self.ST_QUOTE

                elif s_in[i] == '(':
                    out += s_in[i]
                    p_pare += 1
                elif s_in[i] == ')':
                    out += s_in[i]
                    p_pare -= 1

                elif s_in[i] == '[':
                    out += s_in[i]
                    p_brac += 1
                elif s_in[i] == ']':
                    out += s_in[i]
                    p_brac -= 1

                elif s_in[i] == '{':
                    out += s_in[i]
                    p_curl += 1
                elif s_in[i] == '}':
                    out += s_in[i]
                    p_curl -= 1

                elif s_in[i] == '\n':
                    if p_pare == 0 and p_brac == 0 and p_curl == 0:
                        out += s_in[i]
                        c_pos = 0
                    else:
                        out += ' '
                        # remove next line exceeding spaces
                        i = self.joinlines(i, s_in, s_len)
                else:
                    out += s_in[i]
            elif status == self.ST_TRIPLE:
                if (i + 2) < s_len:
                    if (s_in[i] == what_quote and s_in[i+1] == what_quote and
                        s_in[i+2] == what_quote):
                        status = self.ST_BEGIN
                        out += s_in[i] *3
                        i += 3
                        continue
                elif (i + 1) < s_len:
                    if s_in[i] == '\\':
                        out += self.backslash_newline(s_in[i+1])
                        i += 2
                        continue
                if s_in[i] == '\n':
                    out += ' '
                    # remove next line exceeding spaces
                    i = self.joinlines(i, s_in, s_len)
                else:
                    out += s_in[i]
            elif status == self.ST_QUOTE:
                if (i + 1) < s_len:
                    if s_in[i] == '\\':
                        out += self.backslash_newline(s_in[i+1])
                        i += 2
                        continue
                if s_in[i] == what_quote:
                    out += s_in[i]
                    status = self.ST_BEGIN
                elif s_in[i] == '\n':
                    out += ' '
                    # remove next line exceeding spaces
                    i = self.joinlines(i, s_in, s_len)
                else:
                    out += s_in[i]
            elif status == self.ST_COMMENT:
                if s_in[i] == '\n':
                    status = self.ST_BEGIN
                    c_pos = 0
                out += s_in[i]

            # end of while i < s_len ...
            i += 1
        if out[-1] != '\n':
            sys.stderr.write("Warning: no newline at end of file %s\n"
                             % self.name_in)
            out += '\n'
        sys.stdout.write(out)

#
#  MAIN
#

def print_help(name):
    """
    Print command usage.
    """
    print "USAGE\n  %s -h\n  %s [file1 [file2 [...]]]" % (name, name)
    sys.exit(0)

def main():
    """
    Process files or stdin.
    """
    if len(sys.argv) > 1 and (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        print_help(sys.argv[0])
        sys.exit(0)

    if len(sys.argv) == 1:
        lin = Pyline(sys.stdin, '')
        lin.linearize()
    else:
        for f_name in sys.argv[1:]:
            with open(f_name, "r") as f_in:
                lin = Pyline(f_in, f_name)
                lin.linearize()

if __name__ == '__main__':
    main()



