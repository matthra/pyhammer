import React, { createContext, useContext, useState, useEffect } from 'react';
import { getTheme, defaultDarkTheme } from './themes';

/**
 * Theme Context
 * Provides theme state and switching functionality throughout the app
 */
const ThemeContext = createContext();

/**
 * Apply a theme to the document by setting CSS variables
 */
const applyTheme = (theme) => {
  const root = document.documentElement;

  // Apply color variables
  Object.entries(theme.colors).forEach(([key, value]) => {
    const cssVar = `--${key.replace(/([A-Z])/g, '-$1').toLowerCase()}`;
    root.style.setProperty(cssVar, value);
  });

  // Apply spacing variables
  Object.entries(theme.spacing).forEach(([key, value]) => {
    root.style.setProperty(`--spacing-${key}`, value);
  });

  // Apply border radius variables
  Object.entries(theme.borderRadius).forEach(([key, value]) => {
    root.style.setProperty(`--radius-${key}`, value);
  });

  // Apply typography variables
  Object.entries(theme.typography).forEach(([key, value]) => {
    const cssVar = `--${key.replace(/([A-Z])/g, '-$1').toLowerCase()}`;
    root.style.setProperty(cssVar, value);
  });

  // Apply shadow variables
  Object.entries(theme.shadows).forEach(([key, value]) => {
    root.style.setProperty(`--shadow-${key}`, value);
  });

  // Apply transition variables
  Object.entries(theme.transitions).forEach(([key, value]) => {
    root.style.setProperty(`--transition-${key}`, value);
  });
};

/**
 * Theme Provider Component
 * Wraps the app to provide theme context
 */
export const ThemeProvider = ({ children }) => {
  const [currentThemeId, setCurrentThemeId] = useState(() => {
    // Load saved theme from localStorage or use default
    return localStorage.getItem('pyhammer-theme') || defaultDarkTheme.id;
  });

  const currentTheme = getTheme(currentThemeId);

  // Apply theme whenever it changes
  useEffect(() => {
    applyTheme(currentTheme);
    // Save to localStorage
    localStorage.setItem('pyhammer-theme', currentThemeId);
  }, [currentTheme, currentThemeId]);

  const setTheme = (themeId) => {
    setCurrentThemeId(themeId);
  };

  const value = {
    currentTheme,
    currentThemeId,
    setTheme,
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};

/**
 * Hook to use theme context
 * @returns {Object} Theme context value
 */
export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};
