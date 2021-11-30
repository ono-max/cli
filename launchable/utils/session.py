import os
from pathlib import Path
from typing import Optional
import json

SESSION_DIR_KEY = 'LAUNCHABLE_SESSION_DIR'


def _session_file_dir() -> Path:
    return Path(os.environ.get(SESSION_DIR_KEY) or os.getcwd()).expanduser()


def _session_file_path() -> Path:
    return _session_file_dir() / ".launchable"


def read_build() -> Optional[str]:
    f = _session_file_path()
    try:
        if not f.exists():
            return None

        with open(str(_session_file_path())) as session_file:
            session = json.load(session_file)
            return session["build"]

    except Exception as e:
        raise Exception("Can't read {}".format(f)) from e


def read_session(build_name: str) -> Optional[str]:
    f = _session_file_path()
    try:
        if not f.exists():
            return None

        with open(str(_session_file_path())) as session_file:
            session = json.load(session_file)
            if build_name != session.get('build', None):
                raise Exception("Build name is different from saved. input. input:{} saved:{}".format(
                    build_name, session.get('build', None)))

            return session.get("session")

    except Exception as e:
        raise Exception("Can't read {}".format(f)) from e


def write_build(build_name: str) -> None:
    try:
        if not _session_file_dir().exists():
            _session_file_dir().mkdir(parents=True, exist_ok=True)

        session = {}
        session["build"] = build_name

        with open(str(_session_file_path()), 'w') as session_file:
            json.dump(session, session_file)

    except Exception as e:
        raise Exception("Can't write to {}. Perhaps set the {} environment variable to specify an alternative writable path?".format(
            _session_file_path(), SESSION_DIR_KEY)) from e


def write_session(build_name: str, session_id: str) -> None:
    try:
        if not _session_file_path().exists():
            raise Exception(
                "Session file doesn't exist. Make sure to run `launchable record build --name {}` before".format(build_name))

        if read_build() != build_name:
            # TODO: change error message
            raise Exception("Canot write session because build name is different between saved and input. input: {} saved: {}".format(
                build_name, read_build()))

        session = {}
        session["build"] = build_name
        session["session"] = session_id

        with open(str(_session_file_path()), 'w') as session_file:
            json.dump(session, session_file)

    except Exception as e:
        raise Exception("Can't write to {}. Perhaps set the {} environment variable to specify an alternative writable path?".format(
            _session_file_path(), SESSION_DIR_KEY)) from e


def remove_session() -> None:
    """
    Call it after closing a session
    """
    if _session_file_path().exists():
        _session_file_path().unlink()


def clean_session_files(days_ago: int = 0) -> None:
    """
    Call it each build start
    """
    remove_session()


def parse_session(session: str):
    try:
        # session format:
        # builds/<build name>/test_sessions/<test session id>
        _, build_name, _, session_id = session.split("/")
    except Exception as e:
        raise Exception("Can't parse session: {}".format(session)) from e

    return build_name, session_id
