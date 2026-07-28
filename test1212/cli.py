import click
import sys
from test1212.config import load_config
from test1212.watcher import LogWatcher

@click.command()
@click.option('--config', '-c', default='config.yaml', help='Path to config file')
def main(config):
    try:
        cfg = load_config(config)
    except Exception as e:
        click.echo(f"failed to load config: {e}", err=True)
        sys.exit(1)

    watcher = LogWatcher(cfg)
    watcher.run()

if __name__ == '__main__':
    main()
