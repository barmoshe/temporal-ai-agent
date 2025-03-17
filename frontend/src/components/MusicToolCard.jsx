import React, { useState } from "react";

const MusicToolCard = ({
  title,
  description,
  icon,
  gradient = "from-purple-600 to-indigo-700",
  onSelect,
  examples = [],
}) => {
  const [isHovered, setIsHovered] = useState(false);

  // Generate waveform animation for the card
  const renderWaveform = () => (
    <div className="flex items-center h-6 mt-2 justify-start opacity-70">
      {Array.from({ length: 4 }).map((_, i) => (
        <div
          key={i}
          className="waveform-bar"
          style={{
            animationDelay: `${i * 0.2}s`,
            height: "15px",
          }}
        />
      ))}
    </div>
  );

  return (
    <div
      className={`music-card relative overflow-hidden cursor-pointer transition-all duration-300`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onClick={() => onSelect && onSelect()}
    >
      {/* Gradient header */}
      <div className={`p-4 bg-gradient-to-r ${gradient} text-white relative`}>
        <div className="flex items-center">
          <div className="text-3xl mr-3">{icon}</div>
          <h3 className="font-semibold text-lg">{title}</h3>
        </div>
        {renderWaveform()}
      </div>

      {/* Content */}
      <div className="p-4">
        <p className="text-gray-600 dark:text-gray-400 mb-4">{description}</p>

        {/* Examples section */}
        {examples.length > 0 && (
          <div className="mt-2">
            <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Examples:
            </h4>
            <div className="space-y-2">
              {examples.map((example, index) => (
                <button
                  key={index}
                  className="w-full text-left text-sm p-2 rounded-md bg-purple-50 dark:bg-purple-900/20 text-purple-700 dark:text-purple-300 hover:bg-purple-100 dark:hover:bg-purple-900/30 transition-colors"
                  onClick={(e) => {
                    e.stopPropagation();
                    onSelect && onSelect(example);
                  }}
                >
                  {example}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Use Tool button - appears on hover */}
      <div
        className={`absolute bottom-0 left-0 right-0 p-3 bg-gradient-to-t from-white dark:from-gray-800 to-transparent flex justify-center transition-opacity duration-300 ${
          isHovered ? "opacity-100" : "opacity-0"
        }`}
      >
        <button
          className="music-btn px-4 py-2 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-full text-sm font-medium shadow-md"
          onClick={(e) => {
            e.stopPropagation();
            onSelect && onSelect();
          }}
        >
          Use This Tool
        </button>
      </div>
    </div>
  );
};

export default MusicToolCard;
