import React from "react";

const LoadingIndicator = () => {
  return (
    <div className="flex flex-col items-center justify-center">
      <div className="flex space-x-2">
        <div className="flex items-center space-x-1">
          <div
            className="h-2 w-2 bg-blue-500 rounded-full animate-bounce"
            style={{ animationDelay: "0ms" }}
          ></div>
          <div
            className="h-2 w-2 bg-blue-500 rounded-full animate-bounce"
            style={{ animationDelay: "150ms" }}
          ></div>
          <div
            className="h-2 w-2 bg-blue-500 rounded-full animate-bounce"
            style={{ animationDelay: "300ms" }}
          ></div>
        </div>
      </div>
      <p className="text-xs text-gray-500 mt-2 italic">Agent is thinking...</p>
    </div>
  );
};

export default LoadingIndicator;
