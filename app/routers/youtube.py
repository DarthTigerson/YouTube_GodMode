import os
import subprocess
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from pytube import YouTube, exceptions

router = APIRouter(
    prefix="/youtube",
    tags=["youtube"],
)

@router.get("/to_mp3")
async def to_mp3(youtube_url: str = Query(..., description="The URL of the YouTube video to convert to MP3.")):
    # Ensure temp directory exists
    os.makedirs('temp', exist_ok=True)
    
    try:
        yt = YouTube(youtube_url)
    except exceptions.PytubeError as e:
        raise HTTPException(status_code=400, detail=f"Could not fetch YouTube video: {e}")

    video = yt.streams.filter(only_audio=True).first()
    if video is None:
        raise HTTPException(status_code=404, detail="No audio stream found for this YouTube video.")
    
    out_file = video.download(output_path='app/temp/')
    
    base, ext = os.path.splitext(out_file)
    new_file = f"{base}.mp3"
    
    # Convert to MP3 using ffmpeg
    try:
        subprocess.run(['ffmpeg', '-i', out_file, new_file], check=True)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error converting video to MP3: {e}")
    finally:
        # Cleanup: remove the original download
        os.remove(out_file)

    # Return the MP3 file directly
    return FileResponse(path=new_file, filename=os.path.basename(new_file), media_type='audio/mpeg')


@router.get("/to_mp4")
async def to_mp4(youtube_url: str = Query(..., description="The URL of the YouTube video to convert to MP4.")):
    # Ensure temp directory exists
    os.makedirs('temp', exist_ok=True)
    
    try:
        yt = YouTube(youtube_url)
    except exceptions.PytubeError as e:
        raise HTTPException(status_code=400, detail=f"Could not fetch YouTube video: {e}")

    video = yt.streams.get_highest_resolution()
    if video is None:
        raise HTTPException(status_code=404, detail="No suitable video stream found for this YouTube video.")
    
    out_file = video.download(output_path='app/temp/')
    
    # No need to convert, pytube downloads in MP4 format
    # Return the MP4 file directly
    return FileResponse(path=out_file, filename=os.path.basename(out_file), media_type='video/mp4')