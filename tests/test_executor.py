import pytest
from test1212.executor import CommandExecutor

def test_simple_command():
    ex = CommandExecutor(timeout=2)
    # use echo to verify it runs
    out = ex.run("echo 'hello'")
    assert out.strip() == "hello"

