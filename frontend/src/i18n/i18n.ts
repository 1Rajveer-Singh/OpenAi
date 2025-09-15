import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import * as Localization from 'expo-localization';

// Translation resources
import en from './locales/en.json';
import hi from './locales/hi.json';
import te from './locales/te.json';
import ta from './locales/ta.json';
import bn from './locales/bn.json';
import gu from './locales/gu.json';
import mr from './locales/mr.json';
import kn from './locales/kn.json';

const resources = {
  en: { translation: en },
  hi: { translation: hi },
  te: { translation: te },
  ta: { translation: ta },
  bn: { translation: bn },
  gu: { translation: gu },
  mr: { translation: mr },
  kn: { translation: kn },
};

// Detect device language
const detectDeviceLanguage = () => {
  const locale = Localization.locale;
  
  if (locale.startsWith('hi')) return 'hi';
  if (locale.startsWith('te')) return 'te';
  if (locale.startsWith('ta')) return 'ta';
  if (locale.startsWith('bn')) return 'bn';
  if (locale.startsWith('gu')) return 'gu';
  if (locale.startsWith('mr')) return 'mr';
  if (locale.startsWith('kn')) return 'kn';
  
  return 'en'; // Default to English
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: detectDeviceLanguage(),
    fallbackLng: 'en',
    
    interpolation: {
      escapeValue: false, // React already escapes values
    },
    
    // Debug mode
    debug: __DEV__,
    
    // Namespace configuration
    ns: ['translation'],
    defaultNS: 'translation',
    
    // React configuration
    react: {
      useSuspense: false,
    },
    
    // Detection options
    detection: {
      order: ['localStorage', 'navigator'],
      caches: ['localStorage'],
    },
  });

export default i18n;