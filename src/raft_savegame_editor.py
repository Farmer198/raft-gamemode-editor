import os
import shutil
import sys
from datetime import datetime
from typing import List, Optional

SEARCH_SEQUENZ = "47616d654d6f6465010000000776616c75655f5f000802000000"
GAME_MODES = {
    0x00: "Normal",
    0x01: "Hard",
    0x02: "Creative",
    0x03: "Easy",
    0x05: "Peaceful",
}
COLORS = {
    "red": "\033[1;31m",
    "green": "\033[1;32m",
    "blue": "\033[1;36m",
    "yellow": "\033[1;33m"
}


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def format_colored(text: str, color: str) -> str:
    return f"{COLORS.get(color)}{text}\033[0m"


def print_colored(text: str, color: str) -> None:
    print(format_colored(text, color))


def print_header() -> None:
    clear_screen()
    print_colored("┌──────────────────────────────────┐", "blue")
    print_colored("│ Raft Savegame Editor CLI         │", "blue")
    print_colored("└──────────────────────────────────┘", "blue")
    print("\n")


def list_folders(base_path: str) -> List[str]:
    folders = [
        f
        for f in os.listdir(base_path)
        if os.path.isdir(os.path.join(base_path, f))
    ]
    if not folders:
        print_colored("✗ No directories found.", "red")
        sys.exit(1)
    return folders


def find_latest_folder(world_path: str) -> str:
    latest_folders = [
        f
        for f in os.listdir(world_path)
        if f.endswith("-Latest") and os.path.isdir(os.path.join(world_path, f))
    ]
    if not latest_folders:
        print_colored("✗ No '-Latest' folder found.", "red")
        sys.exit(1)
    latest_folders.sort(reverse=True)
    return os.path.join(world_path, latest_folders[0])


def backup_save(latest_path: str) -> None:
    backup_dir = os.path.join(os.path.dirname(latest_path), "backups")
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_target = os.path.join(
        backup_dir, f"{os.path.basename(latest_path)}_{timestamp}"
    )

    shutil.copytree(latest_path, backup_target)
    print_colored(f"✓ Backup created at: {backup_target}", "green")


def read_current_gamemode(rgd_file_path: str) -> int:
    with open(rgd_file_path, "rb") as f:
        data = f.read()

    search_sequence = bytes.fromhex(SEARCH_SEQUENZ)
    idx = data.find(search_sequence)

    if idx == -1:
        print_colored("✗ Could not find GameMode sequence.", "red")
        sys.exit(1)

    value_offset = idx + len(search_sequence)
    if value_offset >= len(data):
        print_colored("✗ Invalid value offset.", "red")
        sys.exit(1)

    return data[value_offset]


def edit_gamemode(rgd_file_path: str, new_mode: int) -> None:
    with open(rgd_file_path, "rb") as f:
        data = f.read()

    search_sequence = bytes.fromhex(SEARCH_SEQUENZ)
    idx = data.find(search_sequence)

    if idx == -1:
        print_colored("✗ Could not find GameMode sequence.", "red")
        sys.exit(1)

    value_offset = idx + len(search_sequence)
    new_data = bytearray(data)
    new_data[value_offset] = new_mode

    with open(rgd_file_path, "wb") as f:
        f.write(new_data)

    print_colored(
        f"✓ Game mode updated to {GAME_MODES.get(new_mode, 'Unknown')} (0x{new_mode:02x})",
        "green"
    )


def select_option(
    prompt: str, options: List[str], return_index: bool = False
) -> str:
    while True:
        print(prompt)
        for i, option in enumerate(options, 1):
            print(f"{format_colored(f"{i}.", "yellow")} {option}")
        try:
            choice = int(input(f"\n{format_colored(f"➤ Select an option: ", "yellow")}")) - 1
            if 0 <= choice < len(options):
                return choice if return_index else options[choice]
            print_colored("✗ Invalid selection. Try again.", "red")
        except ValueError:
            print_colored("✗ Please enter a number.", "red")


def select_game_mode() -> int:
    print("\nAvailable game modes:")
    mode_options = [
        f"{name} (0x{code:02x})"
        for code, name in sorted(GAME_MODES.items(), key=lambda x: x[0])
    ]
    selected = select_option("Select a new game mode:", mode_options)
    return int(selected.split("(0x")[1][:2], 16)


def main() -> None:
    home = os.path.expanduser("~")
    raft_saves_path = os.path.join(
        home, "AppData", "LocalLow", "Redbeet Interactive", "Raft", "User"
    )

    if not os.path.exists(raft_saves_path):
        print_colored("✗ Raft save directory not found.", "red")
        sys.exit(1)

    users = list_folders(raft_saves_path)
    print_header()
    selected_user = select_option("Select a user:", users)

    worlds_path = os.path.join(raft_saves_path, selected_user, "World")
    worlds = list_folders(worlds_path)
    print_header()
    selected_world = select_option("Select a save game:", worlds)

    world_path = os.path.join(worlds_path, selected_world)
    latest_path = find_latest_folder(world_path)

    print_header()
    print_colored(f"Selected save: {selected_world} ({latest_path.split(os.sep)[-1]})", "green")

    rgd_files = [f for f in os.listdir(latest_path) if f.endswith(".rgd")]
    if not rgd_files:
        print_colored("✗ No .rgd save file found.", "red")
        sys.exit(1)

    rgd_file_path = os.path.join(latest_path, rgd_files[0])

    current_mode = read_current_gamemode(rgd_file_path)
    print(
        f"\nCurrent game mode: {
            format_colored(f"{GAME_MODES.get(current_mode, 'Unknown')} (0x{current_mode:02x})", "green")}"
    )

    backup_save(latest_path)

    new_mode = select_game_mode()
    if new_mode not in GAME_MODES:
        print_colored("⚠ Warning: Unknown game mode selected.", "yellow")

    edit_gamemode(rgd_file_path, new_mode)

    print("\n")
    print_colored("✓ Operation completed successfully!", "green")
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    # OS Check
    if os.name != "nt":  # 'nt' is the name for Windows in os.name
        print_colored("✗ This script is only compatible with Windows.", "red")
        sys.exit(1)
    try:
        main()
    except KeyboardInterrupt:
        print_colored("✗ Operation cancelled by user.", "red")
        sys.exit(1)
    except Exception as e:
        print_colored(f"✗ An error occurred: {str(e)}", "red")
        sys.exit(1)
