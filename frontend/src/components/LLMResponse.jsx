import React, { memo, useEffect, useRef, useState } from "react";
import MessageBubble from "./MessageBubble";
import ConfirmInline from "./ConfirmInline";
import useMidiPlayer from "../hooks/useMidiPlayer";

const MidiPlayer = ({ midiData }) => {
  const { playing, playMidi } = useMidiPlayer(midiData);

  return (
    <div className="mt-3 p-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-800">
      <div className="flex justify-between items-center mb-2">
        <h3 className="text-md font-semibold text-gray-800 dark:text-white">
          MIDI Audio Ready
        </h3>
        <button
          onClick={playMidi}
          disabled={playing}
          className="px-3 py-1 bg-green-600 text-white rounded-lg hover:bg-green-700 
                                focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50"
        >
          {playing ? "Playing..." : "🔊 Play MIDI"}
        </button>
      </div>
      <div className="text-xs text-gray-600 dark:text-gray-400">
        {midiData.midi_data.tracks} track(s),{" "}
        {midiData.midi_data.messages_count} MIDI messages
      </div>
    </div>
  );
};

// Helper function to detect if a message has MIDI data
const tryExtractMidiData = (data) => {
  try {
    // First, check if there's a direct tool_result string
    if (data && data.tool_result && typeof data.tool_result === "string") {
      const toolResult = JSON.parse(data.tool_result);
      if (
        toolResult.status === "success" &&
        toolResult.result &&
        toolResult.midi_data
      ) {
        return toolResult;
      }
    }

    // If no direct tool_result, check if this is the response object itself
    if (data && data.status === "success" && data.result && data.midi_data) {
      return data;
    }

    // For testing, check if the response contains MIDI data in a string format
    if (
      data &&
      typeof data.response === "string" &&
      (data.response.includes('"type":"note_on"') ||
        data.response.includes('"type":"note_off"'))
    ) {
      // Try to extract JSON from the response text
      const match = data.response.match(
        /\{.*"result":\s*\[.*\].*"status":\s*"success".*\}/s
      );
      if (match) {
        return JSON.parse(match[0]);
      }
    }

    return null;
  } catch (e) {
    console.error("Failed to extract MIDI data:", e);
    return null;
  }
};

const LLMResponse = memo(
  ({ data, onConfirm, isLastMessage, onHeightChange }) => {
    const [isConfirmed, setIsConfirmed] = React.useState(false);
    const responseRef = React.useRef(null);

    // Notify parent of height changes when confirm UI appears/changes
    useEffect(() => {
      if (isLastMessage && responseRef.current && onHeightChange) {
        onHeightChange();
      }
    }, [isLastMessage, isConfirmed, onHeightChange]);

    const handleConfirm = async () => {
      try {
        if (onConfirm) await onConfirm();
        setIsConfirmed(true);
      } catch (error) {
        console.error("Error confirming action:", error);
      }
    };

    const response =
      typeof data?.response === "object"
        ? data.response.response
        : data?.response;

    const displayText = (response || "").trim();
    const requiresConfirm = data.next === "confirm" && isLastMessage;
    const defaultText = requiresConfirm
      ? `Agent is ready to run "${data.tool}". Please confirm.`
      : "";

    // Check if this is a MIDI tool result using our enhanced detection
    const midiData = tryExtractMidiData(data);

    // Display debug info for tool results
    if (data && data.tool === "MidiCreationTool" && data.tool_result) {
      console.log("MIDI tool result detected:", data.tool_result);
    }

    return (
      <div
        ref={responseRef}
        className="space-y-2"
        style={{ whiteSpace: "pre-line" }}
      >
        <MessageBubble message={{ response: displayText || defaultText }} />
        {requiresConfirm && (
          <ConfirmInline
            data={data}
            confirmed={isConfirmed}
            onConfirm={handleConfirm}
          />
        )}
        {!requiresConfirm && data.tool && data.next === "confirm" && (
          <div className="text-sm text-center text-green-600 dark:text-green-400">
            <div>
              Agent chose tool: <strong>{data.tool ?? "Unknown"}</strong>
            </div>
          </div>
        )}
        {midiData && <MidiPlayer midiData={midiData} />}
      </div>
    );
  }
);

LLMResponse.displayName = "LLMResponse";

export default LLMResponse;
