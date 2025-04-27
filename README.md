# Raft Gamemode Editor CLI

A command-line tool to edit the game mode in your Raft save files. This script allows you to select a save game, back it up, and change the game mode (e.g., Normal, Hard, Creative, etc.) with an easy-to-use CLI interface.

## Features

- **Backup Saves**: Automatically creates a backup of your save game before making changes.
- **Game Mode Editor**: Change the game mode for your Raft world.

## Requirements

- **Python 3.x**: This script is written in Python and requires Python 3.x to run.
- **Raft Save Files**: You need to have the Raft game installed and save files accessible on your computer.

## Installation

1. **Download the Script**: Download the `raft_savegame_editor.py` script to your local machine.
2. **Run the Script**: You can run the script from your terminal using Python.

   ```
   python raft_savegame_editor.py
   ```

## Usage

When you run the script, it will guide you through the following steps:

1. **Select a User**: The script will show a list of available users in your Raft save directory.
2. **Select a Save Game**: After selecting a user, you will be prompted to choose a save game (world).
3. **Backup Your Save**: The script will create a backup of the selected save game before making any changes.
4. **Select a Game Mode**: The available game modes are listed, and you can select a new game mode for the save game.
5. **Game Mode Update**: After selecting a new game mode, the script will update the save file and display a confirmation message.

### Available Game Modes:

- **Normal (0x00)**: Standard game mode.
- **Hard (0x01)**: A more challenging mode.
- **Creative (0x02)**: Unlimited resources and no survival needs.
- **Easy (0x03)**: Easier gameplay, with some advantages.
- **Peaceful (0x05)**: Enemies are disabled, peaceful gameplay.
