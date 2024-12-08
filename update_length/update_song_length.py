import json
import subprocess
import os
import sys
from utils import resource_path


def update_song_length(gtaiv_dir, radio, song, new_length):
    """Update song length in the specified .dat15 file."""
    ivam_path = resource_path("ivam.exe")
    dat15_file = os.path.join(gtaiv_dir, "pc", "audio", "config", "sounds.dat15")
    dat15_dir = os.path.dirname(dat15_file)
    json_file = "sounds.dat15.json"
    backup_file = "sounds.dat15_backup"

    print("Converting dat15 to JSON...")
    if not os.path.exists(dat15_file):
        raise FileNotFoundError(f"Error: {dat15_file} not found in {gtaiv_dir}")

    original_cwd = os.getcwd()
    os.chdir(dat15_dir)
    try:
        print(f"Using ivam.exe from: {ivam_path}")
        subprocess.run([ivam_path, "sounds.dat15"], check=True)

        if not os.path.exists(json_file):
            raise FileNotFoundError(f"Error: {json_file} was not generated after conversion.")

        with open(json_file, "r") as f:
            data = json.load(f)

        entry_name = f"{radio.upper()}_{song.upper()}"
        if entry_name in data:
            print(f"Found entry: {entry_name}")
            data[entry_name]["Metadata"]["__field00"] = new_length
            print(f"Updated {entry_name}.Metadata.__field00 to {new_length} milliseconds.")
        else:
            print(f"Entry {entry_name} not found in {json_file}.")
            return

        with open(json_file, "w") as f:
            json.dump(data, f, indent=4)

        print("Converting JSON back to dat15...")
        subprocess.run([ivam_path, "gen"], check=True)

        if os.path.exists(backup_file):
            print(f"Replacing existing backup: {backup_file}")
            os.remove(backup_file)

        os.rename("sounds.dat15", backup_file)
        os.rename("sounds.dat15.gen", "sounds.dat15")
        print(f"Backup created: {backup_file}")
        print("Update complete!")
    finally:
        os.chdir(original_cwd)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python update_song_length.py <gtaiv_dir> <radio> <song> <new_millisecond_value>")
        sys.exit(1)

    gtaiv_dir = sys.argv[1]
    radio = sys.argv[2]
    song = sys.argv[3]
    try:
        new_length = int(sys.argv[4])
    except ValueError:
        print("Error: <new_millisecond_value> must be an integer.")
        sys.exit(1)

    update_song_length(gtaiv_dir, radio, song, new_length)
