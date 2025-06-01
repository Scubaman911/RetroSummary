# RetroSummary
Summarise a retrospective

## Docker Setup

To build and run the application with MongoDB and Streamlit:
```bash
docker-compose up --build
```
Then open http://localhost:8501 in your browser to access the app.

### Development (Hot Reload)
Thanks to the mounted volume and Streamlit's file watcher, any changes you make to `app.py` or other source files will be picked up automatically, and the app will reload in the browser. Just run:
```bash
docker-compose up --build
```
and edit your code—no container rebuild needed for UI changes.
