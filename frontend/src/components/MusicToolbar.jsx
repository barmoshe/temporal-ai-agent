import React from "react";
import PropTypes from "prop-types";

const MUSIC_TOOLS = [
  {
    id: "melody",
    name: "Melody",
    prompt: "Generate a melody in C major that sounds uplifting",
    icon: (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        className="h-4 w-4 mr-1"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2z"
        />
      </svg>
    ),
  },
  {
    id: "chords",
    name: "Chords",
    prompt: "Create a jazzy chord progression in D minor",
    icon: (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        className="h-4 w-4 mr-1"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2z"
        />
      </svg>
    ),
  },
  {
    id: "drums",
    name: "Drums",
    prompt: "Generate a hip-hop drum pattern at 90 BPM",
    icon: (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        className="h-4 w-4 mr-1"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
      >
        <circle cx="6" cy="6" r="3" strokeWidth="2" />
        <circle cx="18" cy="6" r="3" strokeWidth="2" />
        <circle cx="12" cy="18" r="3" strokeWidth="2" />
        <line x1="6" y1="9" x2="6" y2="21" strokeWidth="2" />
        <line x1="18" y1="9" x2="18" y2="21" strokeWidth="2" />
      </svg>
    ),
  },
  {
    id: "bassline",
    name: "Bassline",
    prompt: "Create a funky bassline to go with a progression of Dm7-G7-Cmaj7",
    icon: (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        className="h-4 w-4 mr-1"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 104 0V7a2 2 0 00-2-2zm0 8a2 2 0 100 4h14a2 2 0 100-4H5z"
        />
      </svg>
    ),
  },
  {
    id: "lyrics",
    name: "Lyrics",
    prompt: "Write lyrics for a love song with a hopeful theme",
    icon: (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        className="h-4 w-4 mr-1"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"
        />
      </svg>
    ),
  },
  {
    id: "arrangement",
    name: "Arrangement",
    prompt:
      "Create a song arrangement for a pop track with verse, chorus, and bridge",
    icon: (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        className="h-4 w-4 mr-1"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M4 6h16M4 10h16M4 14h16M4 18h16"
        />
      </svg>
    ),
  },
  {
    id: "visualization",
    name: "Visualize",
    prompt: "Create a waveform visualization for a dance track",
    icon: (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        className="h-4 w-4 mr-1"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4"
        />
      </svg>
    ),
  },
  {
    id: "samples",
    name: "Samples",
    prompt: "Recommend drum samples for a trap beat",
    icon: (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        className="h-4 w-4 mr-1"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
        />
      </svg>
    ),
  },
  {
    id: "composition",
    name: "Full Track",
    prompt:
      "Create a complete electronic music composition with drums, bass, and melody",
    icon: (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        className="h-4 w-4 mr-1"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"
        />
      </svg>
    ),
  },
];

const MusicToolbar = ({ onSelectTool }) => {
  return (
    <div className="music-toolbar flex items-center gap-2 overflow-x-auto pb-2">
      <div className="flex-shrink-0 mr-2">
        <span className="px-2 py-1 text-sm font-semibold text-gray-700 dark:text-gray-300">
          Quick Tools:
        </span>
      </div>

      {MUSIC_TOOLS.map((tool) => (
        <button
          key={tool.id}
          className="tool-button"
          onClick={() => onSelectTool(tool.prompt)}
          title={tool.prompt}
        >
          {tool.icon}
          {tool.name}
        </button>
      ))}
    </div>
  );
};

MusicToolbar.propTypes = {
  onSelectTool: PropTypes.func.isRequired,
};

export default MusicToolbar;
