# PowerShell setup script for Windows
Write-Host "Creating Python virtual environment..." -ForegroundColor Green
python -m venv venv

Write-Host "Activating virtual environment..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"

Write-Host "Installing Python packages..." -ForegroundColor Green
pip install -r requirements.txt

Write-Host "Creating Django project..." -ForegroundColor Green
django-admin startproject prodigy_auth .

Write-Host "Creating accounts app..." -ForegroundColor Green
python manage.py startapp accounts

Write-Host "Setup complete! Next steps:" -ForegroundColor Yellow
Write-Host "1. Configure settings.py" -ForegroundColor Cyan
Write-Host "2. Run: python manage.py makemigrations accounts" -ForegroundColor Cyan
Write-Host "3. Run: python manage.py migrate" -ForegroundColor Cyan
Write-Host "4. Run: python manage.py createsuperuser" -ForegroundColor Cyan
Write-Host "5. Run: python manage.py runserver" -ForegroundColor Cyan