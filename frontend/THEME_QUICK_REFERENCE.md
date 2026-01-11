# PyHammer Theme System - Quick Reference

## 🎨 CSS Variables

### Colors (use with `rgb(var(--variable))`)
```css
/* Backgrounds */
--bg-primary        /* Main background */
--bg-secondary      /* Cards, panels */
--bg-tertiary       /* Elevated elements */
--bg-hover          /* Hover states */

/* Text */
--text-primary      /* Primary text */
--text-secondary    /* Secondary text */
--text-tertiary     /* Muted text */

/* Borders */
--border-color      /* Default border */
--border-light      /* Light border */
--border-dark       /* Dark border */

/* Accents */
--accent-primary    /* Brand color */
--accent-secondary  /* Secondary accent */
--accent-hover      /* Accent hover */

/* Status */
--success           /* Green/success */
--warning           /* Yellow/warning */
--danger            /* Red/error */
--info              /* Blue/info */
```

### Spacing
```css
--spacing-section   /* 2rem */
--spacing-card      /* 1.5rem */
--spacing-element   /* 1rem */
```

### Border Radius
```css
--radius-sm         /* 4px */
--radius-md         /* 8px */
--radius-lg         /* 12px */
--radius-xl         /* 16px */
```

## 🔧 Tailwind Utility Classes

### Backgrounds
```jsx
className="bg-bg-primary"
className="bg-bg-secondary"
className="bg-bg-tertiary"
className="bg-bg-hover"
```

### Text Colors
```jsx
className="text-text-primary"
className="text-text-secondary"
className="text-text-tertiary"
```

### Borders
```jsx
className="border border-border"
className="border-border-light"
className="border-border-dark"
```

### Accent Colors
```jsx
className="bg-accent-primary"
className="text-accent-primary"
className="hover:bg-accent-hover"
```

### Status Colors
```jsx
className="bg-success"
className="text-success"
className="bg-warning"
className="text-warning"
className="bg-danger"
className="text-danger"
className="bg-info"
className="text-info"
```

### Spacing
```jsx
className="p-section"    /* padding: 2rem */
className="p-card"       /* padding: 1.5rem */
className="p-element"    /* padding: 1rem */
```

### Border Radius
```jsx
className="rounded-sm"   /* 4px */
className="rounded-md"   /* 8px */
className="rounded-lg"   /* 12px */
className="rounded-xl"   /* 16px */
```

## 📦 Pre-built Component Classes

### Buttons
```jsx
<button className="btn-primary">Primary</button>
<button className="btn-secondary">Secondary</button>
<button className="btn-success">Success</button>
<button className="btn-danger">Danger</button>
```

### Cards
```jsx
<div className="card">Basic card</div>
<div className="card-elevated">Elevated card</div>
```

### Form Elements
```jsx
<label className="label">Label text</label>
<input className="input" />
<input className="input input-error" />  /* Error state */
<select className="select">...</select>
```

### Badges
```jsx
<span className="badge-success">Success</span>
<span className="badge-warning">Warning</span>
<span className="badge-danger">Danger</span>
<span className="badge-info">Info</span>
```

## 🚀 Common Patterns

### Card with Content
```jsx
<div className="card p-card">
  <h2 className="text-xl font-semibold text-text-primary mb-4">
    Title
  </h2>
  <p className="text-text-secondary">
    Description
  </p>
</div>
```

### Form Group
```jsx
<div>
  <label className="label">Label</label>
  <input className="input w-full" placeholder="Enter value" />
</div>
```

### Button Group
```jsx
<div className="flex gap-3">
  <button className="btn-primary">Save</button>
  <button className="btn-secondary">Cancel</button>
</div>
```

### Status Badge
```jsx
<span className="badge-success">Active</span>
```

### Icon Button
```jsx
<button className="btn-primary flex items-center gap-2">
  <Icon size={18} />
  <span>Button Text</span>
</button>
```

## 🎯 Component Template

```jsx
import React from 'react';
import { Icon } from 'lucide-react';

function MyComponent({ title, children }) {
  return (
    <div className="card p-card">
      <div className="flex items-center gap-3 mb-4">
        <Icon className="text-accent-primary" size={24} />
        <h2 className="text-xl font-semibold text-text-primary">
          {title}
        </h2>
      </div>

      <div className="space-y-4">
        {children}
      </div>

      <div className="flex gap-3 mt-6">
        <button className="btn-primary">Action</button>
        <button className="btn-secondary">Cancel</button>
      </div>
    </div>
  );
}

export default MyComponent;
```

## 🔄 Using Theme Context

```jsx
import { useTheme } from '../themes/ThemeContext';

function MyComponent() {
  const { currentTheme, currentThemeId, setTheme } = useTheme();

  return (
    <div>
      <p>Current: {currentTheme.name}</p>
      <button onClick={() => setTheme('purple-gaming')}>
        Switch Theme
      </button>
    </div>
  );
}
```

## ⚡ Direct CSS Variables

```jsx
<div style={{
  backgroundColor: 'rgb(var(--bg-secondary))',
  color: 'rgb(var(--text-primary))',
  padding: 'var(--spacing-card)',
  borderRadius: 'var(--radius-lg)',
}}>
  Content
</div>
```

## 🎨 Creating Custom Theme

```javascript
// themes/themes.js
export const myTheme = {
  name: 'My Theme',
  id: 'my-theme',
  colors: {
    bgPrimary: '20 30 40',      // RGB format
    accentPrimary: '255 100 50',
    // ... other colors
  },
  // Copy spacing, typography, etc. from defaultDarkTheme
};

// Add to themes object
export const themes = {
  // ... existing
  [myTheme.id]: myTheme,
};
```

## 📱 Responsive Patterns

```jsx
{/* Stack on mobile, side-by-side on desktop */}
<div className="flex flex-col md:flex-row gap-4">
  <div className="card p-card">Left</div>
  <div className="card p-card">Right</div>
</div>

{/* 1 column mobile, 2 tablet, 3 desktop */}
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <div className="card p-card">Item 1</div>
  <div className="card p-card">Item 2</div>
  <div className="card p-card">Item 3</div>
</div>
```

## 🐛 Debugging

```javascript
// Check if CSS variables are loaded
console.log(getComputedStyle(document.documentElement)
  .getPropertyValue('--accent-primary'));

// Get current theme
const { currentTheme } = useTheme();
console.log(currentTheme);
```

## 📚 Files Overview

```
frontend/
├── src/
│   ├── themes/
│   │   ├── themes.js           # Theme definitions
│   │   └── ThemeContext.jsx    # Theme provider & hook
│   ├── components/
│   │   ├── ThemeSwitcher.jsx   # Theme switcher UI
│   │   └── examples/
│   │       └── ThemedComponents.jsx  # Examples
│   └── index.css               # CSS variables & components
├── tailwind.config.js          # Tailwind configuration
├── THEMING_GUIDE.md            # Complete guide
├── INTEGRATION_EXAMPLE.md      # Integration steps
└── THEME_QUICK_REFERENCE.md    # This file
```

## 💡 Pro Tips

1. **Always use theme colors:** Don't hardcode colors like `bg-blue-500`
2. **Use semantic naming:** `btn-primary` instead of `btn-blue`
3. **Test theme switching:** Make sure all components adapt
4. **Maintain contrast:** Check text readability on backgrounds
5. **Be consistent:** Use theme classes throughout your app

## 🔗 Resources

- Full Guide: `THEMING_GUIDE.md`
- Integration: `INTEGRATION_EXAMPLE.md`
- Examples: `src/components/examples/ThemedComponents.jsx`
- Tailwind Docs: https://tailwindcss.com/docs
