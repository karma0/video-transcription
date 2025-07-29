#!/usr/bin/env python3
import click
from pathlib import Path
import whisper
from .transcriber import VideoTranscriber
from .utils import print_info, print_error, print_success


@click.command()
@click.argument('input_video', type=click.Path(exists=True, path_type=Path))
@click.option('--output', '-o', type=click.Path(path_type=Path), 
              help='Output SRT file path (default: same as input with .srt extension)')
@click.option('--model', '-m', 
              type=click.Choice(['tiny', 'base', 'small', 'medium', 'large', 'large-v2', 'large-v3']),
              default='base',
              help='Whisper model size (default: base)')
@click.option('--language', '-l', default=None,
              help='Language code (e.g., en, es, fr). If not specified, auto-detects.')
@click.option('--device', '-d', 
              type=click.Choice(['cpu', 'cuda', 'auto']),
              default='auto',
              help='Device to use for inference (default: auto)')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
def cli(input_video, output, model, language, device, verbose):
    """Generate SRT subtitles from video files using OpenAI Whisper."""
    
    if output is None:
        output = input_video.with_suffix('.srt')
    
    print_info(f"Input video: {input_video}")
    print_info(f"Output SRT: {output}")
    print_info(f"Model: {model}")
    
    if language:
        print_info(f"Language: {language}")
    else:
        print_info("Language: Auto-detect")
    
    try:
        transcriber = VideoTranscriber(model_name=model, device=device, verbose=verbose)
        transcriber.transcribe_video(input_video, output, language=language)
        print_success(f"Successfully generated subtitles: {output}")
        
    except Exception as e:
        print_error(f"Error: {str(e)}")
        raise click.Abort()


if __name__ == '__main__':
    cli()