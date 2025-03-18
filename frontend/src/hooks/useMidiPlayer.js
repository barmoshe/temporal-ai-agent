import { useState, useRef } from "react";

const useMidiPlayer = (midiData, BPM = 120) => {
  const [playing, setPlaying] = useState(false);
  const audioContextRef = useRef(null);

  // Helper function to convert MIDI note numbers to frequency (Hz)
  const midiNoteToFrequency = (note) => {
    return 440 * Math.pow(2, (note - 69) / 12);
  };

  const playMidi = () => {
    if (!midiData || !midiData.result || midiData.status !== "success") return;
    setPlaying(true);

    // Create audio context if it doesn't exist
    if (!audioContextRef.current) {
      audioContextRef.current = new (window.AudioContext ||
        window.webkitAudioContext)();
    }
    const context = audioContextRef.current;
    const currentTime = context.currentTime;

    // Determine ticks per beat (defaulting to 480 if not provided)
    const ticksPerBeat = midiData.midi_data.ticksPerBeat || 480;
    const tickDuration = 60 / BPM / ticksPerBeat; // seconds per tick

    let currentTimeOffset = 0; // cumulative offset for scheduling events
    const activeOscillators = {};

    // Iterate through all MIDI messages and schedule events accordingly
    midiData.result.forEach((msg) => {
      if (msg.type === "note_on") {
        const startTime = currentTime + currentTimeOffset;
        const frequency = midiNoteToFrequency(msg.note);

        // Create oscillator and gain node
        const oscillator = context.createOscillator();
        const gainNode = context.createGain();

        oscillator.type = "sine";
        oscillator.frequency.value = frequency;
        gainNode.gain.value = msg.velocity / 127; // normalize velocity

        oscillator.connect(gainNode);
        gainNode.connect(context.destination);

        // Start the note
        oscillator.start(startTime);
        activeOscillators[msg.note] = { oscillator, gainNode, startTime };
      } else if (msg.type === "note_off" && activeOscillators[msg.note]) {
        const { oscillator, gainNode, startTime } = activeOscillators[msg.note];
        // Calculate duration based on ticks and BPM
        const noteDuration = msg.time * tickDuration;
        const stopTime = startTime + noteDuration;

        // Fade out to prevent clicking sounds
        gainNode.gain.setValueAtTime(gainNode.gain.value, stopTime - 0.01);
        gainNode.gain.linearRampToValueAtTime(0, stopTime);
        oscillator.stop(stopTime + 0.01);

        delete activeOscillators[msg.note];
        // Update the current time offset based on when the note stops
        currentTimeOffset = stopTime - currentTime;
      } else if (msg.type === "delay") {
        // For explicit delay messages, simply add the delay to the offset
        currentTimeOffset += msg.time * tickDuration;
      }
    });

    // Set a timeout to update the playing state after playback finishes
    setTimeout(() => setPlaying(false), (currentTimeOffset + 0.5) * 1000);
  };

  return { playing, playMidi };
};

export default useMidiPlayer;
