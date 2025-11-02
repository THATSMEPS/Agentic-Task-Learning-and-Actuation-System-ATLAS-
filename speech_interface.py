# speech_interface.py
"""
Speech Interface Module for ATLAS Robot
Handles speech recognition (voice input) and text-to-speech (voice output)
"""

import time

class SpeechRecognizer:
    """Handles speech-to-text conversion for voice commands."""
    
    def __init__(self):
        """
        Initialize speech recognizer.
        
        Hardware Setup (when connected):
        - USB microphone connected to Raspberry Pi or laptop
        - Supported libraries: speech_recognition (using Google Speech API)
        """
        self.is_listening = False
        self.recognizer = None
        self.microphone = None
        
        print("[SPEECH] - Speech Recognizer initialized")
        
    def initialize_hardware(self):
        """
        Initialize speech recognition hardware and libraries.
        
        When hardware is connected, this will:
        - Import speech_recognition library
        - Initialize microphone
        - Set up ambient noise adjustment
        """
        try:
            # TODO: Uncomment when speech_recognition is installed
            # import speech_recognition as sr
            # self.recognizer = sr.Recognizer()
            # self.microphone = sr.Microphone()
            
            # Adjust for ambient noise
            # with self.microphone as source:
            #     print("[SPEECH] - Calibrating for ambient noise... Please wait.")
            #     self.recognizer.adjust_for_ambient_noise(source, duration=2)
            
            print("[MOCK HARDWARE] - Microphone initialized and calibrated")
            return True
            
        except Exception as e:
            print(f"[SPEECH] - ERROR initializing speech recognition: {e}")
            return False
            
    def listen_for_wake_word(self, wake_word="atlas", timeout=10):
        """
        Listen for the wake word to activate the robot.
        
        Args:
            wake_word: The word that activates the robot (default: "atlas")
            timeout: Maximum time to listen in seconds
            
        Returns:
            True if wake word detected, False otherwise
        """
        print(f"[SPEECH] - Listening for wake word '{wake_word}'...")
        
        # TODO: Implement actual speech recognition
        # try:
        #     with self.microphone as source:
        #         audio = self.recognizer.listen(source, timeout=timeout)
        #         text = self.recognizer.recognize_google(audio).lower()
        #         
        #         if wake_word in text:
        #             print(f"[SPEECH] - Wake word '{wake_word}' detected!")
        #             return True
        # except Exception as e:
        #     print(f"[SPEECH] - Error: {e}")
        
        # Simulation: Return True after timeout
        print("[MOCK HARDWARE] - Simulating wake word detection...")
        time.sleep(1)
        return True
        
    def listen_for_command(self, timeout=10):
        """
        Listen for a voice command after wake word is detected.
        
        Args:
            timeout: Maximum time to listen in seconds
            
        Returns:
            The recognized text command, or None if failed
        """
        print("[SPEECH] - Listening for command...")
        
        # TODO: Implement actual speech recognition
        # try:
        #     with self.microphone as source:
        #         audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
        #         
        #     print("[SPEECH] - Processing audio...")
        #     command = self.recognizer.recognize_google(audio)
        #     print(f"[SPEECH] - Recognized: '{command}'")
        #     return command
        #     
        # except sr.UnknownValueError:
        #     print("[SPEECH] - Could not understand audio")
        #     return None
        # except sr.RequestError as e:
        #     print(f"[SPEECH] - API error: {e}")
        #     return None
        # except Exception as e:
        #     print(f"[SPEECH] - Error: {e}")
        #     return None
        
        # Simulation: Use text input
        command = input("[MOCK HARDWARE] - Enter voice command: ")
        print(f"[SPEECH] - Recognized: '{command}'")
        return command
        
    def listen_continuous(self, callback_function, wake_word="atlas"):
        """
        Continuously listen for wake word and commands.
        
        Args:
            callback_function: Function to call with recognized command
            wake_word: Wake word to listen for
        """
        print(f"[SPEECH] - Starting continuous listening mode...")
        print(f"[SPEECH] - Say '{wake_word}' followed by your command")
        
        while True:
            try:
                # Wait for wake word
                if self.listen_for_wake_word(wake_word):
                    # Wake word detected, listen for command
                    command = self.listen_for_command()
                    
                    if command:
                        # Call the callback function with the command
                        callback_function(command)
                    else:
                        print("[SPEECH] - No command received, returning to listening mode")
                        
            except KeyboardInterrupt:
                print("\n[SPEECH] - Stopping continuous listening")
                break
            except Exception as e:
                print(f"[SPEECH] - Error in continuous listening: {e}")
                time.sleep(1)


class TextToSpeech:
    """Handles text-to-speech conversion for robot responses."""
    
    def __init__(self):
        """
        Initialize text-to-speech engine.
        
        Hardware Setup (when connected):
        - Speaker or headphones connected to Raspberry Pi
        - Supported libraries: pyttsx3 (offline) or gTTS (online)
        """
        self.engine = None
        self.use_offline = True  # Use offline TTS by default
        
        print("[TTS] - Text-to-Speech initialized")
        
    def initialize_hardware(self):
        """
        Initialize TTS engine.
        
        When hardware is connected, this will:
        - Import pyttsx3 or gTTS library
        - Initialize TTS engine
        - Configure voice properties
        """
        try:
            # TODO: Uncomment when pyttsx3 is installed
            # import pyttsx3
            # self.engine = pyttsx3.init()
            # 
            # # Set voice properties
            # self.engine.setProperty('rate', 150)  # Speed
            # self.engine.setProperty('volume', 0.9)  # Volume
            
            print("[MOCK HARDWARE] - TTS engine initialized")
            return True
            
        except Exception as e:
            print(f"[TTS] - ERROR initializing TTS: {e}")
            return False
            
    def speak(self, text):
        """
        Convert text to speech and play it.
        
        Args:
            text: The text to speak
        """
        print(f"[TTS] - Speaking: '{text}'")
        
        # TODO: Implement actual TTS
        # if self.engine:
        #     self.engine.say(text)
        #     self.engine.runAndWait()
        # else:
        #     # Fallback to gTTS (requires internet)
        #     from gtts import gTTS
        #     import os
        #     
        #     tts = gTTS(text=text, lang='en')
        #     tts.save("temp_speech.mp3")
        #     os.system("mpg321 temp_speech.mp3")  # Linux
        #     os.remove("temp_speech.mp3")
        
        # Simulation: Just print
        print(f"[MOCK HARDWARE] - Audio output: '{text}'")
        time.sleep(len(text) * 0.05)  # Simulate speaking time
        
    def speak_async(self, text):
        """
        Convert text to speech without blocking.
        Useful for speaking while robot is moving.
        
        Args:
            text: The text to speak
        """
        print(f"[TTS] - Speaking (async): '{text}'")
        # TODO: Implement with threading
        # import threading
        # thread = threading.Thread(target=self.speak, args=(text,))
        # thread.start()
        self.speak(text)


class VoiceInterface:
    """Combined interface for speech recognition and text-to-speech."""
    
    def __init__(self):
        """Initialize complete voice interface."""
        self.speech_recognizer = SpeechRecognizer()
        self.tts = TextToSpeech()
        
        print("[VOICE] - Voice Interface initialized")
        
    def initialize(self):
        """Initialize all voice hardware."""
        print("[VOICE] - Initializing voice interface...")
        
        speech_ok = self.speech_recognizer.initialize_hardware()
        tts_ok = self.tts.initialize_hardware()
        
        if speech_ok and tts_ok:
            print("[VOICE] - Voice interface ready!")
            self.tts.speak("Voice interface initialized. I am ready.")
            return True
        else:
            print("[VOICE] - Voice interface initialization failed!")
            return False
            
    def get_voice_command(self, wake_word="atlas"):
        """
        Listen for wake word, then get command.
        
        Args:
            wake_word: Wake word to activate listening
            
        Returns:
            Command text or None
        """
        if self.speech_recognizer.listen_for_wake_word(wake_word):
            self.tts.speak("Yes, I'm listening")
            return self.speech_recognizer.listen_for_command()
        return None
        
    def respond(self, text, async_speech=False):
        """
        Respond with speech.
        
        Args:
            text: Text to speak
            async_speech: If True, don't wait for speech to complete
        """
        if async_speech:
            self.tts.speak_async(text)
        else:
            self.tts.speak(text)


# --- To test this script directly ---
if __name__ == "__main__":
    print("=== Testing Speech Interface ===\n")
    
    voice = VoiceInterface()
    voice.initialize()
    
    print("\n--- Test 1: Basic TTS ---")
    voice.tts.speak("Hello, I am ATLAS, your robotic assistant.")
    
    print("\n--- Test 2: Wake Word Detection ---")
    if voice.speech_recognizer.listen_for_wake_word("atlas"):
        print("SUCCESS: Wake word detected!")
        
    print("\n--- Test 3: Command Recognition ---")
    command = voice.speech_recognizer.listen_for_command()
    if command:
        print(f"SUCCESS: Command received: '{command}'")
        voice.tts.speak(f"I heard you say: {command}")
    
    print("\n--- Test 4: Complete Voice Interaction ---")
    voice.respond("I am ready for your command")
    command = voice.get_voice_command("atlas")
    if command:
        voice.respond(f"I will execute: {command}")
    
    print("\n=== Speech Interface Test Complete ===")
