import React, { useRef, useEffect, useState } from "react";
import PropTypes from "prop-types";
import remarkGfm from "remark-gfm";
import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { atomDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import MidiBubblePlayer from "./MidiBubblePlayer";

const MessageBubble = ({
  message,
  isDarkMode = false,
  isNew = true,
  onConfirm,
  showConfirmButton = false,
}) => {
  // Element ref for the message bubble
  const bubbleRef = useRef(null);
  const [confirmVisible, setConfirmVisible] = useState(false);

  // Check for content that might need confirmation
  useEffect(() => {
    if (message && message.content) {
      const content = message.content.toLowerCase();
      const needsConfirmation =
        (content.includes("melody") && content.includes("generate")) ||
        (content.includes("tempo") && content.includes("bpm")) ||
        content.includes("would you like me to generate this midi sequence");

      setConfirmVisible(needsConfirmation || showConfirmButton);
    }
  }, [message, showConfirmButton]);

  // Handle confirm button click
  const handleConfirmClick = () => {
    if (onConfirm) {
      onConfirm();
      setConfirmVisible(false);
    }
  };

  // Apply animation class only when the message first appears
  useEffect(() => {
    if (bubbleRef.current && isNew) {
      // Add the class that triggers the animation
      bubbleRef.current.classList.add("appear-once");

      // Optional: Remove animation class after it completes to prevent any future re-animations
      const animationTimeout = setTimeout(() => {
        if (bubbleRef.current) {
          bubbleRef.current.classList.remove("appear-once");
        }
      }, 600); // Animation duration + small buffer

      return () => clearTimeout(animationTimeout);
    }
  }, [isNew]);

  // Extract the message content from different possible formats
  const getMessageContent = () => {
    if (!message) return "";

    // Debug message format if needed
    // console.log("Message format in bubble:", message);

    if (message.content) {
      return message.content;
    } else if (message.response) {
      if (typeof message.response === "string") {
        try {
          // Try parsing as JSON
          const parsed = JSON.parse(message.response);
          if (parsed?.content) {
            return parsed.content;
          }
          if (parsed?.message) {
            return parsed.message;
          }
          // Check for 'response' property that contains actual message text
          if (parsed?.response && typeof parsed.response === "string") {
            return parsed.response;
          }
          // If next is question, this is likely a prompt from the AI
          if (parsed?.next === "question" && parsed?.response) {
            return parsed.response;
          }
          return message.response;
        } catch (e) {
          // Not JSON, just return the string
          return message.response;
        }
      } else if (typeof message.response === "object") {
        if (message.response.content) {
          return message.response.content;
        }
        if (message.response.message) {
          return message.response.message;
        }
        // Direct response field that contains the message
        if (message.response.response) {
          return message.response.response;
        }
        // Return formatted JSON for object responses
        return JSON.stringify(message.response, null, 2);
      }
    }

    // Fallback for unknown formats
    return JSON.stringify(message, null, 2);
  };

  // Determine message role/actor
  const getMessageRole = () => {
    if (!message) return "unknown";

    if (message.role) {
      return message.role;
    } else if (message.actor) {
      return message.actor === "agent" ? "assistant" : message.actor;
    } else if (message.sender) {
      return message.sender;
    }

    return "unknown";
  };

  const isUser = getMessageRole() === "user";
  const isAssistant =
    getMessageRole() === "assistant" || getMessageRole() === "agent";
  const content = getMessageContent();

  // Custom renderer for code blocks
  const CodeBlock = ({ node, inline, className, children, ...props }) => {
    const match = /language-(\w+)/.exec(className || "");
    const language = match ? match[1] : "javascript";

    return !inline ? (
      <div className="code-block-container relative">
        <div className="code-header bg-gray-800 text-gray-300 text-xs px-4 py-1 rounded-t-md flex justify-between items-center">
          <span>{language}</span>
          <button
            onClick={() => {
              navigator.clipboard.writeText(
                String(children).replace(/\n$/, "")
              );
            }}
            className="text-gray-400 hover:text-white focus:outline-none"
            title="Copy code"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-4 w-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
              />
            </svg>
          </button>
        </div>
        <SyntaxHighlighter
          style={atomDark}
          language={language}
          PreTag="div"
          className="rounded-b-md overflow-auto"
          showLineNumbers={true}
          {...props}
        >
          {String(children).replace(/\n$/, "")}
        </SyntaxHighlighter>
      </div>
    ) : (
      <code className="bg-gray-200 dark:bg-gray-800 px-1 py-0.5 rounded font-mono text-sm">
        {children}
      </code>
    );
  };

  // Determine if a tool output contains MIDI data
  const hasMidiData = (response) => {
    if (!response) return false;

    // Check if this is a MidiCreationTool response
    return (
      response.midi_base64 &&
      (response.notes_summary || response.note_count) &&
      typeof response.tempo !== "undefined"
    );
  };

  const renderConfirmButton = () => {
    if (!confirmVisible || getMessageRole() !== "assistant") return null;

    return (
      <div className="mt-4 flex justify-end">
        <button
          onClick={handleConfirmClick}
          className="px-4 py-2 rounded-lg bg-gradient-to-r from-purple-500 to-indigo-600 text-white text-sm font-medium shadow-sm hover:shadow-md transition-all"
        >
          Confirm Music Creation
        </button>
      </div>
    );
  };

  return (
    <div
      ref={bubbleRef}
      className={`message-bubble p-4 rounded-lg ${
        isUser
          ? "user-message bg-secondary-100 dark:bg-secondary-900/30 border-l-4 border-secondary-400 dark:border-secondary-700"
          : "ai-message bg-primary-50 dark:bg-primary-900/30 border-l-4 border-primary-400 dark:border-primary-700"
      } mb-4`}
    >
      <div className="flex items-start">
        <div
          className={`avatar w-8 h-8 ${
            isUser
              ? "bg-gradient-to-r from-secondary-500 to-secondary-700"
              : "bg-gradient-to-r from-primary-500 to-primary-700"
          } rounded-full flex items-center justify-center text-white text-sm font-bold mr-3`}
        >
          {isUser ? "You" : "AI"}
        </div>

        <div className="flex-1 overflow-auto">
          <div
            className={`markdown-content ${
              isAssistant ? "prose dark:prose-invert" : ""
            } max-w-none`}
          >
            {isAssistant ? (
              <ReactMarkdown
                children={content}
                remarkPlugins={[remarkGfm]}
                components={{
                  code: CodeBlock,
                  // Add custom styling for other elements
                  h1: ({ node, ...props }) => (
                    <h1
                      className="text-xl font-bold my-4 text-gray-900 dark:text-gray-100"
                      {...props}
                    />
                  ),
                  h2: ({ node, ...props }) => (
                    <h2
                      className="text-lg font-bold my-3 text-gray-900 dark:text-gray-100"
                      {...props}
                    />
                  ),
                  h3: ({ node, ...props }) => (
                    <h3
                      className="text-md font-bold my-2 text-gray-900 dark:text-gray-100"
                      {...props}
                    />
                  ),
                  a: ({ node, ...props }) => (
                    <a
                      className="text-blue-600 dark:text-blue-400 hover:underline"
                      target="_blank"
                      rel="noreferrer"
                      {...props}
                    />
                  ),
                  ul: ({ node, ...props }) => (
                    <ul className="list-disc pl-5 my-2" {...props} />
                  ),
                  ol: ({ node, ...props }) => (
                    <ol className="list-decimal pl-5 my-2" {...props} />
                  ),
                  li: ({ node, ...props }) => (
                    <li
                      className="my-1 text-gray-800 dark:text-gray-200"
                      {...props}
                    />
                  ),
                  p: ({ node, ...props }) => (
                    <p
                      className="my-2 text-gray-800 dark:text-gray-200"
                      {...props}
                    />
                  ),
                  table: ({ node, ...props }) => (
                    <div className="overflow-x-auto my-4">
                      <table
                        className="min-w-full divide-y divide-gray-300 dark:divide-gray-700"
                        {...props}
                      />
                    </div>
                  ),
                  thead: ({ node, ...props }) => (
                    <thead
                      className="bg-gray-100 dark:bg-gray-800"
                      {...props}
                    />
                  ),
                  tbody: ({ node, ...props }) => (
                    <tbody
                      className="divide-y divide-gray-200 dark:divide-gray-800"
                      {...props}
                    />
                  ),
                  th: ({ node, ...props }) => (
                    <th
                      className="px-3 py-2 text-left text-sm font-semibold text-gray-900 dark:text-gray-100"
                      {...props}
                    />
                  ),
                  td: ({ node, ...props }) => (
                    <td
                      className="px-3 py-2 text-sm text-gray-800 dark:text-gray-200"
                      {...props}
                    />
                  ),
                }}
              />
            ) : (
              <p className="text-gray-900 dark:text-gray-100 whitespace-pre-wrap">
                {content}
              </p>
            )}
          </div>

          {/* Check and render MIDI player if message contains MIDI data */}
          {isAssistant &&
            message?.response &&
            hasMidiData(message.response) && (
              <div className="mt-4 border-t border-gray-200 dark:border-gray-700 pt-4">
                <MidiBubblePlayer
                  midiData={message.response}
                  title={message.response.title || "MIDI Sequence"}
                />
              </div>
            )}

          {/* Display music tool outputs if present */}
          {isAssistant && message?.response?.music_output && (
            <div className="mt-4 border-t border-gray-200 dark:border-gray-700 pt-4">
              <div className="music-output bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm border border-gray-100 dark:border-gray-700">
                <h3 className="font-bold text-lg mb-2 text-gray-900 dark:text-white">
                  {message.response.music_output.title || "Music Output"}
                </h3>

                {message.response.music_output.description && (
                  <p className="mb-3 text-gray-800 dark:text-gray-200">
                    {message.response.music_output.description}
                  </p>
                )}

                {message.response.music_output.content && (
                  <div className="mb-3 whitespace-pre-wrap">
                    {message.response.music_output.content}
                  </div>
                )}

                {message.response.music_output.notation && (
                  <div className="mb-3 font-mono text-sm bg-white dark:bg-gray-900 p-3 rounded border border-gray-300 dark:border-gray-700 overflow-x-auto">
                    <pre>{message.response.music_output.notation}</pre>
                  </div>
                )}

                {message.response.music_output.preview_url && (
                  <div className="mt-3">
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                      Audio Preview:
                    </p>
                    <audio
                      controls
                      className="w-full"
                      src={message.response.music_output.preview_url}
                    />
                  </div>
                )}

                {/* Add visualization if available */}
                {message.response.music_output.visualization_url && (
                  <div className="mt-3">
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                      Visualization:
                    </p>
                    <img
                      src={message.response.music_output.visualization_url}
                      alt="Music Visualization"
                      className="w-full rounded-lg"
                    />
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Display tool confirmation if needed */}
          {isAssistant &&
            message?.response?.tool === "RunCommand" &&
            message?.response?.confirm && (
              <div className="mt-4 border-t border-gray-200 dark:border-gray-700 pt-4">
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                  I need to run a command to proceed:
                </p>
                <div className="bg-gray-100 dark:bg-gray-800 rounded p-2 mb-2 font-mono text-sm overflow-x-auto">
                  {message.response.command}
                </div>
                <button
                  onClick={() => {
                    onConfirm && onConfirm();
                  }}
                  className="px-4 py-1 bg-green-500 hover:bg-green-600 text-white rounded"
                >
                  Approve
                </button>
              </div>
            )}
        </div>
      </div>
      {renderConfirmButton()}
    </div>
  );
};

MessageBubble.propTypes = {
  message: PropTypes.object.isRequired,
  isDarkMode: PropTypes.bool,
  isNew: PropTypes.bool,
  onConfirm: PropTypes.func,
  showConfirmButton: PropTypes.bool,
};

export default MessageBubble;
