class LoginError(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class ConsequentialError(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class NotLoggedIn(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class LogoutError(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class TaskError(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class AccessDenied(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)