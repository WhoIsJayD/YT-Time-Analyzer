
# YouTube Playlist Length

YouTube Playlist Length is a Flask web application that calculates the total length/duration of a YouTube playlist. It provides insights into the time required to watch the entire playlist at different speeds.

## Features

- Retrieve the total duration of a YouTube playlist.
- Display the average length of videos in the playlist.
- Calculate the total length of the playlist.
- Estimate the time required to watch the playlist at various playback speeds.

## Prerequisites

Before running the application, ensure you have the following:

- Python 3.x installed
- Required Python packages (install using `pip install -r requirements.txt`)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/WhoIsJayD/YT-Time-Analyzer.git
   ```

2. Navigate to the project directory:

   ```bash
   cd YT-Time-Analyzer
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Set the `APIS` environment variable with your YouTube Data API keys:

   ```bash
   export APIS="[your_api_key_1, your_api_key_2],...."
   ```

   Replace `[your_api_key_1, your_api_key_2],....` with your actual API keys. Separate multiple keys with commas.

2. Set your Flask secret key. Update the `SECRET_KEY` variable in `app.py`:

   ```python
   SECRET_KEY = 'your_secret_key'
   ```

## Usage

1. Run the Flask application:

   ```bash
   python app.py
   ```

   The application will be accessible at `http://127.0.0.1:5000/`.

2. Open your web browser and navigate to the provided URL.

3. Enter the YouTube playlist link or ID in the input field and submit the form.

## Dependencies

- Flask: 2.2.2
- Flask-CORS: 3.1.1
- Flask-Talisman: 0.8.1
- isodate: 0.6.1
- requests: 2.28.1

## Compatibility

- Tailwind CSS: 2.2.19
- Font Awesome: Latest version from CDN

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- [Tailwind CSS](https://tailwindcss.com/)
- [Font Awesome](https://fontawesome.com/)
