import logging

def log(obj, msg):

	FORMAT = '%(asctime)s - %(name)s - %(funcName)s - %(lineno)d: %(message)s'

	logging.basicConfig(level=logging.INFO, format=FORMAT)
	logger = logging.getLogger(obj.__class__.__name__)
	logger.setLevel('INFO')

	return logger.info(msg)