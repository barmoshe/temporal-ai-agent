import React, { useState, useEffect, useRef } from "react";

const MidiBubblePlayer = ({ midiData, title = "MIDI Sequence" }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentNoteIndex, setCurrentNoteIndex] = useState(-1);
  const [notes, setNotes] = useState([]);
  const audioContextRef = useRef(null);
  const playbackTimerRef = useRef(null);

  // Parse the MIDI data when component mounts or when midiData changes
  useEffect(() => {
    if (!midiData || !midiData.midi_base64 || !midiData.notes_summary) {
      return;
    }

    try {
      // Extract notes from the MIDI data
      // For simplicity, we'll use the notes_summary directly
      // In a real implementation, you might want to decode the base64 MIDI data
      const extractedNotes =
        midiData.note_count > 5
          ? [...midiData.notes_summary.filter((note) => note.note !== "...")]
          : midiData.notes_summary;

      setNotes(extractedNotes);
    } catch (error) {
      console.error("Error parsing MIDI data:", error);
    }
  }, [midiData]);

  // Clean up audio context and timers when component unmounts
  useEffect(() => {
    return () => {
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }

      if (playbackTimerRef.current) {
        clearTimeout(playbackTimerRef.current);
      }
    };
  }, []);

  // Play a single note
  const playNote = (note, duration) => {
    // Skip if it's a rest (note is 0)
    if (note === 0 || note === "...") return;

    // Create audio context if it doesn't exist
    if (!audioContextRef.current) {
      audioContextRef.current = new (window.AudioContext ||
        window.webkitAudioContext)();
    }

    const context = audioContextRef.current;

    // Convert MIDI note to frequency
    const frequency = 440 * Math.pow(2, (note - 69) / 12);

    // Create oscillator
    const oscillator = context.createOscillator();
    const gainNode = context.createGain();

    // Set oscillator properties
    oscillator.type = "sine"; // Use sine wave for simple piano-like sound
    oscillator.frequency.setValueAtTime(frequency, context.currentTime);

    // Connect nodes
    oscillator.connect(gainNode);
    gainNode.connect(context.destination);

    // Apply envelope
    gainNode.gain.setValueAtTime(0, context.currentTime);
    gainNode.gain.linearRampToValueAtTime(0.7, context.currentTime + 0.01);
    gainNode.gain.exponentialRampToValueAtTime(
      0.01,
      context.currentTime + duration * 0.95
    );

    // Start and stop oscillator
    oscillator.start(context.currentTime);
    oscillator.stop(context.currentTime + duration);
  };

  // Play the sequence of notes
  const playSequence = () => {
    setIsPlaying(true);
    setCurrentNoteIndex(0);

    let index = 0;

    // Function to play the next note
    const playNextNote = () => {
      if (index >= notes.length) {
        setIsPlaying(false);
        setCurrentNoteIndex(-1);
        return;
      }

      setCurrentNoteIndex(index);

      const { note, duration } = notes[index];
      playNote(note, duration);

      // Calculate time for next note (fixed tempo of 120 BPM)
      // At 120 BPM, a quarter note (0.25) is 0.5 seconds
      const waitTime = duration * 2 * 1000; // Convert to milliseconds

      index++;
      playbackTimerRef.current = setTimeout(playNextNote, waitTime);
    };

    playNextNote();
  };

  // Stop playing
  const stopSequence = () => {
    if (playbackTimerRef.current) {
      clearTimeout(playbackTimerRef.current);
    }

    setIsPlaying(false);
    setCurrentNoteIndex(-1);
  };

  // Toggle play/stop
  const togglePlay = () => {
    if (isPlaying) {
      stopSequence();
    } else {
      playSequence();
    }
  };

  // Calculate bubble size based on note duration
  const getBubbleSize = (duration) => {
    // Convert duration to a size between 30px and 80px
    return Math.max(30, Math.min(80, 30 + duration * 30));
  };

  // Get bubble color based on note value (pitch)
  const getBubbleColor = (note) => {
    if (note === 0 || note === "...") return "#ccc"; // Gray for rests or placeholder

    // Map note values to colors using HSL
    // Use the note value to determine the hue
    const hue = (note % 12) * 30; // 12 notes in an octave, 30 degrees per note
    return `hsl(${hue}, 80%, 65%)`;
  };

  return (
    <div className="midi-bubble-player bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden border border-purple-100 dark:border-purple-900/30 p-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-gray-800 dark:text-white">
          {title}
        </h3>
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
      </div>

      {/* Description text */}
      <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
        {midiData && midiData.note_count
          ? `This melody contains ${midiData.note_count} notes at ${
              midiData.tempo || 120
            } BPM.`
          : "No MIDI data loaded."}
      </p>

      {/* Bubble visualization */}
      <div className="flex flex-wrap gap-3 items-center justify-center min-h-[120px] py-4">
        {notes.map((noteData, index) => {
          const size = getBubbleSize(noteData.duration);
          const color = getBubbleColor(noteData.note);

          return (
            <div
              key={index}
              className={`bubble flex items-center justify-center rounded-full transition-all duration-300 ${
                currentNoteIndex === index
                  ? "scale-110 ring-4 ring-purple-300 dark:ring-purple-600"
                  : ""
              }`}
              style={{
                width: `${size}px`,
                height: `${size}px`,
                backgroundColor: color,
                opacity: noteData.note === 0 ? 0.5 : 1,
              }}
            >
              <span className="text-xs font-medium text-white">
                {noteData.note !== 0 && noteData.note !== "..."
                  ? noteData.note
                  : ""}
              </span>
            </div>
          );
        })}

        {notes.length === 0 && (
          <div className="text-gray-500 dark:text-gray-400 text-center italic">
            No notes to display
          </div>
        )}
      </div>

      {/* Tempo indicator */}
      <div className="flex justify-center mt-4">
        <div className="text-xs px-3 py-1 bg-gray-100 dark:bg-gray-700 rounded-full text-gray-600 dark:text-gray-300">
          Tempo: {midiData && midiData.tempo ? midiData.tempo : 120} BPM
        </div>
      </div>
    </div>
  );
};

export default MidiBubblePlayer;
