'''Provides console functions. These are platform dependent, i.e. a console on
windows is different from a console on a Mac or Linux.'''

import os


class LinuxOrMac(object):
    def pause(self):
        '''Waits for user input'''
        input('Press any key to continue ...')

    def clear(self):
        '''Clears the console window.'''
        os.system('clear')


class Windows(object):
    def pause(self):
        '''Waits for user input'''
        os.system('pause')

    def clear(self):
        '''Clears the console window.'''
        os.system('cls')


def current():
    '''Returns the current operating system'''
    name = os.name
    if 'posix' in name:
        return LinuxOrMac()
    elif 'nt' in name:
        return Windows()
    else:
        # This is not strictly speaking necessary,
        # as we could just move on silently, but it is
        # important to be explicit and fail early.
        message = 'Sorry, your system is not supported.'
        raise NotImplementedError(message)


__all__ = ['current']
