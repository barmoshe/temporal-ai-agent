import React from "react";

const TabsManager = ({
  tabs,
  activeTabId,
  onTabChange,
  onTabClose,
  onNewTab,
}) => {
  // Handle tab selection
  const handleTabClick = (tabId) => {
    onTabChange(tabId);
  };

  // Handle tab close
  const handleTabClose = (e, tabId) => {
    e.stopPropagation(); // Prevent tab selection when closing
    onTabClose(tabId);
  };

  // Handle new tab creation
  const handleNewTabClick = () => {
    onNewTab();
  };

  return (
    <div className="chat-tabs-container w-full bg-white dark:bg-gray-900 shadow-md">
      <div className="flex overflow-x-auto scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-gray-700 scrollbar-track-transparent">
        {tabs.map((tab) => (
          <div
            key={tab.id}
            onClick={() => handleTabClick(tab.id)}
            className={`flex items-center px-4 py-2.5 max-w-[200px] min-w-[140px] cursor-pointer transition-all duration-150 border-r border-gray-200 dark:border-gray-700 ${
              activeTabId === tab.id
                ? "bg-gradient-to-b from-purple-50 to-white dark:from-purple-900/20 dark:to-gray-900 text-purple-700 dark:text-purple-400"
                : "bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700"
            }`}
          >
            <div className="flex items-center space-x-2 w-full overflow-hidden">
              <div
                className={`flex-shrink-0 ${
                  activeTabId === tab.id
                    ? "text-purple-600 dark:text-purple-400"
                    : "text-gray-500 dark:text-gray-400"
                }`}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-4 w-4"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"
                  />
                </svg>
              </div>
              <div className="truncate flex-grow text-sm font-medium">
                {tab.title || "New Composition"}
              </div>
              <button
                onClick={(e) => handleTabClose(e, tab.id)}
                className="ml-2 flex-shrink-0 opacity-70 hover:opacity-100 hover:bg-gray-300 dark:hover:bg-gray-600 rounded-full p-1 transition-all"
                aria-label="Close tab"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-3.5 w-3.5"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                    clipRule="evenodd"
                  />
                </svg>
              </button>
            </div>
          </div>
        ))}
        <button
          onClick={handleNewTabClick}
          className="flex-shrink-0 flex items-center justify-center min-w-[40px] px-3 border-r border-gray-200 dark:border-gray-700 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
          aria-label="New composition tab"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-5 w-5 text-gray-600 dark:text-gray-400"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fillRule="evenodd"
              d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
              clipRule="evenodd"
            />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default TabsManager;
