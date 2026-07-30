import time
import os
from test1212.watcher import LogWatcher
from test1212.config import Config, Rule

def test_watcher_picks_up_line(tmp_path):
    log_file = tmp_path / "test.log"
    log_file.write_text("init\n")
    
    triggered = []
    def mock_callback(rule, match):
        triggered.append(rule.name)

    rule = Rule(name="test-rule", pattern=r"ERROR (.*)", command="echo 1")
    cfg = Config(path=str(log_file), rules=[rule])
    
    watcher = LogWatcher(cfg, callback=mock_callback)
    
    # we need to run it in a way that we can stop it
    # for testing, let's just trigger one tick if the watcher supports it
    import threading
    stop_event = threading.Event()
    
    def run_watcher():
        watcher.start(stop_event)

    t = threading.Thread(target=run_watcher)
    t.start()
    
    try:
        time.sleep(0.1)
        with open(log_file, "a") as f:
            f.write("ERROR something went wrong\n")
            f.flush()
        
        # print("wrote to file") # dbg
        time.sleep(0.5)
        assert "test-rule" in triggered
    finally:
        stop_event.set()
        t.join(timeout=1)

def test_watcher_ignores_non_matching(tmp_path):
    log_file = tmp_path / "test.log"
    log_file.write_text("\n")
    
    triggered = []
    rule = Rule(name="test-rule", pattern=r"CRITICAL", command="exit 0")
    cfg = Config(path=str(log_file), rules=[rule])
    
    watcher = LogWatcher(cfg, callback=lambda r, m: triggered.append(r.name))
    
    stop_event = threading.Event()
    t = threading.Thread(target=lambda: watcher.start(stop_event))
    t.start()
    
    try:
        time.sleep(0.1)
        with open(log_file, "a") as f:
            f.write("INFO just some info\n")
            f.flush()
        time.sleep(0.3)
        assert len(triggered) == 0
    finally:
        stop_event.set()
        t.join(timeout=1)
