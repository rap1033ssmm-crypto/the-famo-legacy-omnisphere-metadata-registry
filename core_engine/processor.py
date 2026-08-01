import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

# CONFIGURATION: Set folders and silence sensitivity
INPUT_DIR = "audio_ingress"
OUTPUT_DIR = "cleaned_audio"

def strip_dead_air(file_path):
    """Scans an audio file, removes silence, and saves a condensed version."""
    if not os.path.exists(file_path):
        print(f"Error: Target file not found at {file_path}")
        return None
        
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print(f"Loading audio file for processing: {file_path}")
    
    try:
        # Load the raw audio chunk
        sound = AudioSegment.from_file(file_path)
        
        print("Scanning audio waves for dead air gaps...")
        # Split the audio anywhere silence is quieter than -40dB and longer than 1 second
        chunks = split_on_silence(
            sound,
            min_silence_len=1000,
            silence_thresh=-40,
            keep_silence=200 # Leave a tiny 200ms breath gap so it sounds natural
        )
        
        # If no speech was found, we don't waste system space saving empty noise
        if not chunks:
            print("No active speech detected in this transmission. Skipping save.")
            return None
            
        # Seamlessly stitch the active voice chunks together
        combined = AudioSegment.empty()
        for chunk in chunks:
            combined += chunk
            
        # Save the polished, condensed file
        base_name = os.path.basename(file_path)
        output_filename = f"{OUTPUT_DIR}/clean_{base_name}"
        combined.export(output_filename, format="mp3")
        
        print(f"Cleanup complete! Condensed audio saved to: {output_filename}")
        return output_filename
        
    except Exception as e:
        print(f"Processing error: {e}")
        return None

if __name__ == "__main__":
    # Test execution placeholder
    print("Audio Processor Engine Initialized Successfully.")
