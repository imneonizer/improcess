from improcess.improcess import multi_processing, console_log
import time

__version__='1.1'
__author__='Nitin Rai'

st = 0
#default start function for spawning process
def start(processing_func, data=None, repeat=None, max_process=4):
    assert type(max_process) == int, 'max_process value should be an integer'
    assert max_process>0, 'max_process value cannot be less than 1'
    mp_local = multi_processing(processing_func, max_process=max_process)
    global st
    st = time.time()

    if data:
        processed_data = mp_local.start(data)
        return processed_data

    elif repeat:
        assert type(repeat) == int, 'repeat value should be an integer'
        assert repeat>0, 'repeat value cannot be less than 1'
        processed_data = mp_local.start(repeat)
        return processed_data

    else:
        print(f'data: {data}, repeat: {repeat}')


def stop():
    raise Exception('stop_process')

def elapsed(output=False):
    tt = round((time.time()-st), 2)
    if output:
        print(f'>>> Elapsed time: {tt} sec')
    return tt
