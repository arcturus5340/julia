import os
import resource
import signal
import subprocess


def run_subprocess(cmd, timeout=2):
    with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid) as process:
        try:
            output, unused_error = process.communicate(timeout=timeout)
            if unused_error:
                raise subprocess.SubprocessError
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGINT)
            raise subprocess.TimeoutExpired(cmd, timeout)
    return output


class Checker:
    compilation_commands = {
        'c': 'gcc -o {0}.exec {0}',
        'cpp11': 'g++ -static -lm -s -x c++ -O2 -std=c++11 -o {0}.exec {0}',
        'cpp14': 'g++ -static -lm -s -x c++ -O2 -std=c++14 -o {0}.exec {0}',
        'java': 'javac Main.java',
        'nasm': 'nasm -f elf {0} -o {0}.o; ld -melf_i386 {0}.o -o {0}.exec',
        'pabc': 'mono ./pascal/pabcnetc.exe {0}',
    }

    run_commands = {
        'c': '{0}.exec',
        'cpp11': '{0}.exec',
        'cpp14': '{0}.exec',
        'java': 'java Main Main.class',
        'nasm': '{0}.exec',
        'speedy1': 'speedy1/speedy1 {0}',
        'pabc': 'mono {0}.exe',
        'php': 'php {0}',
        'python2': 'python2 {0}',
        'python3': 'python3 {0}',
    }

    SUPPORTED_LANGUAGES = list(run_commands.keys())
    SUPPORTED_STATUS_CODES = ['OK', 'WA', 'TL', 'ME', 'CE', 'RE']

    def __init__(self, code_path, lang, tl=2, ml=2**28):
        self.code_path = code_path
        self.lang = lang
        self.tl = tl

        self.input_data = []
        self.output_data = []

        self.result = {
            'status': dict(),
            'input': dict(),
            'output': dict(),
            'program_output': dict(),
        }
        resource.setrlimit(resource.RLIMIT_AS, (ml, ml))

    def _compile(self):
        bash_command = self.compilation_commands[self.lang].format(self.code_path)
        run_subprocess(bash_command)

    def set_test_cases(self, input, output):
        self.input_data = input
        self.output_data = output

    def run(self):
        if self.lang in self.compilation_commands:
            try:
                self._compile()
            except subprocess.SubprocessError:
                self.result['status'][0] = 'CE'
                return self.result

        for index, (input, output) in enumerate(zip(self.input_data, self.output_data)):
            try:
                program_output = self._run_program(input)
            except subprocess.TimeoutExpired:
                self.result['status'][index] = 'TL'
                break
            except subprocess.SubprocessError:
                self.result['status'][index] = 'RE'
                break

            program_output = program_output.strip().decode('utf-8')
            self.result['program_output'][index] = program_output

            if program_output != output:
                self.result['status'][index] = 'WA'
                break

            self.result['status'][index] = 'OK'
            self.result['input'][index] = input
            self.result['output'][index] = output

        return self.result

    def _run_program(self, input):
        run_command = self.run_commands[self.lang].format(self.code_path)
        bash_command = ('echo {} | {}'.format(input, run_command))
        return run_subprocess(bash_command, self.tl)
