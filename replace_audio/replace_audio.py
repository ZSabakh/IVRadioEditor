import json
import subprocess
import os
import sys
from pydub import AudioSegment
from utils import resource_path


def process_audio(track_name, new_audio_file):
    """Process audio to generate a game-compatible WAV file."""
    output_wav = f"{track_name}.wav"

    audio = AudioSegment.from_file(new_audio_file)

    processed_audio = audio  # + silence

    print(f"Generating WAV for {track_name}...")
    processed_audio.export(output_wav, format="wav", parameters=["-ar", "32000", "-ac", "2"])

    print(f"WAV file generated: {output_wav}")
    return output_wav


def modify_oaf_file(oaf_file, track_name, new_audio_duration):
    """Modify the .oaf file to update DJ timestamps and ensure correct channel relationships."""
    with open(oaf_file, "r") as f:
        oaf_data = json.load(f)

    outro_start = int(new_audio_duration - 7000) 
    outro_end = int(new_audio_duration - 1000) 

    oaf_data["timestamps"][2]["time"] = max(0, outro_start)
    oaf_data["timestamps"][3]["time"] = max(0, outro_end)

    for ts in oaf_data["timestamps"]:
        ts["time"] = int(ts["time"])

    base_track_name = os.path.basename(track_name)

    # Fix channels relationships
    oaf_data["channels"] = [
        {
            "name": f"{base_track_name}_LEFT",
            "compression": "ADPCM",
            "headroom": 136
        },
        {
            "name": f"{base_track_name}_RIGHT",
            "compression": "ADPCM",
            "headroom": 136
        }
    ]

    updated_oaf_file = f"{track_name}.oaf"
    with open(updated_oaf_file, "w") as f:
        json.dump(oaf_data, f, indent=4)

    print(f"Updated .oaf file: {updated_oaf_file}")
    return updated_oaf_file


def convert_back_to_special_audio(track_name):
    """Convert .oaf and .wav files back into a single special audio file."""
    iv_audio_conv_path = resource_path("IVAudioConv.exe")

    oaf_file = f"{track_name}.oaf"
    wav_file = f"{track_name}.wav"

    print(f"Using IVAudioConv.exe from: {iv_audio_conv_path}")
    print(f"Using .oaf file: {oaf_file}")
    print(f"Using .wav file: {wav_file}")

    if not os.path.exists(oaf_file):
        raise FileNotFoundError(f"Error: {oaf_file} not found.")
    if not os.path.exists(wav_file):
        raise FileNotFoundError(f"Error: {wav_file} not found.")

    print(f"Converting updated files back into special audio format for {track_name}...")
    subprocess.run([iv_audio_conv_path, oaf_file, wav_file], check=True)
    special_audio_file = track_name
    print(f"Special audio file created: {special_audio_file}")
    return special_audio_file


def replace_special_audio(original_audio, new_audio_file):
    """Main function to replace special audio file with custom audio."""
    iv_audio_conv_path = resource_path("IVAudioConv.exe")

    print(f"Extracting .oaf and .wav from {original_audio}...")
    subprocess.run([iv_audio_conv_path, original_audio], check=True)
    oaf_file = f"{original_audio}.oaf"
    wav_file = f"{original_audio}.wav"

    new_wav = process_audio(original_audio, new_audio_file)

    new_audio_duration = int(AudioSegment.from_file(new_audio_file).duration_seconds * 1000)

    updated_oaf = modify_oaf_file(oaf_file, original_audio, new_audio_duration)

    os.replace(new_wav, wav_file)
    print(f"Replaced {wav_file} with updated audio.")

    special_audio_file = convert_back_to_special_audio(original_audio)

    print(f"Replacement complete! New file: {special_audio_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python replace_audio.py <original_audio_file> <new_audio_file>")
        sys.exit(1)

    original_audio = sys.argv[1]
    new_audio_file = sys.argv[2]

    replace_special_audio(original_audio, new_audio_file)
