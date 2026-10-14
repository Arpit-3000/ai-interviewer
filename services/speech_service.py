"""
Speech-to-Text and Text-to-Speech Service
Using Whisper (via Groq) for STT and gTTS/ElevenLabs for TTS
"""
import os
from typing import Optional
import tempfile
from dotenv import load_dotenv

load_dotenv()

class SpeechService:
    """
    Handle voice interactions
    Note: This requires additional packages:
    - openai-whisper (for STT)
    - gtts or elevenlabs (for TTS)
    """
    
    def __init__(self):
        self.stt_enabled = False
        self.tts_enabled = False
        
        # Speech-to-text runs on Groq's hosted Whisper (same GROQ_API_KEY as the interviewer), so nothing heavy is installed
        try:
            from groq import Groq
            self.groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
            self.stt_enabled = bool(os.getenv("GROQ_API_KEY"))
        except ImportError:
            print("Warning: groq package not available. Install with: pip install groq")
        
        try:
            from gtts import gTTS
            self.tts_engine = gTTS
            self.tts_enabled = True
        except ImportError:
            print("Warning: gTTS not available. Install with: pip install gtts")
    
    def speech_to_text(self, audio_file_path: str) -> str:
        """Convert audio to text using Whisper on Groq"""
        if not self.stt_enabled:
            raise Exception("Speech-to-text not available. Set GROQ_API_KEY and install groq.")
        
        try:
            with open(audio_file_path, "rb") as f:
                result = self.groq.audio.transcriptions.create(
                    file=(os.path.basename(audio_file_path), f.read()),
                    model="whisper-large-v3-turbo",
                    language="en",
                    temperature=0,
                )
            return (result.text or "").strip()
        except Exception as e:
            raise Exception(f"Speech-to-text error: {str(e)}")
    
    def text_to_speech(self, text: str, output_path: Optional[str] = None) -> str:
        """Convert text to speech using gTTS"""
        if not self.tts_enabled:
            raise Exception("Text-to-speech not available. Install gtts.")
        
        try:
            if output_path is None:
                output_path = tempfile.mktemp(suffix=".mp3")
            
            tts = self.tts_engine(text=text, lang='en', slow=False)
            tts.save(output_path)
            return output_path
        except Exception as e:
            raise Exception(f"Text-to-speech error: {str(e)}")

# Global instance
speech_service = SpeechService()
