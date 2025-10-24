# Jiangxi Weather Dashboard

Flask application that shows real-time conditions and a 5-day forecast for every prefecture-level city, district, and county in Jiangxi Province by calling the free [Open-Meteo](https://open-meteo.com/) API. The project now includes production-oriented assets so you can host it for public access.

## Local Run

```bash
python -m venv .venv
.venv\Scripts\activate               # Windows
# source .venv/bin/activate          # Linux / macOS
pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5000/> and ensure the machine has internet access for API calls.

## Production (Gunicorn)

```bash
pip install -r requirements.txt
gunicorn app:app --bind 0.0.0.0:8000
```

Pair Gunicorn with Nginx (or another reverse proxy) to expose ports 80/443 and enable HTTPS.

## Docker

```bash
docker build -t jiangxi-weather .
docker run -d -p 8000:8000 --name jiangxi-weather jiangxi-weather
```

Browse to `http://<server-ip>:8000/`. Set the `PORT` environment variable to change the listening port.

## Managed Hosting Examples

- **Render / Railway / Fly.io**: Connect the repository and rely on the supplied `Procfile`. The platform will install dependencies and provide a public URL.
- **Heroku**: Enable the Python buildpack and deploy; the `Procfile` entry `web: gunicorn app:app --bind 0.0.0.0:${PORT:-8000}` is used automatically.
- **Self-managed VM**: Use systemd or Supervisor to keep Gunicorn running and proxy traffic through Nginx.

## Environment Variables

- `PORT`: HTTP port (defaults to `5000`; `app.py` respects this value).
- `FLASK_DEBUG`: set to `1` to enable debug mode during development.

## Notes

- Open-Meteo applies rate limits; review their terms before exposing the site publicly.
- The app has no external storage requirements; it only needs outbound internet access.
