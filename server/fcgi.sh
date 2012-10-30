nohup python fcgi.py method=prefork/threaded minspare=50 maxspare=50 maxchildren=1000 > fcgi.out 2>&1 &
