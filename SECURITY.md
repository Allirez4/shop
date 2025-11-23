# Security Policy

## Reporting Security Issues

If you discover a security vulnerability in this project, please report it by emailing the repository owner. Please do not disclose security vulnerabilities publicly until they have been addressed.

## Security Best Practices

When deploying this application, please follow these security guidelines:

### Environment Configuration

1. **Never commit the `.env` file** - This file contains sensitive credentials and should never be added to version control.

2. **Generate a strong SECRET_KEY** - Use Django's built-in key generator:
   ```python
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```

3. **Set DEBUG to False in production** - Debug mode should never be enabled in production environments.

4. **Configure ALLOWED_HOSTS** - Set appropriate domain names in production.

5. **Use strong database passwords** - Never use default or weak passwords for database access.

6. **Secure email credentials** - Use app-specific passwords or OAuth2 for email services.

### Database Security

- Use strong, unique passwords for database users
- Limit database user permissions to only what's necessary
- Use SSL/TLS for database connections in production
- Regularly backup your database
- Never commit database files or backups to version control

### Application Security

- Keep all dependencies up to date
- Regularly run `pip list --outdated` to check for updates
- Use HTTPS in production (configure SSL/TLS certificates)
- Enable Django's security middleware
- Configure CSRF protection properly
- Set secure cookie flags in production

### Celery & RabbitMQ

- Secure RabbitMQ with authentication
- Use separate RabbitMQ users for different environments
- Monitor and limit task queue sizes

### File Permissions

Ensure proper file permissions:
- `.env` file should be readable only by the application user (chmod 600)
- Database files should have restricted access
- Log files should be secured appropriately

### Regular Security Audits

- Review Django security checklist: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
- Run `python manage.py check --deploy` before deployment
- Keep dependencies updated for security patches
- Monitor security advisories for Django and all dependencies

## What's Been Done

This repository has been configured with security in mind:

✅ Sensitive credentials moved to environment variables  
✅ .gitignore configured to prevent committing sensitive files  
✅ Database files excluded from version control  
✅ Python cache files excluded  
✅ .env.example provided as a template  
✅ README with security notes  

## What You Need to Do

When setting up this project:

1. Create your own `.env` file based on `.env.example`
2. Generate and use your own SECRET_KEY
3. Use strong, unique passwords for all services
4. Configure production settings appropriately
5. Set up proper monitoring and logging
6. Keep dependencies updated
