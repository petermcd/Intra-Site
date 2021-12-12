git pull
./djenv/bin/pip install -r requirements.txt
./djenv/bin/python manage.py collectstatic --no-input
./djenv/bin/python manage.py makemigrations
./djenv/bin/python manage.py migrate
sudo systemctl restart apache2