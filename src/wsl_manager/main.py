import controllers
import views


def main():
    try:
        option = views.display_menu()

        if option == "shrink":
            controllers.shrink()
        elif option == "move":
            controllers.move()
        else:
            raise ValueError("Invalid option")
    except Exception:
        views.console.print_exception(show_locals=True)
        views.press_any_key_to_continue()


if __name__ == "__main__":
    main()
