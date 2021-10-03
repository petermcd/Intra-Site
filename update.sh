git pull
./djenv/bin/pip install -r requirements.txt
./djenv/bin/python  manage.py collectstatic --no-input
sudo systemctl restart apache2