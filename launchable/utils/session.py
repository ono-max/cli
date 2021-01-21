import click
import os
import json
from pathlib import Path
import shutil
from typing import Optional

SESSION_DIR_KEY = 'LAUNCHABLE_SESSION_DIR'
DEFAULT_SESSION_DIR = '~/.config/launchable/sessions/'


def _session_file_dir() -> Path:
    return Path(os.environ.get(SESSION_DIR_KEY) or DEFAULT_SESSION_DIR).expanduser()


def _session_file_path(build_name: str) -> Path:
    return _session_file_dir() / "{}:{}.txt".format(build_name, os.getsid(os.getpid()))


def read_session(build_name: str) -> Optional[str]:
    try:
        if not _session_file_path(build_name).exists():
            return None
        return _session_file_path(build_name).read_text()
    except Exception as e:
        raise Exception("Can't read {}. Pleas set accesible directory to {}".format(
            _session_file_path(build_name), SESSION_DIR_KEY)) from e


def write_session(build_name: str, session_id: str) -> None:
    try:
        if not _session_file_dir().exists():
            _session_file_dir().mkdir(parents=True, exist_ok=True)

        _session_file_path(build_name).write_text(session_id)
    except Exception as e:
        raise Exception("Can't write to {}. Pleas set accesible directory to {}".format(
            _session_file_path(build_name), SESSION_DIR_KEY)) from e


def remove_session(build_name: str) -> None:
    """
    Call it after closing a session
    """
    if _session_file_path(build_name).exists():
        _session_file_path(build_name).unlink()


def remove_session_files() -> None:
    """
    Call it each build start
    """
    if _session_file_dir().exists():
        shutil.rmtree(_session_file_dir())
