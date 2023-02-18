import controllers
import views


def main():
    systems = controllers.list_systems()
    selected_system = views.display_systems(systems)

    if selected_system.state != "Stopped":
        is_terminated = views.display_warning_to_terminate_system(
            selected_system
        )
        if not is_terminated:
            return

        controllers.terminate_system(selected_system)

    script_content = controllers.get_script_content(selected_system)
    views.display_script_content(script_content)
    controllers.shrink(script_content)
    views.display_shrink_ok()


if __name__ == "__main__":
    main()
