import sys

from aura.core.app import AuraApp
from aura.core.cli import AuraCLI


def main():
    cli = AuraCLI()

    command_handled = cli.run(sys.argv[1:])

    if command_handled:
        return

    app = AuraApp()
    app.start()


if __name__ == "__main__":
    main()
