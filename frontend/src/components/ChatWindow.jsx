import React, {
  memo,
  useCallback,
  useState,
  useEffect,
  useRef,
  useMemo,
} from "react";
import MessageBubble from "./MessageBubble";
import LoadingIndicator from "./LoadingIndicator";
import PropTypes from "prop-types";

class ChatErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo,
    });
    console.error("ChatWindow error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="chat-error bg-red-100 dark:bg-red-900/50 text-red-800 dark:text-red-200 p-4 rounded-lg mt-4">
          <h2 className="text-lg font-semibold">
            Something went wrong with the chat display
          </h2>
          <p className="mt-2">Please refresh the page or try again later.</p>
          <details className="mt-2 text-sm">
            <summary>Technical details</summary>
            <p className="mt-1">
              {this.state.error && this.state.error.toString()}
            </p>
            <pre className="mt-2 bg-red-50 dark:bg-red-900/20 p-2 rounded overflow-auto max-h-40">
              {this.state.errorInfo && this.state.errorInfo.componentStack}
            </pre>
          </details>
        </div>
      );
    }

    return this.props.children;
  }
}

const LoadingWithTimeout = ({ timeoutMs = 10000, onConfirm }) => {
  const [showLongLoadingMessage, setShowLongLoadingMessage] = useState(false);
  const [waitingForConfirmation, setWaitingForConfirmation] = useState(false);
  const [showTip, setShowTip] = useState(false);

  useEffect(() => {
    // First show the "creating..." message after a short delay
    const timer = setTimeout(() => {
      setShowLongLoadingMessage(true);
    }, timeoutMs);

    // Then show the confirmation prompt after a longer delay
    const confirmationTimer = setTimeout(() => {
      setWaitingForConfirmation(true);
    }, timeoutMs + 5000);

    // Show a tip about numeric inputs after an even longer delay
    const tipTimer = setTimeout(() => {
      setShowTip(true);
    }, timeoutMs + 12000);

    return () => {
      clearTimeout(timer);
      clearTimeout(confirmationTimer);
      clearTimeout(tipTimer);
    };
  }, [timeoutMs]);

  const handleConfirmClick = () => {
    if (onConfirm) {
      onConfirm();
      setWaitingForConfirmation(false);
      setShowTip(false);
    }
  };

  return (
    <div className="chat-message ai-message flex items-start p-4 rounded-lg bg-primary-50 dark:bg-primary-900/30 border-l-4 border-primary-400 dark:border-primary-700 animate-loading-pulse">
      <div className="flex-1">
        <div className="flex items-center">
          <div className="w-8 h-8 bg-gradient-to-r from-primary-500 to-secondary-600 rounded-full flex items-center justify-center text-white text-sm font-bold mr-3">
            AI
          </div>
          <div className="flex-1">
            <p className="text-gray-900 dark:text-gray-100">
              <span className="loading-dots">Composing your music</span>
            </p>
            {showLongLoadingMessage && (
              <p className="text-sm text-gray-700 dark:text-gray-300 mt-2">
                Creating beautiful music takes time. The AI is working on your
                composition...
              </p>
            )}
            {waitingForConfirmation && (
              <div className="mt-3">
                <p className="text-sm text-amber-600 dark:text-amber-400 font-medium">
                  Waiting for confirmation to continue...
                </p>
                <button
                  onClick={handleConfirmClick}
                  className="mt-2 px-4 py-2 bg-gradient-to-r from-purple-500 to-indigo-600 text-white text-sm font-medium rounded-lg shadow-sm hover:shadow-md transition-all"
                >
                  Confirm Music Creation
                </button>
              </div>
            )}
            {showTip && (
              <div className="mt-3 p-2 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-100 dark:border-blue-800">
                <p className="text-xs text-blue-700 dark:text-blue-300">
                  <span className="font-medium">Tip:</span> If you're responding
                  with just a number (like a tempo value), make sure to also
                  click the "Confirm Music Creation" button above or add
                  "confirm" to your message.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

// Create a stable key function to prevent re-rendering of messages
function createStableKey(message, index) {
  // If message has an id, use it
  if (message.id) {
    return message.id;
  }

  // Otherwise create a key from actor/role and content hash
  const actor = message.actor || message.role || "unknown";
  const content =
    typeof message.content === "string"
      ? message.content.slice(0, 20)
      : typeof message.response === "string"
      ? message.response.slice(0, 20)
      : "unknown";

  // Create a stable ID based on actor, index and content
  return `${actor}-${index}-${content}`;
}

const ChatWindow = memo(
  ({
    conversation,
    loading,
    lastMessage,
    onConfirm,
    onContentChange,
    isDarkMode,
  }) => {
    const messagesEndRef = useRef(null);
    const [debugInfo, setDebugInfo] = useState(null);
    const [renderedMessageIds, setRenderedMessageIds] = useState(new Set());

    // Process conversation messages and convert response strings to content
    // Use useMemo to prevent unnecessary re-processing during polling
    const processedConversation = useMemo(() => {
      if (!conversation || !Array.isArray(conversation)) {
        console.log("No conversation array found");
        return [];
      }

      return conversation.map((msg, index) => {
        // Create a copy to avoid mutating the original
        const newMsg = { ...msg };

        // Generate a stable key for this message
        const stableKey = createStableKey(newMsg, index);
        newMsg.stableKey = stableKey;

        // Only process if we haven't seen this message before
        if (!renderedMessageIds.has(stableKey)) {
          // Ensure the message has either actor or role property
          if (!newMsg.actor && !newMsg.role) {
            newMsg.actor = "system";
          }

          // Handle agent/assistant messages
          if (newMsg.actor === "agent" || newMsg.role === "assistant") {
            // Check if the message has response but no content
            if (newMsg.response && !newMsg.content) {
              // If response is a string, use it directly
              if (typeof newMsg.response === "string") {
                try {
                  // Try to parse JSON response
                  const parsedResponse = JSON.parse(newMsg.response);
                  // If response has content field, use that
                  if (parsedResponse.content) {
                    newMsg.content = parsedResponse.content;
                    newMsg.originalResponse = newMsg.response; // store original
                  } else if (parsedResponse.text) {
                    // Some responses might use 'text' field instead
                    newMsg.content = parsedResponse.text;
                    newMsg.originalResponse = newMsg.response; // store original
                  } else if (
                    parsedResponse.response &&
                    typeof parsedResponse.response === "string"
                  ) {
                    // Get message directly from response field
                    newMsg.content = parsedResponse.response;
                    newMsg.originalResponse = newMsg.response; // store original
                  } else if (
                    parsedResponse.next === "question" &&
                    parsedResponse.response
                  ) {
                    // Handle AI questions/prompts
                    newMsg.content = parsedResponse.response;
                    newMsg.originalResponse = newMsg.response; // store original
                  } else {
                    // Otherwise, use the stringified object as content
                    newMsg.content =
                      typeof parsedResponse.response === "string"
                        ? parsedResponse.response
                        : JSON.stringify(parsedResponse);
                    newMsg.originalResponse = newMsg.response;
                  }
                } catch (e) {
                  // If not valid JSON, use the string directly
                  newMsg.content = newMsg.response;
                  newMsg.originalResponse = newMsg.response;
                }
              } else if (typeof newMsg.response === "object") {
                // If response is an object, check for content or text field
                if (newMsg.response.content) {
                  newMsg.content = newMsg.response.content;
                } else if (newMsg.response.text) {
                  newMsg.content = newMsg.response.text;
                } else if (
                  newMsg.response.response &&
                  typeof newMsg.response.response === "string"
                ) {
                  // Get message directly from response field
                  newMsg.content = newMsg.response.response;
                } else if (
                  newMsg.response.next === "question" &&
                  newMsg.response.response
                ) {
                  // Handle AI questions/prompts
                  newMsg.content = newMsg.response.response;
                } else {
                  // Otherwise use stringified object
                  newMsg.content = JSON.stringify(newMsg.response);
                }
                newMsg.originalResponse = newMsg.response;
              }
            }
          }

          // Handle user messages
          if (newMsg.actor === "user" || newMsg.role === "user") {
            // Ensure user messages have content
            if (!newMsg.content && newMsg.text) {
              newMsg.content = newMsg.text;
            } else if (!newMsg.content && newMsg.response) {
              newMsg.content =
                typeof newMsg.response === "string"
                  ? newMsg.response
                  : JSON.stringify(newMsg.response);
            }
          }
        }

        // Update debug info for the last message
        if (index === conversation.length - 1) {
          setDebugInfo(JSON.stringify(newMsg, null, 2));
        }

        return newMsg;
      });
    }, [conversation, renderedMessageIds]);

    // Update the set of rendered message IDs after processing
    useEffect(() => {
      if (processedConversation.length > 0) {
        const newIds = new Set(renderedMessageIds);
        processedConversation.forEach((msg) => {
          if (msg.stableKey) {
            newIds.add(msg.stableKey);
          }
        });

        if (newIds.size !== renderedMessageIds.size) {
          setRenderedMessageIds(newIds);
        }
      }
    }, [processedConversation, renderedMessageIds]);

    // Notify parent when content changes
    useEffect(() => {
      if (processedConversation.length > 0) {
        onContentChange && onContentChange();
      }
    }, [processedConversation.length, onContentChange]);

    // Scroll to bottom on new messages
    useEffect(() => {
      if (messagesEndRef.current) {
        messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
      }
    }, [processedConversation.length, loading]);

    // Show welcome message if no conversation
    const showWelcomeMessage =
      !loading &&
      (!processedConversation || processedConversation.length === 0);

    // Pass the onConfirm handler to message bubbles
    const handleConfirm = useCallback(() => {
      onConfirm && onConfirm();
    }, [onConfirm]);

    return (
      <ChatErrorBoundary>
        <div className="chat-window space-y-4">
          {showWelcomeMessage ? (
            <div className="welcome-message text-center py-8">
              <div className="welcome-icon mb-4">
                <div className="w-16 h-16 mx-auto bg-gradient-to-r from-purple-500 to-indigo-600 rounded-full flex items-center justify-center">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-8 w-8 text-white"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"
                    />
                  </svg>
                </div>
              </div>
              <h2 className="text-xl font-bold text-gray-800 dark:text-gray-200 mb-2">
                Welcome to Music Creation Studio
              </h2>
              <p className="text-gray-600 dark:text-gray-400 max-w-md mx-auto">
                Describe your music ideas, and our AI will help you compose
                beautiful music. Try asking for chord progressions, melodies, or
                complete compositions!
              </p>
            </div>
          ) : (
            <>
              {processedConversation.map((message, index) => (
                <MessageBubble
                  key={
                    message.stableKey ||
                    `${index}-${message.actor || message.role}`
                  }
                  message={message}
                  isLast={index === processedConversation.length - 1}
                  isDarkMode={isDarkMode}
                  onConfirm={handleConfirm}
                  isNew={!renderedMessageIds.has(message.stableKey)}
                />
              ))}
            </>
          )}

          {loading && <LoadingWithTimeout onConfirm={handleConfirm} />}

          {/* Debug information - hidden in production */}
          {process.env.NODE_ENV === "development" && debugInfo && (
            <div className="hidden">
              <pre className="text-xs bg-gray-100 p-2 rounded-md overflow-auto max-h-40">
                {debugInfo}
              </pre>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </ChatErrorBoundary>
    );
  }
);

ChatWindow.propTypes = {
  conversation: PropTypes.array,
  loading: PropTypes.bool,
  lastMessage: PropTypes.object,
  onConfirm: PropTypes.func,
  onContentChange: PropTypes.func,
  isDarkMode: PropTypes.bool,
};

ChatWindow.displayName = "ChatWindow";

export default ChatWindow;
