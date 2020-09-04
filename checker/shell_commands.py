precompile = {
        'c': 'gcc -o {0}.exec {0} 2> {0}.error',
        'cpp11': 'g++ -static -lm -s -x c++ -O2 -std=c++11 -o {0}.exec {0} 2> {0}.error',
        'cpp14': 'g++ -static -lm -s -x c++ -O2 -std=c++14 -o {0}.exec {0} 2> {0}.error',
        'java': 'javac Main.java 2> {0}.error',
        'NASM': 'nasm -f elf {0} -o {0}.o 2> {0}.error; ld -melf_i386 {0}.o -o {0}.exec 2> {0}.error',
        'pabc': 'mono ./pascal/pabcnetc.exe {0} 2> {0}.error',
}

run = {
    'c': '{0}.exec 2> {0}.error',
    'cpp11': '{0}.exec 2> {0}.error',
    'cpp14': '{0}.exec 2> {0}.error',
    'java': 'java Main Main.class 2> {0}.error',
    'nasm': '{0}.exec 2> {0}.error',
    'pabc': 'mono {0}.exe 2> {0}.error',
    'php': 'php {0} 2> {0}.error',
    'python2': 'python2 {0} 2> {0}.error',
    'python3': 'python3 {0} 2> {0}.error',
}