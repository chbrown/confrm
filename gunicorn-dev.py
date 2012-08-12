import multiprocessing
workers = multiprocessing.cpu_count()
bind = "unix:/Users/chbrown/work/confrm-dev/gunicorn.sock"
