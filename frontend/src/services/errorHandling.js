/**
 * Utility functions for API error handling
 */

// Store recent errors to prevent duplicate toasts
const recentErrors = new Map();

// Clear errors older than 5 seconds periodically
setInterval(() => {
  const now = Date.now();
  recentErrors.forEach((timestamp, errorKey) => {
    if (now - timestamp > 5000) {
      recentErrors.delete(errorKey);
    }
  });
}, 10000);

// Enhanced error messages for specific error types
const ERROR_MESSAGES = {
  network: {
    offline: "You appear to be offline. Please check your internet connection.",
    timeout:
      "The request took too long to complete. This might be due to slow internet or server issues.",
    cors: "There was a security issue connecting to the service. This is likely a temporary problem.",
  },
  server: {
    maintenance:
      "Our system is currently undergoing maintenance. Please try again in a few minutes.",
    unavailable:
      "The service is temporarily unavailable. Our team has been notified.",
    overloaded:
      "Our servers are experiencing high load. Please try again shortly.",
  },
  authentication: {
    required: "Please sign in to continue.",
    expired: "Your session has expired. Please sign in again.",
    insufficient: "You don't have permission to perform this action.",
  },
  validation: {
    invalid:
      "The information you provided is invalid. Please check your input and try again.",
    missing: "Please fill in all required fields.",
    format: "One or more fields have an incorrect format.",
  },
  resource: {
    notFound: "The requested resource was not found.",
    deleted: "This resource has been deleted or is no longer available.",
    conflict: "There was a conflict with the current state of the resource.",
  },
  rate: {
    limited: "Too many requests. Please slow down and try again in a moment.",
  },
  unknown: "An unexpected error occurred. Our team has been notified.",
};

// Get a user-friendly error message based on the error
export const getErrorMessage = (error) => {
  // Network error
  if (!navigator.onLine) {
    return ERROR_MESSAGES.network.offline;
  }

  // Handle ApiError instances (from our API service)
  if (error.name === "ApiError") {
    switch (error.status) {
      case 400:
        return error.message || ERROR_MESSAGES.validation.invalid;
      case 401:
        return ERROR_MESSAGES.authentication.required;
      case 403:
        return ERROR_MESSAGES.authentication.insufficient;
      case 404:
        return error.message || ERROR_MESSAGES.resource.notFound;
      case 408:
        return ERROR_MESSAGES.network.timeout;
      case 409:
        return ERROR_MESSAGES.resource.conflict;
      case 422:
        return error.message || ERROR_MESSAGES.validation.format;
      case 429:
        return ERROR_MESSAGES.rate.limited;
      case 500:
        return error.message || ERROR_MESSAGES.server.unavailable;
      case 502:
      case 503:
      case 504:
        return error.message || ERROR_MESSAGES.server.maintenance;
      default:
        return error.message || ERROR_MESSAGES.unknown;
    }
  }

  // Handle specific error types
  if (error.name === "TypeError" && error.message.includes("NetworkError")) {
    return ERROR_MESSAGES.network.cors;
  }

  if (error.name === "TypeError" && error.message.includes("Failed to fetch")) {
    return ERROR_MESSAGES.network.offline;
  }

  if (
    error.name === "TimeoutError" ||
    (error.message && error.message.includes("timeout"))
  ) {
    return ERROR_MESSAGES.network.timeout;
  }

  if (error.name === "SyntaxError" && error.message.includes("JSON")) {
    return "The server response was invalid. Our team has been notified.";
  }

  // Handle regular Error objects
  return error.message || ERROR_MESSAGES.unknown;
};

// More detailed error type categorization
export const getErrorType = (error) => {
  if (!navigator.onLine) {
    return "offline";
  }

  if (error.name === "ApiError") {
    if (error.status >= 500) {
      return "server";
    }
    if (error.status === 401) {
      return "authentication";
    }
    if (error.status === 403) {
      return "authorization";
    }
    if (error.status === 404) {
      return "notFound";
    }
    if (error.status === 429) {
      return "rateLimit";
    }
    if (error.status === 408 || error.status === 504) {
      return "timeout";
    }
    if (error.status === 409) {
      return "conflict";
    }
    if (error.status === 422 || error.status === 400) {
      return "validation";
    }
    return "api";
  }

  // Detect network errors
  if (
    error.name === "TypeError" &&
    (error.message.includes("NetworkError") ||
      error.message.includes("Failed to fetch"))
  ) {
    return "network";
  }

  if (
    error.name === "TimeoutError" ||
    (error.message && error.message.includes("timeout"))
  ) {
    return "timeout";
  }

  if (error.name === "SyntaxError" && error.message.includes("JSON")) {
    return "parsing";
  }

  // Default to unknown error type
  return "unknown";
};

// Get guidance message to help the user resolve the error
export const getErrorGuidance = (error) => {
  const errorType = getErrorType(error);

  switch (errorType) {
    case "offline":
      return "Check your internet connection and try again when you're back online.";
    case "network":
      return "This appears to be a network issue. Check your connection, or try again in a few moments.";
    case "server":
      return "Our servers are experiencing issues. We've been notified and are working to fix it. Please try again later.";
    case "authentication":
      return "Please sign in again to continue.";
    case "authorization":
      return "If you believe you should have access, please contact your administrator.";
    case "notFound":
      return "The item you're looking for might have been moved or deleted. Please check the information and try again.";
    case "rateLimit":
      return "You've made too many requests in a short period. Please wait a moment before trying again.";
    case "timeout":
      return "The request took too long to complete. Try again or check your connection speed.";
    case "validation":
      return "Please check your input and ensure all required fields are correctly filled.";
    case "conflict":
      return "It looks like something changed while you were working. Please refresh and try again.";
    case "parsing":
      return "We received an invalid response from the server. Our team has been notified.";
    case "api":
      return "There was an issue with your request. Please check the information and try again.";
    default:
      return "If this problem persists, please contact support for assistance.";
  }
};

// More specific action recommendations based on error type
export const getErrorActions = (error) => {
  const errorType = getErrorType(error);

  switch (errorType) {
    case "offline":
    case "network":
      return [
        { label: "Check Connection", action: "checkConnection" },
        { label: "Retry", action: "retry" },
      ];
    case "server":
      return [
        { label: "Try Again Later", action: "wait" },
        { label: "Contact Support", action: "support" },
      ];
    case "authentication":
      return [{ label: "Sign In", action: "login" }];
    case "timeout":
      return [
        { label: "Try Again", action: "retry" },
        { label: "Report Issue", action: "report" },
      ];
    case "validation":
      return [{ label: "Edit Input", action: "edit" }];
    default:
      return [
        { label: "Try Again", action: "retry" },
        { label: "Contact Support", action: "support" },
      ];
  }
};

// Create a unique key for an error to prevent duplicate toasts
const getErrorKey = (error) => {
  const message = getErrorMessage(error);
  const type = getErrorType(error);
  return `${type}:${message}`;
};

// Log errors to console (in development) or to a service (in production)
export const logError = (error, context = {}) => {
  const errorType = getErrorType(error);
  const timestamp = new Date().toISOString();

  // Prepare error data for logging
  const errorData = {
    type: errorType,
    message: error.message,
    stack: error.stack,
    timestamp,
    context,
    userAgent: navigator.userAgent,
    url: window.location.href,
  };

  // Log based on environment
  if (process.env.NODE_ENV === "development") {
    console.error(`Error (${errorType}):`, error.message, error, context);
  } else {
    // In production, you might want to log to an error monitoring service like Sentry
    // Example: Sentry.captureException(error, { extra: context });
    console.error(`Error:`, error.message);

    // Implement error reporting to backend
    try {
      // Attempt to send error to backend for logging
      fetch("/api/log-error", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(errorData),
        // Don't wait for response or handle errors from this request
        keepalive: true,
      }).catch(() => {
        // Ignore errors from error logging
      });
    } catch (e) {
      // Ignore errors while sending error reports
    }
  }
};

// Handle an error with toasts, preventing duplicates
export const handleErrorWithToast = (error, toastFn) => {
  if (!toastFn || typeof toastFn !== "function") {
    // If no toast function is provided, just log the error
    logError(error);
    return;
  }

  const message = getErrorMessage(error);
  const guidance = getErrorGuidance(error);
  const actions = getErrorActions(error);
  const fullMessage = `${message} ${guidance}`;

  // Create a unique key for this error
  const errorKey = getErrorKey(error);

  // Check if we've shown this error recently (within 5 seconds)
  const now = Date.now();
  if (!recentErrors.has(errorKey) || now - recentErrors.get(errorKey) > 5000) {
    // Show error toast
    toastFn(fullMessage, {
      autoClose: true,
      duration: 8000, // Longer duration for errors
      // If we have error details for debugging, pass them to the toast
      details: process.env.NODE_ENV === "development" ? error.stack : null,
      // If we have specific actions, provide the first one
      actionLabel: actions.length > 0 ? actions[0].label : null,
      onAction: () => {
        if (actions.length > 0) {
          handleErrorAction(actions[0].action, error);
        }
      },
    });

    // Mark this error as recently shown
    recentErrors.set(errorKey, now);
  }

  // Always log the error
  logError(error);
};

// Handle error actions
const handleErrorAction = (action, error) => {
  switch (action) {
    case "retry":
      // Could trigger the original operation again
      window.dispatchEvent(
        new CustomEvent("retryOperation", { detail: { error } })
      );
      break;
    case "login":
      // Redirect to login page
      window.location.href = "/login";
      break;
    case "edit":
      // Focus back on the form
      window.dispatchEvent(new CustomEvent("focusForm", { detail: { error } }));
      break;
    case "support":
      // Open support modal or redirect to support page
      window.open("https://support.example.com", "_blank");
      break;
    case "report":
      // Open a bug report form
      window.dispatchEvent(
        new CustomEvent("openBugReport", { detail: { error } })
      );
      break;
    case "checkConnection":
      // Refresh the page to test connection
      window.location.reload();
      break;
    default:
      console.log("No handler for action:", action);
  }
};
