import React from 'react';
import { registerRootComponent } from 'expo';
import { Provider } from 'react-redux';
import { PersistGate } from 'redux-persist/integration/react';
import { I18nextProvider } from 'react-i18next';
import { PaperProvider } from 'react-native-paper';
import * as SplashScreen from 'expo-splash-screen';

import App from './src/App';
import { store, persistor } from './src/store/store';
import i18n from './src/i18n/i18n';
import { theme } from './src/theme/theme';
import LoadingScreen from './src/components/LoadingScreen';

// Keep the splash screen visible while we fetch resources
SplashScreen.preventAutoHideAsync();

const VyapaarGPTApp = () => {
  return (
    <Provider store={store}>
      <PersistGate loading={<LoadingScreen />} persistor={persistor}>
        <I18nextProvider i18n={i18n}>
          <PaperProvider theme={theme}>
            <App />
          </PaperProvider>
        </I18nextProvider>
      </PersistGate>
    </Provider>
  );
};

export default registerRootComponent(VyapaarGPTApp);