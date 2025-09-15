import { MD3LightTheme, MD3DarkTheme } from 'react-native-paper';

// VyapaarGPT Brand Colors
const brandColors = {
  primary: '#4CAF50',      // Green - prosperity, growth
  secondary: '#FF9800',    // Orange - energy, enthusiasm
  tertiary: '#2196F3',     // Blue - trust, stability
  success: '#8BC34A',      // Light green
  warning: '#FFC107',      // Amber
  error: '#F44336',        // Red
  info: '#00BCD4',         // Cyan
  
  // Indian-inspired colors
  saffron: '#FF9933',      // Saffron
  white: '#FFFFFF',        // White
  green: '#138808',        // India green
  
  // Business colors
  profit: '#4CAF50',       // Green for profit
  loss: '#F44336',         // Red for loss
  neutral: '#9E9E9E',      // Grey for neutral
};

// Light Theme
export const lightTheme = {
  ...MD3LightTheme,
  colors: {
    ...MD3LightTheme.colors,
    primary: brandColors.primary,
    onPrimary: '#FFFFFF',
    primaryContainer: '#E8F5E8',
    onPrimaryContainer: '#1B5E20',
    
    secondary: brandColors.secondary,
    onSecondary: '#FFFFFF',
    secondaryContainer: '#FFF3E0',
    onSecondaryContainer: '#E65100',
    
    tertiary: brandColors.tertiary,
    onTertiary: '#FFFFFF',
    tertiaryContainer: '#E3F2FD',
    onTertiaryContainer: '#0D47A1',
    
    error: brandColors.error,
    onError: '#FFFFFF',
    errorContainer: '#FFEBEE',
    onErrorContainer: '#B71C1C',
    
    background: '#FAFAFA',
    onBackground: '#1C1B1F',
    surface: '#FFFFFF',
    onSurface: '#1C1B1F',
    surfaceVariant: '#F5F5F5',
    onSurfaceVariant: '#424242',
    
    outline: '#E0E0E0',
    outlineVariant: '#F0F0F0',
    
    // Custom business colors
    profit: brandColors.profit,
    loss: brandColors.loss,
    neutral: brandColors.neutral,
    
    // Status colors
    success: brandColors.success,
    warning: brandColors.warning,
    info: brandColors.info,
    
    // Indian theme colors
    saffron: brandColors.saffron,
    indianGreen: brandColors.green,
  },
  fonts: {
    ...MD3LightTheme.fonts,
    bodyLarge: {
      ...MD3LightTheme.fonts.bodyLarge,
      fontFamily: 'Roboto',
    },
    bodyMedium: {
      ...MD3LightTheme.fonts.bodyMedium,
      fontFamily: 'Roboto',
    },
    bodySmall: {
      ...MD3LightTheme.fonts.bodySmall,
      fontFamily: 'Roboto',
    },
    displayLarge: {
      ...MD3LightTheme.fonts.displayLarge,
      fontFamily: 'Roboto',
    },
    displayMedium: {
      ...MD3LightTheme.fonts.displayMedium,
      fontFamily: 'Roboto',
    },
    displaySmall: {
      ...MD3LightTheme.fonts.displaySmall,
      fontFamily: 'Roboto',
    },
    headlineLarge: {
      ...MD3LightTheme.fonts.headlineLarge,
      fontFamily: 'Roboto',
    },
    headlineMedium: {
      ...MD3LightTheme.fonts.headlineMedium,
      fontFamily: 'Roboto',
    },
    headlineSmall: {
      ...MD3LightTheme.fonts.headlineSmall,
      fontFamily: 'Roboto',
    },
    titleLarge: {
      ...MD3LightTheme.fonts.titleLarge,
      fontFamily: 'Roboto',
    },
    titleMedium: {
      ...MD3LightTheme.fonts.titleMedium,
      fontFamily: 'Roboto',
    },
    titleSmall: {
      ...MD3LightTheme.fonts.titleSmall,
      fontFamily: 'Roboto',
    },
  },
};

// Dark Theme
export const darkTheme = {
  ...MD3DarkTheme,
  colors: {
    ...MD3DarkTheme.colors,
    primary: brandColors.primary,
    onPrimary: '#000000',
    primaryContainer: '#2E7D32',
    onPrimaryContainer: '#C8E6C9',
    
    secondary: brandColors.secondary,
    onSecondary: '#000000',
    secondaryContainer: '#F57C00',
    onSecondaryContainer: '#FFE0B2',
    
    tertiary: brandColors.tertiary,
    onTertiary: '#000000',
    tertiaryContainer: '#1976D2',
    onTertiaryContainer: '#BBDEFB',
    
    error: brandColors.error,
    onError: '#FFFFFF',
    errorContainer: '#C62828',
    onErrorContainer: '#FFCDD2',
    
    background: '#121212',
    onBackground: '#E0E0E0',
    surface: '#1E1E1E',
    onSurface: '#E0E0E0',
    surfaceVariant: '#2C2C2C',
    onSurfaceVariant: '#BDBDBD',
    
    outline: '#616161',
    outlineVariant: '#424242',
    
    // Custom business colors
    profit: brandColors.profit,
    loss: brandColors.loss,
    neutral: brandColors.neutral,
    
    // Status colors
    success: brandColors.success,
    warning: brandColors.warning,
    info: brandColors.info,
    
    // Indian theme colors
    saffron: brandColors.saffron,
    indianGreen: brandColors.green,
  },
  fonts: {
    ...MD3DarkTheme.fonts,
    bodyLarge: {
      ...MD3DarkTheme.fonts.bodyLarge,
      fontFamily: 'Roboto',
    },
    bodyMedium: {
      ...MD3DarkTheme.fonts.bodyMedium,
      fontFamily: 'Roboto',
    },
    bodySmall: {
      ...MD3DarkTheme.fonts.bodySmall,
      fontFamily: 'Roboto',
    },
    displayLarge: {
      ...MD3DarkTheme.fonts.displayLarge,
      fontFamily: 'Roboto',
    },
    displayMedium: {
      ...MD3DarkTheme.fonts.displayMedium,
      fontFamily: 'Roboto',
    },
    displaySmall: {
      ...MD3DarkTheme.fonts.displaySmall,
      fontFamily: 'Roboto',
    },
    headlineLarge: {
      ...MD3DarkTheme.fonts.headlineLarge,
      fontFamily: 'Roboto',
    },
    headlineMedium: {
      ...MD3DarkTheme.fonts.headlineMedium,
      fontFamily: 'Roboto',
    },
    headlineSmall: {
      ...MD3DarkTheme.fonts.headlineSmall,
      fontFamily: 'Roboto',
    },
    titleLarge: {
      ...MD3DarkTheme.fonts.titleLarge,
      fontFamily: 'Roboto',
    },
    titleMedium: {
      ...MD3DarkTheme.fonts.titleMedium,
      fontFamily: 'Roboto',
    },
    titleSmall: {
      ...MD3DarkTheme.fonts.titleSmall,
      fontFamily: 'Roboto',
    },
  },
};

// Default theme (light)
export const theme = lightTheme;

// Component-specific styles
export const componentStyles = {
  card: {
    borderRadius: 12,
    elevation: 4,
    marginVertical: 8,
  },
  button: {
    borderRadius: 8,
    paddingVertical: 4,
  },
  fab: {
    borderRadius: 28,
    elevation: 8,
  },
  chip: {
    borderRadius: 16,
  },
  textInput: {
    borderRadius: 8,
    marginVertical: 4,
  },
};

// Spacing constants
export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};

// Animation constants
export const animations = {
  duration: {
    short: 200,
    medium: 300,
    long: 500,
  },
  easing: {
    ease: 'ease',
    easeIn: 'ease-in',
    easeOut: 'ease-out',
    easeInOut: 'ease-in-out',
  },
};

// Breakpoints for responsive design
export const breakpoints = {
  small: 375,
  medium: 768,
  large: 1024,
  xlarge: 1200,
};

// Typography scale
export const typography = {
  fontSize: {
    xs: 10,
    sm: 12,
    md: 14,
    lg: 16,
    xl: 18,
    xxl: 20,
    xxxl: 24,
  },
  lineHeight: {
    xs: 12,
    sm: 16,
    md: 20,
    lg: 22,
    xl: 24,
    xxl: 28,
    xxxl: 32,
  },
  fontWeight: {
    light: '300',
    normal: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
  },
};