from django.shortcuts import render
from a2c.forms import ConvertForm
from a2c.settings import A2C_BINARY
import tempfile
from subprocess import Popen, TimeoutExpired, PIPE

def convert_code(algo_code):
    tmp_file = tempfile.TemporaryFile()
    tmp_file.write(algo_code)
    args = [tmp_file.name]
    with Popen([A2C_BINARY] + args, stdout=PIPE, stderr=PIPE, stdin=PIPE,
               universal_newlines=True) as proc:
        try:
            stdout, stderr = proc.communicate(input=test_input, timeout=TIMEOUT)
        except TimeoutExpired:
            proc.kill()
            return ('Timeout expired', False)
        except UnicodeDecodeError:
            return ('Output contains unprintable characters.. Dahell bro',
                    False)
        return_code = proc.returncode
    if return_code == 0:
        return (True, stdout)
    else:
        return (False, stderr)

def convert(request):
    context = {}
    form = ConvertForm()
    if request.method == 'POST':
        form = ConvertForm(request.POST)

        if form.is_valid():
            algo_code = form.cleaned_data['algo_code']
            a2c_output, algo_is_valid = convert_code(algo_code)
            if not algo_is_valid:
                context['error'] = a2c_output
                form.cleaned_data['c_code'] = '// Compilation Error :(\n' \
                                              '// See a2c\'s output below'
            else:
                form.cleaned_data['c_code'] = a2c_output

    context['form'] = ConvertForm()
    return render(request, 'convert.html', context)
