# test1212

I got tired of manually restarting things or running notifications when a long-running process logs a specific error. This is a small daemon/cli that tails a file and runs a command when a regex matches.

It's simpler than fail2ban and doesn't need root if you're just watching your own dev logs.

## setup

```bash
pip install .
```

## usage

Create a `rules.yaml`:

```yaml
- name: "notify-on-crash"
  pattern: "CRITICAL|FATAL"
  cmd: "notify-send 'Process crashed!'"
```

Then run:

```bash
test1212 watch my-app.log --config rules.yaml
```

I keep the logic minimal. If it gets too complex, I'll probably rewrite the core in Go or Rust, but for now, Python's `watchdog` and `subprocess` are enough.

<!-- checked: 2026-09-03 -->
