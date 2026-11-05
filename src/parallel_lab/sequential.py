"""
ParallelLab-MPI
Experiment 1: Sequential Computing

This program calculates the sum of squares
using a single Python process.
"""

import time


def calculate_sum_of_squares(number):
    """
    Calculate the sum of squares from 1 to number.

    Formula:
    1² + 2² + 3² + ... + n²
    """

    total = 0

    for i in range(1, number + 1):
        total += i * i

    return total


def main():

    # Number of values to process
    number = 5_000_000

    print("=" * 50)
    print("PARALLELLAB-MPI")
    print("SEQUENTIAL COMPUTING EXPERIMENT")
    print("=" * 50)

    # Start measuring execution time
    start_time = time.perf_counter()

    # Perform calculation
    result = calculate_sum_of_squares(number)

    # Stop measuring execution time
    end_time = time.perf_counter()

    # Calculate execution duration
    execution_time = end_time - start_time

    print(f"\nNumbers processed: {number:,}")
    print(f"Final result: {result:,}")
    print(f"Execution time: {execution_time:.6f} seconds")

    print("\nExperiment completed successfully!")


if __name__ == "__main__":
    main()
