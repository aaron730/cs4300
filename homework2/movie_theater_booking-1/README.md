# Movie Theater Booking — Development README

## Citations
Used Copilot as pair programming, code review and documentation.

## Quick steps to run this Django app locally.

### Prerequisites
- Python 3.8+ installed (python3 on macOS).
- Git (optional).

### Setup (development)
1. Open a terminal and change to the project root (where manage.py lives).
   - Example:
     ```
     cd /Users/theaaron730/Documents/cs4300/homework2/movie_theater_booking
     ```

2. Create and activate a virtual environment:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Install dependencies:
   - If a requirements.txt exists:
     ```
     pip install -r requirements.txt
     ```
   - Install Django (and any other needed packages):
     ```
     pip install django
     ```

### Database setup and migrations
1. Apply migrations:
     ```
     python manage.py migrate
     ```

2. Create a superuser (admin account for Django admin site):
     ```
     python manage.py createsuperuser
     ```

3. Run the development server:
     ```
     python manage.py runserver
     ```
     - Visit `http://127.0.0.1:8000/` in your web browser.

4. (Optional) Install and configure Django Debug Toolbar for debugging:
   - Install:
     ```
     pip install django-debug-toolbar
     ```
   - Add `'debug_toolbar'` to `INSTALLED_APPS` in settings.py.
   - Add the toolbar middleware to `MIDDLEWARE` in settings.py.

### Testing
- To run tests:
  ```
  python manage.py test
  ```

## Deployment on Render
1. Ensure you have a `requirements.txt` file with all dependencies listed.
2. Create a `Procfile` with the following content:
   ```
   web: gunicorn movie_theater_booking.wsgi
   ```
3. Create a `runtime.txt` file specifying the Python version, e.g.:
   ```
   python-3.8.10
   ```
4. Create a `render.yaml` file for Render configuration:
   ```yaml
   version: 1
   services:
     - type: web
       name: movie-theater-booking
       env: python
       plan: free
       buildCommand: pip install -r requirements.txt
       startCommand: gunicorn movie_theater_booking.wsgi
   ```
5. Set up environment variables in Render based on your `.env.sample` file.
6. Push your code to a Git repository and connect it to Render for deployment.