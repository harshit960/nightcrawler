import time

# Without print()
start = time.time()
for i in range(1000000):
    pass  # Do nothing
end = time.time()
print(f"Without print(): {end - start:.4f} seconds")

# With print()
start = time.time()
for i in range(1000000):
    print(i)  # Print each number
end = time.time()
print(f"With print(): {end - start:.4f} seconds")
