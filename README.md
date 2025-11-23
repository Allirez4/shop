# Shop - Django E-commerce Platform

A Django-based e-commerce platform with REST API, WebSocket support, and async task processing.

## Features

- User authentication with email/phone support
- Product catalog management
- Order processing
- REST API with JWT authentication
- Real-time features with WebSockets (Channels)
- Async task processing with Celery
- API documentation with Swagger/OpenAPI

## Requirements

- Python 3.8+
- PostgreSQL
- RabbitMQ (for Celery)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Allirez4/shop.git
cd shop
```

2. Create a virtual environment and activate it:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory based on `.env.example`:
```bash
cp .env.example .env
```

5. Update the `.env` file with your configuration:
   - Generate a new SECRET_KEY for Django
   - Set your database credentials
   - Configure email settings if needed
   - Adjust other settings as necessary

6. Run migrations:
```bash
cd Shop
python manage.py migrate
```

7. Create a superuser:
```bash
python manage.py createsuperuser
```

8. Run the development server:
```bash
python manage.py runserver
```

## Configuration

### Environment Variables

The following environment variables can be configured in your `.env` file:

- `SECRET_KEY`: Django secret key (generate a secure random key)
- `DEBUG`: Set to `False` in production
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`: Database configuration
- `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`: Email configuration
- `CELERY_BROKER_URL`: Celery broker URL (RabbitMQ)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### Database Setup

1. Install PostgreSQL
2. Create a database and user:
```sql
CREATE DATABASE shop;
CREATE USER shop WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE shop TO shop;
```

### Celery Setup

1. Install RabbitMQ
2. Start Celery worker:
```bash
celery -A Shop worker -l info
```

## API Documentation

API documentation is available via Swagger UI at `/api/schema/swagger-ui/` when running the development server.

## Project Structure

```
Shop/
├── accounts/       # User authentication and management
├── home/          # Homepage and general views
├── order/         # Order management
├── product/       # Product catalog (if exists)
├── Shop/          # Project settings and configuration
├── static/        # Static files (CSS, JS, images)
└── templates/     # HTML templates
```

## Development

### Running Tests

```bash
python manage.py test
```

### Code Style

Follow PEP 8 guidelines for Python code.

## Security Notes

- Never commit the `.env` file to version control
- Keep `SECRET_KEY` secret and use a strong random value
- Set `DEBUG = False` in production
- Use strong database passwords
- Keep dependencies up to date

## License

This project is currently private. Please contact the owner for licensing information.
