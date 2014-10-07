#!/usr/bin/env python
import sys

class Pyline:
    ST_BEGIN=0
    ST_TRIPLE=1
    ST_QUOTE=2
    ST_COMMENT=3

    def __init__(self, f_in, name_in):
        self.f_in    = f_in
        self.name_in = name_in
        self.data = f_in.read()

    @staticmethod
    def backslash_newline(c):
        if (c == '\n'):
            return ''
        else:
            return c

    @staticmethod
    def joinlines(i, s, ct):
        while i+1 < ct and (s[i+1] == ' ' or s[i+1] == '\t'):
            i += 1
        return i

    def linearize(self):
        s = self.data
        ct = len(s)
        c_pos = 0
        i = 0
        p_pare = 0
        p_brac = 0
        p_curl = 0
        what_quote = ''

        out = ""

        st = self.ST_BEGIN
        while i < ct:
            if c_pos == 0:
                out += ("" if self.name_in == "" else "%s:" % self.name_in)
                c_pos = 1
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
                        out += self.backslash_newline(s[i+1])
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
                        c_pos = 0
                    else:
                        out += ' '
                        # remove next line exceeding spaces
                        i = self.joinlines(i, s, ct)
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
                        out += self.backslash_newline(s[i+1])
                        i += 2
                        continue
                if s[i] == '\n':
                    out += ' '
                    # remove next line exceeding spaces
                    i = self.joinlines(i, s, ct)
                else:
                    out += s[i]
            elif st == self.ST_QUOTE:
                if (i + 1) < ct:
                    if s[i] == '\\':
                        out += self.backslash_newline(s[i+1])
                        i += 2
                        continue
                if s[i] == what_quote:
                    out += s[i]
                    st = self.ST_BEGIN
                elif s[i] == '\n':
                    out += ' '
                    # remove next line exceeding spaces
                    i = self.joinlines(i, s, ct)
                else:
                    out += s[i]
            elif st == self.ST_COMMENT:
                if s[i] == '\n':
                    st = self.ST_BEGIN
                    c_pos = 0
                out += s[i]

            # end of while i < ct ...
            i += 1
        if out[-1] != '\n':
            sys.stderr.write("Warning: no newline at end of file %s\n" % self.name_in)
            out += '\n'
        sys.stdout.write(out)

#
#  MAIN
#

def print_help(name):
    print "USAGE\n  %s -h\n  %s [file1 [file2 [...]]]" % (name, name)
    sys.exit(0)
def main():
    if len(sys.argv) > 1 and (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        print_help(sys.argv[0])
        sys.exit(0)

    if len(sys.argv) == 1:
        a = Pyline(sys.stdin, '')
        a.linearize()
    else:
        for f_name in sys.argv[1:]:
            with open(f_name, "r") as f_in:
                a = Pyline(f_in, f_name)
                a.linearize()

if __name__ == '__main__':
    main()



