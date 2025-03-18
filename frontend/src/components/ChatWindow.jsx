import React, { memo, useCallback, useEffect, useRef } from "react";
import LLMResponse from "./LLMResponse";
import MessageBubble from "./MessageBubble";
import LoadingIndicator from "./LoadingIndicator";

class ChatErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ChatWindow error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="text-red-500 p-6 text-center bg-red-50 dark:bg-red-900/20 rounded-lg shadow-inner mx-4">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-8 w-8 mx-auto mb-2"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
            />
          </svg>
          <p className="font-medium">
            Something went wrong with the chat display.
          </p>
          <p className="text-sm mt-1">
            Please terminate the workflow and try again.
          </p>
        </div>
      );
    }
    return this.props.children;
  }
}

const safeParse = (str) => {
  try {
    return typeof str === "string" ? JSON.parse(str) : str;
  } catch (err) {
    console.error("safeParse error:", err, "Original string:", str);
    return str;
  }
};

const Message = memo(
  ({ msg, idx, isLastMessage, onConfirm, onContentChange }) => {
    const { actor, response } = msg;

    if (actor === "user") {
      return <MessageBubble message={{ response }} isUser />;
    }

    if (actor === "agent") {
      const data = safeParse(response);
      return (
        <LLMResponse
          data={data}
          onConfirm={onConfirm}
          isLastMessage={isLastMessage}
          onHeightChange={onContentChange}
        />
      );
    }

    if (actor === "system") {
      // Handle system messages (like continue-as-new notifications)
      return (
        <div className="flex justify-center my-4 animate-fadeIn">
          <div className="bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 py-2 px-4 rounded-lg shadow-sm border border-blue-200 dark:border-blue-800 text-sm max-w-md">
            <div className="flex items-center">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5 mr-2 flex-shrink-0"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <span>
                {typeof response === "string"
                  ? response
                  : response.message ||
                    response.content ||
                    "System notification"}
              </span>
            </div>
          </div>
        </div>
      );
    }

    if (actor === "conversation_summary") {
      // Handle conversation summaries (used in continue-as-new)
      const summary =
        typeof response === "string"
          ? response.startsWith("{")
            ? JSON.parse(response).summary
            : response
          : response.summary || "Conversation continued from previous session";

      return (
        <div className="flex justify-center my-4 animate-fadeIn">
          <div className="bg-gray-100 dark:bg-gray-800 p-3 rounded-lg border border-gray-200 dark:border-gray-700 text-sm max-w-md w-full">
            <div className="text-gray-500 dark:text-gray-400 text-center">
              <div className="font-medium mb-1">Conversation Summary</div>
              <p>{summary}</p>
            </div>
          </div>
        </div>
      );
    }

    return null;
  }
);

Message.displayName = "Message";

const ChatWindow = memo(
  ({ conversation, loading, onConfirm, onContentChange }) => {
    const messagesEndRef = useRef(null);

    const validateConversation = useCallback((conv) => {
      if (!Array.isArray(conv)) {
        console.error(
          "ChatWindow expected conversation to be an array, got:",
          conv
        );
        return [];
      }
      return conv;
    }, []);

    const filtered = validateConversation(conversation).filter((msg) => {
      const { actor } = msg;
      return actor === "user" || actor === "agent";
    });

    // Auto-scroll to the bottom when messages change
    useEffect(() => {
      if (messagesEndRef.current) {
        messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
      }
    }, [filtered, loading]);

    return (
      <ChatErrorBoundary>
        <div className="flex-grow flex flex-col">
          <div className="flex-grow flex flex-col p-4 overflow-y-auto space-y-1 scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-gray-600">
            {filtered.length === 0 && !loading && (
              <div className="flex items-center justify-center h-full opacity-70">
                <div className="text-center p-6 rounded-lg bg-gray-50 dark:bg-gray-800/50 max-w-md mx-auto">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-12 w-12 mx-auto mb-3 text-gray-400"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={1.5}
                      d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                    />
                  </svg>
                  <h3 className="text-lg font-medium mb-1">
                    Start a new conversation
                  </h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Type a message below to begin chatting with the AI agent.
                  </p>
                </div>
              </div>
            )}

            {filtered.map((msg, idx) => (
              <div
                key={`${msg.actor}-${idx}-${
                  typeof msg.response === "string"
                    ? msg.response
                    : msg.response?.response
                }`}
                className="animate-fadeIn"
              >
                <Message
                  msg={msg}
                  idx={idx}
                  isLastMessage={idx === filtered.length - 1}
                  onConfirm={onConfirm}
                  onContentChange={onContentChange}
                />
              </div>
            ))}

            {loading && (
              <div className="py-4 flex justify-center animate-fadeIn">
                <LoadingIndicator />
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>
      </ChatErrorBoundary>
    );
  }
);

ChatWindow.displayName = "ChatWindow";

export default ChatWindow;
