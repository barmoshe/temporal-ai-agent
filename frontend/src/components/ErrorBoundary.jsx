import React from "react";
import ErrorFallback from "./ErrorFallback";

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
      retryCount: 0,
    };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo,
    });
    console.error("ErrorBoundary caught an error:", error, errorInfo);

    // Report to error tracking service if available
    if (window.reportError && typeof window.reportError === "function") {
      window.reportError(error, errorInfo);
    }
  }

  handleReset = () => {
    this.setState((prevState) => ({
      hasError: false,
      error: null,
      errorInfo: null,
      retryCount: prevState.retryCount + 1,
    }));

    if (this.props.resetError) {
      this.props.resetError();
    }
  };

  render() {
    if (this.state.hasError) {
      // Generate helpful links based on error type
      const helpLinks = [];

      // If we have documentation links provided by props, use those
      if (this.props.helpLinks && Array.isArray(this.props.helpLinks)) {
        helpLinks.push(...this.props.helpLinks);
      }

      // Add default help links based on error type if we can detect it
      const errorMessage = this.state.error?.message?.toLowerCase() || "";

      if (
        errorMessage.includes("network") ||
        errorMessage.includes("fetch") ||
        errorMessage.includes("connection")
      ) {
        helpLinks.push({
          label: "Network Troubleshooting Guide",
          url: "https://support.example.com/network-issues",
        });
      }

      if (
        errorMessage.includes("permission") ||
        errorMessage.includes("access") ||
        errorMessage.includes("denied")
      ) {
        helpLinks.push({
          label: "Permissions Help",
          url: "https://support.example.com/permissions",
        });
      }

      // Always add general help link if none were added
      if (helpLinks.length === 0) {
        helpLinks.push({
          label: "Help Center",
          url: "https://support.example.com",
        });
      }

      // Use our enhanced ErrorFallback component
      return (
        <ErrorFallback
          error={this.state.error}
          resetError={this.handleReset}
          title={this.props.fallbackTitle || "Something went wrong"}
          message={
            this.props.fallbackMessage ||
            "We encountered an unexpected error. Please try again."
          }
          actionLabel={this.props.actionLabel || "Try Again"}
          variant="error"
          retryCount={this.state.retryCount}
          helpLinks={helpLinks}
        />
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
