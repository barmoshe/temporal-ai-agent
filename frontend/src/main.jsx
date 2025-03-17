import React from "react";
import { createRoot } from "react-dom/client";
import App from "./pages/App";
import "./index.css"; // Tailwind imports
import { ToastContainer } from "./components/ToastContainer";
import ErrorBoundary from "./components/ErrorBoundary";
import ServiceStatus from "./components/ServiceStatus";

const container = document.getElementById("root");
const root = createRoot(container);

root.render(
  <ErrorBoundary fallbackMessage="Something went wrong with the application. Please refresh the page.">
    <App />
    <ToastContainer />
    <ServiceStatus />
  </ErrorBoundary>
);
