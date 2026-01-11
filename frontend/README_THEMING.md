# 🎨 PyHammer Theming System

> **A complete, production-ready theming solution for content creators and streamers**

## 📋 Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Features](#features)
4. [Documentation](#documentation)
5. [File Structure](#file-structure)
6. [Usage Examples](#usage-examples)
7. [Creating Custom Themes](#creating-custom-themes)
8. [FAQ](#faq)

## Overview

PyHammer now includes a comprehensive theming system that allows content creators to easily rebrand the entire application with their own colors and styles. The system is built on:

- **CSS Variables** - Centralized theme control
- **Tailwind CSS v4** - Utility-first styling
- **React Context** - Runtime theme switching
- **6 Predefined Themes** - Ready to use

### What This Means for You

✅ **Content Creators:** Change your brand colors in one place - the entire app updates
✅ **Streamers:** Switch between themes to match different games or events
✅ **Developers:** Use consistent styling with minimal effort
✅ **Tournament Organizers:** Apply sponsor branding quickly

## Quick Start

### 1. Activate the Theme System (2 steps)

**Step 1:** Add ThemeProvider to `src/main.jsx`

```jsx
import { ThemeProvider } from './themes/ThemeContext'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <ThemeProvider>  {/* 👈 Add this */}
          <App />
          <Toaster position="top-right" />
        </ThemeProvider>
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>,
)
```

**Step 2:** Add ThemeSwitcher to your navigation

```jsx
import ThemeSwitcher from './components/ThemeSwitcher'

function YourNav() {
  return (
    <nav>
      {/* Your nav items */}
      <ThemeSwitcher variant="dropdown" />
    </nav>
  )
}
```

### 2. Start Using Themed Components

```jsx
function MyComponent() {
  return (
    <div className="card" style={{padding: 'var(--spacing-card)'}}>
      <h2 className="text-xl font-semibold text-text-primary">Title</h2>
      <button className="btn-primary">Action</button>
      <button className="btn-secondary">Cancel</button>
    </div>
  )
}
```

### 3. Customize Your Brand

Edit `src/index.css` to change your brand color:

```css
:root {
  --accent-primary: 255 100 50;  /* Your brand color in RGB */
}
```

**That's it!** The entire app now uses your brand colors.

## Features

### ✨ Core Features

- **6 Predefined Themes** - Default Dark, Purple Gaming, Cyberpunk, Military, Ocean, Blood Red
- **Runtime Theme Switching** - No page reload required
- **LocalStorage Persistence** - Theme preference saved
- **CSS Variables** - Centralized control of all theme aspects
- **Tailwind Integration** - Full Tailwind CSS v4 support
- **Pre-built Components** - Buttons, cards, forms, badges ready to use
- **Production Ready** - Build tested and verified ✅

### 🎯 Theme Aspects You Can Control

- **Colors:** Backgrounds, text, borders, accents, status colors
- **Spacing:** Section, card, and element spacing
- **Typography:** Font families, sizes, weights, line heights
- **Borders:** Border radius (sharp to rounded)
- **Shadows:** Box shadow depths
- **Transitions:** Animation timing and duration

## Documentation

| Document | Description | Best For |
|----------|-------------|----------|
| **SETUP_COMPLETE.md** | Setup summary & next steps | Everyone (start here) |
| **THEMING_GUIDE.md** | Complete theming guide | Content creators |
| **INTEGRATION_EXAMPLE.md** | Integration steps | Developers |
| **THEME_QUICK_REFERENCE.md** | Quick syntax reference | Developers |
| **CSS_MODULES_MIGRATION.md** | Migrating existing CSS | Developers |
| **README_THEMING.md** | This file (overview) | Everyone |

### Quick Links

- 🚀 [Setup Instructions](SETUP_COMPLETE.md)
- 📖 [Complete Guide](THEMING_GUIDE.md)
- ⚡ [Quick Reference](THEME_QUICK_REFERENCE.md)
- 🔄 [Migration Guide](CSS_MODULES_MIGRATION.md)

## File Structure

```
frontend/
├── src/
│   ├── themes/
│   │   ├── themes.js                # Theme definitions
│   │   └── ThemeContext.jsx         # Theme provider & hook
│   ├── components/
│   │   ├── ThemeSwitcher.jsx        # Theme switcher UI
│   │   └── examples/
│   │       └── ThemedComponents.jsx # Usage examples
│   └── index.css                    # CSS variables & component classes
├── postcss.config.js                # Tailwind v4 PostCSS config
├── SETUP_COMPLETE.md                # Setup instructions
├── THEMING_GUIDE.md                 # Complete guide
├── INTEGRATION_EXAMPLE.md           # Integration steps
├── THEME_QUICK_REFERENCE.md         # Quick reference
├── CSS_MODULES_MIGRATION.md         # Migration guide
└── README_THEMING.md                # This file
```

## Usage Examples

### Example 1: Using Pre-built Button Classes

```jsx
<button className="btn-primary">Primary Action</button>
<button className="btn-secondary">Secondary Action</button>
<button className="btn-success">Confirm</button>
<button className="btn-danger">Delete</button>
```

### Example 2: Using Pre-built Card Class

```jsx
<div className="card" style={{padding: 'var(--spacing-card)'}}>
  <h2>Card Title</h2>
  <p>Card content goes here</p>
</div>
```

### Example 3: Using Pre-built Form Classes

```jsx
<div>
  <label className="label">Your Name</label>
  <input className="input w-full" placeholder="Enter name" />
</div>

<div>
  <label className="label">Type</label>
  <select className="select w-full">
    <option>Option 1</option>
    <option>Option 2</option>
  </select>
</div>
```

### Example 4: Using Status Badges

```jsx
<span className="badge-success">Active</span>
<span className="badge-warning">Pending</span>
<span className="badge-danger">Critical</span>
<span className="badge-info">Info</span>
```

### Example 5: Using Tailwind with Theme Colors

```jsx
<div className="bg-bg-secondary text-text-primary rounded-lg p-6 border border-border">
  <h2 className="text-xl font-semibold text-text-primary mb-4">Title</h2>
  <p className="text-text-secondary">Description text</p>
  <button className="bg-accent-primary hover:bg-accent-hover text-white px-4 py-2 rounded-md">
    Action
  </button>
</div>
```

### Example 6: Using CSS Variables Directly

```jsx
<div style={{
  backgroundColor: 'rgb(var(--bg-tertiary))',
  color: 'rgb(var(--text-primary))',
  padding: 'var(--spacing-card)',
  borderRadius: 'var(--radius-lg)',
}}>
  Custom styled content
</div>
```

### Example 7: Accessing Theme in JavaScript

```jsx
import { useTheme } from '../themes/ThemeContext'

function MyComponent() {
  const { currentTheme, setTheme } = useTheme()

  return (
    <div>
      <p>Current theme: {currentTheme.name}</p>
      <button onClick={() => setTheme('purple-gaming')}>
        Switch to Purple Gaming
      </button>
    </div>
  )
}
```

## Creating Custom Themes

### Method 1: Quick Brand Color (Easiest)

Edit `src/index.css`:

```css
:root {
  /* Your brand color */
  --accent-primary: 168 85 247;  /* Purple */
  --accent-hover: 147 51 234;    /* Darker purple */

  /* Optional: adjust backgrounds */
  --bg-primary: 15 10 25;        /* Deep purple background */
}
```

### Method 2: Full Custom Theme

Edit `src/themes/themes.js`:

```javascript
export const myBrandTheme = {
  name: 'My Brand',
  id: 'my-brand',
  colors: {
    // Background colors (RGB format)
    bgPrimary: '20 30 40',
    bgSecondary: '30 40 50',
    bgTertiary: '40 50 60',
    bgHover: '50 60 70',

    // Text colors
    textPrimary: '240 240 250',
    textSecondary: '180 180 190',
    textTertiary: '140 140 150',

    // Border colors
    borderColor: '60 70 80',
    borderLight: '70 80 90',
    borderDark: '50 60 70',

    // Accent colors (your brand!)
    accentPrimary: '255 100 50',    // Your main brand color
    accentSecondary: '255 150 100', // Complementary color
    accentHover: '230 80 40',       // Darker version for hover

    // Status colors
    success: '63 185 80',
    warning: '210 153 34',
    danger: '248 81 73',
    info: '56 139 253',
  },
  // Copy other settings from defaultDarkTheme
  spacing: defaultDarkTheme.spacing,
  borderRadius: defaultDarkTheme.borderRadius,
  typography: defaultDarkTheme.typography,
  shadows: defaultDarkTheme.shadows,
  transitions: defaultDarkTheme.transitions,
}

// Add to themes object
export const themes = {
  'default-dark': defaultDarkTheme,
  'purple-gaming': purpleGamingTheme,
  'cyberpunk': cyberpunkTheme,
  'military': militaryTheme,
  'ocean': oceanTheme,
  'blood-red': bloodRedTheme,
  'my-brand': myBrandTheme,  // 👈 Add here
}
```

Your theme will automatically appear in the theme switcher!

### Converting Hex to RGB

Use this formula: `#RRGGBB` → `R G B` (decimal values)

Examples:
- `#FF6432` → `255 100 50`
- `#A855F7` → `168 85 247`
- `#1F2937` → `31 41 55`

Or use an online converter.

## FAQ

### Q: Do I need to modify all my existing components?

**A:** No! You have options:
1. Keep using CSS Modules and update them to use CSS variables
2. Gradually migrate to Tailwind classes
3. Mix both approaches during transition

See [CSS_MODULES_MIGRATION.md](CSS_MODULES_MIGRATION.md) for details.

### Q: Can I use both Tailwind classes and my own CSS?

**A:** Yes! The system is flexible:
- Use Tailwind utilities for quick styling
- Use pre-built component classes (.btn-primary, .card, etc.)
- Use CSS Modules with CSS variables
- Write custom CSS with CSS variables
- Mix all approaches

### Q: How do I create a theme for my streaming brand?

**A:** Follow Method 2 above. Pick your brand's main color and convert it to RGB format. The system will handle the rest. See [THEMING_GUIDE.md](THEMING_GUIDE.md) for detailed instructions.

### Q: Will themes affect performance?

**A:** No! CSS variables are native browser features with zero performance impact. Theme switching is instant.

### Q: Can users create their own themes?

**A:** Currently, themes are defined in code. You could add a UI for custom theme creation, but that's beyond the current system's scope.

### Q: What if I want to override a specific component's color?

**A:** You can use inline styles or create component-specific CSS classes:

```jsx
<button
  className="btn-primary"
  style={{backgroundColor: 'rgb(255 100 50)'}}
>
  Custom colored button
</button>
```

### Q: How do I test my theme on all pages?

**A:** After creating your theme:
1. Start dev server: `npm run dev`
2. Use ThemeSwitcher to select your theme
3. Navigate through all pages
4. Check readability, contrast, and visual appeal
5. Adjust colors as needed

### Q: Can I export my theme for others to use?

**A:** Yes! Just share your theme object from `themes.js`. Others can copy it into their `themes.js` file.

### Q: Does this work on mobile?

**A:** Yes! The theming system is fully responsive and works on all devices.

## Available Themes

| Theme | Description | Best For |
|-------|-------------|----------|
| **Default Dark** | GitHub-inspired dark theme | General use, development |
| **Purple Gaming** | Vibrant purple | Gaming streams, esports |
| **Cyberpunk Neon** | High-contrast cyan/magenta | Tech content, cyberpunk games |
| **Military Tactical** | Tactical green | Military simulators, strategy games |
| **Ocean Blue** | Calming blue/aqua | Professional streams, educational |
| **Blood Red** | Intense red | Action games, aggressive content |

## Component Class Reference

### Buttons
- `.btn-primary` - Primary action button
- `.btn-secondary` - Secondary action button
- `.btn-success` - Success/confirm button
- `.btn-danger` - Delete/destructive button

### Cards
- `.card` - Basic card container
- `.card-elevated` - Card with more shadow

### Forms
- `.input` - Text input field
- `.select` - Dropdown select
- `.label` - Form label
- `.input-error` - Error state for inputs

### Badges
- `.badge-success` - Green success badge
- `.badge-warning` - Yellow warning badge
- `.badge-danger` - Red danger/error badge
- `.badge-info` - Blue informational badge

## Tailwind Classes for Theme Colors

### Backgrounds
- `bg-bg-primary`, `bg-bg-secondary`, `bg-bg-tertiary`, `bg-bg-hover`

### Text
- `text-text-primary`, `text-text-secondary`, `text-text-tertiary`

### Borders
- `border-border`, `border-border-light`, `border-border-dark`

### Accents
- `bg-accent-primary`, `bg-accent-secondary`, `bg-accent-hover`
- `text-accent-primary`, `text-accent-secondary`

### Status
- `bg-success`, `bg-warning`, `bg-danger`, `bg-info`
- `text-success`, `text-warning`, `text-danger`, `text-info`

## Support & Resources

- 📖 **Complete Documentation:** See [THEMING_GUIDE.md](THEMING_GUIDE.md)
- ⚡ **Quick Reference:** See [THEME_QUICK_REFERENCE.md](THEME_QUICK_REFERENCE.md)
- 🔧 **Integration Help:** See [INTEGRATION_EXAMPLE.md](INTEGRATION_EXAMPLE.md)
- 🔄 **Migration Guide:** See [CSS_MODULES_MIGRATION.md](CSS_MODULES_MIGRATION.md)
- 💻 **Code Examples:** See `src/components/examples/ThemedComponents.jsx`
- 🎨 **Theme Definitions:** See `src/themes/themes.js`

## Next Steps

1. ✅ Read [SETUP_COMPLETE.md](SETUP_COMPLETE.md) for activation steps
2. ✅ Add ThemeProvider to your app
3. ✅ Add ThemeSwitcher to navigation
4. ✅ Test theme switching
5. ✅ Create your custom theme
6. ✅ Share your themed PyHammer!

---

**Ready to make PyHammer your own? Start with [SETUP_COMPLETE.md](SETUP_COMPLETE.md)!** 🚀

*Built with ❤️ for content creators, streamers, and wargaming enthusiasts*
