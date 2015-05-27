from django.shortcuts import render
from a2c.forms import ConvertForm
from a2c.settings import A2C_BINARY, A2C_TIMEOUT, A2C_GCC_FLAGS
import tempfile
import shutil
from subprocess import Popen, TimeoutExpired, PIPE

def convert_code(algo_code):
    algo_code = algo_code.replace('\r', '')
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    tmp_file.write(algo_code.encode('utf-8'))
    tmp_file.close()
    args = [tmp_file.name]
    with Popen([A2C_BINARY] + args, stdout=PIPE, stderr=PIPE, stdin=PIPE,
               universal_newlines=True) as proc:
        try:
            stdout, stderr = proc.communicate(timeout=A2C_TIMEOUT)
        except TimeoutExpired:
            proc.kill()
            return ('Timeout while converting', False)
        except UnicodeDecodeError:
            return ('Output contains unprintable characters.. Dahell?', False)
        return_code = proc.returncode
    if return_code == 0:
        return (stdout, True)
    else:
        return (stderr, False)

def run_algo(c_code):
    ret = dict()
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    tmp_file.write(c_code.encode('utf-8'))
    tmp_file.close()
    shutil.copy(tmp_file.name, tmp_file.name + '.c')
    args = A2C_GCC_FLAGS + [tmp_file.name + '.c'] + ['-o', tmp_file.name]
    with Popen(['gcc'] + args, stdout=PIPE, stderr=PIPE, stdin=PIPE,
               universal_newlines=True) as proc:
        try:
            stdout, stderr = proc.communicate(timeout=A2C_TIMEOUT)
        except TimeoutExpired:
            proc.kill()
            ret['error'] = 'Timeout while compiling'
            return ret
        except UnicodeDecodeError:
            ret['error'] = 'Output contains unprintable characters.. Dahell?'
            return ret
        ret['comp_return_code'] = proc.returncode
    ret['comp_stdout'] = stdout
    ret['comp_stderr'] = stderr
    with Popen([tmp_file.name], stdout=PIPE, stderr=PIPE,
               universal_newlines=True) as proc:
        try:
            stdout, stderr = proc.communicate(timeout=A2C_TIMEOUT)
        except TimeoutExpired:
            proc.kill()
            return ('Timeout while running', False)
        except UnicodeDecodeError:
            return ('Output contains unprintable characters.. Dahell?', False)
        ret['run_return_code'] = proc.returncode
    ret['run_stdout'] = stdout
    ret['run_stderr'] = stderr
    return ret

def convert(request):
    context = {}
    form = ConvertForm()
    if request.method == 'POST':
        form = ConvertForm(request.POST)

        if form.is_valid():
            algo_code = form.cleaned_data['algo_code']
            a2c_output, algo_is_valid = convert_code(algo_code)
            form.data = form.data.copy()
            if not algo_is_valid:
                context['error'] = a2c_output
                form.data['c_code'] = '// Compilation Error :(\n' \
                                      '// See a2c\'s output below'
            else:
                form.data['c_code'] = a2c_output
                out = run_algo(a2c_output)
                if 'error' in out:
                    context['error'] = a2c_output
                else:
                    context['algo_output'] = out['run_stdout']


    context['form'] = form
    return render(request, 'convert.html', context)
