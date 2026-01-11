# PyHammer Theming System Guide

## Overview

PyHammer uses a centralized theming system based on CSS variables and Tailwind CSS. This allows content creators to easily customize the entire application's appearance by modifying values in one place.

## Quick Start for Content Creators

### Option 1: Use a Predefined Theme (Easiest)

The app comes with several predefined themes:
- **Default Dark** - GitHub-inspired dark theme (current default)
- **Purple Gaming** - Vibrant purple for gaming content
- **Cyberpunk Neon** - High-contrast cyan/magenta theme
- **Military Tactical** - Tactical green military theme
- **Ocean Blue** - Calming blue with aqua accents
- **Blood Red** - Intense red theme

To switch themes, use the theme switcher component in your app settings or navigation.

### Option 2: Create Your Own Custom Theme

1. Open `src/themes/themes.js`
2. Copy one of the existing theme objects
3. Modify the values to match your brand
4. Add your theme to the `themes` object
5. Your new theme will appear in the theme switcher

Example:
```javascript
export const myCustomTheme = {
  name: 'My Brand',
  id: 'my-brand',
  colors: {
    bgPrimary: '20 30 40',        // Your dark background
    accentPrimary: '255 100 50',  // Your brand color
    // ... other colors
  },
  // ... other settings
};

// Add to themes object
export const themes = {
  // ... existing themes
  [myCustomTheme.id]: myCustomTheme,
};
```

### Option 3: Quick CSS Variable Override

For quick branding changes, you can override CSS variables directly in `src/index.css`:

```css
:root {
  /* Change your brand color */
  --accent-primary: 255 100 50;  /* RGB format */

  /* Change background */
  --bg-primary: 20 30 40;

  /* Add your logo/font */
  --font-family-sans: 'Your Custom Font', sans-serif;
}
```

## How the Theming System Works

### CSS Variables (Custom Properties)

All theme values are stored as CSS variables in the `:root` selector. These variables are defined in `src/index.css` and can be overridden by the theme system.

**Important:** Colors are stored in RGB format (e.g., `15 20 25`) instead of hex format. This allows Tailwind to apply opacity/alpha values.

To convert hex to RGB:
- `#0f1419` → `15 20 25`
- Use an online converter or: RGB(R, G, B) where R, G, B are decimal values

### Tailwind Integration

Tailwind CSS is configured to use these CSS variables via `tailwind.config.js`. This means you can use Tailwind utility classes with your theme colors:

```jsx
<div className="bg-bg-secondary text-text-primary">
  <button className="bg-accent-primary hover:bg-accent-hover">
    Click me
  </button>
</div>
```

### Pre-built Component Classes

Common components have pre-built classes in `src/index.css`:

- **Buttons:** `btn-primary`, `btn-secondary`, `btn-danger`, `btn-success`
- **Cards:** `card`, `card-elevated`
- **Inputs:** `input`, `select`, `label`
- **Badges:** `badge-success`, `badge-warning`, `badge-danger`, `badge-info`

Example:
```jsx
<button className="btn-primary">Primary Button</button>
<div className="card">Card content</div>
<input className="input" placeholder="Type here..." />
```

## Available CSS Variables

### Colors (RGB format)

#### Backgrounds
- `--bg-primary` - Main background color
- `--bg-secondary` - Cards, panels, secondary areas
- `--bg-tertiary` - Elevated elements, hover states
- `--bg-hover` - Interactive element hover state

#### Text
- `--text-primary` - Primary text color
- `--text-secondary` - Secondary/muted text
- `--text-tertiary` - Very muted text

#### Borders
- `--border-color` - Default border color
- `--border-light` - Lighter borders
- `--border-dark` - Darker borders

#### Accents
- `--accent-primary` - Primary brand/accent color
- `--accent-secondary` - Secondary accent
- `--accent-hover` - Accent hover state

#### Status Colors
- `--success` - Success states (green)
- `--warning` - Warning states (yellow/orange)
- `--danger` - Error/danger states (red)
- `--info` - Informational states (blue)

### Spacing
- `--spacing-section` - Large section spacing (default: 2rem)
- `--spacing-card` - Card/panel padding (default: 1.5rem)
- `--spacing-element` - General element spacing (default: 1rem)

### Border Radius
- `--radius-sm` - Small radius (4px)
- `--radius-md` - Medium radius (8px)
- `--radius-lg` - Large radius (12px)
- `--radius-xl` - Extra large radius (16px)

### Typography
- `--font-family-sans` - Sans-serif font stack
- `--font-family-mono` - Monospace font stack
- `--font-size-xs` through `--font-size-3xl` - Font sizes
- `--line-height-xs` through `--line-height-3xl` - Line heights
- `--font-weight-normal` through `--font-weight-bold` - Font weights

### Shadows
- `--shadow-sm` - Small shadow
- `--shadow-md` - Medium shadow
- `--shadow-lg` - Large shadow
- `--shadow-xl` - Extra large shadow

### Transitions
- `--transition-duration` - Default transition duration (150ms)
- `--transition-timing` - Transition timing function (ease-in-out)

## Using the Theme System in Components

### Method 1: Tailwind Utility Classes (Recommended)

```jsx
function MyComponent() {
  return (
    <div className="bg-bg-secondary text-text-primary p-card rounded-lg border border-border">
      <h2 className="text-xl font-semibold text-text-primary mb-4">
        Title
      </h2>
      <p className="text-text-secondary">
        Description text
      </p>
      <button className="btn-primary mt-4">
        Action
      </button>
    </div>
  );
}
```

### Method 2: Pre-built Component Classes

```jsx
function MyForm() {
  return (
    <form className="card p-card">
      <label className="label">Your Name</label>
      <input className="input w-full" placeholder="Enter name" />

      <label className="label mt-4">Status</label>
      <select className="select w-full">
        <option>Active</option>
        <option>Inactive</option>
      </select>

      <div className="flex gap-3 mt-6">
        <button className="btn-primary">Submit</button>
        <button className="btn-secondary">Cancel</button>
      </div>
    </form>
  );
}
```

### Method 3: Direct CSS Variables (When Needed)

```jsx
function CustomComponent() {
  return (
    <div style={{
      backgroundColor: 'rgb(var(--bg-tertiary))',
      color: 'rgb(var(--text-primary))',
      padding: 'var(--spacing-card)',
      borderRadius: 'var(--radius-lg)',
    }}>
      Content with direct CSS variables
    </div>
  );
}
```

### Method 4: Using the Theme Context

For accessing theme information in JavaScript:

```jsx
import { useTheme } from '../themes/ThemeContext';

function MyComponent() {
  const { currentTheme, currentThemeId, setTheme } = useTheme();

  return (
    <div>
      <p>Current theme: {currentTheme.name}</p>
      <button onClick={() => setTheme('purple-gaming')}>
        Switch to Purple Gaming
      </button>
    </div>
  );
}
```

## Adding the Theme System to Your App

### 1. Wrap Your App with ThemeProvider

Edit `src/main.jsx` or `src/App.jsx`:

```jsx
import { ThemeProvider } from './themes/ThemeContext';

function App() {
  return (
    <ThemeProvider>
      {/* Your app content */}
    </ThemeProvider>
  );
}
```

### 2. Add Theme Switcher to Navigation

```jsx
import ThemeSwitcher from './components/ThemeSwitcher';

function Navigation() {
  return (
    <nav>
      {/* Other nav items */}
      <ThemeSwitcher variant="dropdown" />
    </nav>
  );
}
```

ThemeSwitcher variants:
- `dropdown` - Compact dropdown (good for navbar)
- `grid` - Grid of theme cards (good for settings page)
- `list` - Vertical list (good for sidebar)

## Tips for Content Creators

### 1. Choose Your Brand Colors

Pick 2-3 main colors that represent your brand:
- **Primary color** - Your main brand color (set as `accent-primary`)
- **Secondary color** - Complementary color (set as `accent-secondary`)
- **Background tone** - Dark or light (adjust `bg-primary`, `bg-secondary`, `bg-tertiary`)

### 2. Maintain Contrast

Ensure good contrast between:
- Background and text colors (use a contrast checker)
- Button backgrounds and button text
- Border colors and backgrounds

### 3. Test Your Theme

After creating a custom theme:
1. Navigate through all pages of the app
2. Check forms, buttons, and interactive elements
3. Verify readability in both light and dark conditions
4. Test with different screen sizes

### 4. Keep It Consistent

Stick to your theme variables instead of hard-coding colors:
- ❌ Bad: `className="bg-blue-500"`
- ✅ Good: `className="bg-accent-primary"`

### 5. Use Semantic Colors

Use status colors for their intended purpose:
- `success` - Confirmations, successful actions
- `warning` - Caution, important notices
- `danger` - Errors, destructive actions
- `info` - General information

## Advanced Customization

### Custom Fonts

1. Add your font to the project (via Google Fonts or local files)
2. Update the font variable in your theme:

```javascript
typography: {
  fontFamilySans: "'Your Font', -apple-system, sans-serif",
  // ... other typography settings
}
```

### Custom Shadows for Brand Effect

Create unique shadow effects:

```javascript
shadows: {
  sm: '0 2px 4px rgba(255, 100, 50, 0.2)',  // Brand color shadow
  md: '0 4px 8px rgba(255, 100, 50, 0.3)',
  lg: '0 8px 16px rgba(255, 100, 50, 0.4)',
  xl: '0 12px 24px rgba(255, 100, 50, 0.5)',
}
```

### Different Border Styles

Adjust border radius for different aesthetics:
- **Sharp/Technical:** `sm: '0'`, `md: '0.125rem'`
- **Rounded/Friendly:** `sm: '0.5rem'`, `md: '1rem'`
- **Pill-shaped:** Use `rounded-full` class on elements

## Troubleshooting

### Theme not updating?
- Clear browser cache
- Check that ThemeProvider is wrapping your app
- Verify CSS variables are in RGB format (not hex)

### Colors look wrong?
- Ensure RGB values are correct (0-255 for each component)
- Check that you're using `rgb(var(--variable-name))` format
- Verify Tailwind config matches CSS variable names

### Custom theme not appearing in switcher?
- Ensure theme is added to `themes` object in `themes.js`
- Check that theme has unique `id` and `name` properties

## Examples

See `src/components/examples/ThemedComponents.jsx` for complete component examples using the theming system.

## Support

For issues or questions:
1. Check this guide
2. Review the example components
3. Examine the existing theme definitions in `themes.js`
4. Refer to Tailwind CSS documentation: https://tailwindcss.com/docs

---

**Happy Theming! Make PyHammer your own!** 🎨
