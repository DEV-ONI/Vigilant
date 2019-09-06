import logging
import inspect

def custom_log(msg):

	frame = inspect.currentframe().f_back
	backframe_info = None

	try:
		backframe_info = inspect.getframeinfo(frame)
		function_name = backframe_info.function
		# bounding_class = function_name.__self__
		# print(bounding_class)
	finally:
		del backframe_info

	FORMAT = '%(asctime)s - %(name)s - %(function_name)s - %(lineno)d: %(message)s'

	# sensitive to multithreading. these functions delegate to the root logger
	logging.basicConfig(level=logging.INFO, format=FORMAT)

	logger = logging.getLogger(__name__)
	logger.setLevel('INFO')

	return logger.info(msg, extra={'function_name': function_name})


class TestClass:
	custom_log('hi')

	def __init__(self):
		pass

	def testmethod(self):
		custom_log('hello')

tc = TestClass()
tc.testmethod()

