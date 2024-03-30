from pathlib import Path
import subprocess
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from pytube import YouTube, exceptions

# Define the root folder (this could be set to be more dynamic, e.g., based on the file's location)
ROOT_FOLDER = Path(__file__).resolve().parent

router = APIRouter(
    prefix="/youtube",
    tags=["youtube"],
)

@router.get("/to_mp3")
async def to_mp3(youtube_url: str = Query(..., description="The URL of the YouTube video to convert to MP3.")):
    # Ensure temp directory exists
    temp_folder = Path('app/temp')
    temp_folder.mkdir(parents=True, exist_ok=True)
    
    try:
        yt = YouTube(youtube_url)
    except exceptions.PytubeError as e:
        raise HTTPException(status_code=400, detail=f"Could not fetch YouTube video: {e}")

    video = yt.streams.filter(only_audio=True).first()
    if video is None:
        raise HTTPException(status_code=404, detail="No audio stream found for this YouTube video.")
    
    # Download the file and create a Path object from the returned path
    out_file_path = Path(video.download(output_path=str(temp_folder)))
    
    # Now you can use with_suffix since out_file_path is a Path object
    new_file_path = out_file_path.with_suffix('.mp3')
    
    # Convert to MP3 using ffmpeg
    try:
        subprocess.run(['ffmpeg', '-i', str(out_file_path), str(new_file_path)], check=True)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error converting video to MP3: {e}")
    finally:
        # Cleanup: remove the original download
        out_file_path.unlink(missing_ok=True)

    # Return the MP3 file directly
    return FileResponse(path=str(new_file_path), filename=new_file_path.name, media_type='audio/mpeg')


@router.get("/to_mp4")
async def to_mp4(youtube_url: str = Query(..., description="The URL of the YouTube video to convert to MP4.")):
    # Ensure temp directory exists
    temp_folder = Path('app/temp')
    temp_folder.mkdir(parents=True, exist_ok=True)
    
    try:
        yt = YouTube(youtube_url)
    except exceptions.PytubeError as e:
        raise HTTPException(status_code=400, detail=f"Could not fetch YouTube video: {e}")

    video = yt.streams.get_highest_resolution()
    if video is None:
        raise HTTPException(status_code=404, detail="No suitable video stream found for this YouTube video.")
    
    # Using pathlib for the download path
    out_file = Path(video.download(output_path=str(temp_folder)))
    
    # No need to convert, pytube downloads in MP4 format
    # Return the MP4 file directly
    return FileResponse(path=str(out_file), filename=out_file.name, media_type='video/mp4')
