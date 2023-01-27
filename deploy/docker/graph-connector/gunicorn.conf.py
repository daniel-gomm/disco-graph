import multiprocessing

bind = "0.0.0.0:5000"
workers = int((multiprocessing.cpu_count()/2)+1)