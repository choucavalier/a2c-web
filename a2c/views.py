from django.shortcuts import render
from a2c.forms import ConvertForm
from a2c.settings import A2C_BINARY, A2C_TIMEOUT
import tempfile
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
            return ('Timeout expired', False)
        except UnicodeDecodeError:
            return ('Output contains unprintable characters.. Dahell?', False)
        return_code = proc.returncode
    if return_code == 0:
        return (stdout, True)
    else:
        return (stderr, False)

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

    context['form'] = form
    return render(request, 'convert.html', context)
