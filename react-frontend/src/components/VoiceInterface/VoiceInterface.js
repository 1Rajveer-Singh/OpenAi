import React, { useState } from 'react';
import './VoiceInterface.css';

const VoiceInterface = () => {
  const [isListening, setIsListening] = useState(false);
  const [isVisible, setIsVisible] = useState(false);

  const toggleListening = () => {
    setIsListening(!isListening);
    setIsVisible(!isVisible);
  };

  return (
    <>
      {/* Voice Button */}
      <button 
        className={`voice-fab ${isListening ? 'listening' : ''}`}
        onClick={toggleListening}
        title="Voice Assistant"
      >
        <i className="fas fa-microphone"></i>
      </button>

      {/* Voice Interface Modal */}
      {isVisible && (
        <div className="voice-modal">
          <div className="voice-modal-content">
            <div className="voice-header">
              <h3>Voice Assistant</h3>
              <button className="close-btn" onClick={() => setIsVisible(false)}>
                <i className="fas fa-times"></i>
              </button>
            </div>
            <div className="voice-body">
              <div className="voice-animation">
                <div className={`voice-circle ${isListening ? 'pulse' : ''}`}>
                  <i className="fas fa-microphone"></i>
                </div>
              </div>
              <p className="voice-status">
                {isListening ? 'Listening... Speak now' : 'Click to start listening'}
                <br />
                <span className="voice-status-hi">
                  {isListening ? 'सुन रहा हूँ... अब बोलें' : 'सुनने के लिए क्लिक करें'}
                </span>
              </p>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default VoiceInterface;