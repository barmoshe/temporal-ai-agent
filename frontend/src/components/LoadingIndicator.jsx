import React from "react";
import PropTypes from "prop-types";

const LoadingIndicator = ({
  size = "medium",
  color = "purple",
  label = "Loading...",
}) => {
  // Size classes
  const sizeClasses = {
    small: "h-8 w-8",
    medium: "h-12 w-12",
    large: "h-16 w-16",
  };

  // Color classes
  const colorClasses = {
    purple: "text-purple-600 dark:text-purple-400",
    indigo: "text-indigo-600 dark:text-indigo-400",
    blue: "text-blue-600 dark:text-blue-400",
    pink: "text-pink-600 dark:text-pink-400",
  };

  return (
    <div className="flex flex-col items-center justify-center">
      <div className={`${sizeClasses[size]} relative animate-spin`}>
        <svg
          className={`${colorClasses[color]}`}
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

        {/* Music note overlay */}
        <div className="absolute inset-0 flex items-center justify-center">
          <svg
            className="h-1/2 w-1/2 text-white dark:text-gray-800"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="currentColor"
          >
            <path d="M9 17.5c0 .83-.67 1.5-1.5 1.5S6 18.33 6 17.5 6.67 16 7.5 16 9 16.67 9 17.5ZM17 15.5c0 .83-.67 1.5-1.5 1.5s-1.5-.67-1.5-1.5.67-1.5 1.5-1.5 1.5.67 1.5 1.5ZM9 10V3h10v7.5c0 .83-.67 1.5-1.5 1.5s-1.5-.67-1.5-1.5V9H9Z" />
          </svg>
        </div>
      </div>

      {label && (
        <p className={`mt-2 text-sm ${colorClasses[color]}`}>
          <span className="loading-dots">{label}</span>
        </p>
      )}
    </div>
  );
};

LoadingIndicator.propTypes = {
  size: PropTypes.oneOf(["small", "medium", "large"]),
  color: PropTypes.oneOf(["purple", "indigo", "blue", "pink"]),
  label: PropTypes.string,
};

export default LoadingIndicator;
