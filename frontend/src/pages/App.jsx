import React, { useEffect, useState, useRef, useCallback } from "react";
import NavBar from "../components/NavBar";
import ChatWindow from "../components/ChatWindow";
import { apiService } from "../services/api";

const POLL_INTERVAL = 3000; // 3 seconds (increased from 0.5 seconds)
const INITIAL_ERROR_STATE = { visible: false, message: "" };
const DEBOUNCE_DELAY = 300; // 300ms debounce for user input

function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

export default function App() {
  const containerRef = useRef(null);
  const inputRef = useRef(null);
  const pollingRef = useRef(null);
  const scrollTimeoutRef = useRef(null);
  const initialLoadRef = useRef(true); // Track if this is the initial load
  const workflowCheckRef = useRef(null); // Reference for workflow state checking interval

  const [conversation, setConversation] = useState([]);
  const [lastMessage, setLastMessage] = useState(null);
  const [userInput, setUserInput] = useState("");
  const [loading, setLoading] = useState(true); // Start with loading state
  const [error, setError] = useState(INITIAL_ERROR_STATE);
  const [done, setDone] = useState(false); // Start with done=false since we're loading
  const [isCreatingNewChat, setIsCreatingNewChat] = useState(false);
  const [workflowStarted, setWorkflowStarted] = useState(false);
  const [workflowState, setWorkflowState] = useState({
    exists: false,
    message_count: 0,
    continued_from_previous: false,
  });
  const [isUserActive, setIsUserActive] = useState(true);
  const [stopAgentMode, setStopAgentMode] = useState(false);
  const [messageCountWarning, setMessageCountWarning] = useState(false);

  const debouncedUserInput = useDebounce(userInput, DEBOUNCE_DELAY);

  const errorTimerRef = useRef(null);
  const errorCountRef = useRef(0);
  const stuckDetectionRef = useRef(null);
  const lastUpdatedRef = useRef(Date.now()); // Track when the UI state was last updated
  const noAutoResponseRef = useRef(true); // Start with true to prevent auto-response on initial load
  const userActivityTimeoutRef = useRef(null); // Track the timeout for user inactivity

  // Add refs for loop detection
  const previousMessagesRef = useRef([]);
  const identicalMessageCountRef = useRef(0);
  const fetchConversationHistoryRef = useRef(null);

  // Define clearErrorOnSuccess early
  const clearErrorOnSuccess = useCallback(() => {
    if (errorTimerRef.current) {
      clearTimeout(errorTimerRef.current);
    }
    setError(INITIAL_ERROR_STATE);
  }, []);

  // Define handleError early
  const handleError = useCallback((error, context) => {
    console.error(`${context}:`, error);

    const isConversationFetchError = error.status === 404;
    const errorMessage = isConversationFetchError
      ? "Error fetching conversation. Retrying..." // Updated message
      : `Error ${context.toLowerCase()}. Please try again.`;

    setError((prevError) => {
      // If the same 404 error is already being displayed, don't reset state (prevents flickering)
      if (prevError.visible && prevError.message === errorMessage) {
        return prevError;
      }
      return { visible: true, message: errorMessage };
    });

    // Clear any existing timeout
    if (errorTimerRef.current) {
      clearTimeout(errorTimerRef.current);
    }

    // Only auto-dismiss non-404 errors after 3 seconds
    if (!isConversationFetchError) {
      errorTimerRef.current = setTimeout(
        () => setError(INITIAL_ERROR_STATE),
        3000
      );
    }
  }, []);

  // Add a safer way to parse JSON in the LLM responses
  const safeParseResponse = useCallback((lastMsg) => {
    if (!lastMsg) return { next: "done" }; // Default if no message

    try {
      // Check if the message is from the agent (not the user)
      if (lastMsg.actor === "agent") {
        if (typeof lastMsg.response === "string") {
          // If it's a JSON string, try to parse it
          if (lastMsg.response.startsWith("{")) {
            try {
              const parsed = JSON.parse(lastMsg.response);
              // If parsed has a next property, use it, otherwise consider it done
              return parsed.next !== undefined ? parsed : { next: "done" };
            } catch (e) {
              console.warn("Error parsing JSON response:", e);
              return { next: "done" }; // If we can't parse JSON, treat as done
            }
          } else {
            // For plain text responses, they're always considered done
            return { next: "done" };
          }
        } else if (
          typeof lastMsg.response === "object" &&
          lastMsg.response !== null
        ) {
          // If it's already an object, check if it has a next property
          return lastMsg.response.next !== undefined
            ? lastMsg.response
            : { next: "done" };
        } else {
          // For any other type of response (or null/undefined), assume done
          return { next: "done" };
        }
      }
      // If not an agent message, return default
      return { next: "done" };
    } catch (err) {
      console.error("Error in safeParseResponse:", err);
      return { next: "done" }; // Fallback to done state on error
    }
  }, []);

  // Add function to stop excessive agent responses (without fetchConversationHistory dependency)
  const handleStopAgent = useCallback(() => {
    console.log("Stopping agent responses");
    setStopAgentMode(true);

    // Clear any existing polling
    if (pollingRef.current) {
      clearInterval(pollingRef.current);
      pollingRef.current = null;
    }

    // Reset UI state
    setLoading(false);
    setDone(true);

    // After 5 seconds, resume normal operation but with longer polling interval
    setTimeout(() => {
      setStopAgentMode(false);
      if (!pollingRef.current && fetchConversationHistoryRef.current) {
        pollingRef.current = setInterval(
          fetchConversationHistoryRef.current,
          10000
        ); // Use a longer interval after stopping
      }
      console.log("Resumed polling with longer interval");
    }, 5000);
  }, []);

  // Improve resetInputState to be more thorough
  const resetInputState = useCallback(() => {
    console.log("Resetting input state...");
    setLoading(false);
    setDone(true);
    lastUpdatedRef.current = Date.now(); // Update timestamp when resetting
    if (errorCountRef.current) {
      errorCountRef.current = 0;
    }

    // Cancel any pending stuck detection
    if (stuckDetectionRef.current) {
      clearTimeout(stuckDetectionRef.current);
      stuckDetectionRef.current = null;
    }

    // Ensure the input field is focused and enabled
    if (inputRef.current) {
      inputRef.current.disabled = false;
      inputRef.current.focus();
    }
  }, []);

  // Modify fetchConversationHistory to detect message loops/stuck behavior
  const fetchConversationHistory = useCallback(async () => {
    // Skip polling if we're in the process of creating a new chat or in stop mode
    if (isCreatingNewChat || stopAgentMode) return;

    try {
      const data = await apiService.getConversationHistory();
      // Ensure messages is always an array
      const newConversation = Array.isArray(data?.messages)
        ? data.messages
        : [];

      // Loop detection: Check if conversation size is growing rapidly
      if (newConversation.length > 20 && !messageCountWarning) {
        console.log("Large message count detected:", newConversation.length);
        setMessageCountWarning(true);
      }

      // Loop detection: Check if we're receiving identical messages repeatedly
      if (
        newConversation.length > 0 &&
        previousMessagesRef.current.length > 0
      ) {
        const lastNewMsg = JSON.stringify(
          newConversation[newConversation.length - 1]
        );
        const lastPrevMsg = JSON.stringify(
          previousMessagesRef.current[previousMessagesRef.current.length - 1]
        );

        if (lastNewMsg === lastPrevMsg) {
          identicalMessageCountRef.current += 1;
          console.log(
            `Identical message detected ${identicalMessageCountRef.current} times`
          );

          // If we detect 5+ identical messages in a row, something is stuck in a loop
          if (identicalMessageCountRef.current >= 5) {
            console.log("Loop detected - automatically stopping agent");
            handleStopAgent();
            return;
          }
        } else {
          // Reset the counter if messages are different
          identicalMessageCountRef.current = 0;
        }
      }

      // Update previous messages reference
      previousMessagesRef.current = [...newConversation];

      // Only update state if there's a change (prevents unnecessary rerenders)
      setConversation((prevConversation) =>
        JSON.stringify(prevConversation) !== JSON.stringify(newConversation)
          ? newConversation
          : prevConversation
      );

      if (newConversation.length > 0) {
        const lastMsg = newConversation[newConversation.length - 1];
        const isAgentMessage = lastMsg?.actor === "agent";

        setLoading(!isAgentMessage);

        // Use the safer parsing function
        const responseObj = safeParseResponse(lastMsg);
        const isDone = responseObj.next === "done";

        // Add debugging to track response format issues
        if (isAgentMessage) {
          console.log("Agent response format:", {
            messageType: typeof lastMsg.response,
            parsed: responseObj,
            isDone: isDone,
          });
        }

        setDone(isDone);
        if (isDone) {
          lastUpdatedRef.current = Date.now(); // Update timestamp when marking as done
        }

        // Safely update last message with null checks
        if (lastMsg) {
          setLastMessage((prevLastMessage) => {
            try {
              // Avoid potential null/undefined access errors
              const prevResponse = prevLastMessage?.response?.response;
              const currentResponse = lastMsg?.response?.response;

              if (!prevLastMessage || prevResponse !== currentResponse) {
                return lastMsg;
              }
              return prevLastMessage;
            } catch (e) {
              console.warn("Error updating last message:", e);
              return lastMsg; // Just use the new message on error
            }
          });
        }

        // Reset error counter on successful fetch
        if (errorCountRef.current) {
          errorCountRef.current = 0;
        }

        // Clear any stuck detection timeout
        if (stuckDetectionRef.current) {
          clearTimeout(stuckDetectionRef.current);
          stuckDetectionRef.current = null;
        }

        // If we're still loading, set a timeout to detect stuck UI
        if (!isDone) {
          // Set timeout to detect if UI gets stuck in loading state
          stuckDetectionRef.current = setTimeout(() => {
            console.log("Stuck detection triggered - resetting UI state");
            resetInputState();
          }, 20000); // 20 seconds should be enough for most responses
        }
      } else {
        // Reset UI state if we have no messages but workflow is started
        if (workflowStarted) {
          setLoading(false);
          setDone(true);
        }
        setLastMessage(null);
      }

      // Successfully fetched data, clear any persistent errors
      clearErrorOnSuccess();
    } catch (err) {
      // Only show polling errors if we're not in the middle of starting a new chat
      if (pollingRef.current && !isCreatingNewChat) {
        handleError(err, "fetching conversation");

        // Increment error counter and reset UI if we've had multiple consecutive errors
        if (errorCountRef.current) {
          errorCountRef.current += 1;
          if (errorCountRef.current > 3) {
            console.log("Multiple consecutive errors - resetting UI state");
            resetInputState();
          }
        } else {
          errorCountRef.current = 1;
        }
      }
    }
  }, [
    handleError,
    clearErrorOnSuccess,
    isCreatingNewChat,
    workflowStarted,
    resetInputState,
    safeParseResponse,
    stopAgentMode,
    messageCountWarning,
    handleStopAgent,
  ]);

  // Store the fetchConversationHistory function in a ref to avoid circular dependencies
  useEffect(() => {
    fetchConversationHistoryRef.current = fetchConversationHistory;
  }, [fetchConversationHistory]);

  // Check workflow state periodically to detect continue-as-new transitions (fixed dependency)
  const checkWorkflowState = useCallback(async () => {
    if (isCreatingNewChat) return;

    try {
      const state = await apiService.getWorkflowState();

      // Update workflow state
      setWorkflowState((prevState) => {
        // Only update if there's a change to avoid unnecessary re-renders
        if (JSON.stringify(prevState) !== JSON.stringify(state)) {
          return state;
        }
        return prevState;
      });

      // Handle cases where workflow exists but we have no conversation
      // This can happen after a continue-as-new
      if (state.exists && conversation.length === 0) {
        console.log(
          "Workflow exists but conversation is empty. Fetching history..."
        );

        // Access the function via ref instead of directly
        if (fetchConversationHistoryRef.current) {
          await fetchConversationHistoryRef.current();
        }
      }

      // If this is a new continuation, show a notification to the user
      if (
        state.continued_from_previous &&
        !state.continued_from_previous_acknowledged
      ) {
        console.log("Detected workflow continuation");
        setWorkflowState((prev) => ({
          ...prev,
          continued_from_previous_acknowledged: true,
        }));
      }
    } catch (err) {
      console.warn("Error checking workflow state:", err);
    }
  }, [isCreatingNewChat, conversation.length]);

  // Modify polling interval based on user activity - use ref instead of direct function
  useEffect(() => {
    // Clear existing interval
    if (pollingRef.current) {
      clearInterval(pollingRef.current);
      pollingRef.current = null;
    }

    // Only set up the interval if the ref is populated
    if (fetchConversationHistoryRef.current) {
      // Set new interval with appropriate timing
      const interval = isUserActive ? POLL_INTERVAL : 10000; // 3s when active, 10s when inactive
      pollingRef.current = setInterval(
        fetchConversationHistoryRef.current,
        interval
      );

      console.log(
        `Polling interval set to ${interval}ms based on user activity`
      );
    }

    return () => {
      if (pollingRef.current) {
        clearInterval(pollingRef.current);
        pollingRef.current = null;
      }
    };
  }, [isUserActive]);

  // Add a state to track Temporal server status
  const [temporalAvailable, setTemporalAvailable] = useState(true);

  // Add activity detection
  useEffect(() => {
    const resetUserActivity = () => {
      setIsUserActive(true);
      if (userActivityTimeoutRef.current) {
        clearTimeout(userActivityTimeoutRef.current);
      }

      // Set timeout to mark user as inactive after 5 minutes without interaction
      userActivityTimeoutRef.current = setTimeout(() => {
        setIsUserActive(false);
        console.log("User inactive - pausing frequent polling");
      }, 5 * 60 * 1000); // 5 minutes
    };

    // Track user activity
    const activityEvents = ["mousedown", "keypress", "scroll", "touchstart"];
    activityEvents.forEach((event) => {
      window.addEventListener(event, resetUserActivity);
    });

    // Initial activity state
    resetUserActivity();

    return () => {
      activityEvents.forEach((event) => {
        window.removeEventListener(event, resetUserActivity);
      });
      if (userActivityTimeoutRef.current) {
        clearTimeout(userActivityTimeoutRef.current);
      }
    };
  }, []);

  // Improve the checkTemporalStatus function to retry more aggressively
  const checkTemporalStatus = useCallback(
    async (forceCheck = false) => {
      // If we recently checked and all was good, don't check again unless forced
      if (
        temporalAvailable &&
        !forceCheck &&
        sessionStorage.getItem("lastTemporalCheckTime") &&
        Date.now() - parseInt(sessionStorage.getItem("lastTemporalCheckTime")) <
          5000
      ) {
        return true;
      }

      try {
        console.log("Checking Temporal status...");
        const result = await apiService.getTemporalStatus();

        // Store the time of the last check
        sessionStorage.setItem("lastTemporalCheckTime", Date.now().toString());

        // Update UI state
        setTemporalAvailable(result.available);

        if (result.available) {
          console.log("Temporal service is available");
        } else {
          console.warn(
            "Temporal service is unavailable:",
            result.error || "Unknown error"
          );
        }

        return result.available;
      } catch (error) {
        console.error("Error checking Temporal status:", error);
        setTemporalAvailable(false);
        return false;
      }
    },
    [temporalAvailable]
  );

  // Start workflow state checking
  useEffect(() => {
    if (!workflowCheckRef.current) {
      workflowCheckRef.current = setInterval(checkWorkflowState, 2000); // Check every 2 seconds
    }

    return () => {
      if (workflowCheckRef.current) {
        clearInterval(workflowCheckRef.current);
        workflowCheckRef.current = null;
      }
    };
  }, [checkWorkflowState]);

  // Add this to the useEffect for initializing
  useEffect(() => {
    // Set noAutoResponseRef to true for the first 5 seconds after page load
    // This prevents auto-responses when refreshing the page
    noAutoResponseRef.current = true;
    console.log("Auto-response prevention enabled for 5 seconds");
    setTimeout(() => {
      noAutoResponseRef.current = false;
      console.log("Auto-response prevention disabled");
    }, 5000); // Increased from 2000ms to 5000ms for more reliable prevention

    // Check Temporal status periodically
    const statusCheckInterval = setInterval(checkTemporalStatus, 10000); // Check every 10 seconds

    // Initial check
    checkTemporalStatus();

    return () => {
      clearInterval(statusCheckInterval);
    };
  }, [checkTemporalStatus]);

  // Start workflow on initial load
  useEffect(() => {
    async function startInitialWorkflow() {
      if (initialLoadRef.current) {
        initialLoadRef.current = false;

        // First check if Temporal service is available
        const isTemporalAvailable = await checkTemporalStatus();
        if (!isTemporalAvailable) {
          console.log(
            "Temporal service unavailable, won't try to start workflow"
          );
          setWorkflowStarted(true); // Pretend we started to avoid infinite retries
          setLoading(false);
          setDone(true);
          return;
        }

        // Check localStorage to prevent duplicate starts on refresh within a short time
        const lastStartTime = localStorage.getItem("lastWorkflowStartTime");
        const currentTime = Date.now();

        if (lastStartTime && currentTime - parseInt(lastStartTime) < 10000) {
          console.log(
            "Preventing duplicate workflow start within 10 seconds of last start"
          );
          setWorkflowStarted(true);
          setLoading(false);
          setDone(true);
          return;
        }

        // To prevent auto-responses after refresh
        if (noAutoResponseRef.current) {
          console.log("Preventing auto-response on page refresh");
          setWorkflowStarted(true);
          setLoading(false);
          setDone(true);
          return;
        }

        // First, check if a workflow already exists
        try {
          const state = await apiService.getWorkflowState();
          if (state.exists) {
            console.log("Found existing workflow:", state);
            setWorkflowStarted(true);
            setWorkflowState(state);
            setLoading(false);
            setDone(true);
            return; // Don't start a new workflow if one exists
          }
        } catch (err) {
          console.warn("Error checking initial workflow state:", err);
          // Continue to create a new workflow
        }

        // No existing workflow, start a new one
        try {
          console.log("Starting initial workflow...");
          setLoading(true);
          setDone(false);
          await apiService.startWorkflow();
          localStorage.setItem("lastWorkflowStartTime", currentTime.toString());
          setWorkflowStarted(true);
          console.log("Initial workflow started successfully");
        } catch (err) {
          console.error("Failed to start initial workflow:", err);
          handleError(err, "starting initial workflow");
          // Still set workflowStarted to avoid infinite retry loops
          setWorkflowStarted(true);
        } finally {
          // Set a short delay before allowing user input
          setTimeout(() => {
            setLoading(false);
            setDone(true);
          }, 1000);
        }
      }
    }

    startInitialWorkflow();
  }, []);

  const scrollToBottom = useCallback(() => {
    if (containerRef.current) {
      if (scrollTimeoutRef.current) {
        clearTimeout(scrollTimeoutRef.current);
      }

      scrollTimeoutRef.current = setTimeout(() => {
        const element = containerRef.current;
        element.scrollTop = element.scrollHeight;
        scrollTimeoutRef.current = null;
      }, 100);
    }
  }, []);

  const handleContentChange = useCallback(() => {
    scrollToBottom();
  }, [scrollToBottom]);

  useEffect(() => {
    if (lastMessage) {
      scrollToBottom();
    }
  }, [lastMessage, scrollToBottom]);

  // Modify the useEffect for input focusing
  useEffect(() => {
    if (inputRef.current) {
      if (!loading && done) {
        inputRef.current.disabled = false;
        inputRef.current.focus();
      }
    }

    // Auto-reset if the UI appears to be stuck for too long
    let stuckTimer;
    if (loading && !isCreatingNewChat) {
      stuckTimer = setTimeout(() => {
        resetInputState();
      }, 10000); // 10 seconds timeout if loading state persists too long
    }

    return () => {
      if (scrollTimeoutRef.current) {
        clearTimeout(scrollTimeoutRef.current);
      }
      if (stuckTimer) {
        clearTimeout(stuckTimer);
      }
    };
  }, [loading, done, isCreatingNewChat, resetInputState]);

  // Modify the handleSendMessage function to check for Temporal availability first
  const handleSendMessage = async () => {
    const trimmedInput = userInput.trim();
    if (!trimmedInput) return;

    // First check if Temporal is available
    const isAvailable = await checkTemporalStatus(true);
    if (!isAvailable) {
      handleError(
        { status: 500, message: "Temporal service is unavailable" },
        "sending message - Temporal unavailable"
      );
      return;
    }

    try {
      setLoading(true);
      setDone(false);
      setError(INITIAL_ERROR_STATE);
      await apiService.sendMessage(trimmedInput);
      setUserInput("");
    } catch (err) {
      handleError(err, "sending message");
      setLoading(false);
      // Force-enable the input field if it might be stuck due to an error
      resetInputState();
    }
  };

  // Modify the handleConfirm function to check for Temporal availability first
  const handleConfirm = async () => {
    // First check if Temporal is available
    const isAvailable = await checkTemporalStatus(true);
    if (!isAvailable) {
      handleError(
        { status: 500, message: "Temporal service is unavailable" },
        "confirming action - Temporal unavailable"
      );
      resetInputState();
      return;
    }

    try {
      setLoading(true);
      setDone(false);
      setError(INITIAL_ERROR_STATE);
      await apiService.confirm();
    } catch (err) {
      handleError(err, "confirming action");
      setLoading(false);
      resetInputState();
    }
  };

  const handleStartNewChat = async () => {
    try {
      // Check if Temporal is available first
      const isAvailable = await checkTemporalStatus(true);
      if (!isAvailable) {
        handleError(
          {
            status: 500,
            message: "Cannot start new chat: Temporal service unavailable",
          },
          "starting new chat - Temporal unavailable"
        );
        return;
      }

      // Clear any existing polling
      if (pollingRef.current) {
        clearInterval(pollingRef.current);
        pollingRef.current = null;
      }

      // Clear conversation state immediately to give immediate feedback
      setConversation([]);
      setLastMessage(null);
      setUserInput("");
      setDone(false); // Disable input while we're creating a new chat

      setIsCreatingNewChat(true);
      setError(INITIAL_ERROR_STATE);
      setLoading(true);

      // End the current workflow with a special signal
      try {
        await apiService.endChat();
        console.log("Successfully ended previous chat");
      } catch (err) {
        console.warn(
          "Error ending previous chat (may be normal if no chat existed):",
          err
        );
        // Continue anyway - this error is expected if no previous workflow exists
      }

      // Short delay to ensure previous operations completed
      await new Promise((resolve) => setTimeout(resolve, 500));

      // Check Temporal again before trying to start a new workflow
      const stillAvailable = await checkTemporalStatus(true);
      if (!stillAvailable) {
        throw new Error(
          "Temporal service became unavailable during new chat creation"
        );
      }

      // Start a new workflow
      await apiService.startWorkflow();
      console.log("New workflow started successfully");
      setWorkflowStarted(true);

      // Reset workflow state
      setWorkflowState({
        exists: true,
        message_count: 0,
        continued_from_previous: false,
      });

      // Add a delay before restarting polling to allow the backend to initialize
      setTimeout(() => {
        setIsCreatingNewChat(false);
        setLoading(false);
        setDone(true);

        // Restart polling using the ref
        if (!pollingRef.current && fetchConversationHistoryRef.current) {
          pollingRef.current = setInterval(
            fetchConversationHistoryRef.current,
            POLL_INTERVAL
          );
        }
      }, 2000); // 2 seconds delay for more reliable reset
    } catch (err) {
      handleError(err, "starting new chat");
      setIsCreatingNewChat(false);
      setLoading(false);
      setDone(true);
      // Restart polling even if there was an error, using the ref
      if (!pollingRef.current && fetchConversationHistoryRef.current) {
        pollingRef.current = setInterval(
          fetchConversationHistoryRef.current,
          POLL_INTERVAL
        );
      }
    }
  };

  // Add an error recovery useEffect
  useEffect(() => {
    // Add a global window error handler for debugging
    const errorHandler = (event) => {
      console.error("Global error caught:", event.error || event.message);

      // Auto-reset the UI state if we detect a rendering error
      if (
        event.error &&
        (event.error
          .toString()
          .includes("Cannot read properties of undefined") ||
          event.error.toString().includes("Cannot read properties of null"))
      ) {
        console.log(
          "Detected potential undefined/null error, resetting UI state"
        );
        setTimeout(() => {
          try {
            setLoading(false);
            setDone(true);

            // Reset any detected error refs
            if (errorCountRef.current) {
              errorCountRef.current = 0;
            }

            // Clear stuck detection timeout
            if (stuckDetectionRef.current) {
              clearTimeout(stuckDetectionRef.current);
              stuckDetectionRef.current = null;
            }
          } catch (e) {
            console.error("Error during auto-recovery:", e);
          }
        }, 500);
      }
    };

    window.addEventListener("error", errorHandler);

    return () => {
      window.removeEventListener("error", errorHandler);
    };
  }, []);

  // Define a TemporalWarning component to reuse in both render paths
  const TemporalWarning = () =>
    !temporalAvailable && (
      <div className="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 mb-4 mx-4 mt-2">
        <div className="flex items-center">
          <div className="py-1">
            <svg
              className="h-6 w-6 text-yellow-500 mr-3"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
          </div>
          <div className="flex-grow">
            <p className="font-medium">Temporal service is unavailable</p>
            <p className="text-sm">
              Chat functionality is limited. Please try again later or contact
              support.
            </p>
          </div>
          <button
            onClick={async (e) => {
              // Set loading state for the button
              const button = e.currentTarget;
              button.disabled = true;
              button.textContent = "Checking...";

              // Force check
              const available = await checkTemporalStatus(true);

              // Reset button state
              button.disabled = false;
              button.textContent = "Retry Connection";

              if (available) {
                // If connection restored, start workflow
                console.log("Connection restored, starting workflow");
                setWorkflowStarted(false); // Reset so it will try to start again
                initialLoadRef.current = true; // Allow startInitialWorkflow to run again
                await startInitialWorkflow();
              }
            }}
            className="ml-3 px-3 py-1 bg-yellow-200 hover:bg-yellow-300 text-yellow-800 text-xs font-semibold rounded"
          >
            Retry Connection
          </button>
        </div>
      </div>
    );

  // Define an ErrorDisplay component to reuse in both render paths
  const ErrorDisplay = () =>
    error.visible && (
      <div className="fixed top-0 left-0 right-0 mx-auto p-3 z-50 animate-slideUp">
        <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mx-auto max-w-md rounded shadow-lg">
          <div className="flex items-center">
            <div className="py-1">
              <svg
                className="h-6 w-6 text-red-500 mr-3"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <div>
              <p className="font-medium">{error.message}</p>
            </div>
          </div>
        </div>
      </div>
    );

  // Add a StopAgentButton component
  const StopAgentButton = () => (
    <button
      className="stop-agent-button"
      onClick={handleStopAgent}
      style={{
        position: "fixed",
        top: "10px",
        right: "10px",
        backgroundColor: "#ff4d4f",
        color: "white",
        border: "none",
        borderRadius: "4px",
        padding: "8px 16px",
        fontWeight: "bold",
        cursor: "pointer",
        zIndex: 1000,
      }}
    >
      Stop Agent Responses
    </button>
  );

  // Add MessageCountWarning component
  const MessageCountWarning = () =>
    messageCountWarning &&
    !stopAgentMode && (
      <div
        style={{
          position: "fixed",
          top: "60px", // Below the stop button
          right: "10px",
          backgroundColor: "#faad14",
          color: "white",
          padding: "10px 15px",
          borderRadius: "4px",
          boxShadow: "0 2px 8px rgba(0, 0, 0, 0.15)",
          zIndex: 1000,
          maxWidth: "300px",
        }}
      >
        <div style={{ marginBottom: "8px", fontWeight: "bold" }}>
          ⚠️ High Message Count Detected
        </div>
        <div style={{ fontSize: "14px" }}>
          The agent is generating a lot of messages. This may lead to higher
          costs. Click "Stop Agent Responses" if needed.
        </div>
        <button
          onClick={handleStopAgent}
          style={{
            backgroundColor: "#ff4d4f",
            color: "white",
            border: "none",
            borderRadius: "4px",
            padding: "5px 10px",
            marginTop: "10px",
            cursor: "pointer",
            width: "100%",
          }}
        >
          Stop Agent Now
        </button>
      </div>
    );

  // Wrap the return statement in try-catch to provide additional stability
  try {
    return (
      <div className="flex flex-col h-full bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
        <NavBar onNewChat={handleStartNewChat} loading={loading} />
        <TemporalWarning />
        <div
          ref={containerRef}
          className="flex-grow overflow-y-auto pb-20 md:pb-24 relative"
        >
          <ErrorDisplay />
          <ChatWindow
            conversation={conversation}
            loading={loading}
            onConfirm={handleConfirm}
            onContentChange={() => {
              if (containerRef.current) {
                containerRef.current.scrollTop =
                  containerRef.current.scrollHeight;
              }
            }}
          />
        </div>

        <div className="fixed bottom-0 left-0 right-0 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 shadow-lg transition-all">
          <div className="max-w-4xl mx-auto px-4 py-3">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSendMessage();
              }}
              className="flex items-center gap-3"
            >
              <div className="relative flex-grow">
                <input
                  ref={inputRef}
                  type="text"
                  placeholder={
                    loading ? "Waiting for response..." : "Type a message..."
                  }
                  value={userInput}
                  onChange={(e) => setUserInput(e.target.value)}
                  onKeyDown={(e) => {
                    // Allow sending with Enter
                    if (
                      e.key === "Enter" &&
                      userInput.trim() &&
                      !loading &&
                      done
                    ) {
                      e.preventDefault();
                      handleSendMessage();
                    }
                    // Force reset if Escape is pressed - useful if UI gets stuck
                    if (e.key === "Escape") {
                      resetInputState();
                    }
                    // If input is stuck for any reason, reset it on any key press
                    if (
                      inputRef.current &&
                      inputRef.current.disabled &&
                      debouncedUserInput !== userInput
                    ) {
                      resetInputState();
                    }
                  }}
                  onFocus={() => {
                    // If the input is focused but disabled, something might be wrong
                    if (
                      inputRef.current &&
                      inputRef.current.disabled &&
                      !loading
                    ) {
                      resetInputState();
                    }
                  }}
                  className={`chat-input ${
                    loading || !done ? "opacity-70" : ""
                  }`}
                  disabled={loading || !done}
                  aria-label="Chat message input"
                />
                {/* "Reset" button visible when input is stuck */}
                {loading && (
                  <button
                    type="button"
                    onClick={resetInputState}
                    className="absolute right-20 top-1/2 transform -translate-y-1/2 text-xs text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 bg-blue-50 dark:bg-blue-900/30 px-2 py-1 rounded"
                    aria-label="Reset stuck state"
                  >
                    Reset
                  </button>
                )}
                {userInput.length > 0 && !loading && (
                  <button
                    type="button"
                    className="absolute right-12 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                    onClick={() => setUserInput("")}
                    aria-label="Clear input"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-5 w-5"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path
                        fillRule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </button>
                )}
                {loading && (
                  <div className="absolute right-12 top-1/2 transform -translate-y-1/2">
                    <div className="spinner w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                  </div>
                )}
                {/* Emergency reset button - appears when stuck for more than 10 seconds */}
                {!done && Date.now() - lastUpdatedRef.current > 10000 && (
                  <button
                    type="button"
                    onClick={() => {
                      console.log("Emergency reset triggered by user");
                      resetInputState();
                      // Force reset all state
                      setLoading(false);
                      setDone(true);
                      if (errorCountRef.current) {
                        errorCountRef.current = 0;
                      }
                    }}
                    className="absolute right-20 top-1/2 transform -translate-y-1/2 text-xs text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300 bg-red-50 dark:bg-red-900/30 px-2 py-1 rounded font-medium"
                    aria-label="Emergency reset"
                  >
                    Reset UI
                  </button>
                )}
              </div>
              <button
                type="submit"
                className="btn-primary flex items-center justify-center min-w-[44px] h-[44px]"
                disabled={!userInput.trim() || loading || !done}
                aria-label="Send message"
              >
                {loading ? (
                  <svg
                    className="animate-spin h-5 w-5 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                ) : (
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-5 w-5"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fillRule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 1.414L10.586 9H7a1 1 0 100 2h3.586l-1.293 1.293a1 1 0 101.414 1.414l3-3a1 1 0 000-1.414z"
                      clipRule="evenodd"
                    />
                  </svg>
                )}
              </button>
            </form>
            <div className="text-xs text-center text-gray-500 dark:text-gray-400 mt-2">
              {done
                ? "Ask me anything to get started"
                : loading && Date.now() - lastUpdatedRef.current > 15000
                ? "Processing is taking longer than expected... you can reset using ESC key"
                : loading
                ? "Processing previous request..."
                : "Waiting for response..."}
            </div>
          </div>
        </div>
        {stopAgentMode && (
          <div
            className="agent-stopped-overlay"
            style={{
              position: "fixed",
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              backgroundColor: "rgba(0, 0, 0, 0.3)",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              zIndex: 999,
            }}
          >
            <div
              style={{
                backgroundColor: "white",
                padding: "20px",
                borderRadius: "8px",
                boxShadow: "0 4px 12px rgba(0, 0, 0, 0.15)",
              }}
            >
              <h3>Agent Responses Paused</h3>
              <p>
                The system has paused all agent responses. You can now safely
                interact with the application.
              </p>
            </div>
          </div>
        )}

        {!stopAgentMode && <StopAgentButton />}
        <MessageCountWarning />
      </div>
    );
  } catch (err) {
    console.error("Error in App component:", err);
    return (
      <div className="flex flex-col h-full bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
        <NavBar onNewChat={handleStartNewChat} loading={loading} />
        <TemporalWarning />
        <div className="p-6 bg-white dark:bg-gray-800 rounded-lg shadow m-4">
          <h2 className="text-xl font-semibold text-gray-800 dark:text-gray-100 mb-2">
            Application Error
          </h2>
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            Something went wrong with the chat interface. Please try refreshing
            the page.
          </p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded"
          >
            Refresh Page
          </button>
        </div>
      </div>
    );
  }
}
