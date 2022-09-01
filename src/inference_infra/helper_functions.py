import os
import shutil
import contextlib

def create_dir(dirname):
    '''Creates temp dir and returns full path'''
    path = os.path.join(os.getcwd(), dirname) 
    if not os.path.exists(path):
        os.mkdir(path)
    return path


@contextlib.contextmanager
def tempdir_context(dirname = 'temp/'):
    '''
    Context Maneger for temporary files
    '''
    # create dir if not exists
    tempdir = create_dir(dirname)

    yield tempdir 

    #remove dir
    shutil.rmtree(tempdir)