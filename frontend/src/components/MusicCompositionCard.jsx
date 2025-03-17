import React, { useState, useRef, useEffect } from "react";

const MusicCompositionCard = ({
  title,
  description,
  audioUrl,
  waveformUrl,
  details = {},
  stems = [],
}) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const audioRef = useRef(null);
  const progressBarRef = useRef(null);

  // Set up audio event listeners
  useEffect(() => {
    const audioElement = audioRef.current;
    if (!audioElement) return;

    const handleTimeUpdate = () => {
      setCurrentTime(audioElement.currentTime);
    };

    const handleDurationChange = () => {
      setDuration(audioElement.duration);
    };

    const handleEnded = () => {
      setIsPlaying(false);
      setCurrentTime(0);
      audioElement.currentTime = 0;
    };

    audioElement.addEventListener("timeupdate", handleTimeUpdate);
    audioElement.addEventListener("durationchange", handleDurationChange);
    audioElement.addEventListener("ended", handleEnded);

    return () => {
      audioElement.removeEventListener("timeupdate", handleTimeUpdate);
      audioElement.removeEventListener("durationchange", handleDurationChange);
      audioElement.removeEventListener("ended", handleEnded);
    };
  }, []);

  // Format time in MM:SS
  const formatTime = (time) => {
    if (isNaN(time)) return "0:00";
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60)
      .toString()
      .padStart(2, "0");
    return `${minutes}:${seconds}`;
  };

  // Handle play/pause
  const togglePlay = () => {
    if (isPlaying) {
      audioRef.current.pause();
    } else {
      audioRef.current.play();
    }
    setIsPlaying(!isPlaying);
  };

  // Handle seeking in the progress bar
  const handleSeek = (e) => {
    const rect = progressBarRef.current.getBoundingClientRect();
    const pos = (e.clientX - rect.left) / rect.width;
    const newTime = pos * duration;
    audioRef.current.currentTime = newTime;
    setCurrentTime(newTime);
  };

  // Generate dynamic waveform visualization
  const renderVisualizer = () => {
    return (
      <div className="music-visualizer h-16 my-3">
        {Array.from({ length: 40 }).map((_, i) => {
          const height = Math.sin((i / 40) * Math.PI) * 70 + 20;
          const isActive = i / 40 <= currentTime / duration;

          return (
            <div
              key={i}
              className={`visualizer-bar transition-all duration-300 ${
                isActive ? "opacity-100" : "opacity-50"
              }`}
              style={{
                height: `${height}%`,
                backgroundColor: isActive
                  ? "var(--primary-color)"
                  : "var(--accent-light)",
              }}
            />
          );
        })}
      </div>
    );
  };

  return (
    <div className="music-card bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden border border-purple-100 dark:border-purple-900/30">
      {/* Hidden audio element */}
      <audio ref={audioRef} src={audioUrl} preload="metadata" />

      {/* Header */}
      <div className="p-4 bg-gradient-to-r from-purple-600 to-indigo-700 text-white">
        <h3 className="text-lg font-semibold">
          {title || "Music Composition"}
        </h3>
        <p className="text-sm opacity-90">{description}</p>
      </div>

      {/* Controls */}
      <div className="p-4">
        {/* Waveform visualization */}
        {waveformUrl ? (
          <img
            src={waveformUrl}
            alt="Audio waveform"
            className="w-full h-24 object-cover rounded-lg mb-3"
          />
        ) : (
          <div
            ref={progressBarRef}
            className="cursor-pointer"
            onClick={handleSeek}
          >
            {renderVisualizer()}
          </div>
        )}

        {/* Playback controls */}
        <div className="flex items-center justify-between mb-4">
          <button
            className="w-10 h-10 rounded-full bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center text-purple-600 dark:text-purple-400 hover:bg-purple-200 dark:hover:bg-purple-900/50 transition-colors"
            onClick={togglePlay}
          >
            {isPlaying ? (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z"
                  clipRule="evenodd"
                />
              </svg>
            ) : (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z"
                  clipRule="evenodd"
                />
              </svg>
            )}
          </button>

          {/* Time display */}
          <div className="text-xs text-gray-600 dark:text-gray-400">
            {formatTime(currentTime)} / {formatTime(duration)}
          </div>

          {/* Download button */}
          <a
            href={audioUrl}
            download
            className="text-purple-600 dark:text-purple-400 hover:text-purple-700 dark:hover:text-purple-300 transition-colors"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fillRule="evenodd"
                d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
                clipRule="evenodd"
              />
            </svg>
          </a>
        </div>

        {/* Composition details */}
        {Object.keys(details).length > 0 && (
          <div className="bg-gray-50 dark:bg-gray-700/30 rounded-lg p-3 mb-4 text-sm">
            <h4 className="font-medium text-gray-700 dark:text-gray-300 mb-2">
              Composition Details
            </h4>
            <div className="grid grid-cols-2 gap-2">
              {Object.entries(details).map(([key, value]) => (
                <div key={key}>
                  <span className="text-gray-500 dark:text-gray-400">
                    {key}:{" "}
                  </span>
                  <span className="text-gray-800 dark:text-gray-200">
                    {value}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Stems section */}
        {stems.length > 0 && (
          <div>
            <h4 className="font-medium text-gray-700 dark:text-gray-300 mb-2">
              Instrument Stems
            </h4>
            <div className="space-y-2">
              {stems.map((stem, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between bg-gray-50 dark:bg-gray-700/30 rounded-lg p-2"
                >
                  <div className="flex items-center">
                    <span className="text-lg mr-2">
                      {stem.instrument === "drums"
                        ? "🥁"
                        : stem.instrument === "bass"
                        ? "🎸"
                        : stem.instrument === "piano"
                        ? "🎹"
                        : stem.instrument === "guitar"
                        ? "🎸"
                        : stem.instrument === "vocals"
                        ? "🎤"
                        : stem.instrument === "strings"
                        ? "🎻"
                        : "🎵"}
                    </span>
                    <span className="text-gray-800 dark:text-gray-200">
                      {stem.instrument}
                    </span>
                  </div>
                  <a
                    href={stem.url}
                    download
                    className="text-purple-600 dark:text-purple-400 hover:text-purple-700 dark:hover:text-purple-300"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-5 w-5"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path
                        fillRule="evenodd"
                        d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </a>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MusicCompositionCard;
