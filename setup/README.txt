# create WSGI service

sudo cp pywer4.service /etc/systemd/system/
sudo sudo systemctl start pywer4
sudo systemctl enable pywer4

# configuring nginx

sudo apt install nginx
sudo cp nginx.conf /etc/nginx/sites-available/pywer4
sudo ln -s /etc/nginx/sites-available/pywer4 /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
sudo ufw allow 'Nginx Full'

# securing with certbot

# install with apt or install with snapd as recommended
sudo add-apt-repository ppa:certbot/certbot
sudo apt install python3-certbot-nginx

sudo certbot --nginx -d gkcb.fr -d www.gkcb.fr
# it will update the nginx config - attention to the ports if you don't use the standard ones