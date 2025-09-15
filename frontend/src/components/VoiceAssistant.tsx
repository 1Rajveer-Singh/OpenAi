import React, { useState, useEffect } from 'react';
import { 
  View, 
  StyleSheet, 
  Animated, 
  TouchableOpacity,
  Dimensions,
  PanResponder 
} from 'react-native';
import { FAB, Text, Portal, Modal } from 'react-native-paper';
import { useSelector, useDispatch } from 'react-redux';
import * as Speech from 'expo-speech';
import Voice from 'react-native-voice';

import { RootState } from '../store/store';
import { startListening, stopListening, processVoiceCommand } from '../store/slices/voiceSlice';
import VoiceCommandModal from './VoiceCommandModal';

const { width, height } = Dimensions.get('window');

const VoiceAssistant: React.FC = () => {
  const dispatch = useDispatch();
  const { isListening, isProcessing, language } = useSelector((state: RootState) => state.voice);
  const { language: currentLanguage } = useSelector((state: RootState) => state.app);
  
  const [showModal, setShowModal] = useState(false);
  const [fabPosition] = useState(new Animated.ValueXY({ x: width - 80, y: height - 200 }));
  const [pulseAnim] = useState(new Animated.Value(1));

  // Drag handler for floating button
  const panResponder = PanResponder.create({
    onMoveShouldSetPanResponder: () => true,
    onPanResponderGrant: () => {
      fabPosition.setOffset({
        x: fabPosition.x._value,
        y: fabPosition.y._value,
      });
    },
    onPanResponderMove: Animated.event(
      [null, { dx: fabPosition.x, dy: fabPosition.y }],
      { useNativeDriver: false }
    ),
    onPanResponderRelease: () => {
      fabPosition.flattenOffset();
      
      // Snap to edges
      const currentX = fabPosition.x._value;
      const currentY = fabPosition.y._value;
      
      const snapX = currentX < width / 2 ? 20 : width - 80;
      const snapY = Math.max(100, Math.min(height - 200, currentY));
      
      Animated.spring(fabPosition, {
        toValue: { x: snapX, y: snapY },
        useNativeDriver: false,
      }).start();
    },
  });

  // Pulse animation for listening state
  useEffect(() => {
    if (isListening) {
      Animated.loop(
        Animated.sequence([
          Animated.timing(pulseAnim, {
            toValue: 1.2,
            duration: 500,
            useNativeDriver: true,
          }),
          Animated.timing(pulseAnim, {
            toValue: 1,
            duration: 500,
            useNativeDriver: true,
          }),
        ])
      ).start();
    } else {
      pulseAnim.setValue(1);
    }
  }, [isListening, pulseAnim]);

  const handleVoicePress = () => {
    if (isListening) {
      dispatch(stopListening());
    } else {
      setShowModal(true);
      dispatch(startListening());
    }
  };

  const handleModalClose = () => {
    setShowModal(false);
    if (isListening) {
      dispatch(stopListening());
    }
  };

  const getVoiceButtonIcon = () => {
    if (isProcessing) return 'loading';
    if (isListening) return 'microphone';
    return 'microphone-outline';
  };

  const getVoiceButtonColor = () => {
    if (isProcessing) return '#FF9800';
    if (isListening) return '#F44336';
    return '#4CAF50';
  };

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) {
      return currentLanguage === 'hindi' ? 'सुप्रभात!' : 'Good Morning!';
    } else if (hour < 17) {
      return currentLanguage === 'hindi' ? 'नमस्कार!' : 'Good Afternoon!';
    } else {
      return currentLanguage === 'hindi' ? 'शुभ संध्या!' : 'Good Evening!';
    }
  };

  return (
    <>
      {/* Floating Voice Assistant Button */}
      <Animated.View
        style={[
          styles.fabContainer,
          {
            transform: [
              { translateX: fabPosition.x },
              { translateY: fabPosition.y },
              { scale: pulseAnim },
            ],
          },
        ]}
        {...panResponder.panHandlers}
      >
        <FAB
          icon={getVoiceButtonIcon()}
          onPress={handleVoicePress}
          style={[styles.fab, { backgroundColor: getVoiceButtonColor() }]}
          color="#FFFFFF"
          animated={true}
        />
        
        {/* Status indicator */}
        {(isListening || isProcessing) && (
          <View style={styles.statusBadge}>
            <Text style={styles.statusText}>
              {isProcessing ? '⚡' : '🎤'}
            </Text>
          </View>
        )}
      </Animated.View>

      {/* Voice Command Modal */}
      <Portal>
        <Modal
          visible={showModal}
          onDismiss={handleModalClose}
          contentContainerStyle={styles.modalContainer}
        >
          <VoiceCommandModal
            isListening={isListening}
            isProcessing={isProcessing}
            onClose={handleModalClose}
            greeting={getGreeting()}
          />
        </Modal>
      </Portal>
    </>
  );
};

const styles = StyleSheet.create({
  fabContainer: {
    position: 'absolute',
    zIndex: 1000,
  },
  fab: {
    elevation: 8,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.3,
    shadowRadius: 4.65,
  },
  statusBadge: {
    position: 'absolute',
    top: -5,
    right: -5,
    backgroundColor: '#FFFFFF',
    borderRadius: 10,
    width: 20,
    height: 20,
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 4,
  },
  statusText: {
    fontSize: 10,
  },
  modalContainer: {
    backgroundColor: 'white',
    padding: 20,
    margin: 20,
    borderRadius: 15,
    elevation: 5,
  },
});

export default VoiceAssistant;