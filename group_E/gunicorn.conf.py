import multiprocessing

bind = '0.0.0.0:5003'
workers = multiprocessing.cpu_count() * 2 + 1
proc_name = 'online-medical'
reload = True

loglevel = 'info'
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
accesslog = "log/access.log"
errorlog = "log/error.log"
