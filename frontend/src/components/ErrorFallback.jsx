import React, { useState } from "react";
import { getErrorGuidance } from "../services/errorHandling";

/**
 * ErrorFallback provides a consistent way to show error states in the UI
 * This can be used outside of error boundaries for expected errors
 */
const ErrorFallback = ({
  error,
  resetError,
  title = "Something went wrong",
  message,
  actionLabel = "Try Again",
  variant = "error", // error, warning, info
  compact = false,
  helpLinks = [], // Array of {label, url} objects for relevant help resources
  retryCount = 0, // How many times the user has retried this operation
}) => {
  const [isExpanded, setIsExpanded] = useState(false);

  // Determine styles based on variant
  const styles = {
    error: {
      container:
        "bg-red-50 dark:bg-red-900/30 border-red-200 dark:border-red-700",
      icon: "text-red-500 dark:text-red-400",
      title: "text-red-700 dark:text-red-300",
      button: "bg-red-600 hover:bg-red-700 text-white",
    },
    warning: {
      container:
        "bg-yellow-50 dark:bg-yellow-900/30 border-yellow-200 dark:border-yellow-700",
      icon: "text-yellow-500 dark:text-yellow-400",
      title: "text-yellow-700 dark:text-yellow-300",
      button: "bg-yellow-600 hover:bg-yellow-700 text-white",
    },
    info: {
      container:
        "bg-blue-50 dark:bg-blue-900/30 border-blue-200 dark:border-blue-700",
      icon: "text-blue-500 dark:text-blue-400",
      title: "text-blue-700 dark:text-blue-300",
      button: "bg-blue-600 hover:bg-blue-700 text-white",
    },
  };

  const style = styles[variant] || styles.error;

  // Determine what content to show
  const errorMessage =
    message ||
    (error && error.message) ||
    "An unexpected error occurred. Please try again.";

  // Get guidance for this error type
  const guidance = error ? getErrorGuidance(error) : "";

  // Show a different message if retried multiple times
  const showAlternativeSuggestion = retryCount >= 3;

  // Get Stack trace if available
  const errorStack = error && error.stack;
  const shortStack = errorStack
    ? errorStack.split("\n").slice(0, 3).join("\n")
    : null;

  return (
    <div
      className={`rounded-lg border shadow-sm ${style.container} ${
        compact ? "p-3" : "p-5"
      }`}
      role="alert"
      aria-live="polite"
    >
      <div className="flex items-start">
        {/* Icon */}
        <div className={`flex-shrink-0 ${compact ? "mr-2" : "mr-4"}`}>
          <div
            className={`${
              compact ? "w-8 h-8" : "w-10 h-10"
            } rounded-full flex items-center justify-center ${style.icon}`}
          >
            {variant === "error" && (
              <svg
                className={compact ? "w-5 h-5" : "w-6 h-6"}
                fill="currentColor"
                viewBox="0 0 20 20"
                aria-hidden="true"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clipRule="evenodd"
                />
              </svg>
            )}
            {variant === "warning" && (
              <svg
                className={compact ? "w-5 h-5" : "w-6 h-6"}
                fill="currentColor"
                viewBox="0 0 20 20"
                aria-hidden="true"
              >
                <path
                  fillRule="evenodd"
                  d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                  clipRule="evenodd"
                />
              </svg>
            )}
            {variant === "info" && (
              <svg
                className={compact ? "w-5 h-5" : "w-6 h-6"}
                fill="currentColor"
                viewBox="0 0 20 20"
                aria-hidden="true"
              >
                <path
                  fillRule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                  clipRule="evenodd"
                />
              </svg>
            )}
          </div>
        </div>

        {/* Content */}
        <div className="flex-1">
          <h3
            className={`${
              compact ? "text-sm font-semibold" : "text-lg font-bold"
            } ${style.title} mb-1`}
          >
            {title}
          </h3>
          <div
            className={`text-gray-600 dark:text-gray-300 ${
              compact ? "text-xs" : "text-sm"
            }`}
          >
            <p>{errorMessage}</p>

            {guidance && (
              <p
                className={`mt-2 ${
                  compact ? "text-xs" : "text-sm"
                } font-medium`}
              >
                {guidance}
              </p>
            )}

            {showAlternativeSuggestion && (
              <div className="mt-2 p-2 bg-gray-100 dark:bg-gray-800 rounded-md">
                <p className={`${compact ? "text-xs" : "text-sm"} font-medium`}>
                  It seems this issue persists. You might want to try:
                </p>
                <ul className="list-disc ml-5 mt-1 text-xs space-y-1">
                  <li>Refreshing the page</li>
                  <li>Checking your internet connection</li>
                  <li>Trying again later</li>
                  {helpLinks.length > 0 && (
                    <li>Checking our help resources below</li>
                  )}
                </ul>
              </div>
            )}

            {/* Help resources */}
            {helpLinks.length > 0 && (
              <div className={`${compact ? "mt-2" : "mt-3"}`}>
                <p className={`${compact ? "text-xs" : "text-sm"} font-medium`}>
                  Helpful resources:
                </p>
                <ul className="mt-1 space-y-1">
                  {helpLinks.map((link, index) => (
                    <li key={index}>
                      <a
                        href={link.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className={`${
                          compact ? "text-xs" : "text-sm"
                        } text-blue-600 dark:text-blue-400 hover:underline`}
                      >
                        {link.label} ↗
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* Collapsible error details for debugging */}
          {shortStack && (
            <div className={`${compact ? "mt-2" : "mt-3"}`}>
              <button
                type="button"
                onClick={() => setIsExpanded(!isExpanded)}
                className={`inline-flex items-center ${
                  compact ? "text-xs" : "text-sm"
                } text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200`}
              >
                <svg
                  className={`${
                    isExpanded ? "rotate-90" : ""
                  } w-4 h-4 mr-1 transition-transform`}
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 5l7 7-7 7"
                  />
                </svg>
                {isExpanded ? "Hide" : "Show"} technical details
              </button>

              {isExpanded && (
                <div className="mt-2 p-2 bg-gray-100 dark:bg-gray-800 rounded-md overflow-auto max-h-40">
                  <pre className="whitespace-pre-wrap font-mono text-xs text-gray-700 dark:text-gray-300">
                    {shortStack}
                  </pre>
                </div>
              )}
            </div>
          )}

          {/* Buttons */}
          {resetError && (
            <div
              className={`${compact ? "mt-2" : "mt-4"} flex flex-wrap gap-2`}
            >
              <button
                onClick={resetError}
                className={`${style.button} ${
                  compact ? "text-xs py-1 px-2" : "text-sm py-2 px-4"
                } rounded-md transition-colors shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2`}
              >
                {actionLabel}
              </button>

              <button
                onClick={() => window.location.reload()}
                className={`bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 ${
                  compact ? "text-xs py-1 px-2" : "text-sm py-2 px-4"
                } rounded-md transition-colors shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2`}
              >
                Refresh Page
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ErrorFallback;
