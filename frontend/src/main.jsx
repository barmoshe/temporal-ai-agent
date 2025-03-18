import React from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import App from "./pages/App";
import "./index.css"; // Tailwind imports

// Global error handling for uncaught errors
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      hasError: false,
      errorInfo: null,
      resetAttempted: false,
    };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Global error caught:", error, errorInfo);
    this.setState({ errorInfo: errorInfo });
  }

  resetApplication = () => {
    // Try to restart the application
    this.setState({ resetAttempted: true }, () => {
      // Clear any localStorage data that might be corrupting the app
      try {
        localStorage.removeItem("temporal_app_state");
        console.log("Application state reset");
      } catch (e) {
        console.error("Failed to clear localStorage:", e);
      }

      // After a brief delay, reload the page
      setTimeout(() => {
        window.location.reload();
      }, 500);
    });
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900 p-4">
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg max-w-md w-full">
            <div className="text-red-500 mb-4">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-10 w-10 mx-auto"
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
            </div>
            <h2 className="text-xl font-bold text-center mb-2 dark:text-white">
              {this.state.resetAttempted
                ? "Restarting Application..."
                : "Something went wrong"}
            </h2>
            <p className="text-gray-600 dark:text-gray-300 text-center mb-4">
              {this.state.resetAttempted
                ? "Please wait while we restart the application..."
                : "The application encountered an error. Please use the button below to restore functionality."}
            </p>
            {!this.state.resetAttempted && (
              <button
                onClick={this.resetApplication}
                className="w-full py-2 px-4 bg-blue-500 hover:bg-blue-600 text-white rounded-md transition-colors"
                disabled={this.state.resetAttempted}
              >
                Reset Application
              </button>
            )}
            {this.state.resetAttempted && (
              <div className="flex justify-center mt-4">
                <div className="spinner w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
              </div>
            )}
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}

// Initialize the application
function initApp() {
  const container = document.getElementById("root");
  if (!container) {
    console.error("Root element not found!");
    return;
  }

  try {
    const root = createRoot(container);

    root.render(
      <ErrorBoundary>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<App />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </ErrorBoundary>
    );
  } catch (error) {
    console.error("Failed to initialize application:", error);
    // Fallback to a basic error page if React fails to render
    container.innerHTML = `
      <div style="display:flex;justify-content:center;align-items:center;height:100vh;text-align:center;">
        <div>
          <h1 style="color:red;margin-bottom:20px;">Critical Application Error</h1>
          <p>The application failed to initialize. Please refresh the page.</p>
          <button 
            style="background:blue;color:white;padding:10px 20px;border:none;border-radius:4px;margin-top:20px;"
            onclick="window.location.reload()">
            Refresh Page
          </button>
        </div>
      </div>
    `;
  }
}

// Add event listener for unhandled promise rejections
window.addEventListener("unhandledrejection", (event) => {
  console.error("Unhandled Promise Rejection:", event.reason);
});

// Start the application
initApp();
