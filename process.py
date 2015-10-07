'''
@author Mark Vismer
Functions related to string stuff
'''

from string import *
import win32api, win32process, win32con
import subprocess
import threading


def set_app_id(app_id='mycompany.myproduct.subproduct.version'):
    '''
    This is necessary to use the main window (or app icon) as the task bar
    icon.
    '''
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)


def set_priority(priority=2, pid=None):
    """
    Set The Priority of a Windows Process.
    """
    print "TODO: add os independent support"
    priorityclasses = [win32process.IDLE_PRIORITY_CLASS,
                       win32process.BELOW_NORMAL_PRIORITY_CLASS,
                       win32process.NORMAL_PRIORITY_CLASS,
                       win32process.ABOVE_NORMAL_PRIORITY_CLASS,
                       win32process.HIGH_PRIORITY_CLASS,
                       win32process.REALTIME_PRIORITY_CLASS]
    if pid == None:
        pid = win32api.GetCurrentProcessId()
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
    win32process.SetPriorityClass(handle, priorityclasses[priority])


def launch_app(app_path):
    '''
    Runs a program as a separate process.
    '''
    subprocess.Popen(app_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def launch_baretail(glob_filter = '*.*'):
    '''
    Launches baretail as a realtime log viewer of multiple files.
    '''
    baretail_path = r'"baretail.exe"'
    path = '.'
    the_files = glob.glob(os.path.join(path, glob_filter))

    the_files = [quote_it(os.path.join(path, a_file[idx])) for a_file in the_files]

    subprocess.Popen(' '.join([baretail_path] + the_files),
                     stdout=subprocess.PIPE,stderr=subprocess.PIPE)


def parallel_it(func, args_list):
    '''
    Runs func in a separate thread for each args in args-list.
    '''
    threads = [threading.Thread(target=func, args=args) for args in args_list]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
