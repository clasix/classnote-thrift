nohup python fcgi.py method=prefork/threaded minspare=50 maxspare=50 maxchildren=1000 > fcgi.out 2>&1 &
sleep 5s
chmod 777 /tmp/flask_clasix_tk_app.sock
