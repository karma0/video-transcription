from pathlib import Path
from .utils import format_timestamp


class SRTGenerator:
    """Generate SRT subtitle files from transcription segments."""
    
    def generate(self, segments, output_path):
        """
        Generate an SRT file from transcription segments.
        
        Args:
            segments: List of segment dictionaries from Whisper
            output_path: Path to write the SRT file
        """
        output_path = Path(output_path)
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(segments, 1):
                # Write subtitle number
                f.write(f"{i}\n")
                
                # Write timestamps
                start_time = format_timestamp(segment['start'])
                end_time = format_timestamp(segment['end'])
                f.write(f"{start_time} --> {end_time}\n")
                
                # Write text (strip to remove extra whitespace)
                text = segment['text'].strip()
                f.write(f"{text}\n")
                
                # Add blank line between subtitles (except for the last one)
                if i < len(segments):
                    f.write("\n")
    
    def generate_with_word_timestamps(self, segments, output_path, max_chars_per_line=42):
        """
        Generate an SRT file with word-level timestamps for better synchronization.
        
        Args:
            segments: List of segment dictionaries from Whisper (with word timestamps)
            output_path: Path to write the SRT file
            max_chars_per_line: Maximum characters per subtitle line
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Extract all words with timestamps
        all_words = []
        for segment in segments:
            if 'words' in segment:
                all_words.extend(segment['words'])
        
        if not all_words:
            # Fall back to regular generation if no word timestamps
            self.generate(segments, output_path)
            return
        
        # Group words into subtitle entries
        subtitles = []
        current_subtitle = {'words': [], 'start': None, 'end': None}
        current_length = 0
        
        for word in all_words:
            word_text = word['word'].strip()
            word_length = len(word_text) + 1  # +1 for space
            
            # Check if adding this word would exceed the limit
            if current_length + word_length > max_chars_per_line and current_subtitle['words']:
                # Finalize current subtitle
                current_subtitle['text'] = ' '.join(current_subtitle['words'])
                subtitles.append(current_subtitle)
                
                # Start new subtitle
                current_subtitle = {
                    'words': [word_text],
                    'start': word['start'],
                    'end': word['end']
                }
                current_length = word_length
            else:
                # Add word to current subtitle
                current_subtitle['words'].append(word_text)
                if current_subtitle['start'] is None:
                    current_subtitle['start'] = word['start']
                current_subtitle['end'] = word['end']
                current_length += word_length
        
        # Don't forget the last subtitle
        if current_subtitle['words']:
            current_subtitle['text'] = ' '.join(current_subtitle['words'])
            subtitles.append(current_subtitle)
        
        # Write SRT file
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, subtitle in enumerate(subtitles, 1):
                f.write(f"{i}\n")
                
                start_time = format_timestamp(subtitle['start'])
                end_time = format_timestamp(subtitle['end'])
                f.write(f"{start_time} --> {end_time}\n")
                
                f.write(f"{subtitle['text']}\n")
                
                if i < len(subtitles):
                    f.write("\n")