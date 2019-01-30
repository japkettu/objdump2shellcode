# objdump2shellcode

Tool for extracting  shellcode bytes from objdump output.

```sh
$ python2 objdump2shellcode.py -h
usage: objdump2shellcode.py [-h] [-c CPU] [-q] [-e ENDIANNES] file

positional arguments:
  file

optional arguments:
  -h, --help            show this help message and exit
  -c CPU, --cpu CPU     specify CPU architechture [arm, x86]
  -q, --quiet           reduced output
  -e ENDIANNES, --endiannes ENDIANNES
                        change endiannes [big, little]
```



## Basic usage and workflow:

```sh
$ as shellcode.asm -o shellcode.o
$ objdump -d shellcode.o > shellcode.dump
$ python2 objdump2shellcode.py shellcode.dump
0000000000000000 <_start>:
0:	eb 32                	jmp    34 <path>

0000000000000002 <code>:
2:	5f                   	pop    %rdi
3:	31 c0                	xor    %eax,%eax
5:	83 c0 02             	add    $0x2,%eax
8:	31 f6                	xor    %esi,%esi
a:	0f 05                	syscall
c:	89 c7                	mov    %eax,%edi
e:	31 c0                	xor    %eax,%eax
10:	31 d2                	xor    %edx,%edx
12:	48 89 e6             	mov    %rsp,%rsi
15:	83 c2 32             	add    $0x32,%edx
18:	0f 05                	syscall
1a:	88 e6                	mov    %ah,%dh
1c:	31 c0                	xor    %eax,%eax
1e:	83 c0 01             	add    $0x1,%eax
21:	48 89 e6             	mov    %rsp,%rsi
24:	48 31 ff             	xor    %rdi,%rdi
27:	48 83 c7 01          	add    $0x1,%rdi
2b:	0f 05                	syscall
2d:	31 c0                	xor    %eax,%eax
2f:	83 c0 3c             	add    $0x3c,%eax
32:	0f 05                	syscall

0000000000000034 <path>:
34:	e8 c9 ff ff ff       	callq  2 <code>

0000000000000039 <var>:
39:	2f                   	(bad)
3a:	65                   	gs
3b:	74 63                	je     a0 <var+0x67>
3d:	2f                   	(bad)
3e:	70 61                	jo     a1 <var+0x68>
40:	73 73                	jae    b5 <var+0x7c>
42:	77 64                	ja     a8 <var+0x6f>
----------------------------------------------------------------
Architecture: x86
Endiannes: little
Length: 272
Null bytes: 0
\x32\xeb\x5f\xc0\x31\x02\xc0\x83\xf6\x31\x05\x0f\xc7\x89\xc0\x31\xd2\x31\xe6\x89\x48\x32\xc2\x83\x05\x0f\xe6\x88\xc0\x31\x01\xc0\x83\xe6\x89\x48\xff\x31\x48\x01\xc7\x83\x48\x05\x0f\xc0\x31\x3c\xc0\x83\x05\x0f\xff\xff\xff\xc9\xe8\x2f\x65\x63\x74\x2f\x61\x70\x73\x73\x64\x77
```



## Example usage (quiet, big endian):

```sh
$ python2 objdump2shellcode.py -q -ebig arm_shellcode.dump
\x01\x60\x8f\xe2\x16\xff\x2f\xe1\x24\x1b\x21\x1c\x78\x46\x1e\x30\x05\x27\x01\xdf\x69\x46\x20\x22\x03\x27\x05\xdf\x02\x1c\x69\x46\x01\x20\x04\x27\x01\xdf\x24\x1b\x20\x1c\x01\x27\x01\xdf\x2f\x63\x68\x61\x6c\x6c\x65\x6e\x67\x65\x2f\x61\x70\x70\x2d\x73\x79\x73\x74\x65\x6d\x65\x2f\x63\x68\x34\x35\x2f\x2e\x6d\x6f\x74\xff
```


