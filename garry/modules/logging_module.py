import logging
from modules.Path_manager import PATH



class logs:
    def __init__(self):
        
        self.error_log = logging.getLogger("error") # purpose: logger for WARNING/ERROR messages
        self.data_log = logging.getLogger("data") # normal INFO
        self.dataWarn_log = logging.getLogger("dataWARN") # data-related warnings
        self.chunks_log = logging.getLogger("chunks") # chunk-processing information
         
        self.error_log.setLevel(logging.WARNING) # purpose: only log WARNING and above in error_log
        self.data_log.setLevel(logging.INFO) # all INFO data messages
        self.dataWarn_log.setLevel(logging.WARNING) # warnings about data quality/coruption
        self.chunks_log.setLevel(logging.INFO) # log chunk operations
        
        self.error_handler  = logging.FileHandler(PATH.logs_file.log_errors(),  mode="w", encoding="utf-8") # writes error log output to errors.log
        self.data_handler   = logging.FileHandler(PATH.logs_file.log_data(),    mode="w", encoding="utf-8") # data logs to data.log
        self.dataWarn_handler = logging.FileHandler(PATH.logs_file.log_dataWarn(),    mode="w", encoding="utf-8") # data warning logs to dataWARN.log
        self.chunks_handler = logging.FileHandler(PATH.logs_file.log_chunks(),  mode="w", encoding="utf-8") # chunk logs to chunks.log
        
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
        
        self.error_handler.setFormatter(formatter)
        self.data_handler.setFormatter(formatter)
        self.dataWarn_handler.setFormatter(formatter)
        self.chunks_handler.setFormatter(formatter)
        
        self.error_log.addHandler(self.error_handler)
        self.data_log.addHandler(self.data_handler)
        self.dataWarn_log.addHandler(self.dataWarn_handler)
        self.chunks_log.addHandler(self.chunks_handler)
        
        self.root_logger = logging.getLogger() 
        self.root_logger.setLevel(logging.WARNING)
        self.root_logger.addHandler(self.error_handler)
        
        self.error_log.propagate = False
        self.data_log.propagate = False
        self.chunks_log.propagate = False
        self.dataWarn_log.propagate = False

LOG = logs()

      #  LOG.data_log.info("Test: data log ready.")
      #  LOG.error_log.info("Test: data log ready.")
      #  LOG.dataWarn_log.info("Test: data log ready.")
      #  LOG.chunks_log.info("Test: data log ready.")

