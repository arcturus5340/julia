import collections
import os
import resource
import subprocess
import sys
import threading

from . import shell_commands
from contest.models import TestCase


def threading_function(func):
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


def check(lang, file_path, task_obj):
    print(lang in shell_commands.precompile)
    if lang in shell_commands.precompile.keys():
        bash_comand = shell_commands.precompile[lang].format(file_path)
        execute_command(bash_comand).join()

    response_dict = collections.OrderedDict([('status', collections.OrderedDict()),
                                             ('input', collections.OrderedDict()),
                                             ('output', collections.OrderedDict()),
                                             ('program_output', collections.OrderedDict()),
                                             ])

    resource.setrlimit(resource.RLIMIT_AS, (2**28, 2**28))

    test_cases = TestCase.objects.filter(task=task_obj).values_list('input', 'output')
    for index, (ipt, opt) in enumerate(test_cases):
        run_command = shell_commands.run[lang].format(file_path)
        bash_command = ('program_output=`echo {} | {}`; if [ $? = 0 ]; then echo $program_output;'
                        'else echo __non_zero_return; fi'.format(ipt, run_command))
        program = execute_command(bash_command)
        program_output = program.get(2)

        if program_output is None:
            response_dict['status'][str(index)] = 'TL'
            break

        program_output = program_output if program_output else bytes()
        program_output = program_output.strip().decode('utf-8')
        response_dict['program_output'][str(index)] = ' ' if program_output == '__non_zero_return' else program_output

        if os.stat('{}.error'.format(file_path)).st_size != 0:
            with open('{}.error'.format(file_path)) as ferr:
                if ferr.readlines()[-1] == 'MemoryError\n':
                    response_dict['status'][str(index)] = 'ME'
                    break
            response_dict['status'][str(index)] = 'CE'
            break
        elif program_output == '__non_zero_return':
            response_dict['status'][str(index)] = 'RE'
            break
        elif program_output == opt:
            response_dict['status'][str(index)] = 'OK'
        else:
            response_dict['status'][str(index)] = 'Wrong Answer'
            break
        response_dict['input'][str(index)] = ipt
        response_dict['output'][str(index)] = opt

    return response_dict
