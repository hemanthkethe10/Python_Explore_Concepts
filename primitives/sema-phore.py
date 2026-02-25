import threading
import time
import random

# 1. Initialize a Semaphore with a counter of 3
# This means only 3 threads can enter the 'critical section' at once.
max_concurrent_tasks = threading.Semaphore(3)

def generate_thumbnailmanual(image_id):
    print(f"--- Image {image_id} is waiting for a slot...")
    
    # 2. Acquire a slot (P operation)
    # If counter > 0, decrement and proceed. If 0, block here.
    max_concurrent_tasks.acquire()
    
    try:
        print(f"  [Processing] Image {image_id} has started.")
        # Simulate a heavy CPU task (e.g., resizing an image)
        duration = random.uniform(1, 3)
        time.sleep(duration) 
        print(f"  [Finished] Image {image_id} took {duration:.2f}s.")
    finally:
        # 3. Release the slot (V operation)
        # Increment the counter so a waiting thread can start.
        max_concurrent_tasks.release()

def generate_thumbnail_clean(image_id):
    with max_concurrent_tasks:
        # The semaphore is automatically acquired here
        print(f"Processing {image_id}...")
        time.sleep(2)
        # The semaphore is automatically released here, even if an exception occurs
# Create 10 threads (representing 10 images to process)
threads = []
for i in range(1, 11):
    t = threading.Thread(target=generate_thumbnail_clean, args=(i,))
    threads.append(t)
    t.start()

# Wait for all threads to finish
for t in threads:
    t.join()

print("\nAll images processed.")