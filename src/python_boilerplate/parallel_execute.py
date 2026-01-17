"""Parallel executor module for running functions concurrently using multithreading."""

import logging
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

logger = logging.getLogger(__name__)


class ParallelExecutor:
    """Execute functions in parallel using Python multithreading.

    This class provides a convenient interface for executing functions concurrently
    across multiple variables using thread pools.
    """

    def __init__(self, max_workers: int | None = None):
        """Initialize the ParallelExecutor.

        Args:
            max_workers: Maximum number of threads to use. If None, defaults to
                        number of CPU cores times 5.
        """
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.results: dict[int, Any] = {}
        self.errors: dict[int, Exception] = {}

    def execute(self, func: Callable, variables: list[Any], *args, **kwargs) -> list[Any]:
        """Execute a function with multiple variables in parallel.

        Args:
            func: The function to execute in parallel.
            variables: List of variables to pass to the function.
            *args: Additional positional arguments to pass to the function.
            **kwargs: Additional keyword arguments to pass to the function.

        Returns:
            List of results from executing the function with each variable.

        Raises:
            Exception: If any thread encounters an error during execution.
        """
        futures = {}

        # Submit all tasks
        for idx, var in enumerate(variables):
            future = self.executor.submit(func, var, *args, **kwargs)
            futures[idx] = future

        # Collect results
        results = []
        for idx, future in sorted(futures.items()):
            try:
                result = future.result()
                results.append(result)
                self.results[idx] = result
                logger.debug(f"Task {idx} completed successfully")
            except Exception as e:
                self.errors[idx] = e
                logger.error(f"Task {idx} failed with error: {e}")
                results.append(None)

        return results

    def execute_with_callback(
        self,
        func: Callable,
        variables: list[Any],
        on_complete: Callable[[int, Any], None] | None = None,
        on_error: Callable[[int, Exception], None] | None = None,
        *args,
        **kwargs,
    ) -> list[Any]:
        """Execute a function with callbacks for completion and errors.

        Args:
            func: The function to execute in parallel.
            variables: List of variables to pass to the function.
            on_complete: Callback function called on successful completion with
                        (index, result) arguments.
            on_error: Callback function called on error with (index, exception) arguments.
            *args: Additional positional arguments to pass to the function.
            **kwargs: Additional keyword arguments to pass to the function.

        Returns:
            List of results from executing the function with each variable.
        """
        futures = {}
        future_to_idx = {}

        # Submit all tasks
        for idx, var in enumerate(variables):
            future = self.executor.submit(func, var, *args, **kwargs)
            futures[idx] = future
            future_to_idx[future] = idx

        # Process results as they complete
        results = [None] * len(variables)
        for future in as_completed(futures.values()):
            idx = future_to_idx[future]

            try:
                result = future.result()
                results[idx] = result
                self.results[idx] = result
                if on_complete:
                    on_complete(idx, result)
                logger.debug(f"Task {idx} completed successfully")
            except Exception as e:
                self.errors[idx] = e
                if on_error:
                    on_error(idx, e)
                logger.error(f"Task {idx} failed with error: {e}")

        return results

    def get_results(self) -> dict[int, Any]:
        """Get all successful results indexed by task number.

        Returns:
            Dictionary mapping task indices to their results.
        """
        return self.results.copy()

    def get_errors(self) -> dict[int, Exception]:
        """Get all errors indexed by task number.

        Returns:
            Dictionary mapping task indices to their exceptions.
        """
        return self.errors.copy()

    def clear(self) -> None:
        """Clear stored results and errors."""
        self.results.clear()
        self.errors.clear()

    def shutdown(self, wait: bool = True) -> None:
        """Shutdown the thread pool executor.

        Args:
            wait: If True, wait for all pending tasks to complete before returning.
        """
        self.executor.shutdown(wait=wait)

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.shutdown()
