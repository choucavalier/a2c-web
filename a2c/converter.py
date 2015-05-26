import tempfile
from subprocess import Popen, TimeoutExpired, PIPE
from a2c.settings import A2C_BINARY, A2C_TIMEOUT

def convert_algo(algo):
    algo = algo.replace('\r', '')
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    tmp_file.write(algo.encode('utf-8'))
    tmp_file.close()
    args = [tmp_file.name]
    with Popen([A2C_BINARY] + args, stdout=PIPE, stderr=PIPE, stdin=PIPE,
               universal_newlines=True) as proc:
        try:
            stdout, stderr = proc.communicate(timeout=A2C_TIMEOUT)
        except TimeoutExpired:
            proc.kill()
            return 'Timeout expired'
        except UnicodeDecodeError:
            return 'Output contains unprintable characters.. Dahell?'
        return_code = proc.returncode
    if return_code == 0:
        return stdout
    else:
        return stderr
