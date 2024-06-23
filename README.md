# CVBack

A back end for computer vision.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## TODO

- Front
  - scss
  - event list
  - camera list
- Authentication (native)
- storage: what we want to do?
- Alerts (app)
  - Telegram
  - Whatsapp
- Inference computers: add what data?
  - IP adress?
  - Specs? (GPU, ram, etc)
- 

## Some criteria

- [REST for devices and graphQL for events](https://www.baeldung.com/graphql-vs-rest)

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Development Setup

```bash
# To create .envs directory and .django file with environment variables
python generate_env_var.py

docker-compose -f production.yml build
docker-compose -f production.yml up

# To create a superuser for admin panel: http://localhost:8000/admin/
docker-compose -f production.yml exec django python manage.py createsuperuser

#To create dummy data in local
docker-compose -f production.yml exec django python manage.py generate_fake_data

http://localhost:8000/admin
```

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy cvback

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at <https://sentry.io/signup/?code=cookiecutter> or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).
