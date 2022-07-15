import logging

logging.basicConfig(
    filename='logfile.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

manager_logger = logging.getLogger('MANAGER')
extractor_logger = logging.getLogger('EXTRACTOR')
loader_logger = logging.getLogger('LOADER')
