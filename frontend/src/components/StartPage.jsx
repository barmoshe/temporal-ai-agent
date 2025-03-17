import React, { useState, useEffect } from "react";
import { apiService } from "../services/api";
import ErrorFallback from "./ErrorFallback";
import LoadingIndicator from "./LoadingIndicator";

const StartPage = ({ onStart, isDarkMode }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [retryCount, setRetryCount] = useState(0);
  const [serviceStatus, setServiceStatus] = useState({
    isAvailable: false,
    message: "Checking service status...",
  });
  const [selectedGenre, setSelectedGenre] = useState("");

  // Check if the service is available
  useEffect(() => {
    const checkServiceStatus = async () => {
      setLoading(true);
      try {
        // Try to get conversation history as a simple API check
        await apiService.getConversationHistory();
        setServiceStatus({
          isAvailable: true,
          message: "Service is available and ready!",
        });
        setError(null);
      } catch (err) {
        console.error("Service status check failed:", err);
        setServiceStatus({
          isAvailable: false,
          message: "Service is currently unavailable.",
        });
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    checkServiceStatus();
  }, [retryCount]);

  const handleRetry = () => {
    setRetryCount((prev) => prev + 1);
  };

  const handleStart = () => {
    if (serviceStatus.isAvailable && onStart) {
      onStart(selectedGenre);
    }
  };

  // List of popular music genres for quick selection
  const musicGenres = [
    {
      id: "pop",
      name: "Pop",
      icon: "🎵",
      color: "from-pink-500 to-purple-500",
    },
    {
      id: "rock",
      name: "Rock",
      icon: "🎸",
      color: "from-red-500 to-orange-500",
    },
    {
      id: "hiphop",
      name: "Hip Hop",
      icon: "🎤",
      color: "from-yellow-500 to-amber-500",
    },
    {
      id: "electronic",
      name: "Electronic",
      icon: "🎛️",
      color: "from-blue-500 to-cyan-500",
    },
    {
      id: "jazz",
      name: "Jazz",
      icon: "🎷",
      color: "from-purple-500 to-indigo-500",
    },
    {
      id: "classical",
      name: "Classical",
      icon: "🎻",
      color: "from-green-500 to-emerald-500",
    },
  ];

  // Generate animated waveform
  const renderWaveform = () => (
    <div className="flex items-center justify-center gap-1 h-8 my-4">
      {Array.from({ length: 9 }).map((_, i) => (
        <div
          key={i}
          className="waveform-bar h-8"
          style={{
            animationDelay: `${i * 0.1}s`,
            backgroundColor:
              i % 2 === 0 ? "var(--primary-color)" : "var(--accent-color)",
          }}
        />
      ))}
    </div>
  );

  return (
    <div className={`h-full w-full flex flex-col ${isDarkMode ? "dark" : ""}`}>
      <div className="flex-grow flex flex-col items-center justify-center p-6 md:p-10 bg-gradient-to-b from-white to-purple-50 dark:from-gray-900 dark:to-gray-800 text-gray-800 dark:text-gray-200">
        <div className="max-w-3xl w-full">
          {/* Animated Header with Music Theme */}
          <div className="text-center mb-8">
            <div className="inline-block relative">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-24 w-24 mx-auto text-purple-600 dark:text-purple-400 mb-4 animate-pulse"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.5"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"
                />
              </svg>
              <div className="absolute top-0 right-0 h-5 w-5 bg-accent-500 rounded-full animate-ping"></div>
            </div>
            <h1 className="text-5xl md:text-6xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-purple-600 to-indigo-600 dark:from-purple-400 dark:to-indigo-400 font-poppins">
              Music Creation Studio
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
              Create professional music with the power of AI. Generate melodies,
              chord progressions, drum patterns, and complete compositions in
              seconds.
            </p>

            {renderWaveform()}
          </div>

          {/* Status Card */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 mb-8 border border-purple-100 dark:border-purple-900/30">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <svg
                className="w-6 h-6 mr-2 text-purple-500"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
              System Status
            </h2>

            {loading ? (
              <div className="flex flex-col items-center py-4">
                <LoadingIndicator size="medium" />
                <p className="mt-4 text-gray-600 dark:text-gray-400">
                  Checking service availability...
                </p>
              </div>
            ) : error ? (
              <ErrorFallback
                error={error}
                resetError={handleRetry}
                title="Connection Error"
                message="We're having trouble connecting to the service."
                actionLabel="Retry Connection"
                variant="warning"
              />
            ) : (
              <div className="flex flex-col items-center py-4">
                <div className="rounded-full bg-green-100 dark:bg-green-900/30 p-3 mb-4">
                  <svg
                    className="w-8 h-8 text-green-500 dark:text-green-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                </div>
                <p className="text-lg font-medium text-gray-800 dark:text-gray-200 mb-6">
                  {serviceStatus.message}
                </p>

                {/* Genre Selection */}
                <div className="w-full max-w-2xl mx-auto mb-6">
                  <h3 className="text-lg font-medium text-gray-700 dark:text-gray-300 mb-3">
                    Select a music genre to get started:
                  </h3>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                    {musicGenres.map((genre) => (
                      <button
                        key={genre.id}
                        className={`music-btn p-3 rounded-xl border transition-all ${
                          selectedGenre === genre.id
                            ? "bg-gradient-to-r " +
                              genre.color +
                              " text-white border-transparent"
                            : "bg-white dark:bg-gray-700 border-gray-200 dark:border-gray-600 hover:border-purple-300 dark:hover:border-purple-500"
                        }`}
                        onClick={() => setSelectedGenre(genre.id)}
                      >
                        <div className="flex flex-col items-center justify-center">
                          <span className="text-2xl mb-1">{genre.icon}</span>
                          <span className="font-medium">{genre.name}</span>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>

                <button
                  onClick={handleStart}
                  className="music-btn px-6 py-3 text-lg font-medium text-white bg-gradient-to-r from-purple-600 to-indigo-600 rounded-full shadow-lg hover:from-purple-700 hover:to-indigo-700 transition-all duration-300 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-opacity-50"
                >
                  Start Creating Music
                </button>
              </div>
            )}
          </div>

          {/* Feature Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
            <FeatureCard title="AI Melodies" icon="🎵" isDarkMode={isDarkMode}>
              Generate beautiful melodies in any key, scale, or mood with our
              advanced AI algorithms.
            </FeatureCard>

            <FeatureCard
              title="Chord Progressions"
              icon="🎹"
              isDarkMode={isDarkMode}
            >
              Create harmonic chord progressions that follow music theory
              principles with a click.
            </FeatureCard>

            <FeatureCard
              title="Drum Patterns"
              icon="🥁"
              isDarkMode={isDarkMode}
            >
              Design rhythm sections with customizable complexity and style to
              match your track.
            </FeatureCard>

            <FeatureCard title="Basslines" icon="🎸" isDarkMode={isDarkMode}>
              Generate groovy basslines that perfectly complement your chord
              progressions.
            </FeatureCard>

            <FeatureCard
              title="Music Analysis"
              icon="📊"
              isDarkMode={isDarkMode}
            >
              Analyze any audio track to extract key, tempo, chord progression,
              and more.
            </FeatureCard>

            <FeatureCard
              title="Visualizations"
              icon="📈"
              isDarkMode={isDarkMode}
            >
              Create stunning visual representations of your music with
              customizable themes.
            </FeatureCard>
          </div>
        </div>
      </div>
    </div>
  );
};

const FeatureCard = ({ title, icon, children, isDarkMode }) => (
  <div
    className={`music-card p-5 rounded-xl bg-white dark:bg-gray-800 shadow-md hover:shadow-lg transition-all border border-purple-100 dark:border-purple-900/30 transform hover:-translate-y-1 ${
      isDarkMode ? "dark" : ""
    }`}
  >
    <div className="flex items-center mb-3">
      <div className="w-10 h-10 flex items-center justify-center rounded-full bg-purple-100 dark:bg-purple-900/30 text-2xl mr-3">
        {icon}
      </div>
      <h3 className="font-semibold text-lg">{title}</h3>
    </div>
    <p className="text-gray-600 dark:text-gray-400">{children}</p>
  </div>
);

export default StartPage;
