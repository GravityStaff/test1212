import pytest
from test1212.executor import CommandExecutor

def test_simple_command():
    ex = CommandExecutor(timeout=2)
    # use echo to verify it runs
    out = ex.run("echo 'hello'")
    assert out.strip() == "hello"

def test_env_passing():
    ex = CommandExecutor()
    out = ex.run("echo $MY_VAR", extra_env={"MY_VAR": "found_it"})
    assert out.strip() == "found_it"

def test_failure_handling():
    ex = CommandExecutor()
    # this should return None on failure rather than crashing
    res = ex.run("exit 1")
    assert res is None
