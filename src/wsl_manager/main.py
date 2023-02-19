import controllers
import views


def main():
    option = views.display_menu()

    if option == "shrink":
        controllers.shrink()
    elif option == "move":
        controllers.move()
    else:
        raise ValueError("Invalid option")


if __name__ == "__main__":
    main()
