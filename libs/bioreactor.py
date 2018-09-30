import subprocess
import time

GET = ['gosh', 'scm_scripts/get_values.scm']
SET = ['gosh', 'scm_scripts/set_values.scm']

def get_output():
    '''
    Reads output from bioreactor by calling a Scheme script
    '''
    result = subprocess.run(['gosh', 'scm_scripts/get_values.scm'], stdout=subprocess.PIPE)
    return eval(result.stdout.decode('utf-8'))

def set_input(value, input):
    '''
    Sets particular <input> for bioreactor to <value> 
    Requires definition of possible inputs.
    '''
    subprocess.call(SET + [str(value), input])


# while True:
#     print(get_output())
#     time.sleep(2)

print(get_output())
set_input(10, "set-valve-tflow")