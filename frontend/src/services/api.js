const API_BASE_URL = "http://127.0.0.1:8000";

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
    this.name = "ApiError";
  }
}

async function handleResponse(response) {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new ApiError(
      errorData.message ||
        `API error: ${response.status} ${response.statusText}`,
      response.status
    );
  }

  try {
    return await response.json();
  } catch (error) {
    console.error("Error parsing JSON response:", error);
    throw new ApiError("Invalid response format from server", 500);
  }
}

export const apiService = {
  async getConversationHistory() {
    try {
      const res = await fetch(`${API_BASE_URL}/get-conversation-history`, {
        // Add timeout to avoid long-hanging requests
        signal: AbortSignal.timeout(7000), // Increase timeout to 7 seconds for more reliability
      });

      // Special handling for 404 errors during startup
      if (res.status === 404) {
        console.warn(
          "Received 404 when fetching conversation history - returning empty array"
        );
        return { messages: [] }; // Return empty messages array instead of failing
      }

      return handleResponse(res);
    } catch (error) {
      // Handle timeout/abort errors
      if (error.name === "AbortError") {
        console.warn("Request timed out while fetching conversation history");
        return { messages: [] }; // Return empty instead of failing the UI
      }

      // If this is a network error (not a server response), return empty to avoid breaking the UI
      if (!error.status) {
        console.warn("Network error fetching conversation history:", error);
        return { messages: [] };
      }

      throw new ApiError(
        "Failed to fetch conversation history",
        error.status || 500
      );
    }
  },

  async getWorkflowState() {
    try {
      const res = await fetch(`${API_BASE_URL}/get-workflow-state`, {
        signal: AbortSignal.timeout(7000), // Increase timeout to 7 seconds for more reliability
      });

      if (res.status === 404) {
        console.log("Workflow doesn't exist (404 response)");
        return { exists: false }; // Workflow doesn't exist
      }

      // For 500 errors, we might still have a workflow - get the response and check
      if (res.status === 500) {
        try {
          const errorData = await res.json();
          console.warn("Received 500 from workflow state endpoint:", errorData);
          // If the error mentions the query handler not found, the workflow likely exists
          // but is using an older version without the query handler
          if (
            errorData.detail &&
            errorData.detail.includes(
              "Query handler for 'get_workflow_state' expected but not found"
            )
          ) {
            console.log("Query handler missing but workflow exists");
            return {
              exists: true,
              error: "Query handler missing",
              message_count: -1, // Indicate we don't know the count
              waiting_for_confirm: false, // Conservative default
            };
          }
        } catch (parseError) {
          // JSON parse error - just continue to return exists:false
          console.warn("Failed to parse 500 error response:", parseError);
        }
      }

      try {
        const data = await handleResponse(res);
        return { ...data, exists: true };
      } catch (parseError) {
        console.warn("Error parsing workflow state response:", parseError);
        // Still return exists:true to prevent duplicate workflow creation
        return { exists: true, error: "Parse error" };
      }
    } catch (error) {
      console.warn("Failed to get workflow state:", error);

      // For timeout errors, return exists:true to be conservative
      if (error.name === "AbortError") {
        return {
          exists: true,
          error: "Request timed out",
        };
      }

      // For other errors, return exists:false to allow fresh start
      return { exists: false, error: error.message };
    }
  },

  async sendMessage(message) {
    if (!message?.trim()) {
      throw new ApiError("Message cannot be empty", 400);
    }

    try {
      const res = await fetch(
        `${API_BASE_URL}/send-prompt?prompt=${encodeURIComponent(message)}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          signal: AbortSignal.timeout(10000), // 10 second timeout
        }
      );
      return handleResponse(res);
    } catch (error) {
      if (error.name === "AbortError") {
        throw new ApiError("Send message request timed out", 408);
      }
      throw new ApiError(
        `Failed to send message: ${error.message || "Unknown error"}`,
        error.status || 500
      );
    }
  },

  async startWorkflow() {
    try {
      const res = await fetch(`${API_BASE_URL}/start-workflow`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        // Add timeout to avoid long-hanging requests
        signal: AbortSignal.timeout(10000), // 10 second timeout for starting workflow
      });
      return handleResponse(res);
    } catch (error) {
      // Handle timeout errors
      if (error.name === "AbortError") {
        throw new ApiError("Workflow start request timed out", 408);
      }

      throw new ApiError(
        `Failed to start workflow: ${error.message || "Unknown error"}`,
        error.status || 500
      );
    }
  },

  async endChat() {
    try {
      const res = await fetch(`${API_BASE_URL}/end-chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        // Add timeout to avoid long-hanging requests
        signal: AbortSignal.timeout(5000), // 5 second timeout
      });
      return handleResponse(res);
    } catch (error) {
      // Handle timeout errors
      if (error.name === "AbortError") {
        throw new ApiError("End chat request timed out", 408);
      }

      throw new ApiError(
        `Failed to end chat: ${error.message || "Unknown error"}`,
        error.status || 500
      );
    }
  },

  async confirm() {
    try {
      const res = await fetch(`${API_BASE_URL}/confirm`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });
      return handleResponse(res);
    } catch (error) {
      throw new ApiError("Failed to confirm action", error.status || 500);
    }
  },

  async runTool(toolName, toolArgs) {
    try {
      const res = await fetch(`${API_BASE_URL}/run-tool`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          tool_name: toolName,
          tool_args: toolArgs,
        }),
      });
      return handleResponse(res);
    } catch (error) {
      throw new ApiError(
        `Failed to run tool: ${toolName}`,
        error.status || 500
      );
    }
  },

  async getTemporalStatus() {
    // Track how many times we've called this method for retry purposes
    if (!window.temporalCheckRetryCount) {
      window.temporalCheckRetryCount = 0;
    }

    try {
      const res = await fetch(`${API_BASE_URL}/get-temporal-status`, {
        signal: AbortSignal.timeout(5000), // 5 second timeout
      });

      // Reset retry count on success
      window.temporalCheckRetryCount = 0;

      if (!res.ok) {
        console.warn(`Temporal status check failed with status: ${res.status}`);
        return { available: false };
      }

      const result = await res.json();

      if (result.refreshed) {
        console.log("Temporal client was refreshed successfully");
      }

      return result;
    } catch (error) {
      console.warn("Error checking Temporal status:", error);

      // If we've had multiple failures in a row, try waiting longer
      // between retries to avoid overwhelming the server
      window.temporalCheckRetryCount++;

      if (window.temporalCheckRetryCount > 3) {
        // After 3 failures, wait longer between retries
        await new Promise((resolve) => setTimeout(resolve, 2000));
      }

      return { available: false, error: error.message };
    }
  },
};
