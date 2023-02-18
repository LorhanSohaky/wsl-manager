from typing import List

from models import System


def display_systems(systems: List[System]) -> System:
    selected_option = None
    while selected_option is None:
        print("All systems:")
        for number, system in enumerate(systems, 1):
            print(f"[{number}] {system.name} ({system.state})")

        selected_option = input(
            "Insert the number of the system you want to select: "
        )

        is_not_a_number = not selected_option.isdigit()
        is_out_of_range = (
            int(selected_option) > len(systems) or int(selected_option) < 1
        )
        if is_not_a_number or is_out_of_range:
            print("Invalid option")
            selected_option = None
            continue

        selected_option = int(selected_option)

    return systems[selected_option - 1]


def display_warning_to_terminate_system(system: System) -> bool:
    is_valid_confirmation = False
    while is_valid_confirmation is False:
        print(
            "This system is not terminated. To continue, you must"
            " terminate it."
        )
        print(f"Are you sure you want to terminate {system.name}? (y/n)")

        confirmation = input("Confirmation: ").lower()
        is_valid_confirmation = confirmation in ["yes", "y", "no", "n"]
        if not is_valid_confirmation:
            print("Invalid confirmation")
            continue

        if confirmation not in ["yes", "y"]:
            print("Termination cancelled")
            return False

    return True
