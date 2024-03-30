
# YouTube GodMode

YouTube GodMode is a FastAPI application designed to provide additional functionality for YouTube video handling, such as downloading videos and converting them into different formats.

## Features

- Download YouTube videos as MP4.
- Convert YouTube videos to MP3.

## Requirements

- Docker
- Python 3.12 or higher

## Installation

### Docker

You can run this application using Docker. First, clone the repository:

\```bash
git clone https://github.com/DarthTigerson/YouTube_GodMode/
cd YouTube_GodMode
\```

Then, build the Docker image:

\```bash
docker build -t youtube_godmode .
\```

After building the image, run the container:

\```bash
docker run -d -p 8000:8000 youtube_godmode
\```

The application will be available at `http://127.0.0.1:8000`.

### Local Setup

If you prefer not to use Docker, ensure you have Python 3.12 and pip installed on your machine.

Install the dependencies using PDM:

\```bash
pdm install
\```

Run the application:

\```bash
pdm run uvicorn main:app --host 0.0.0.0 --port 8000
\```

## Usage

Once the application is running, you can access the API documentation at `http://127.0.0.1:8000/docs` where you can test the endpoints directly through the Swagger UI.

To download a YouTube video as MP4, use the `/youtube/to_mp4` endpoint with the YouTube video URL as a parameter.

To convert a YouTube video to MP3, use the `/youtube/to_mp3` endpoint with the YouTube video URL as a parameter.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests to us.

## Acknowledgments

- This project uses the [pytube](https://github.com/pytube/pytube) library for interacting with YouTube.
- [moviepy](https://github.com/Zulko/moviepy) is used for video to audio conversion.
- [FastAPI](https://fastapi.tiangolo.com/) is used for creating the web API.