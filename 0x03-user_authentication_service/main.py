#!/usr/bin/env python3
"""this docs contains main file"""
import requests


def register_user(email: str, password: str) -> None:
    """
    func to register a user with the given email and password.
    Args:
        email: email of the user.
        password: password of the user.
    """
    rp = requests.post('http://127.0.0.1:5000/users',
                       data={'email': email, 'password': password})

    if rp.status_code == 200:
        assert (rp.json() == {"email": email, "message": "user created"})

    else:
        assert(rp.status_code == 400)
        assert(rp.json() == {"message": "email already registered"})


def log_in_wrong_password(email: str, password: str) -> None:
    """
    func to Test log in with the given wrong credentials.
    Args:
        email: email of the user.
        password: password of the user.
    """
    rs = requests.post('http://127.0.0.1:5000/sessions',
                       data={'email': email, 'password': password})

    assert (rs.status_code == 401)


def log_in(email: str, password: str) -> str:
    """
    func to Test for log in with the given correct
    Args:
        email: email of the user.
        password: password of the user.
    """
    rp = requests.post('http://127.0.0.1:5000/sessions',
                       data={'email': email, 'password': password})

    assert(rp.status_code == 200)
    assert(rp.json() == {"email": email, "message": "logged in"})

    return rp.cookies['session_id']


def profile_unlogged() -> None:
    """
    func to Test for profile without being logged in with session_id.
    Returns:
        Nothing
    """
    rsp = requests.get('http://127.0.0.1:5000/profile')

    assert(rsp.status_code == 403)


def profile_logged(session_id: str) -> None:
    """
    func to Test for profile with being logged in with session_id.
    Args:
        session_id: session_id of the user.
    """
    cookies = {'session_id': session_id}

    rsp = requests.get('http://127.0.0.1:5000/profile',
                       cookies=cookies)

    assert(rsp.status_code == 200)


def log_out(session_id: str) -> None:
    """
    func to Test for log out with the given session_id.
    Args:
        session_id: session_id of the user.
    """
    cookies = {'session_id': session_id}

    rsp = requests.delete('http://127.0.0.1:5000/sessions',
                          cookies=cookies)

    if rsp.status_code == 302:
        assert(rsp.url == 'http://127.0.0.1:5000/')

    else:
        assert(rsp.status_code == 200)


def reset_password_token(email: str) -> str:
    """
    func to Test for reset password token with the given email.
    Args:
        email: email of the user.
    Returns:
        reset_token of the user.
    """
    rsp = requests.post('http://127.0.0.1:5000/reset_password',
                        data={'email': email})

    if rsp.status_code == 200:
        return rsp.json()['reset_token']

    assert(rsp.status_code == 401)


def update_password(email: str, reset_token: str,
                    new_password: str) -> None:
    """
    func to Test for update password with the given email
    Args:
        email: email of the user.
        reset_token: reset_token of the user.
        new_password: new password of the user.
    Returns:
        Nothing
    """
    data = {'email': email, 'reset_token': reset_token,
            'new_password': new_password}

    rsp = requests.put('http://127.0.0.1:5000/reset_password',
                       data=data)

    if rsp.status_code == 200:
        assert(rsp.json() == {"email": email, "message": "Password updated"})

    else:
        assert(rsp.status_code == 403)


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
