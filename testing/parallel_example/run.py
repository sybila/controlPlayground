import parallel
from threading import Event
from random import randint

threads = []
global_results = []  # important variable shared by all threads (including checker)

for _ in range(10):
	conds = [randint(0, 100) for _ in range(3)]
	threads.append(parallel.Worker(conds, global_results))

checker = parallel.Checker(global_results)

checker.start()

for thread in threads:
	thread.start()

while checker.is_alive():
	pass # we just have to wait until the checker thread is finished

print("************* Time to end ***********")

for thread in threads:
	thread.join()

print("\n++++++++++++ OVERALL RESULTS ++++++++++++\n")

for thread in threads:
	print("------- Results for thread", thread.name)
	print(list(zip(thread.history_cond, thread.local_results)))
	print()

print(checker.best_cond, checker.best_result)