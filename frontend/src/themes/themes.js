/**
 * Theme Configuration System for PyHammer
 *
 * This file contains predefined themes that content creators can use or customize.
 * Each theme defines all the CSS variables used throughout the application.
 *
 * To add a new theme:
 * 1. Copy an existing theme object
 * 2. Modify the colors/values to match your brand
 * 3. Add it to the 'themes' object at the bottom
 */

/**
 * Default Dark Theme (GitHub-inspired)
 * Current default theme for PyHammer
 */
export const defaultDarkTheme = {
  name: 'Default Dark',
  id: 'default-dark',
  colors: {
    // Background Colors (RGB format)
    bgPrimary: '15 20 25',           // #0f1419
    bgSecondary: '26 31 46',         // #1a1f2e
    bgTertiary: '37 43 59',          // #252b3b
    bgHover: '48 54 71',

    // Text Colors
    textPrimary: '230 237 243',      // #e6edf3
    textSecondary: '139 148 158',    // #8b949e
    textTertiary: '107 114 128',

    // Border Colors
    borderColor: '48 54 61',         // #30363d
    borderLight: '58 64 71',
    borderDark: '38 44 51',

    // Accent Colors
    accentPrimary: '88 166 255',     // #58a6ff
    accentSecondary: '139 92 246',   // #8b5cf6
    accentHover: '31 111 235',       // #1f6feb

    // Status Colors
    success: '63 185 80',            // #3fb950
    warning: '210 153 34',           // #d29922
    danger: '248 81 73',             // #f85149
    info: '56 139 253',              // #388bfd
  },
  spacing: {
    section: '2rem',
    card: '1.5rem',
    element: '1rem',
  },
  borderRadius: {
    sm: '0.25rem',
    md: '0.5rem',
    lg: '0.75rem',
    xl: '1rem',
  },
  typography: {
    fontFamilySans: "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif",
    fontFamilyMono: "'Source Code Pro', Menlo, Monaco, Consolas, 'Courier New', monospace",
    fontSizeXs: '0.75rem',
    fontSizeSm: '0.875rem',
    fontSizeBase: '1rem',
    fontSizeLg: '1.125rem',
    fontSizeXl: '1.25rem',
    fontSize2xl: '1.5rem',
    fontSize3xl: '1.875rem',
    lineHeightXs: '1.25',
    lineHeightSm: '1.375',
    lineHeightBase: '1.5',
    lineHeightLg: '1.625',
    lineHeightXl: '1.75',
    lineHeight2xl: '1.875',
    lineHeight3xl: '2',
  },
  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.3)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -1px rgba(0, 0, 0, 0.3)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -2px rgba(0, 0, 0, 0.3)',
    xl: '0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 10px 10px -5px rgba(0, 0, 0, 0.2)',
  },
  transitions: {
    duration: '150ms',
    timing: 'cubic-bezier(0.4, 0, 0.2, 1)',
  },
};

/**
 * Purple Gaming Theme
 * A vibrant purple theme perfect for gaming content
 */
export const purpleGamingTheme = {
  name: 'Purple Gaming',
  id: 'purple-gaming',
  colors: {
    bgPrimary: '15 10 25',           // Deep purple background
    bgSecondary: '25 18 40',
    bgTertiary: '35 25 55',
    bgHover: '45 32 70',

    textPrimary: '240 235 255',
    textSecondary: '180 170 200',
    textTertiary: '140 130 160',

    borderColor: '60 45 85',
    borderLight: '75 60 100',
    borderDark: '45 30 70',

    accentPrimary: '168 85 247',     // Bright purple
    accentSecondary: '236 72 153',   // Pink accent
    accentHover: '147 51 234',

    success: '34 197 94',
    warning: '251 191 36',
    danger: '239 68 68',
    info: '96 165 250',
  },
  spacing: defaultDarkTheme.spacing,
  borderRadius: defaultDarkTheme.borderRadius,
  typography: defaultDarkTheme.typography,
  shadows: defaultDarkTheme.shadows,
  transitions: defaultDarkTheme.transitions,
};

/**
 * Cyberpunk Neon Theme
 * High-contrast neon theme with cyan/magenta accents
 */
export const cyberpunkTheme = {
  name: 'Cyberpunk Neon',
  id: 'cyberpunk',
  colors: {
    bgPrimary: '10 10 20',           // Almost black
    bgSecondary: '18 18 30',
    bgTertiary: '25 25 40',
    bgHover: '35 35 50',

    textPrimary: '0 255 255',        // Cyan text
    textSecondary: '150 200 255',
    textTertiary: '100 150 200',

    borderColor: '0 180 180',        // Cyan border
    borderLight: '0 200 200',
    borderDark: '0 140 140',

    accentPrimary: '0 255 255',      // Cyan
    accentSecondary: '255 0 255',    // Magenta
    accentHover: '0 200 255',

    success: '0 255 128',
    warning: '255 215 0',
    danger: '255 0 128',
    info: '0 200 255',
  },
  spacing: defaultDarkTheme.spacing,
  borderRadius: {
    sm: '0.125rem',                  // Sharper corners for cyber look
    md: '0.25rem',
    lg: '0.5rem',
    xl: '0.75rem',
  },
  typography: defaultDarkTheme.typography,
  shadows: {
    sm: '0 0 5px rgba(0, 255, 255, 0.3)',
    md: '0 0 10px rgba(0, 255, 255, 0.4), 0 4px 6px rgba(0, 0, 0, 0.5)',
    lg: '0 0 20px rgba(0, 255, 255, 0.5), 0 8px 16px rgba(0, 0, 0, 0.6)',
    xl: '0 0 30px rgba(0, 255, 255, 0.6), 0 12px 24px rgba(0, 0, 0, 0.7)',
  },
  transitions: defaultDarkTheme.transitions,
};

/**
 * Military Green Theme
 * Tactical military-inspired theme with green accents
 */
export const militaryTheme = {
  name: 'Military Tactical',
  id: 'military',
  colors: {
    bgPrimary: '20 22 18',           // Dark olive
    bgSecondary: '30 35 25',
    bgTertiary: '40 45 35',
    bgHover: '50 55 45',

    textPrimary: '220 230 210',
    textSecondary: '160 170 150',
    textTertiary: '120 130 110',

    borderColor: '60 70 50',
    borderLight: '75 85 65',
    borderDark: '45 55 35',

    accentPrimary: '106 168 79',     // Military green
    accentSecondary: '212 175 55',   // Gold accent
    accentHover: '86 148 59',

    success: '120 200 80',
    warning: '220 180 60',
    danger: '200 80 60',
    info: '100 150 200',
  },
  spacing: defaultDarkTheme.spacing,
  borderRadius: defaultDarkTheme.borderRadius,
  typography: defaultDarkTheme.typography,
  shadows: defaultDarkTheme.shadows,
  transitions: defaultDarkTheme.transitions,
};

/**
 * Ocean Blue Theme
 * Calming blue theme with aqua accents
 */
export const oceanTheme = {
  name: 'Ocean Blue',
  id: 'ocean',
  colors: {
    bgPrimary: '12 18 30',           // Deep ocean blue
    bgSecondary: '18 28 45',
    bgTertiary: '25 38 60',
    bgHover: '32 48 75',

    textPrimary: '225 240 255',
    textSecondary: '160 185 210',
    textTertiary: '120 145 170',

    borderColor: '45 70 100',
    borderLight: '60 85 115',
    borderDark: '30 55 85',

    accentPrimary: '59 130 246',     // Bright blue
    accentSecondary: '34 211 238',   // Aqua
    accentHover: '37 99 235',

    success: '52 211 153',
    warning: '251 146 60',
    danger: '248 113 113',
    info: '96 165 250',
  },
  spacing: defaultDarkTheme.spacing,
  borderRadius: defaultDarkTheme.borderRadius,
  typography: defaultDarkTheme.typography,
  shadows: defaultDarkTheme.shadows,
  transitions: defaultDarkTheme.transitions,
};

/**
 * Blood Red Theme
 * Intense red theme for aggressive content
 */
export const bloodRedTheme = {
  name: 'Blood Red',
  id: 'blood-red',
  colors: {
    bgPrimary: '20 10 10',           // Dark red
    bgSecondary: '30 15 15',
    bgTertiary: '45 20 20',
    bgHover: '60 25 25',

    textPrimary: '255 240 240',
    textSecondary: '200 170 170',
    textTertiary: '160 130 130',

    borderColor: '80 30 30',
    borderLight: '100 40 40',
    borderDark: '60 20 20',

    accentPrimary: '239 68 68',      // Bright red
    accentSecondary: '251 146 60',   // Orange accent
    accentHover: '220 38 38',

    success: '34 197 94',
    warning: '251 191 36',
    danger: '220 38 38',
    info: '147 51 234',
  },
  spacing: defaultDarkTheme.spacing,
  borderRadius: defaultDarkTheme.borderRadius,
  typography: defaultDarkTheme.typography,
  shadows: defaultDarkTheme.shadows,
  transitions: defaultDarkTheme.transitions,
};

/**
 * All available themes
 * Add new themes to this object to make them available in the theme switcher
 */
export const themes = {
  [defaultDarkTheme.id]: defaultDarkTheme,
  [purpleGamingTheme.id]: purpleGamingTheme,
  [cyberpunkTheme.id]: cyberpunkTheme,
  [militaryTheme.id]: militaryTheme,
  [oceanTheme.id]: oceanTheme,
  [bloodRedTheme.id]: bloodRedTheme,
};

/**
 * Get a theme by ID
 */
export const getTheme = (themeId) => {
  return themes[themeId] || defaultDarkTheme;
};

/**
 * Get all theme IDs and names
 */
export const getThemeList = () => {
  return Object.values(themes).map(theme => ({
    id: theme.id,
    name: theme.name,
  }));
};
