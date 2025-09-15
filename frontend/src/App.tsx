import React, { useEffect, useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { StatusBar } from 'expo-status-bar';
import { useSelector, useDispatch } from 'react-redux';
import * as SplashScreen from 'expo-splash-screen';
import * as Font from 'expo-font';

import AuthNavigator from './navigation/AuthNavigator';
import MainNavigator from './navigation/MainNavigator';
import VoiceAssistant from './components/VoiceAssistant';
import LoadingScreen from './components/LoadingScreen';
import { RootState } from './store/store';
import { loadFonts } from './utils/fontLoader';
import { initializeApp } from './store/slices/appSlice';

const Stack = createStackNavigator();

const App: React.FC = () => {
  const dispatch = useDispatch();
  const { isAuthenticated, isLoading } = useSelector((state: RootState) => state.auth);
  const { isInitialized } = useSelector((state: RootState) => state.app);
  const [isAppReady, setIsAppReady] = useState(false);

  useEffect(() => {
    async function prepare() {
      try {
        // Load fonts
        await loadFonts();
        
        // Initialize app
        dispatch(initializeApp());
        
        // Artificial delay to show splash screen
        await new Promise(resolve => setTimeout(resolve, 2000));
      } catch (e) {
        console.warn('Error during app initialization:', e);
      } finally {
        setIsAppReady(true);
        await SplashScreen.hideAsync();
      }
    }

    prepare();
  }, [dispatch]);

  if (!isAppReady || !isInitialized || isLoading) {
    return <LoadingScreen />;
  }

  return (
    <>
      <StatusBar style="auto" />
      <NavigationContainer>
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          {isAuthenticated ? (
            <Stack.Screen name="Main" component={MainNavigator} />
          ) : (
            <Stack.Screen name="Auth" component={AuthNavigator} />
          )}
        </Stack.Navigator>
      </NavigationContainer>
      
      {/* Voice Assistant - Always available when authenticated */}
      {isAuthenticated && <VoiceAssistant />}
    </>
  );
};

export default App;