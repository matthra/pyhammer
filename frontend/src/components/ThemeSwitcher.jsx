import React, { useState } from 'react';
import { useTheme } from '../themes/ThemeContext';
import { getThemeList } from '../themes/themes';
import { Palette, Check } from 'lucide-react';

/**
 * Theme Switcher Component
 * Allows users to switch between predefined themes
 * Can be placed in settings, navbar, or anywhere in the app
 */
const ThemeSwitcher = ({ variant = 'dropdown' }) => {
  const { currentThemeId, setTheme } = useTheme();
  const [isOpen, setIsOpen] = useState(false);
  const themeList = getThemeList();

  const currentTheme = themeList.find(t => t.id === currentThemeId);

  if (variant === 'dropdown') {
    return (
      <div className="relative">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="btn-secondary flex items-center gap-2"
          aria-label="Change theme"
        >
          <Palette size={18} />
          <span className="hidden sm:inline">{currentTheme?.name}</span>
        </button>

        {isOpen && (
          <>
            {/* Backdrop */}
            <div
              className="fixed inset-0 z-10"
              onClick={() => setIsOpen(false)}
            />

            {/* Dropdown menu */}
            <div className="absolute right-0 mt-2 w-56 bg-bg-secondary border border-border rounded-lg shadow-lg z-20">
              <div className="p-2">
                <div className="px-3 py-2 text-sm font-semibold text-text-secondary border-b border-border mb-2">
                  Select Theme
                </div>
                {themeList.map((theme) => (
                  <button
                    key={theme.id}
                    onClick={() => {
                      setTheme(theme.id);
                      setIsOpen(false);
                    }}
                    className={`
                      w-full flex items-center justify-between px-3 py-2 rounded-md
                      text-left text-sm transition-colors
                      ${theme.id === currentThemeId
                        ? 'bg-accent-primary/20 text-accent-primary'
                        : 'text-text-primary hover:bg-bg-hover'
                      }
                    `}
                  >
                    <span>{theme.name}</span>
                    {theme.id === currentThemeId && (
                      <Check size={16} />
                    )}
                  </button>
                ))}
              </div>
            </div>
          </>
        )}
      </div>
    );
  }

  if (variant === 'grid') {
    return (
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-text-primary flex items-center gap-2">
          <Palette size={20} />
          Theme Selection
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {themeList.map((theme) => (
            <button
              key={theme.id}
              onClick={() => setTheme(theme.id)}
              className={`
                relative p-4 rounded-lg border-2 transition-all
                text-left
                ${theme.id === currentThemeId
                  ? 'border-accent-primary bg-accent-primary/10'
                  : 'border-border bg-bg-secondary hover:border-border-light hover:bg-bg-tertiary'
                }
              `}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium text-text-primary">{theme.name}</span>
                {theme.id === currentThemeId && (
                  <div className="flex items-center justify-center w-6 h-6 rounded-full bg-accent-primary">
                    <Check size={14} className="text-white" />
                  </div>
                )}
              </div>
              <div className="text-xs text-text-secondary">
                Click to apply this theme
              </div>
            </button>
          ))}
        </div>
      </div>
    );
  }

  if (variant === 'list') {
    return (
      <div className="space-y-2">
        <h3 className="text-lg font-semibold text-text-primary flex items-center gap-2 mb-3">
          <Palette size={20} />
          Theme Selection
        </h3>
        <div className="space-y-2">
          {themeList.map((theme) => (
            <button
              key={theme.id}
              onClick={() => setTheme(theme.id)}
              className={`
                w-full flex items-center justify-between p-3 rounded-lg
                transition-all
                ${theme.id === currentThemeId
                  ? 'bg-accent-primary/20 border-2 border-accent-primary'
                  : 'bg-bg-secondary border border-border hover:bg-bg-tertiary'
                }
              `}
            >
              <span className="font-medium text-text-primary">{theme.name}</span>
              {theme.id === currentThemeId && (
                <Check size={18} className="text-accent-primary" />
              )}
            </button>
          ))}
        </div>
      </div>
    );
  }

  return null;
};

export default ThemeSwitcher;
