#!/bin/bash

# Default environment
ENV=${DJANGO_ENV:-development}
PORT=${PORT:-8000}
HOST=${HOST:-0.0.0.0}

# Process arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --env)
      ENV="$2"
      shift 2
      ;;
    --port)
      PORT="$2"
      shift 2
      ;;
    --host)
      HOST="$2"
      shift 2
      ;;
    --ssl)
      USE_SSL=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Load environment variables
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Make sure database migrations are applied
python manage.py migrate

# Collect static files if in production
if [ "$ENV" = "production" ]; then
  python manage.py collectstatic --noinput
fi

# Run server with appropriate settings
if [ "$ENV" = "development" ]; then
  echo "Starting Django in DEVELOPMENT mode on $HOST:$PORT"
  export DJANGO_ENV=development
  export DJANGO_DEBUG=True
  export DISABLE_SSL_REDIRECT=True
  
  if [ "$USE_SSL" = true ]; then
    # Check if django-extensions is installed
    if ! python -c "import django_extensions" 2>/dev/null; then
      echo "Installing required packages for SSL..."
      pip install django-extensions Werkzeug pyOpenSSL
      
      # Add django_extensions to INSTALLED_APPS if not already there
      if ! grep -q "django_extensions" backend/settings.py; then
        sed -i "s/'csp',/'csp',\n    'django_extensions',/" backend/settings.py
      fi
    fi
    
    # Generate self-signed certificate if it doesn't exist
    if [ ! -f cert.key ] || [ ! -f cert.crt ]; then
      echo "Generating self-signed certificate..."
      openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout cert.key -out cert.crt -subj "/CN=localhost"
    fi
    
    echo "Starting with SSL support..."
    python manage.py runserver_plus --cert-file cert.crt --key-file cert.key "$HOST:$PORT"
  else
    python manage.py runserver "$HOST:$PORT"
  fi
else
  echo "Starting Django in PRODUCTION mode on $HOST:$PORT"
  export DJANGO_ENV=production
  python manage.py runserver "$HOST:$PORT"
fi