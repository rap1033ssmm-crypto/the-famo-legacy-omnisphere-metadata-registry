import os
import whisper
from datetime import datetime

# CONFIGURATION: Set folders and ledger path
INPUT_DIR = "cleaned_audio"
LEDGER_DIR = "transcripts_ledger"

def transcribe_audio(file_path):
    """Uses Whisper AI to transcribe audio and appends it to our permanent text ledger."""
    if not os.path.exists(file_path):
        print(f"Error: Target file not found at {file_path}")
        return None
        
    if not os.path.exists(LEDGER_DIR):
        os.makedirs(LEDGER_DIR)
        
    print(f"Initializing AI transcription engine for: {file_path}")
    
    try:
        # Load the highly optimized Whisper transcription model
        model = whisper.load_model("tiny") # 'tiny' is fast, efficient, and perfect for clear radio speech
        
        # Run the audio through the AI engine
        result = model.transcribe(file_path, fp16=False)
        transcript_text = result.get("text", "").strip()
        
        # If the audio had no recognizable words, don't write blank space to the ledger
        if not transcript_text:
            print("No speech text recognized in this audio clip.")
            return None
            
        # Structure the ledger entry with a clean markdown layout
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        base_name = os.path.basename(file_path)
        
        ledger_file = f"{LEDGER_DIR}/system_chatter_log.md"
        
        # Append the new transcript to our continuous markdown ledger
        with open(ledger_file, "a") as f:
            f.write(f"### [SIGNAL RECORDED: {timestamp}]\n")
            f.write(f"* **Source File**: `{base_name}`\n")
            f.write(f"* **Decoded Text**: \"{transcript_text}\"\n\n")
            f.write("---\n\n")
            
        print(f"Transcription successful! Logged to ledger: {ledger_file}")
        return transcript_text
        
    except Exception as e:
        print(f"Transcription engine error: {e}")
        return None

if __name__ == "__main__":
    print("AI Transcriber Engine Initialized Successfully.")
