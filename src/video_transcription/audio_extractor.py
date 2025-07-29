import ffmpeg
import tempfile
from pathlib import Path
from .utils import print_info, print_error


class AudioExtractor:
    """Extract audio from video files using ffmpeg."""
    
    SUPPORTED_FORMATS = {
        '.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', 
        '.m4v', '.mpg', '.mpeg', '.3gp', '.ogv', '.ts', '.mts'
    }
    
    def __init__(self, verbose=False):
        self.verbose = verbose
    
    def extract_audio(self, video_path):
        """
        Extract audio from video file and return path to temporary audio file.
        
        Args:
            video_path: Path to input video file
            
        Returns:
            Path to temporary audio file (WAV format)
        """
        video_path = Path(video_path)
        
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        if video_path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported video format: {video_path.suffix}")
        
        # Create temporary file for audio
        temp_audio = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        temp_audio_path = temp_audio.name
        temp_audio.close()
        
        if self.verbose:
            print_info(f"Extracting audio to: {temp_audio_path}")
        
        try:
            # Extract audio using ffmpeg
            stream = ffmpeg.input(str(video_path))
            stream = ffmpeg.output(stream, temp_audio_path, 
                                 acodec='pcm_s16le',  # WAV format
                                 ac=1,  # Mono
                                 ar='16k')  # 16kHz sample rate (optimal for Whisper)
            
            if not self.verbose:
                stream = ffmpeg.overwrite_output(stream)
                ffmpeg.run(stream, quiet=True)
            else:
                stream = ffmpeg.overwrite_output(stream)
                ffmpeg.run(stream)
            
            return Path(temp_audio_path)
            
        except ffmpeg.Error as e:
            print_error(f"FFmpeg error: {e.stderr.decode() if e.stderr else 'Unknown error'}")
            raise
        except Exception as e:
            print_error(f"Error extracting audio: {str(e)}")
            raise
    
    @classmethod
    def is_format_supported(cls, file_path):
        """Check if the video format is supported."""
        return Path(file_path).suffix.lower() in cls.SUPPORTED_FORMATS