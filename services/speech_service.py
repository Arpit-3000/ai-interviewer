"""
Speech-to-Text and Text-to-Speech Service
Using OpenAI Whisper for STT and gTTS/ElevenLabs for TTS
"""
import os
from typing import Optional
import tempfile

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
        
        try:
            # Try to import speech libraries
            import whisper
            self.whisper_model = whisper.load_model("base")
            self.stt_enabled = True
        except ImportError:
            print("Warning: Whisper not available. Install with: pip install openai-whisper")
        
        try:
            from gtts import gTTS
            self.tts_engine = gTTS
            self.tts_enabled = True
        except ImportError:
            print("Warning: gTTS not available. Install with: pip install gtts")
    
    def speech_to_text(self, audio_file_path: str) -> str:
        """Convert audio to text using Whisper"""
        if not self.stt_enabled:
            raise Exception("Speech-to-text not available. Install openai-whisper.")
        
        try:
            result = self.whisper_model.transcribe(audio_file_path)
            return result["text"]
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
