#!/usr/bin/env python3
"""
VoiceMeet-Sum - A desktop application for transcribing video/audio files using OpenAI Whisper API
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import os
import threading
import subprocess
import requests
from pathlib import Path

class VoiceMeetSumApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VoiceMeet-Sum")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Configuration
        self.config_file = "config.json"
        self.api_key = ""
        self.selected_file = None
        self.transcription_text = ""
        
        # Load saved API key if exists
        self.load_config()
        
        # Setup GUI
        self.setup_gui()
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def load_config(self):
        """Load API key from config.json if it exists"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.api_key = config.get('api_key', '')
            except Exception as e:
                print(f"Error loading config: {e}")
    
    def save_config(self):
        """Save API key to config.json"""
        try:
            config = {'api_key': self.api_key}
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def setup_gui(self):
        """Setup the GUI components"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # API Key section
        ttk.Label(main_frame, text="OpenAI API Key:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.api_key_entry = ttk.Entry(main_frame, width=50, show="*")
        self.api_key_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        if self.api_key:
            self.api_key_entry.insert(0, self.api_key)
        
        # File selection section
        ttk.Label(main_frame, text="Video/Audio File:").grid(row=1, column=0, sticky=tk.W, pady=5)
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        file_frame.columnconfigure(0, weight=1)
        
        self.file_label = ttk.Label(file_frame, text="No file selected", foreground="gray")
        self.file_label.grid(row=0, column=0, sticky=tk.W)
        
        browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_btn.grid(row=0, column=1, padx=5)
        
        # Buttons section
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.transcribe_btn = ttk.Button(button_frame, text="Start Transcription", 
                                         command=self.start_transcription, state=tk.DISABLED)
        self.transcribe_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_btn = ttk.Button(button_frame, text="Save as .txt", 
                                  command=self.save_transcription, state=tk.DISABLED)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress and output section
        ttk.Label(main_frame, text="Progress & Output:").grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=20)
        self.output_text.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Status bar
        self.status_label = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
    
    def browse_file(self):
        """Open file dialog to select video/audio file"""
        filetypes = [
            ("Video files", "*.mp4 *.mov *.mkv *.avi"),
            ("Audio files", "*.mp3 *.wav *.m4a *.flac"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Video or Audio File",
            filetypes=filetypes
        )
        
        if filename:
            self.selected_file = filename
            self.file_label.config(text=os.path.basename(filename), foreground="black")
            self.transcribe_btn.config(state=tk.NORMAL)
            self.log_output(f"Selected file: {os.path.basename(filename)}\n")
    
    def log_output(self, message):
        """Add message to output text widget"""
        self.output_text.insert(tk.END, message)
        self.output_text.see(tk.END)
        self.root.update()
    
    def update_status(self, message):
        """Update status bar"""
        self.status_label.config(text=message)
        self.root.update()
    
    def validate_api_key(self):
        """Validate OpenAI API key by calling the models endpoint"""
        api_key = self.api_key_entry.get().strip()
        if not api_key:
            messagebox.showerror("Error", "Please enter your OpenAI API key")
            return False
        
        self.update_status("Validating API key...")
        self.log_output("Validating API key...\n")
        
        try:
            headers = {
                "Authorization": f"Bearer {api_key}"
            }
            response = requests.get("https://api.openai.com/v1/models", headers=headers, timeout=10)
            
            if response.status_code == 200:
                self.log_output("API key validated successfully!\n\n")
                self.api_key = api_key
                return True
            else:
                messagebox.showerror("Error", f"Invalid API key. Status code: {response.status_code}")
                self.log_output(f"API key validation failed: {response.status_code}\n")
                return False
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Network error: {str(e)}")
            self.log_output(f"Network error: {str(e)}\n")
            return False
    
    def check_ffmpeg(self):
        """Check if FFmpeg is installed"""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def check_cuda(self):
        """Check if CUDA is available for GPU acceleration"""
        try:
            result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def extract_audio(self, input_file, output_file):
        """Extract audio from video file using FFmpeg"""
        self.log_output("Extracting audio from video...\n")
        self.update_status("Extracting audio...")
        
        # Check if FFmpeg is available
        if not self.check_ffmpeg():
            raise Exception("FFmpeg is not installed. Please install FFmpeg to use this feature.")
        
        # Check for CUDA support
        cuda_available = self.check_cuda()
        
        # Build FFmpeg command
        cmd = ['ffmpeg', '-i', input_file]
        
        # Add GPU acceleration if CUDA is available
        if cuda_available:
            cmd.extend(['-hwaccel', 'cuda'])
            self.log_output("Using GPU acceleration (CUDA)...\n")
        
        # Extract audio as MP3
        cmd.extend(['-vn', '-acodec', 'libmp3lame', '-ar', '16000', '-ac', '1', '-y', output_file])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            self.log_output("Audio extraction completed!\n\n")
            return True
        except subprocess.CalledProcessError as e:
            raise Exception(f"FFmpeg error: {e.stderr}")
    
    def transcribe_audio(self, audio_file):
        """Send audio file to OpenAI Whisper API for transcription"""
        self.log_output("Sending audio to OpenAI Whisper API...\n")
        self.update_status("Transcribing audio...")
        
        url = "https://api.openai.com/v1/audio/transcriptions"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        with open(audio_file, 'rb') as audio:
            files = {
                'file': (os.path.basename(audio_file), audio, 'audio/mpeg')
            }
            data = {
                'model': 'whisper-1',
                'language': 'en'  # Optional: specify language
            }
            
            try:
                response = requests.post(url, headers=headers, files=files, data=data, timeout=300)
                
                if response.status_code == 200:
                    result = response.json()
                    self.transcription_text = result.get('text', '')
                    self.log_output("Transcription completed!\n\n")
                    self.log_output("=" * 50 + "\n")
                    self.log_output("TRANSCRIPTION:\n")
                    self.log_output("=" * 50 + "\n\n")
                    self.log_output(self.transcription_text + "\n\n")
                    self.log_output("=" * 50 + "\n")
                    return True
                else:
                    raise Exception(f"API error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                raise Exception(f"Network error: {str(e)}")
    
    def start_transcription(self):
        """Start the transcription process in a separate thread"""
        # Disable buttons during processing
        self.transcribe_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)
        
        # Clear previous output
        self.output_text.delete(1.0, tk.END)
        
        # Validate API key
        if not self.validate_api_key():
            self.transcribe_btn.config(state=tk.NORMAL)
            return
        
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a video or audio file")
            self.transcribe_btn.config(state=tk.NORMAL)
            return
        
        # Run transcription in a separate thread
        thread = threading.Thread(target=self.transcription_worker)
        thread.daemon = True
        thread.start()
    
    def transcription_worker(self):
        """Worker function to run transcription in background thread"""
        try:
            input_file = self.selected_file
            file_ext = Path(input_file).suffix.lower()
            
            # Check if file is already an audio file
            audio_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.ogg']
            is_audio_file = file_ext in audio_extensions
            
            if is_audio_file:
                self.log_output("File is already an audio file, skipping extraction...\n\n")
                audio_file = input_file
            else:
                # Extract audio from video
                audio_file = "temp_audio.mp3"
                self.extract_audio(input_file, audio_file)
            
            # Transcribe audio
            self.transcribe_audio(audio_file)
            
            # Clean up temporary audio file
            if not is_audio_file and os.path.exists(audio_file):
                os.remove(audio_file)
                self.log_output("\nTemporary audio file removed.\n")
            
            self.update_status("Transcription completed successfully!")
            self.save_btn.config(state=tk.NORMAL)
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.log_output(f"\n{error_msg}\n")
            self.update_status("Error occurred")
            messagebox.showerror("Error", error_msg)
        
        finally:
            self.transcribe_btn.config(state=tk.NORMAL)
    
    def save_transcription(self):
        """Save transcription to a text file"""
        if not self.transcription_text:
            messagebox.showwarning("Warning", "No transcription to save")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save Transcription",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.transcription_text)
                messagebox.showinfo("Success", f"Transcription saved to {filename}")
                self.log_output(f"\nTranscription saved to: {filename}\n")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def on_closing(self):
        """Handle window close event"""
        if self.api_key:
            result = messagebox.askyesno("Save API Key", "Do you want to save your API key for next time?")
            if result:
                self.save_config()
        self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = VoiceMeetSumApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

