from multiprocessing import cpu_count
from threading import Thread
from collections import deque
from time import sleep

DEBUTT_FLAG = False
WORKER_PER_QUEUE_THRESHOLD = 250
FUNCTION_TIME_THRESHOLD = 0

# If anytime <0.1s is used for sleep within DefaultWorkerWithFunction's run routine,
# then  either immediately, or after a number of iterations the queue count will
# immediately drop to 0?

# Default worker based on Thread that holds a queue of information to work on
class DefaultWorker(Thread):
	def __init__(self, thrd_id = "", queue = None):
		Thread.__init__(self)
		self.THREAD_ID = thrd_id
		self.RUNNING = False
		self.QUEUE = queue
		self.PROCESSED_DATA = list()
	
	def add_queue(self, queue):
		self.QUEUE = queue
	
	def get_processed_data(self):
		if self.RUNNING:
			raise ValueError("Cannot return processed data while DefaultWorker instance is running!")
		return self.PROCESSED_DATA
	
	def get_queue_count(self):
		return len(self.QUEUE)
	
	def get_processed_count(self):
		return len(self.PROCESSED_DATA)

# Simple derivative of DefaultWorker that also holds a function to perform on each
# item fetched from the queue
class DefaultWorkerWithFunction(DefaultWorker):
	def __init__(self, thrd_id = "", queue = None, function = None):
		DefaultWorker.__init__(self, thrd_id, queue)
		self.__FUNCTION = function
	
	def run(self):
		if not self.__FUNCTION:
			raise ValueError("Function in DefaultWorkerWithFunction instance must be non-null.")
			
		self.RUNNING = True
		next_item = None
		
		while (True):
			try:
				next_item = self.QUEUE.popleft()
				self.PROCESSED_DATA.append( self.__FUNCTION(next_item) )
			except IndexError:
				break

		if _DEBUTT_FLAG: print("[DEBUG] (%s) Thread worker finished!" % self.THREAD_ID)
		self.RUNNING = False
		
	def add_function(self, function):
		if self.RUNNING:
			raise ValueError("Cannot add/change function to DefaultWorker instance while it is running!")
		self.__FUNCTION = function

# Worker based on Thread that holds onto a list of child worker instances.
# When run, regularly checks the running status of child threads and
# provides an easy access point to check if all threads are finished
class ChildThreadStateChecker(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.RUNNING = False
		self.__CHILD_THREADS = list()
		
	def run(self):
		self.RUNNING = True
		
		count = 0
		while (True):
			for child_thread in self.__CHILD_THREADS:
				if not child_thread.RUNNING:
					count += 1
				else:
					if _DEBUTT_FLAG: print("[DEBUG] (%s) Queue count remaining = %d" % (child_thread.THREAD_ID, len(child_thread.QUEUE)))
			if count == len(self.__CHILD_THREADS):
				break
			count = 0
			if _DEBUTT_FLAG: print("--------------------------------------")
			sleep(0.1)
		
		if _DEBUTT_FLAG: print("[DEBUG] All child threads finished running!")
		self.RUNNING = False
	
	def register_child(self, child_thread):
		self.__CHILD_THREADS.append(child_thread)

# Main class to initialize, that holds options, threads, information, queues, handles separating work into threads etc
# also... Debutt = debug. I'm just immature :p
class MultiThreader:
	def __init__(self, async_flag = False, thread_count = -1):
		self._ASYNC_FLAG = async_flag
		self._THREAD_COUNT = thread_count
		self._RUNNING = False
		self._HAS_RUN = False
		
		self.__THREAD_WORKERS = list() # Not just a list, but a list OF lists :P
		self.__WORKER_STATE = None
		self.__DATA = list()
		self.__QUEUED_DATA_INDEX = 0 # This is assuming that DATA is all ordered and stays this way (which it SHOULD be)
		self.__FUNCTION = None
		self.__PROCESSED_DATA = list()
	
	def add_data(self, data = list()):
		self.__DATA = data
		if self._RUNNING: self.__UPDATE_QUEUES()
	
	def add_worker(self, worker):
		# Change this in the future to allow adding extra workers with their own separate data queues.
		if type(worker) is not DefaultWorker:
			raise ValueError("Supplied worker must be a derivative of DefaultWorker class.")
		if self._RUNNING:
			raise ValueError("MultiThreader instance is already running. Cannot add extra workers while running!")
		self.__THREAD_WORKERS.append(worker)
		
	def set_function(self, function = None):
		if self._RUNNING:
			raise ValueError("MultiThreader instance is already running. Cannot change data manipulation function while running!")
		self.__FUNCTION = function
	
	def run(self):
		# Initial checks before running. By the time we hit 'RUNNING', number of thread
		# workers and thread count MUST be equal
		if self._HAS_RUN:
			raise ValueError("This Multithreader instance has already been run. Please create another to run again")
		if self._THREAD_COUNT != -1 and len(self.__THREAD_WORKERS) != 0:
			raise ValueError("If manually supplying thread workers via add_worker(), cannot manually set thread count!")
		if len(self.__THREAD_WORKERS) == 0:
			if not self.__FUNCTION:
				raise ValueError("Please supply function to act upon data, or supply custom workers derived from class DefaultWorker.")
			self._THREAD_COUNT = cpu_count()
			self.__BUILD_THREAD_WORKERS()
		else:
			# TODO figure out how this gonna work with multiple threads per main thread pool??
			self._THREAD_COUNT = len(self.__THREAD_WORKERS)
		
		self.__WORKER_STATE = ChildThreadStateChecker()
		self.__BUILD_QUEUE()
		if _DEBUTT_FLAG: print("[DEBUG] Currently there are %d thread workers" % len(self.__THREAD_WORKERS))
		self._RUNNING = True
		if _DEBUTT_FLAG: print("[DEBUG] Running MultiThreader instance!")
		for thread_worker_list in self.__THREAD_WORKERS:
			if _DEBUTT_FLAG: print("[DEBUG] Adding worker list to main pool...")
			for thread_worker in thread_worker_list:
				if _DEBUTT_FLAG: print("[DEBUG] Adding worker.")
				self.__WORKER_STATE.register_child(thread_worker)
						
		# If not async, blocks thread until all child threads have finished
		if _DEBUTT_FLAG: print("[DEBUG] Blocking thread until all queues are finished / empty.\n[DEBUG] Starting thread workers...")
		for worker_list in self.__THREAD_WORKERS:
			for worker in worker_list: worker.start()
		self.__WORKER_STATE.start()
		if not self._ASYNC_FLAG:
			while (True):
				sleep(1)
				if not self.__WORKER_STATE.RUNNING:
					if _DEBUTT_FLAG: print("[DEBUG] Finished! Queues empty, breaking loop.")
					break
			
		# Collect and combine processed data
		# TODO: figure out keeping data ordered in some way or another?
		if _DEBUTT_FLAG: print("[DEBUG] Collected processed data from workers")
		for thread_worker_list in self.__THREAD_WORKERS:
			for thread_worker in thread_worker_list:
				self.__PROCESSED_DATA.extend( thread_worker.get_processed_data() )
		
		if _DEBUTT_FLAG: print("[DEBUG] Finished running!")
		self._RUNNING = False
		self._HAS_RUN
		
	def is_running(self):
		return self._RUNNING
		
	def get_processed_data(self):
		if self._RUNNING:
			raise ValueError("Cannot collect processed data while thread workers are still running!")
		return self.__PROCESSED_DATA
			
	def __UPDATE_QUEUES(self):
		# Update thread worker queues with new data assuming MultiThreader is RUNNING
		if not self._RUNNING:
			# This should just catch fringe cases. Leaving this here now for debugging
			raise ValueError("MultiThreader instance not currently running. No need to update queues, just add to data list? (this is more of an internal error message, please bug report if you see this)")
		
		new_data_count = len(self.__DATA) - self.__QUEUED_DATA_INDEX
		section_count = new_data_count // self._THREAD_COUNT
		next_index = section_count
		for thread_worker_list in self.__THREAD_WORKERS:
			# Only need to edit queue from one worker in each pool set since in each pool set
			# they all hold onto the same queue instance.
			data_section = self.__DATA[self.__QUEUED_DATA_INDEX : next_index]
			thread_worker.QUEUE.extend(data_section)
			self.__QUEUED_DATA_INDEX = next_index
			next_index += section_count
		
	def __BUILD_THREAD_WORKERS(self):
		# Build thread workers (if not already supplied) using provided thread count and
		# function to manipulate data. Figures out from data size whether to use one or
		# more thread workers per individual queue.
		# NB: queue count is WILL represent number CPU cores (logical + virtual)
		#	/ supplied thread_count. Tool itself will decide whether to use 1 or more
		#	threads per queue. TODO: maybe customise in the future?? Or to many options??
		
		# By this point, if no thread workers (and so, also queues) have been supplied
		# we should still just have a big pool of data. Figure out from data size
		# (and maybe function complexity?) whether to 1 or more workers per queue
		for i in range(self._THREAD_COUNT):
			base_id = str.format("%d:" % i)
			per_queue_count = self.__ANALYSE_DATA_POOL()
			worker_queue_pool = list()
			for j in range(per_queue_count):
				thrd_id = base_id + str.format("%d" % j)
				new_worker = DefaultWorkerWithFunction(thrd_id = thrd_id, function = self.__FUNCTION)
				worker_queue_pool.append(new_worker)
			self.__THREAD_WORKERS.append(worker_queue_pool)
			
	def __ANALYSE_DATA_POOL(self):
		# Analyses size of data pool, and by comparing to a threshold number for max queue
		# size per worker, increases the number of workers per queue accordingly.
		worker_count = 1
		queue_size = len(self.__DATA) // self._THREAD_COUNT
		
		if queue_size > _WORKER_PER_QUEUE_THRESHOLD:
			worker_count = queue_size // _WORKER_PER_QUEUE_THRESHOLD
			
		# check function complexity and also modify worker count from this?????????
		
		return worker_count
	
	def __BUILD_QUEUE(self):
		# Divide data by number of working threads and create a queue for each thread.
		# Initially checks to see if thread workers already have queues (e.g. in cases
		# of provided thread workers)
		if len(self.__DATA) == 0:
			for thread_worker in self.__THREAD_WORKERS:
				if not thread_worker.QUEUE:
					raise ValueError("Either supplied no data, or supplied thread workers were not populated with queues of data!")
		
		section_count = len(self.__DATA) // self._THREAD_COUNT
		next_index = section_count
		for thread_worker_list in self.__THREAD_WORKERS:
			new_queue = deque()
			data_section = self.__DATA[self.__QUEUED_DATA_INDEX : next_index]
			new_queue.extend(data_section)
			for thread_worker in thread_worker_list:
				thread_worker.add_queue(new_queue)
			self.__QUEUED_DATA_INDEX = next_index
			next_index += section_count
			
			
		
		
		
		
		
		
		
		
