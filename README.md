# Hotel Booking System (Flask) – Black-Box Testing App

This is a small Flask web app that lets students interact with a hotel booking system **without seeing the Python source code**. It is designed for a Criterion D testing/evaluation activity.

**Important:** The app stores bookings **in memory** (a Python list). If you restart the server, bookings reset.

## 1) Download / copy into GitHub

- Create a new GitHub repo (e.g. `hotel-booking-flask`)
- Upload these files/folders into the repo

Repo structure:

```
hotel-booking-flask/
  app.py
  requirements.txt
  README.md
  templates/
    base.html
    index.html
```

## 2) Run locally (recommended for classroom)

### Windows / macOS / Linux

```bash
cd hotel-booking-flask
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python app.py
```

Then open:

- http://127.0.0.1:5000

## 3) Run with GitHub Codespaces

1. Open the repo in **Codespaces**
2. In the terminal:

```bash
pip install -r requirements.txt
python app.py
```

Codespaces will offer a forwarded port. Open the forwarded URL.

## Teacher tips

- For true black-box testing, do not share `app.py` with students. Share only the web link.
- Use `/reset` button between classes to clear bookings.

