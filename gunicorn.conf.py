import multiprocessing

bind = "unix:/www/confrm/gunicorn.sock"
workers = multiprocessing.cpu_count()
