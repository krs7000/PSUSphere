# PSUSphere

PSUSphere is a Django-based web application designed to manage student organizations, colleges, programs, and memberships.

## Features

- Manage colleges, programs, organizations, and students
- Track organization memberships
- Admin dashboard with search and filtering
- Faker-based automatic data generation for demos

## Technologies Used

- Python
- Django
- SQLite
- Faker

## Installation

1. Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Set OAuth environment variables for Google login:
   - `GOOGLE_OAUTH_CLIENT_ID`
   - `GOOGLE_OAUTH_CLIENT_SECRET`
   - Optional: `USE_SETTINGS_GOOGLE_APP=True` (use settings-based Google app instead of Admin SocialApp)
   - Optional: `SITE_ID` (default `1`)
4. Run migrations via `python manage.py migrate`.
5. Create an admin via `python manage.py createsuperuser`.
6. Start the development server with `python manage.py runserver`.

## Google OAuth (django-allauth)

1. Open `http://127.0.0.1:8000/admin/` and login as superuser.
2. Go to `Sites` and ensure your local domain exists (example: `127.0.0.1:8000`).
3. Go to `Social applications` and add a Google app:
   - Provider: `Google`
   - Add your OAuth Client ID and Client Secret
   - Attach the matching Site
4. Test login at `http://127.0.0.1:8000/accounts/login/`.

Note: use either Admin `Social applications` or `USE_SETTINGS_GOOGLE_APP=True`, but not both at the same time.

## Authors

- Owen Christian Sanchez
- Richo Baterzal
