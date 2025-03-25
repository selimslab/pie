from youtube_transcript_api import YouTubeTranscriptApi
import logging
from pathlib import Path
import requests
import re

def get_youtube_transcript(video_id: str) -> str:
    """Get transcript for YouTube video in English or Turkish"""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'tr'])
        return '\n'.join(t['text'] for t in transcript)
    except Exception as e:
        raise ValueError(f"Failed to get transcript: {str(e)}")

def get_video_title(video_id: str) -> str:
    """Get the title of a YouTube video"""
    try:
        response = requests.get(f"https://www.youtube.com/watch?v={video_id}")
        response.raise_for_status()
        
        # Extract title from the HTML
        title_match = re.search(r'<title>(.*?) - YouTube</title>', response.text)
        if title_match:
            title = title_match.group(1)
            # Sanitize title for use as filename
            title = re.sub(r'[\\/*?:"<>|]', "", title)
            return title
        return video_id  # Fallback to video ID if title not found
    except Exception as e:
        logging.warning(f"Could not get video title: {e}")
        return video_id  # Fallback to video ID

def save_transcript(video_id: str, transcript: str, output_dir: Path = Path('transcripts')):
    """Save transcript to a text file using video title as filename"""
    output_dir.mkdir(exist_ok=True)
    
    # Get video title for filename
    title = get_video_title(video_id)
    
    # Use title for filename, but keep video ID as fallback and for reference
    filename = f"{title}_{video_id}.txt"
    output_file = output_dir / filename
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(transcript)
    
    return output_file

def process_video(video_id, output_dir=Path('transcripts')):
    """Process a single video transcript"""
    try:
        transcript = get_youtube_transcript(video_id)
        output_file = save_transcript(video_id, transcript, output_dir)
        logging.info(f"Transcript saved to: {output_file}")
        return True
    except Exception as e:
        logging.error(str(e))
        return False

def run_interactive_mode(output_dir=Path('transcripts')):
    """Run the CLI in interactive mode"""
    print("YouTube Transcript Downloader - Interactive Mode")
    print("Enter 'quit' or 'exit' to end the program")
    
    while True:
        video_id = input("\nEnter YouTube video ID: ").strip()
        
        if video_id.lower() in ['exit', 'quit', 'q']:
            print("Exiting program")
            break
            
        if not video_id:
            print("Please enter a valid video ID")
            continue
            
        process_video(video_id, output_dir)

def cli():
    """Command line interface for transcript download"""
    logging.basicConfig(level=logging.INFO)
    run_interactive_mode()

if __name__ == '__main__':
    cli() 