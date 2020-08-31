import collections
import os
import resource
import subprocess
import sys
import threading

from functools import wraps


def threading_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        def run():
            try:
                thread.ret = func(*args, **kwargs)
            except:
                thread.exception = sys.exc_info()

        def get(timeout=0):
            thread.join(timeout)
            if thread.is_alive():
                thread._tstate_lock = None
                thread._stop()
            if thread.exception:
                raise thread.exception[1]
            return thread.ret

        thread = threading.Thread(None, run)
        thread.exception = None
        thread.ret = None
        thread.get = get
        thread.start()
        return thread

    return wrapper


@threading_function
def execute_command(bash_command):
    command_output = subprocess.Popen(bash_command, shell=True, stdout=subprocess.PIPE).stdout.read()
    return command_output


class Checker:
    compilation_commands = {
        'c': 'gcc -o {0}.exec {0} 2> {0}.error',
        'cpp11': 'g++ -static -lm -s -x c++ -O2 -std=c++11 -o {0}.exec {0} 2> {0}.error',
        'cpp14': 'g++ -static -lm -s -x c++ -O2 -std=c++14 -o {0}.exec {0} 2> {0}.error',
        'java': 'javac Main.java 2> {0}.error',
        'NASM': 'nasm -f elf {0} -o {0}.o 2> {0}.error; ld -melf_i386 {0}.o -o {0}.exec 2> {0}.error',
        'pabc': 'mono ./pascal/pabcnetc.exe {0} 2> {0}.error',
    }

    run_commands = {
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

    result = collections.OrderedDict([
        ('status', collections.OrderedDict()),
        ('input', collections.OrderedDict()),
        ('output', collections.OrderedDict()),
        ('program_output', collections.OrderedDict()),
    ])

    def __init__(self, code_path, lang):
        self.code_path = code_path
        self.lang = lang

        if lang in self.compilation_commands:
            self._compile()

        resource.setrlimit(resource.RLIMIT_AS, (2**28, 2**28))

    def run(self):
        for index, (input, output) in enumerate(zip(self.input_data, self.output_data)):
            program_output = self._run_program(input)

            if program_output is None:
                self.result['status'][index] = 'TL'
                break

            program_output = program_output if program_output else bytes()
            program_output = program_output.strip().decode('utf-8')
            self.result['program_output'][index] = ' ' if program_output == '__non_zero_return' else program_output

            if os.stat('{}.error'.format(self.code_path)).st_size != 0:
                with open('{}.error'.format(self.code_path)) as ferr:
                    if ferr.readlines()[-1] == 'MemoryError\n':
                        self.result['status'][index] = 'ME'
                        break
                self.result['status'][index] = 'CE'
                break
            elif program_output == '__non_zero_return':
                self.result['status'][index] = 'RE'
                break
            elif program_output == output:
                self.result['status'][index] = 'OK'
            else:
                self.result['status'][index] = 'WA'
                break

            self.result['input'][index] = input
            self.result['output'][index] = output

        return self.result

    def _run_program(self, input):
        run_command = self.run_commands[self.lang].format(self.code_path)
        bash_command = ('program_output=`echo {} | {}`; if [ $? = 0 ]; then echo $program_output;'
                        'else echo __non_zero_return; fi'.format(input, run_command))
        program = execute_command(bash_command)
        program_output = program.get(2)
        return program_output

    def set_test_cases(self, input, output):
        self.input_data = input
        self.output_data = output

    def _compile(self):
        bash_command = self.compilation_commands[self.lang].format(self.code_path)
        execute_command(bash_command).join()
