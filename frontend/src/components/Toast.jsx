import React, { useState, useEffect, useRef } from "react";

// Icons for different toast types
const icons = {
  success: (
    <svg
      className="w-5 h-5"
      fill="currentColor"
      viewBox="0 0 20 20"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      <path
        fillRule="evenodd"
        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
        clipRule="evenodd"
      ></path>
    </svg>
  ),
  error: (
    <svg
      className="w-5 h-5"
      fill="currentColor"
      viewBox="0 0 20 20"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      <path
        fillRule="evenodd"
        d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
        clipRule="evenodd"
      ></path>
    </svg>
  ),
  warning: (
    <svg
      className="w-5 h-5"
      fill="currentColor"
      viewBox="0 0 20 20"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      <path
        fillRule="evenodd"
        d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
        clipRule="evenodd"
      ></path>
    </svg>
  ),
  info: (
    <svg
      className="w-5 h-5"
      fill="currentColor"
      viewBox="0 0 20 20"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      <path
        fillRule="evenodd"
        d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
        clipRule="evenodd"
      ></path>
    </svg>
  ),
};

// Toast background colors for different types
const toastStyles = {
  success: {
    bg: "bg-green-50 dark:bg-green-900/30",
    border: "border-green-200 dark:border-green-800",
    icon: "text-green-500 dark:text-green-400",
    text: "text-green-800 dark:text-green-100",
    progressBar: "bg-green-500 dark:bg-green-400",
  },
  error: {
    bg: "bg-red-50 dark:bg-red-900/30",
    border: "border-red-200 dark:border-red-800",
    icon: "text-red-500 dark:text-red-400",
    text: "text-red-800 dark:text-red-100",
    progressBar: "bg-red-500 dark:bg-red-400",
  },
  warning: {
    bg: "bg-yellow-50 dark:bg-yellow-900/30",
    border: "border-yellow-200 dark:border-yellow-800",
    icon: "text-yellow-500 dark:text-yellow-400",
    text: "text-yellow-800 dark:text-yellow-100",
    progressBar: "bg-yellow-500 dark:bg-yellow-400",
  },
  info: {
    bg: "bg-blue-50 dark:bg-blue-900/30",
    border: "border-blue-200 dark:border-blue-800",
    icon: "text-blue-500 dark:text-blue-400",
    text: "text-blue-800 dark:text-blue-100",
    progressBar: "bg-blue-500 dark:bg-blue-400",
  },
};

const Toast = ({
  message,
  type = "info",
  duration = 5000,
  onClose,
  autoClose = true,
  showProgressBar = true,
  actionLabel = null,
  onAction = null,
  details = null,
}) => {
  const [isVisible, setIsVisible] = useState(true);
  const [progress, setProgress] = useState(100);
  const [showDetails, setShowDetails] = useState(false);
  const style = toastStyles[type] || toastStyles.info;
  const toastRef = useRef(null);

  // Handle keyboard navigation and accessibility
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === "Escape") {
        handleClose();
      }
    };

    document.addEventListener("keydown", handleKeyDown);
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, []);

  useEffect(() => {
    if (!autoClose) return;

    const interval = setInterval(() => {
      setProgress((prev) => {
        const newProgress = prev - 100 / (duration / 100);
        return newProgress <= 0 ? 0 : newProgress;
      });
    }, 100);

    const timer = setTimeout(() => {
      handleClose();
    }, duration);

    return () => {
      clearTimeout(timer);
      clearInterval(interval);
    };
  }, [duration, onClose, autoClose]);

  // Focus the toast when it appears
  useEffect(() => {
    if (toastRef.current) {
      toastRef.current.focus();
    }
  }, []);

  const handleClose = () => {
    setIsVisible(false);
    setTimeout(() => onClose(), 300); // Wait for animation to finish
  };

  if (!isVisible) return null;

  return (
    <div
      ref={toastRef}
      className={`flex max-w-md w-full shadow-lg rounded-lg border overflow-hidden ${
        style.bg
      } ${style.border} transition-all duration-300 transform ${
        isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-2"
      }`}
      role="alert"
      aria-live="assertive"
      tabIndex={0}
    >
      <div className="flex-shrink-0 flex items-center justify-center w-12 bg-opacity-10 dark:bg-opacity-20">
        <div className={`p-2 rounded-full ${style.icon}`}>{icons[type]}</div>
      </div>

      <div className="w-0 flex-1 p-4 pr-8 relative">
        <div className={`font-medium ${style.text}`}>{message}</div>

        {details && (
          <div className="mt-1">
            <button
              type="button"
              onClick={() => setShowDetails(!showDetails)}
              className={`inline-flex items-center text-xs ${style.text} opacity-80 hover:opacity-100 focus:outline-none focus:underline`}
            >
              {showDetails ? "Hide details" : "Show details"}
              <svg
                className={`ml-1 h-3 w-3 transform transition-transform ${
                  showDetails ? "rotate-180" : ""
                }`}
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </button>
            {showDetails && (
              <div className="mt-2 text-xs p-2 bg-white/30 dark:bg-black/20 rounded border border-current border-opacity-10 font-mono overflow-auto max-h-24">
                {details}
              </div>
            )}
          </div>
        )}

        {actionLabel && onAction && (
          <div className="mt-2">
            <button
              type="button"
              onClick={onAction}
              className={`px-3 py-1 text-xs font-medium rounded-md ${style.text} bg-opacity-20 hover:bg-opacity-30 focus:outline-none focus:ring-2 focus:ring-offset-1 bg-current transition-colors`}
            >
              {actionLabel}
            </button>
          </div>
        )}

        {showProgressBar && (
          <div className="absolute bottom-0 left-0 h-1 w-full bg-gray-200 dark:bg-gray-700">
            <div
              className={`h-full ${style.progressBar} transition-all duration-100`}
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        )}
      </div>

      <button
        onClick={handleClose}
        className={`flex-shrink-0 flex p-2 ${style.text} opacity-70 hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-100 dark:focus:ring-offset-gray-800`}
        aria-label="Close notification"
      >
        <svg
          className="h-4 w-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            d="M6 18L18 6M6 6l12 12"
          />
        </svg>
      </button>
    </div>
  );
};

export default Toast;
