import os
import time
from ingress import capture_stream
from processor import strip_dead_air
from transcriber import transcribe_audio

def run_scanner_pipeline():
    """Executes the complete end-to-end data pipeline."""
    print("=== STARTING ELITE SCANNER SYSTEM CORES ===")
    
    # 1. Capture the raw stream chunk (Run for 30 seconds)
    raw_file = capture_stream(duration_seconds=30)
    
    if not raw_file:
        print("Pipeline aborted: Stream capture failed.")
        return
        
    # 2. Process the audio to slice out dead air static
    cleaned_file = strip_dead_air(raw_file)
    
    # Optional cleanup: Delete the raw bulky file to save repository storage space
    if raw_file and os.path.exists(raw_file):
        os.remove(raw_file)
        print(f"Temporary file removed to conserve storage: {raw_file}")
        
    if not cleaned_file:
        print("Pipeline complete: No active audio detected to transcribe.")
        return
        
    # 3. Pass the condensed audio straight into the AI transcription ledger
    transcript = transcribe_audio(cleaned_file)
    
    if transcript:
        print(f"Pipeline Success! Decoded Message: {transcript}")
    
    print("=== SYSTEM PIPELINE CYCLE COMPLETE ===")

if __name__ == "__main__":
    # Run a single standalone cycle to verify the complete link
    run_scanner_pipeline()
