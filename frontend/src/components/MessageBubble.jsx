import React, { memo } from "react";

const MessageBubble = memo(({ message, fallback = "", isUser = false }) => {
  const displayText = message.response?.trim() ? message.response : fallback;
  const timestamp = new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });

  if (displayText.startsWith("###")) {
    return null;
  }

  const renderTextWithLinks = (text) => {
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    const parts = text.split(urlRegex);

    return parts.map((part, index) => {
      if (urlRegex.test(part)) {
        return (
          <a
            key={index}
            href={part}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:text-blue-600 underline transition-colors"
            aria-label={`External link to ${part}`}
          >
            {part}
          </a>
        );
      }
      return part;
    });
  };

  return (
    <div
      className={`flex w-full mb-4 ${isUser ? "justify-end" : "justify-start"}`}
    >
      {!isUser && (
        <div className="flex-shrink-0 mr-3">
          <div className="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center text-white">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              className="w-5 h-5"
            >
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13v6l5 3-1 1.73-6-3.53V7z" />
            </svg>
          </div>
        </div>
      )}

      <div
        className={`max-w-[75%] flex flex-col ${
          isUser ? "items-end" : "items-start"
        }`}
      >
        <div
          className={`
                    px-4 py-3 rounded-2xl shadow-sm 
                    ${
                      isUser
                        ? "bg-gradient-to-br from-blue-500 to-blue-600 text-white"
                        : "bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700"
                    }
                    break-words text-sm md:text-base
                `}
        >
          <div
            className={`${
              isUser ? "text-white" : "text-gray-800 dark:text-gray-200"
            }`}
          >
            {renderTextWithLinks(displayText)}
          </div>
        </div>
        <div className="text-xs text-gray-500 mt-1 px-1">{timestamp}</div>
      </div>

      {isUser && (
        <div className="flex-shrink-0 ml-3">
          <div className="w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center text-gray-600">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              className="w-5 h-5"
            >
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13v6l5 3-1 1.73-6-3.53V7h2z" />
            </svg>
          </div>
        </div>
      )}
    </div>
  );
});

MessageBubble.displayName = "MessageBubble";

export default MessageBubble;
