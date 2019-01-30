#!/usr/bin/env python2

import re
import sys
import argparse


def nullbytes(shellcode):
    c = 0
    for byte in shellcode.split('\\x'):
        if ('00' in byte):
            c += 1
    return c
    
def show_info(shellcode, endiannes, arch, quiet_mode):
    if not quiet_mode:
        print "-" * 64
        print "Architecture: %s" % (arch)
        print "Endiannes: %s" % (endiannes)
        print "Length: %d" % (len(shellcode))
        print "Null bytes: %d" % (nullbytes(shellcode))
        print shellcode

    else:
        print shellcode

def detectArch(line):
    string =  line.split(' ')[-1]
    string = string.lower()   
    if 'arm' in string:
        return 'arm'
    elif 'x86' in string:
        return 'x86'
    else:
        print 'Could not detect architecture! Exiting.'
        sys.exit(0)

def arm(fd, endiannes, quiet_mode):
    
    shellcode = '' 
    code_section = False

    for line in fd:
        line = line.strip()
        if "_start" in line:
            code_section = True
            continue

        if code_section == True:
            if not quiet_mode:
                print line
            if len(line) > 5:
                if line.endswith('>:'):
                    continue
                columns = line.replace('\t',' ').split(' ')
                columns = filter(None, columns) 
                code_col = columns[1].strip()
                pairs = re.findall('..',code_col)
                if endiannes == 'little':
                    pairs = pairs[::-1]
                for pair in pairs:
                    shellcode += '\\x'+pair

    return shellcode


def x86(fd, endiannes, quiet_mode):
    
    shellcode = '' 
    code_section = False

    for line in fd:
        line = line.strip()
        if "_start" in line:
            if not quiet_mode:
                 print line
            code_section = True
            continue

        if code_section == True:
            if not quiet_mode:
                print line
            if len(line) > 5:
                if line.endswith('>:'):
                    continue
                columns = line.replace('\t',' ').split(' ')
                code_col = columns[1:columns.index('')]
                code_col = "".join(code_col)
                pairs = re.findall('..',code_col)
                if endiannes == 'little':
                    pairs = pairs[::-1]
                for pair in pairs:
                    shellcode += '\\x'+pair

    return shellcode

def main():

    ap = argparse.ArgumentParser()
    ap.add_argument('-c', '--cpu', required=False, help='set CPU architechture [arm, x86]')
    ap.add_argument('-q', '--quiet', required=False, default=False, help='reduced output', action='store_true') 
    ap.add_argument('-e', '--endiannes', required=False, default='little', help='change endiannes [big, little]')
    ap.add_argument("file")
    args = vars(ap.parse_args())

    
    endiannes = args["endiannes"]
    shellcode = ''
    arch = args["cpu"]
    filepath = args["file"]
    quiet_mode =  args["quiet"]


    with open(filepath) as fd:    

        for line in fd:
            line = line.strip()
            if not arch:
                if len(line.strip()) != 0 :
                    arch = detectArch(line)
            else:
                if arch == 'arm':
                    shellcode = arm(fd, endiannes, quiet_mode)             
                if arch == 'x86':
                    shellcode = x86(fd, endiannes, quiet_mode)


        show_info(shellcode, endiannes, arch, quiet_mode)

if __name__ == '__main__':
        main()
