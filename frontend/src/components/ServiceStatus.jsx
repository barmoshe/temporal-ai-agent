import React, { useState, useEffect, useCallback, useRef } from "react";
import { useToast } from "./ToastContainer";

/**
 * ServiceStatus component monitors API availability and displays a notification
 * when backend services are unavailable
 */
const ServiceStatus = () => {
  const [isApiAvailable, setIsApiAvailable] = useState(true);
  const [isChecking, setIsChecking] = useState(true);
  const lastToastTimeRef = useRef(0); // Track when the last toast was shown
  const toast = useToast();

  // Debounced toast function to prevent too many notifications
  const showDebouncedToast = useCallback(
    (type, message, options = {}) => {
      const now = Date.now();
      const minInterval = 5000; // Minimum time between toasts (5 seconds)

      if (now - lastToastTimeRef.current > minInterval) {
        lastToastTimeRef.current = now;

        if (type === "error") {
          toast.error(message, options);
        } else if (type === "success") {
          toast.success(message, options);
        }
      }
    },
    [toast]
  );

  // Check API availability with retry mechanism
  const checkApiStatus = useCallback(async () => {
    try {
      setIsChecking(true);
      const response = await fetch("http://127.0.0.1:8000/", {
        method: "GET",
        headers: { Accept: "application/json" },
        // Use a short timeout to avoid hanging
        signal: AbortSignal.timeout(3000),
      });

      const wasUnavailable = !isApiAvailable;
      const isNowAvailable = response.ok;

      setIsApiAvailable(isNowAvailable);

      // If service was down but now is back up, show a success toast
      if (wasUnavailable && isNowAvailable) {
        showDebouncedToast("success", "Backend services are now available!");
      }
    } catch (error) {
      const wasAvailable = isApiAvailable;
      setIsApiAvailable(false);

      // Only show the error toast when the service first becomes unavailable
      if (wasAvailable) {
        showDebouncedToast(
          "error",
          "Backend services are currently unavailable. Some features may not work correctly.",
          { duration: 10000 }
        );
      }
    } finally {
      setIsChecking(false);
    }
  }, [isApiAvailable, showDebouncedToast]);

  // Check API availability periodically
  useEffect(() => {
    // Check immediately with a small initial delay to avoid race conditions
    const initialCheckTimer = setTimeout(() => {
      checkApiStatus();
    }, 1000);

    // Then check every 10 seconds
    const intervalId = setInterval(checkApiStatus, 10000);

    return () => {
      clearTimeout(initialCheckTimer);
      clearInterval(intervalId);
    };
  }, [checkApiStatus]);

  // Don't render anything if the API is available or we're still checking
  if (isApiAvailable || isChecking) {
    return null;
  }

  // Render a service unavailable indicator
  return (
    <div className="fixed bottom-4 left-4 z-50 max-w-xs bg-red-50 dark:bg-red-900/40 border border-red-200 dark:border-red-800 rounded-lg shadow-lg p-3 pointer-events-auto">
      <div className="flex items-center">
        <div className="flex-shrink-0">
          <div className="w-8 h-8 rounded-full bg-red-100 dark:bg-red-800 flex items-center justify-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5 text-red-600 dark:text-red-300"
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
        </div>
        <div className="ml-3">
          <h3 className="text-sm font-medium text-red-800 dark:text-red-200">
            Service Unavailable
          </h3>
          <div className="mt-1 text-xs text-red-700 dark:text-red-300">
            <p>
              Backend services are currently offline. Some features may not work
              correctly.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ServiceStatus;
