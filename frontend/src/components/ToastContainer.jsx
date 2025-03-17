import React, { useState, useEffect, useCallback } from "react";
import ReactDOM from "react-dom";
import Toast from "./Toast";

/**
 * Helper function to generate a truly unique ID
 * Combines timestamp with a random number to ensure uniqueness
 */
const generateUniqueId = () => {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
};

/**
 * ToastContainer component manages multiple toast notifications
 * It creates a portal to render toasts outside the normal DOM hierarchy
 */
const ToastContainer = () => {
  const [toasts, setToasts] = useState([]);

  // Remove a toast by its id
  const removeToast = useCallback((id) => {
    setToasts((prevToasts) => prevToasts.filter((toast) => toast.id !== id));
  }, []);

  // Create a new toast notification
  const addToast = useCallback(
    ({ message, type = "info", duration = 5000, autoClose = true }) => {
      // Use a truly unique ID instead of just Date.now()
      const id = generateUniqueId();
      setToasts((prevToasts) => [
        ...prevToasts,
        { id, message, type, duration, autoClose },
      ]);
      return id;
    },
    []
  );

  // Expose the addToast and removeToast methods to the window object
  useEffect(() => {
    window.toastManager = {
      addToast,
      removeToast,
      success: (message, options) =>
        addToast({ message, type: "success", ...options }),
      error: (message, options) =>
        addToast({ message, type: "error", ...options }),
      warning: (message, options) =>
        addToast({ message, type: "warning", ...options }),
      info: (message, options) =>
        addToast({ message, type: "info", ...options }),
    };

    return () => {
      delete window.toastManager;
    };
  }, [addToast, removeToast]);

  // Create a portal to render toasts
  return ReactDOM.createPortal(
    <div className="fixed top-4 right-4 z-50 flex flex-col gap-3 pointer-events-none">
      {toasts.map((toast) => (
        <div key={toast.id} className="pointer-events-auto">
          <Toast
            message={toast.message}
            type={toast.type}
            duration={toast.duration}
            autoClose={toast.autoClose}
            onClose={() => removeToast(toast.id)}
          />
        </div>
      ))}
    </div>,
    document.body
  );
};

export { ToastContainer };

// Create a reusable hook for adding toasts from any component
export const useToast = () => {
  const addToast = useCallback((props) => {
    if (window.toastManager) {
      return window.toastManager.addToast(props);
    }
    return null;
  }, []);

  const success = useCallback(
    (message, options) => addToast({ message, type: "success", ...options }),
    [addToast]
  );

  const error = useCallback(
    (message, options) => addToast({ message, type: "error", ...options }),
    [addToast]
  );

  const warning = useCallback(
    (message, options) => addToast({ message, type: "warning", ...options }),
    [addToast]
  );

  const info = useCallback(
    (message, options) => addToast({ message, type: "info", ...options }),
    [addToast]
  );

  return {
    addToast,
    success,
    error,
    warning,
    info,
  };
};

export default ToastContainer;
