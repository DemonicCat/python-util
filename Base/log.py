
import logging
from logging.handlers import TimedRotatingFileHandler
'''
配置
 'S'         |  秒

 'M'         |  分

 'H'         |  时

 'D'         |  天

 'W0'-'W6'   |  周一至周日

 'midnight'  |  每天的凌晨
#######
logger.debug('Quick zephyrs blow, vexing daft Jim.')
logger.info('How quickly daft jumping zebras vex.')
logger.warning('Jail zesty vixen who grabbed pay from quack.')
logger.error('The five boxing wizards jump quickly.')

'''
def get_logger(self, path=None):
    logger = logging.getLogger("threading_eg")
    logger.setLevel(logging.WARNING)
    path = path or './log/app.log'
    #fh = logging.FileHandler(path)
    fh = TimedRotatingFileHandler(path,
                                  when = 'd',
                                  interval = 1,
                                  backupCount=7)
    fmt = '%(asctime)s - %(name)s - %(processName)s - %(threadName)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    fh.close()
    return logger
    
