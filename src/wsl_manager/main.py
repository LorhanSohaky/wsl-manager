import logging

import controllers
import views
from rich.logging import RichHandler

logging.basicConfig(
    level="ERROR",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=False)],
)


def main():
    try:
        option = views.display_menu()

        if option == "shrink":
            controllers.shrink()
        elif option == "move":
            controllers.move()
        elif option == "recover":
            controllers.recover()
        else:
            raise ValueError("Invalid option")
    except Exception as exception:
        log = logging.getLogger("rich")
        log.exception(exception)
        views.press_any_key_to_continue()


if __name__ == "__main__":
    main()
