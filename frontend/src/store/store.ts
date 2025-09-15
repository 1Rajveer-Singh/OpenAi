import { configureStore } from '@reduxjs/toolkit';
import { persistStore, persistReducer } from 'redux-persist';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { combineReducers } from '@reduxjs/toolkit';

import authSlice from './slices/authSlice';
import appSlice from './slices/appSlice';
import inventorySlice from './slices/inventorySlice';
import customerSlice from './slices/customerSlice';
import financeSlice from './slices/financeSlice';
import voiceSlice from './slices/voiceSlice';

const persistConfig = {
  key: 'root',
  storage: AsyncStorage,
  whitelist: ['auth', 'app'], // Only persist auth and app state
};

const rootReducer = combineReducers({
  auth: authSlice,
  app: appSlice,
  inventory: inventorySlice,
  customer: customerSlice,
  finance: financeSlice,
  voice: voiceSlice,
});

const persistedReducer = persistReducer(persistConfig, rootReducer);

export const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE'],
      },
    }),
});

export const persistor = persistStore(store);

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;