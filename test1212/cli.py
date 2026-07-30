import click
import sys
import logging
from test1212.config import load_config
from test1212.watcher import LogWatcher

@click.command()
@click.option('--config', '-c', type=click.Path(exists=True), default='rules.yaml')
@click.option('--debug', is_flag=True, help='Enable verbose logging')
def main(config, debug):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format='%(levelname)s: %(message)s')
    
    try:
        cfg = load_config(config)
    except FileNotFoundError:
        click.secho(f"Config file not found: {config}", fg='red')
        sys.exit(1)
    except Exception as e:
        click.secho(f"Fatal error: {e}", fg='red')
        sys.exit(1)

    watcher = LogWatcher(cfg)
    click.echo(f"Watching logs based on {config}...")
    watcher.run()

if __name__ == '__main__':
    main()
