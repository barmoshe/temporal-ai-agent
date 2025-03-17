import React, {
  useEffect,
  useState,
  useRef,
  useCallback,
  useMemo,
} from "react";
import NavBar from "../components/NavBar";
import ChatWindow from "../components/ChatWindow";
import { apiService } from "../services/api";
import { MusicToolbar } from "../components/MusicComponents";

const POLL_INTERVAL = 2000; // Increase polling interval to reduce flickering
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
  const previousConversationRef = useRef([]);

  const [conversation, setConversation] = useState([]);
  const [lastMessage, setLastMessage] = useState(null);
  const [userInput, setUserInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(INITIAL_ERROR_STATE);
  const [done, setDone] = useState(true);
  const [isStuck, setIsStuck] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(
    window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches
  );

  const debouncedUserInput = useDebounce(userInput, DEBOUNCE_DELAY);

  const errorTimerRef = useRef(null);
  const stuckTimerRef = useRef(null);

  // Add state to detect when we're waiting for music confirmation
  const [waitingForMusicConfirmation, setWaitingForMusicConfirmation] =
    useState(false);

  // Add reference for music confirmation auto-trigger
  const musicConfirmationTimerRef = useRef(null);

  // Function to compare conversations and check if there are actual changes
  const hasConversationChanged = useCallback((oldConv, newConv) => {
    if (oldConv.length !== newConv.length) {
      return true;
    }

    // Compare each message
    for (let i = 0; i < oldConv.length; i++) {
      const oldMsg = oldConv[i];
      const newMsg = newConv[i];

      // Check ID consistency
      if (oldMsg.id !== newMsg.id) {
        return true;
      }

      // Check content changes
      if (oldMsg.content !== newMsg.content) {
        return true;
      }

      // Check response changes
      if (JSON.stringify(oldMsg.response) !== JSON.stringify(newMsg.response)) {
        return true;
      }
    }

    return false;
  }, []);

  // Toggle dark mode
  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [isDarkMode]);

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

  const clearErrorOnSuccess = useCallback(() => {
    if (errorTimerRef.current) {
      clearTimeout(errorTimerRef.current);
    }
    setError(INITIAL_ERROR_STATE);
  }, []);

  // Function to handle when the system appears to be stuck
  const handleStuckState = useCallback(() => {
    setIsStuck(true);
    // Stop polling when we detect a stuck state
    if (pollingRef.current) {
      clearInterval(pollingRef.current);
      pollingRef.current = null;
    }
  }, []);

  // Reset the stuck state when starting a new conversation
  const resetStuckState = useCallback(() => {
    setIsStuck(false);
    if (stuckTimerRef.current) {
      clearTimeout(stuckTimerRef.current);
      stuckTimerRef.current = null;
    }
  }, []);

  // Enhanced confirm action function with better feedback
  const handleConfirm = useCallback(async () => {
    try {
      // Indicate that we're processing the confirmation
      setWaitingForMusicConfirmation(false);

      // Start loading state if not already loading
      if (!loading) {
        setLoading(true);
      }

      // Send confirm request
      await apiService.confirm();
      clearErrorOnSuccess();

      // Restart polling to get updated conversation
      startPolling();
    } catch (error) {
      handleError(error, "confirming action");
    }
  }, [clearErrorOnSuccess, handleError, loading, startPolling]);

  // Check messages for potential music creation confirmation needed
  const checkForMusicConfirmation = useCallback((messages) => {
    if (!messages || messages.length === 0) return false;

    // Get the last couple of messages to analyze
    const lastMessages = messages.slice(-3);

    for (const message of lastMessages) {
      // Skip user messages
      if (message.role === "user" || message.actor === "user") continue;

      // Check content for music creation prompts
      const content = message.content || "";
      const isMusicPrompt =
        (content.includes("tempo") && content.includes("BPM")) ||
        (content.includes("create") && content.includes("melody")) ||
        (content.includes("generate") && content.includes("MIDI"));

      // Check if we have a response object that needs confirmation
      const hasToolResponse =
        message.response &&
        typeof message.response === "object" &&
        message.response.next === "confirm_tool_use";

      if (isMusicPrompt && hasToolResponse) {
        return true;
      }
    }

    return false;
  }, []);

  // Enhanced polling function
  const startPolling = useCallback(() => {
    // Clear any existing polling
    if (pollingRef.current) {
      clearInterval(pollingRef.current);
    }

    console.log("Starting polling with interval", POLL_INTERVAL);

    // Start new polling
    pollingRef.current = setInterval(() => {
      // Use a function reference to avoid circular dependency
      const fetchData = async () => {
        try {
          const data = await apiService.getConversationHistory();
          const newConversation = data.messages || [];

          // Check for backend tool errors in the conversation
          const checkForToolErrors = (messages) => {
            if (!messages || messages.length === 0) return false;

            const lastMsg = messages[messages.length - 1];

            if (lastMsg.role === "assistant" || lastMsg.actor === "agent") {
              if (lastMsg.response && typeof lastMsg.response === "object") {
                return (
                  lastMsg.response.error ||
                  lastMsg.response.next === "error" ||
                  (lastMsg.content &&
                    lastMsg.content.toLowerCase().includes("error"))
                );
              }
            }
            return false;
          };

          // Check if waiting for music confirmation
          const needsMusicConfirmation =
            checkForMusicConfirmation(newConversation);

          if (needsMusicConfirmation && !waitingForMusicConfirmation) {
            setWaitingForMusicConfirmation(true);
          }

          // If we're waiting for confirmation but now the flow has moved on,
          // reset the confirmation state
          if (
            waitingForMusicConfirmation &&
            newConversation.length > previousConversationRef.current.length + 1
          ) {
            setWaitingForMusicConfirmation(false);
          }

          // Check for backend tool errors in the conversation
          const hasToolErrors = checkForToolErrors(newConversation);
          if (!hasToolErrors) {
            // Only update state if the conversation has actually changed
            if (
              hasConversationChanged(
                previousConversationRef.current,
                newConversation
              )
            ) {
              setConversation(newConversation);
              previousConversationRef.current = newConversation;

              // Set last message for scrolling
              if (newConversation.length > 0) {
                const lastMsg = newConversation[newConversation.length - 1];
                setLastMessage(lastMsg);
              }
            }

            if (newConversation.length > 0) {
              const lastMsg = newConversation[newConversation.length - 1];
              const isAgentMessage = lastMsg.actor === "agent";

              // Check if this is a successful response
              let isDone = false;

              if (isAgentMessage) {
                if (typeof lastMsg.response === "string") {
                  try {
                    const jsonResponse = JSON.parse(lastMsg.response);
                    isDone = jsonResponse.next === "done";
                  } catch (e) {
                    // Not JSON, continue
                  }
                } else if (
                  lastMsg.response &&
                  lastMsg.response.next === "done"
                ) {
                  isDone = true;
                }

                if (isDone) {
                  setDone(true);
                  setLoading(false);
                  clearErrorOnSuccess(); // Clear any 404 errors

                  // Stop polling when we're done
                  if (pollingRef.current) {
                    clearInterval(pollingRef.current);
                    pollingRef.current = null;
                  }
                }
              }
            }
          }

          clearErrorOnSuccess(); // Clear any 404 errors on successful fetch
        } catch (error) {
          // Only display error if something specific is wrong
          if (error.status !== 404) {
            handleError(error, "Fetching conversation");
          }
        }
      };

      fetchData();
    }, POLL_INTERVAL);
  }, [
    clearErrorOnSuccess,
    handleError,
    isStuck,
    resetStuckState,
    hasConversationChanged,
    waitingForMusicConfirmation,
    previousConversationRef,
  ]);

  // Handle quick tool selection from toolbar
  const handleToolSelect = useCallback((prompt) => {
    setUserInput(prompt);
    // Focus the input field
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  const handleContentChange = useCallback((action) => {
    if (action === "stop") {
      setDone(true);
      setLoading(false);
    }
  }, []);

  const handleSendMessage = useCallback(async () => {
    if (!userInput.trim() || loading || done) return;

    // Special case for numeric inputs when waiting for music confirmation
    // This handles the case when the user responds with just "120" to a tempo question
    if (waitingForMusicConfirmation && /^\d+$/.test(userInput.trim())) {
      // First send the message
      const userMessage = {
        id: `user-${Date.now()}`,
        role: "user",
        content: userInput,
      };

      // Add user message to conversation
      const newConversation = [...conversation, userMessage];
      setConversation(newConversation);
      previousConversationRef.current = newConversation;

      // Clear input
      setUserInput("");

      // Then auto-confirm after a short delay
      setTimeout(() => {
        handleConfirm();
      }, 500);

      return;
    }

    // Clear conversation if starting new
    if (done) {
      setConversation([]);
      previousConversationRef.current = [];
    }

    setDone(false);
    setLoading(true);

    try {
      // Update UI immediately with user message
      const userMessage = {
        id: `user-${Date.now()}`,
        role: "user",
        content: userInput,
      };

      // Add user message to conversation
      const newConversation = [...conversation, userMessage];
      setConversation(newConversation);
      previousConversationRef.current = newConversation;

      // Clear input
      setUserInput("");

      // Reset stuck state
      resetStuckState();

      // Set a timeout to detect stuck state (after 30 seconds with no response)
      if (stuckTimerRef.current) {
        clearTimeout(stuckTimerRef.current);
      }
      stuckTimerRef.current = setTimeout(() => {
        handleStuckState();
      }, 30000);

      // Start polling for responses
      startPolling();

      // Send message to API
      await apiService.sendMessage(userMessage.content);
      clearErrorOnSuccess();
    } catch (error) {
      setLoading(false);
      handleError(error, "sending message");
    }
  }, [
    userInput,
    loading,
    done,
    conversation,
    resetStuckState,
    handleStuckState,
    startPolling,
    clearErrorOnSuccess,
    handleError,
    waitingForMusicConfirmation,
    handleConfirm,
  ]);

  const handleStartNewChat = useCallback(async () => {
    if (loading) return;

    setConversation([]);
    previousConversationRef.current = [];
    setLastMessage(null);
    setUserInput("");
    setLoading(false);
    setDone(false);
    resetStuckState();

    try {
      // Call API to start a new workflow
      await apiService.startWorkflow();

      // Start polling for responses
      startPolling();
      clearErrorOnSuccess();
    } catch (error) {
      handleError(error, "starting new chat");
    }
  }, [
    loading,
    resetStuckState,
    startPolling,
    clearErrorOnSuccess,
    handleError,
  ]);

  // Memoize the ChatWindow props to prevent unnecessary rerenders
  const chatWindowProps = useMemo(
    () => ({
      conversation,
      loading,
      lastMessage,
      onConfirm: handleConfirm,
      onContentChange: handleContentChange,
      isDarkMode,
    }),
    [
      conversation,
      loading,
      lastMessage,
      handleConfirm,
      handleContentChange,
      isDarkMode,
    ]
  );

  useEffect(() => {
    // On mount, start a new workflow
    handleStartNewChat();

    // Set focus to input
    if (inputRef.current) {
      inputRef.current.focus();
    }

    return () => {
      // Clean up on unmount
      if (pollingRef.current) {
        clearInterval(pollingRef.current);
      }
      if (errorTimerRef.current) {
        clearTimeout(errorTimerRef.current);
      }
      if (stuckTimerRef.current) {
        clearTimeout(stuckTimerRef.current);
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Set up an effect to auto-confirm after a longer timeout
  useEffect(() => {
    // If we're waiting for music confirmation, set a timer to auto-confirm
    if (waitingForMusicConfirmation && loading) {
      if (musicConfirmationTimerRef.current) {
        clearTimeout(musicConfirmationTimerRef.current);
      }

      // Auto-confirm after 25 seconds if the user hasn't done it manually
      musicConfirmationTimerRef.current = setTimeout(() => {
        console.log("Auto-confirming music creation after timeout");
        handleConfirm();
      }, 25000);
    } else if (
      !waitingForMusicConfirmation &&
      musicConfirmationTimerRef.current
    ) {
      clearTimeout(musicConfirmationTimerRef.current);
      musicConfirmationTimerRef.current = null;
    }

    return () => {
      if (musicConfirmationTimerRef.current) {
        clearTimeout(musicConfirmationTimerRef.current);
      }
    };
  }, [waitingForMusicConfirmation, loading, handleConfirm]);

  // Clean up timers on component unmount
  useEffect(() => {
    return () => {
      if (pollingRef.current) {
        clearInterval(pollingRef.current);
      }
      if (errorTimerRef.current) {
        clearTimeout(errorTimerRef.current);
      }
      if (stuckTimerRef.current) {
        clearTimeout(stuckTimerRef.current);
      }
      if (musicConfirmationTimerRef.current) {
        clearTimeout(musicConfirmationTimerRef.current);
      }
    };
  }, []);

  return (
    <div
      className={`flex flex-col min-h-screen bg-gray-50 dark:bg-gray-900 ${
        isDarkMode ? "dark" : ""
      }`}
    >
      <NavBar title="Music Creation Studio" />

      {error.visible && (
        <div
          className="fixed top-16 left-0 right-0 z-50 mx-auto max-w-2xl mt-4 bg-red-100 dark:bg-red-900/30 border border-red-400 dark:border-red-700 text-red-700 dark:text-red-200 px-4 py-3 rounded-lg shadow-lg"
          role="alert"
        >
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <svg
                className="h-5 w-5 text-red-500"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
            <div className="ml-3">
              <p className="font-bold">Error</p>
              <p>{error.message}</p>
              <div className="mt-2">
                <button
                  onClick={handleStartNewChat}
                  className="px-3 py-1 bg-red-500 hover:bg-red-600 text-white rounded-md shadow-sm text-sm"
                >
                  Start New Composition
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {isStuck && !error.visible && (
        <div
          className="fixed top-16 left-0 right-0 z-50 mx-auto max-w-2xl mt-4 bg-yellow-100 dark:bg-yellow-900 border border-yellow-400 dark:border-yellow-700 text-yellow-700 dark:text-yellow-200 px-4 py-3 rounded-lg shadow-lg"
          role="alert"
        >
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <svg
                className="h-5 w-5 text-yellow-500"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
            <div className="ml-3">
              <p className="font-bold">System appears to be stuck</p>
              <p>
                The backend may be experiencing issues with music composition
                tools. Please try starting a new composition.
              </p>
              <button
                onClick={handleStartNewChat}
                className="mt-2 px-3 py-1 bg-yellow-500 hover:bg-yellow-600 text-white rounded-md shadow-sm text-sm"
              >
                Start New Composition
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="flex-grow overflow-auto p-4 md:p-6 mt-16">
        <div className="max-w-4xl mx-auto bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-purple-200 dark:border-purple-900/30 overflow-hidden">
          <div
            ref={containerRef}
            className="h-[calc(100vh-13rem)] md:h-[calc(100vh-14rem)] overflow-y-auto p-4 space-y-4"
          >
            <ChatWindow {...chatWindowProps} />
            {done && conversation.length > 0 && (
              <div
                className="text-center text-sm text-gray-400 mt-4 
                              animate-appear-once"
              >
                Music session ended
              </div>
            )}
          </div>
          <div className="p-4 border-t border-purple-200 dark:border-purple-800 bg-white dark:bg-gray-700">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSendMessage();
              }}
              className="flex space-x-2"
            >
              <input
                ref={inputRef}
                type="text"
                className={`flex-grow px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 focus:outline-none music-input bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100
                              ${
                                loading || done
                                  ? "opacity-50 cursor-not-allowed"
                                  : ""
                              }`}
                placeholder="Describe your music creation ideas..."
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                disabled={loading || done}
                aria-label="Type your message"
              />
              <button
                type="submit"
                disabled={loading || done || !debouncedUserInput.trim()}
                className={`music-btn px-4 py-2 rounded-lg bg-gradient-to-r from-purple-500 to-indigo-600 text-white font-medium flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed
                              ${
                                loading || done || !debouncedUserInput.trim()
                                  ? "opacity-50 cursor-not-allowed"
                                  : ""
                              }`}
                aria-label="Send message"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-5 w-5 mr-1"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path d="M18 3a1 1 0 00-1.447-.894L8.763 6H5a3 3 0 000 6h.28l1.771 5.316A1 1 0 008 18h1a1 1 0 001-1v-4.382l6.553 3.276A1 1 0 0018 15V3z" />
                </svg>
                Compose
              </button>
            </form>
          </div>
        </div>
        <div className="max-w-4xl mx-auto mt-4 flex justify-between">
          <button
            onClick={() => setIsDarkMode(!isDarkMode)}
            className="music-btn p-2 rounded-full bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600"
            title={isDarkMode ? "Switch to light mode" : "Switch to dark mode"}
          >
            {isDarkMode ? (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z"
                  fillRule="evenodd"
                  clipRule="evenodd"
                />
              </svg>
            ) : (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
              </svg>
            )}
          </button>
          <button
            onClick={handleStartNewChat}
            className="music-btn px-4 py-2 rounded-lg bg-gradient-to-r from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700 text-white font-medium flex items-center"
            disabled={loading}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5 mr-1"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fillRule="evenodd"
                d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"
                clipRule="evenodd"
              />
            </svg>
            New Composition
          </button>
        </div>
      </div>

      {/* Music Tools Toolbar */}
      <MusicToolbar onSelectTool={handleToolSelect} />
    </div>
  );
}
