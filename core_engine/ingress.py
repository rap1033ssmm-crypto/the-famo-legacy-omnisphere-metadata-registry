import os
import requests
from datetime import datetime

# CONFIGURATION: Direct high-performance audio stream pipe
STREAM_URL = "https://icecast.walmradio.com:8000/classic"
OUTPUT_DIR = "audio_ingress"

def capture_stream(duration_seconds=30):
    """Connects to the audio stream and captures a chunk of raw data."""
    # Ensure the ingress folder exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    # Generate a unique timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{OUTPUT_DIR}/stream_{timestamp}.mp3"
    
    print(f"Connecting to stream engine at: {STREAM_URL}")
    
    try:
        # Open a continuous data pipeline to the stream
        with requests.get(STREAM_URL, stream=True, timeout=10) as r:
            r.raise_for_status()
            print(f"Connection locked. Capturing {duration_seconds} seconds of audio...")
            
            # Write the streaming chunks straight to our file
            with open(filename, 'wb') as f:
                start_time = datetime.now()
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                    
                    # Stop writing once our duration target is hit
                    elapsed = (datetime.now() - start_time).total_seconds()
                    if elapsed >= duration_seconds:
                        break
                        
        print(f"Capture successful! Chunk saved to: {filename}")
        return filename
        
    except Exception as e:
        print(f"Connection error: {e}")
        return None

if __name__ == "__main__":
    capture_stream()
