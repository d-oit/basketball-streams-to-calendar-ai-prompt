import os
import asyncio
import logging
from datetime import datetime
from pathlib import Path
import tempfile
from typing import Optional
from dotenv import load_dotenv

# Third-party imports
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import cv2
import pytesseract
import pyttsx3
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
from mistralai.models.chat_completion import ChatMessage

# Load environment variables from .env file
load_dotenv()

# Constants
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Constants
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
VIDEO_DIMENSIONS = {'width': 1280, 'height': 720}
SPEECH_RATE = 150
SPEECH_VOLUME = 0.9

class VideoProcessingError(Exception):
    """Custom exception for video processing errors"""
    pass

def setup_environment():
    """Set up necessary directories and configurations"""
    try:
        # Set Tesseract path
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

        # Create necessary directories
        directories = ['videos', 'output', 'audio', 'temp']
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)

        logger.info("Environment setup completed")
    except Exception as e:
        logger.error(f"Environment setup failed: {str(e)}")
        raise VideoProcessingError(f"Setup error: {str(e)}")

def get_unique_filename(base_path: str, extension: str) -> str:
    """Generate a unique filename using timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return str(Path(base_path).parent / f"{Path(base_path).stem}_{timestamp}{extension}")

def test_tts_engine():
    """Test if TTS engine is working properly"""
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        logger.info(f"Available voices: {len(voices)}")
        for voice in voices:
            logger.info(f"Voice: {voice.name} ({voice.id})")
        return True
    except Exception as e:
        logger.error(f"TTS engine test failed: {str(e)}")
        return False

def extract_text_from_video(video_path: str) -> str:
    """Extract text from video frames using OCR"""
    try:
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        cap = cv2.VideoCapture(video_path)
        extracted_text = []

        if not cap.isOpened():
            raise VideoProcessingError("Failed to open video file")

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_sample_rate = max(1, int(fps / 2))  # Sample twice per second

        logger.info(f"Processing video: {fps:.2f} FPS, {total_frames} frames")
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            if frame_count % frame_sample_rate == 0:
                # Enhance frame for better OCR
                frame = cv2.resize(frame, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                cv2.THRESH_BINARY, 11, 2)

                # Perform OCR
                text = pytesseract.image_to_string(binary, config='--oem 3 --psm 6')
                cleaned_text = text.strip()

                if cleaned_text and len(cleaned_text) > 5:
                    extracted_text.append(cleaned_text)

            if frame_count % (frame_sample_rate * 10) == 0:
                progress = (frame_count / total_frames) * 100
                logger.info(f"Processing: {progress:.1f}% complete")

        cap.release()

        # Remove duplicates while preserving order
        final_text = []
        seen = set()
        for text in extracted_text:
            if text not in seen:
                seen.add(text)
                final_text.append(text)

        result = "\n\n".join(final_text)
        logger.info(f"Extracted {len(final_text)} unique text segments")
        return result

    except Exception as e:
        logger.error(f"Text extraction failed: {str(e)}")
        if 'cap' in locals():
            cap.release()
        raise VideoProcessingError(f"Text extraction error: {str(e)}")

async def safe_click(page, selector: str, description: str = "element", timeout: int = 5000) -> bool:
    """Safely click an element with timeout and logging"""
    try:
        element = await page.wait_for_selector(selector, timeout=timeout)
        if element:
            await element.click()
            logger.info(f"Clicked {description}")
            return True
    except PlaywrightTimeoutError:
        logger.warning(f"Timeout waiting for {description}")
        return False
    except Exception as e:
        logger.warning(f"Failed to click {description}: {str(e)}")
        return False

async def record_video(url: str, video_filename: str = "recorded_video.mp4") -> str:
    """Record webpage interaction using Playwright"""
    videos_dir = 'videos'
    final_path = get_unique_filename(str(Path(videos_dir) / video_filename), '.mp4')

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(
                record_video_dir=videos_dir,
                record_video_size=VIDEO_DIMENSIONS,
                viewport=VIDEO_DIMENSIONS
            )

            page = await context.new_page()
            logger.info(f"Navigating to {url}")
            await page.goto(url, wait_until='networkidle')

            # Define interactive elements
            interactions = [
                ('button:has-text("Prompt")', "Prompt button"),
                ('button:has-text("Sample Data")', "Sample Data button"),
                ('textarea[placeholder="Enter custom prompt here..."]', "Custom prompt"),
                ('button:has-text("Configuration")', "Configuration button"),
                ('button:has-text("Import")', "Import button"),
                ('button:has-text("Export")', "Export button")
            ]

            # Perform interactions
            for selector, description in interactions:
                await safe_click(page, selector, description)
                await page.wait_for_timeout(2000)

            # Final wait for animations
            await page.wait_for_timeout(3000)

            # Get video path
            video_path = await page.video.path()
            await context.close()
            await browser.close()

            # Move video to final location
            if os.path.exists(video_path):
                if os.path.exists(final_path):
                    os.remove(final_path)
                os.rename(video_path, final_path)
                logger.info(f"Video saved to: {final_path}")
                return final_path
            else:
                raise VideoProcessingError("No video file created")

    except Exception as e:
        logger.error(f"Video recording failed: {str(e)}")
        raise VideoProcessingError(f"Recording error: {str(e)}")

def generate_speech(text: str, output_path: str) -> bool:
    """Generate speech from text with enhanced error handling"""
    try:
        engine = pyttsx3.init()

        # Configure speech properties
        engine.setProperty('rate', SPEECH_RATE)
        engine.setProperty('volume', SPEECH_VOLUME)

        # Select voice (preferably female voice if available)
        voices = engine.getProperty('voices')
        if len(voices) > 1:
            engine.setProperty('voice', voices[1].id)

        # Clean up the text
        cleaned_text = ' '.join(text.split())

        # Break text into smaller chunks
        max_chunk_length = 1000
        text_chunks = [cleaned_text[i:i+max_chunk_length]
                      for i in range(0, len(cleaned_text), max_chunk_length)]

        logger.info(f"Converting {len(text_chunks)} text chunks to speech...")

        # Save to temporary file first
        temp_file = output_path + ".temp.mp3"
        engine.save_to_file(cleaned_text, temp_file)
        engine.runAndWait()

        # Verify the audio file was created
        if os.path.exists(temp_file) and os.path.getsize(temp_file) > 0:
            os.replace(temp_file, output_path)
            logger.info(f"Speech generated: {output_path}")
            return True
        else:
            raise VideoProcessingError("Generated audio file is empty or missing")

    except Exception as e:
        logger.error(f"Speech generation failed: {str(e)}")
        if os.path.exists(temp_file):
            os.remove(temp_file)
        return False

def verify_audio_file(file_path: str) -> bool:
    """Verify that the audio file exists and has content"""
    try:
        if not os.path.exists(file_path):
            logger.error(f"Audio file does not exist: {file_path}")
            return False

        if os.path.getsize(file_path) < 100:
            logger.error(f"Audio file appears to be empty or corrupted: {file_path}")
            return False

        # Verify with moviepy
        audio = AudioFileClip(file_path)
        duration = audio.duration
        audio.close()

        if duration < 0.1:
            logger.error(f"Audio file too short: {duration} seconds")
            return False

        logger.info(f"Audio file verified: {file_path} (duration: {duration:.2f}s)")
        return True

    except Exception as e:
        logger.error(f"Audio file verification failed: {str(e)}")
        return False


def combine_video_and_audio(video_path: str, audio_path: str, output_path: str) -> bool:
    """Combine video with audio narration"""
    temp_video = None
    try:
        logger.info("Loading video and audio files...")
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)

        logger.info(f"Video duration: {video.duration:.2f}s")
        logger.info(f"Audio duration: {audio.duration:.2f}s")

        # Handle duration mismatch
        if abs(video.duration - audio.duration) > 0.5:
            logger.info("Adjusting durations...")
            if audio.duration > video.duration:
                # Trim the audio to match the video duration
                audio = audio.subclip(0, video.duration)
            else:
                # Extend the audio to match the video duration
                audio = audio.set_duration(video.duration)

        # Create temporary output file
        temp_output = output_path + ".temp.mp4"

        logger.info("Combining video and audio...")
        final_video = video.set_audio(audio)

        final_video.write_videofile(
            temp_output,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            logger=None
        )

        # Verify and move to final location
        if os.path.exists(temp_output) and os.path.getsize(temp_output) > 0:
            if os.path.exists(output_path):
                os.remove(output_path)
            os.rename(temp_output, output_path)
            logger.info(f"Final video created: {output_path}")
            return True
        else:
            raise VideoProcessingError("Final video file is empty or missing")

    except Exception as e:
        logger.error(f"Video-audio combination failed: {str(e)}")
        if temp_video and os.path.exists(temp_video):
            os.remove(temp_video)
        return False
    finally:
        if 'video' in locals(): video.close()
        if 'audio' in locals(): audio.close()
        if 'final_video' in locals(): final_video.close()

def optimize_text(text: str) -> str:
    try:
        client = MistralClient(api_key=MISTRAL_API_KEY)
        messages = [
            ChatMessage(role="user", content=f"Please optimize the following text for better clarity and coherence: {text}")
        ]
        response = client.chat(
            model="mistral-small",
            messages=messages
        )
        optimized_text = response.choices[0].message.content
        logger.info("Text optimization completed")
        return optimized_text
    except Exception as e:
        logger.error(f"Text optimization failed: {str(e)}")
        return text


async def process_webpage(url: str) -> None:
    """Main processing function"""
    try:
        # Setup environment
        setup_environment()

        # Test TTS engine
        if not test_tts_engine():
            raise VideoProcessingError("Text-to-speech engine initialization failed")

        # Record webpage
        video_path = await record_video(url)
        if not os.path.exists(video_path):
            raise VideoProcessingError("Video recording failed")

        # Extract text
        extracted_text = extract_text_from_video(video_path)
        if not extracted_text:
            raise VideoProcessingError("No text was extracted from the video")

        # Optimize text
        optimized_text = optimize_text(extracted_text)

        # Save text
        text_path = get_unique_filename("output/extracted_text", ".txt")
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(optimized_text)
        logger.info(f"Text saved to: {text_path}")

        # Generate speech
        audio_path = get_unique_filename("audio/narration", ".mp3")
        if not generate_speech(optimized_text, audio_path):
            raise VideoProcessingError("Speech generation failed")

        # Verify audio
        if not verify_audio_file(audio_path):
            raise VideoProcessingError("Generated audio file is invalid")

        # Create final video
        final_video_path = get_unique_filename("output/final_video", ".mp4")
        if not combine_video_and_audio(video_path, audio_path, final_video_path):
            raise VideoProcessingError("Video-audio combination failed")

        logger.info("Processing completed successfully!")
        logger.info(f"Final video: {final_video_path}")

    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        raise

async def main():
    try:
        url = "https://streams2cal.netlify.app"  # Replace with your target URL
        await process_webpage(url)
    except Exception as e:
        logger.error(f"Main execution failed: {str(e)}")
        return 1

if __name__ == "__main__":
    asyncio.run(main())
