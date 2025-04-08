#!/usr/bin/env python3
import threading
import queue
from typing import Any, Callable, Dict, Optional
from dataclasses import dataclass

@dataclass
class FunctionRequest:
    func: Callable
    args: tuple = ()
    kwargs: Dict[str, Any] = None
    result: Any = None
    exception: Optional[Exception] = None
    done: bool = False

_function_queue = queue.Queue()
_function_thread = None
_should_run = True

def _process_function_queue():
    global _should_run
    while _should_run:
        try:
            request = _function_queue.get()
            if request.kwargs is None:
                request.kwargs = {}
            
            try:
                request.result = request.func(*request.args, **request.kwargs)
            except Exception as e:
                request.exception = e
            finally:
                request.done = True
                _function_queue.task_done()
        except queue.Empty:
            continue
        except Exception as e:
            print(f"Error in function thread: {e}")
            continue

def _ensure_function_thread():
    global _function_thread, _should_run
    if _function_thread is None or not _function_thread.is_alive():
        _should_run = True
        _function_thread = threading.Thread(target=_process_function_queue, daemon=True)
        _function_thread.start()

def enqueue_run(f, *args, **kwargs):
    """
    Enqueues a function to be run asynchronously.
    
    Args:
        f: The function to run
        *args: Positional arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        FunctionRequest object which can be checked for completion
    """
    _ensure_function_thread()
    request = FunctionRequest(f, args, kwargs)
    _function_queue.put(request)
    return request

def stop_all():
    """
    Stops the function thread and clears the queue.
    """
    global _should_run, _function_thread
    _should_run = False
    while not _function_queue.empty():
        try:
            _function_queue.get_nowait()
            _function_queue.task_done()
        except queue.Empty:
            break
    if _function_thread is not None:
        _function_thread.join()
        _function_thread = None

def wait_until_done():
    """
    Waits until all queued functions have been executed.
    """
    _function_queue.join()

if __name__ == "__main__":
    # Test the function queue
    import time
    
    def test_function(name, sleep_time):
        print(f"Starting {name}")
        time.sleep(sleep_time)
        print(f"Finished {name}")
        return f"{name} completed in {sleep_time} seconds"
    
    print("Testing the function queueing system...")
    
    # Enqueue a few test functions
    req1 = enqueue_run(test_function, "Task 1", 1)
    req2 = enqueue_run(test_function, "Task 2", 0.5)
    req3 = enqueue_run(test_function, "Task 3", 2)
    
    # Wait for all functions to complete
    wait_until_done()
    
    # Check the results
    print("\nResults:")
    print(f"Task 1 result: {req1.result}")
    print(f"Task 2 result: {req2.result}")
    print(f"Task 3 result: {req3.result}")
    
    print("\nAll functions completed.")
