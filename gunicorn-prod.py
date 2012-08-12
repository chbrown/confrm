import multiprocessing
workers = multiprocessing.cpu_count()
bind = "unix:/www/confrm.org/gunicorn.sock"
