import os
import torch
import whisper
from pathlib import Path
from tqdm import tqdm
from .audio_extractor import AudioExtractor
from .srt_generator import SRTGenerator
from .utils import print_info, print_warning, print_error


class VideoTranscriber:
    """Main class for transcribing video files to SRT."""
    
    def __init__(self, model_name='base', device='auto', verbose=False):
        """
        Initialize the transcriber.
        
        Args:
            model_name: Whisper model size ('tiny', 'base', 'small', 'medium', 'large', etc.)
            device: Device to use ('cpu', 'cuda', or 'auto')
            verbose: Enable verbose output
        """
        self.model_name = model_name
        self.verbose = verbose
        
        # Determine device
        if device == 'auto':
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        else:
            self.device = device
        
        if self.verbose:
            print_info(f"Using device: {self.device}")
        
        # Initialize components
        self.audio_extractor = AudioExtractor(verbose=verbose)
        self.srt_generator = SRTGenerator()
        
        # Load Whisper model
        print_info(f"Loading Whisper model '{model_name}'...")
        self.model = whisper.load_model(model_name, device=self.device)
        print_info("Model loaded successfully")
    
    def transcribe_video(self, video_path, output_path, language=None):
        """
        Transcribe a video file and generate SRT subtitles.
        
        Args:
            video_path: Path to input video file
            output_path: Path for output SRT file
            language: Language code (optional, auto-detects if None)
        """
        video_path = Path(video_path)
        output_path = Path(output_path)
        
        # Check if video format is supported
        if not self.audio_extractor.is_format_supported(video_path):
            raise ValueError(f"Unsupported video format: {video_path.suffix}")
        
        audio_path = None
        
        try:
            # Step 1: Extract audio
            print_info("Extracting audio from video...")
            audio_path = self.audio_extractor.extract_audio(video_path)
            
            # Step 2: Transcribe audio
            print_info("Transcribing audio...")
            
            # Prepare transcription options
            options = {
                'task': 'transcribe',
                'verbose': self.verbose,
                'fp16': self.device == 'cuda',  # Use FP16 on CUDA for speed
            }
            
            if language:
                options['language'] = language
            
            # Transcribe with progress indication
            if not self.verbose:
                # For non-verbose mode, we'll use a custom progress callback
                result = self.model.transcribe(
                    str(audio_path),
                    **options
                )
            else:
                result = self.model.transcribe(
                    str(audio_path),
                    **options
                )
            
            # Display detected language if auto-detected
            if not language and 'language' in result:
                detected_lang = result['language']
                print_info(f"Detected language: {detected_lang}")
            
            # Step 3: Generate SRT file
            print_info("Generating SRT file...")
            self.srt_generator.generate(result['segments'], output_path)
            
            # Display statistics
            if self.verbose:
                print_info(f"Total segments: {len(result['segments'])}")
                if result['segments']:
                    duration = result['segments'][-1]['end']
                    print_info(f"Total duration: {duration:.2f} seconds")
            
        finally:
            # Clean up temporary audio file
            if audio_path and audio_path.exists():
                try:
                    os.unlink(audio_path)
                except Exception as e:
                    print_warning(f"Failed to delete temporary audio file: {e}")
    
    def get_supported_languages(self):
        """Get list of supported languages."""
        return whisper.tokenizer.LANGUAGES