import React from 'react';
import { View, StyleSheet, ActivityIndicator } from 'react-native';
import { Text } from 'react-native-paper';
import { LinearGradient } from 'expo-linear-gradient';

const LoadingScreen: React.FC = () => {
  return (
    <LinearGradient
      colors={['#4CAF50', '#2E7D32']}
      style={styles.container}
    >
      <View style={styles.content}>
        <Text variant="headlineLarge" style={styles.title}>
          VyapaarGPT
        </Text>
        <Text variant="bodyLarge" style={styles.subtitle}>
          आपका AI व्यापार सहायक
        </Text>
        <ActivityIndicator 
          size="large" 
          color="#FFFFFF" 
          style={styles.loader}
        />
        <Text variant="bodyMedium" style={styles.loadingText}>
          सिस्टम लोड हो रहा है...
        </Text>
      </View>
    </LinearGradient>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  content: {
    alignItems: 'center',
    paddingHorizontal: 40,
  },
  title: {
    color: '#FFFFFF',
    fontWeight: 'bold',
    marginBottom: 8,
    textAlign: 'center',
  },
  subtitle: {
    color: '#E8F5E8',
    marginBottom: 40,
    textAlign: 'center',
  },
  loader: {
    marginBottom: 20,
  },
  loadingText: {
    color: '#E8F5E8',
    textAlign: 'center',
  },
});

export default LoadingScreen;