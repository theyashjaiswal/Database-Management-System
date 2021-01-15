import logging

class ConfigureLogs():
    def configure_log(self,typ,fname):
        dt_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        log_handler = logging.FileHandler(fname+"_logs.log")
        log_handler.setFormatter(dt_formatter)
        log_obj = logging.getLogger(typ)
        log_obj.setLevel(logging.DEBUG)
        log_obj.addHandler(log_handler)
        return log_obj