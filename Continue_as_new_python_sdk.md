s
# Temporal Python SDK: Continue-As-New Syntax Overview

## Overview

**Continue-As-New** allows a workflow to complete its current run and immediately start a new run with the same workflow ID but a fresh event history. This is useful for long-running workflows when the history might grow too large or when you want to "restart" the workflow with updated parameters.

> **Key Points:**
> - The current run completes immediately.
> - A new run is started with the same workflow ID but a new run ID.
> - The new run receives new parameters, and its history starts fresh.
> - This operation is atomic from the Temporal service’s perspective.

## Detailed Syntax

Inside your workflow code, you can invoke the continue-as-new functionality by calling the `continue_as_new()` function from the `temporalio.workflow` module. Its typical syntax is:

```python
workflow.continue_as_new(*new_args, **new_kwargs)
```

**Important Notes:**

- **Location:** Call this function from within your main workflow method (the method decorated with `@workflow.run`).
- **Arguments:** You can pass new positional and/or keyword arguments for the restarted workflow.
- **Effect:** This call halts the current execution and immediately starts a new run with the provided arguments.
- **Restrictions:**
  - You cannot call continue-as-new from signal, query, or update handlers.
  - The workflow must be deterministic, so any values passed must be reproducible.

## Example

Below is an example of a simple looping workflow that increments a counter until it reaches 5:

```python
from temporalio import workflow
import asyncio

@workflow.defn
class LoopingWorkflow:
    @workflow.run
    async def run(self, iteration: int) -> None:
        # If iteration reaches 5, complete the workflow.
        if iteration == 5:
            return
        # Simulate work with a 10-second delay.
        await asyncio.sleep(10)
        # Continue the workflow as new with an incremented iteration value.
        workflow.continue_as_new(iteration + 1)
```

### Explanation

1. **Workflow Definition:**  
   The class is decorated with `@workflow.defn` and the main method with `@workflow.run`.

2. **Control Logic:**  
   The workflow checks if `iteration` equals 5. If so, it returns normally to complete the execution.

3. **Work Simulation:**  
   Before continuing, the workflow simulates work by sleeping for 10 seconds.

4. **Continue-As-New Call:**  
   The call `workflow.continue_as_new(iteration + 1)` stops the current execution and starts a new run with the updated `iteration`.

## Best Practices and Notes

- **History Size Management:**  
  Use continue-as-new to reset the workflow history and avoid performance degradation from large event histories.

- **Parameter Consistency:**  
  Ensure that the new parameters passed are valid and that your workflow logic can handle the restart appropriately.

- **Atomic Operation:**  
  The continue-as-new operation is atomic; no intermediate state is visible between the end of the current run and the start of the new run.

- **Determinism:**  
  All workflow code, including continue-as-new calls, must be deterministic. Non-deterministic behavior can lead to errors during history replay.

- **Error Handling:**  
  After invoking continue-as-new, any code following that call is not executed. Ensure it is the final operation in the current execution path.

## References

This overview is based on the [Temporal Python SDK documentation for Continue-As-New](citeturn0search0).

