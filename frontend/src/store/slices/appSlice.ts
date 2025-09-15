import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import * as Localization from 'expo-localization';
import { api } from '../../services/api';

interface AppState {
  isInitialized: boolean;
  isLoading: boolean;
  language: string;
  theme: 'light' | 'dark';
  deviceInfo: {
    locale: string;
    timezone: string;
    isTablet: boolean;
  };
  error: string | null;
}

const initialState: AppState = {
  isInitialized: false,
  isLoading: false,
  language: 'hindi',
  theme: 'light',
  deviceInfo: {
    locale: 'en-IN',
    timezone: 'Asia/Kolkata',
    isTablet: false,
  },
  error: null,
};

// Async thunks
export const initializeApp = createAsyncThunk(
  'app/initialize',
  async (_, { rejectWithValue }) => {
    try {
      // Get device info
      const locale = Localization.locale;
      const timezone = Localization.timezone;
      
      // Detect language from locale
      const deviceLanguage = locale.startsWith('hi') ? 'hindi' :
                           locale.startsWith('te') ? 'telugu' :
                           locale.startsWith('ta') ? 'tamil' :
                           locale.startsWith('bn') ? 'bengali' :
                           locale.startsWith('gu') ? 'gujarati' :
                           locale.startsWith('mr') ? 'marathi' :
                           locale.startsWith('kn') ? 'kannada' :
                           'english';

      return {
        locale,
        timezone,
        deviceLanguage,
      };
    } catch (error) {
      return rejectWithValue('Failed to initialize app');
    }
  }
);

export const changeLanguage = createAsyncThunk(
  'app/changeLanguage',
  async (language: string, { getState, rejectWithValue }) => {
    try {
      // Update language in i18n
      const { default: i18n } = await import('../../i18n/i18n');
      await i18n.changeLanguage(language);
      
      return language;
    } catch (error) {
      return rejectWithValue('Failed to change language');
    }
  }
);

const appSlice = createSlice({
  name: 'app',
  initialState,
  reducers: {
    setTheme: (state, action: PayloadAction<'light' | 'dark'>) => {
      state.theme = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      // Initialize app
      .addCase(initializeApp.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(initializeApp.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isInitialized = true;
        state.deviceInfo.locale = action.payload.locale;
        state.deviceInfo.timezone = action.payload.timezone;
        state.language = action.payload.deviceLanguage;
      })
      .addCase(initializeApp.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      
      // Change language
      .addCase(changeLanguage.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(changeLanguage.fulfilled, (state, action) => {
        state.isLoading = false;
        state.language = action.payload;
      })
      .addCase(changeLanguage.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const { setTheme, setError, clearError, setLoading } = appSlice.actions;
export default appSlice.reducer;