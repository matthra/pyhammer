# Theme System Integration Example

This guide shows you how to integrate the theming system into your existing PyHammer app.

## Step 1: Update main.jsx

Add the ThemeProvider to wrap your app:

```jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Toaster } from 'react-hot-toast'
import { ThemeProvider } from './themes/ThemeContext'  // Add this import
import App from './App.jsx'
import './index.css'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000,
    },
  },
})

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <ThemeProvider>  {/* Add ThemeProvider here */}
          <App />
          <Toaster position="top-right" />
        </ThemeProvider>
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>,
)
```

## Step 2: Add Theme Switcher to Your Navigation

Example: Adding to the Layout component:

```jsx
import ThemeSwitcher from './ThemeSwitcher'

function Layout({ children }) {
  return (
    <div className="layout">
      <nav className="navbar">
        {/* Your existing nav items */}
        <div className="nav-right">
          <ThemeSwitcher variant="dropdown" />
        </div>
      </nav>

      <main>{children}</main>
    </div>
  )
}
```

## Step 3: Convert Existing Components to Use Theme Classes

### Before (CSS Modules):
```jsx
// WeaponEditor.jsx
import styles from './WeaponEditor.module.css'

function WeaponEditor() {
  return (
    <div className={styles.container}>
      <button className={styles.primaryButton}>Save</button>
      <input className={styles.input} />
    </div>
  )
}
```

### After (Tailwind + Theme):
```jsx
// WeaponEditor.jsx
function WeaponEditor() {
  return (
    <div className="bg-bg-secondary p-card rounded-lg border border-border">
      <button className="btn-primary">Save</button>
      <input className="input w-full" />
    </div>
  )
}
```

## Step 4: Update Existing CSS Modules (Gradual Migration)

You can mix CSS modules with the theme system during migration:

```css
/* WeaponEditor.module.css */
.container {
  background-color: rgb(var(--bg-secondary));
  border: 1px solid rgb(var(--border-color));
  border-radius: var(--radius-lg);
  padding: var(--spacing-card);
}

.primaryButton {
  background-color: rgb(var(--accent-primary));
  color: white;
  padding: 0.5rem 1rem;
  border-radius: var(--radius-md);
}

.primaryButton:hover {
  background-color: rgb(var(--accent-hover));
}
```

## Step 5: Add a Settings Page with Theme Switcher

```jsx
// src/pages/Settings.jsx
import ThemeSwitcher from '../components/ThemeSwitcher'

function Settings() {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold text-text-primary">Settings</h1>

      <div className="card p-card">
        <ThemeSwitcher variant="grid" />
      </div>

      {/* Other settings */}
    </div>
  )
}

export default Settings
```

## Component Conversion Cheat Sheet

### Containers/Cards
```jsx
// CSS Module
<div className={styles.card}>

// Tailwind Theme
<div className="card p-card">
// or
<div className="bg-bg-secondary border border-border rounded-lg p-4">
```

### Buttons
```jsx
// CSS Module
<button className={styles.primaryBtn}>

// Tailwind Theme
<button className="btn-primary">

// CSS Module
<button className={styles.secondaryBtn}>

// Tailwind Theme
<button className="btn-secondary">
```

### Inputs
```jsx
// CSS Module
<input className={styles.input} />

// Tailwind Theme
<input className="input" />
```

### Labels
```jsx
// CSS Module
<label className={styles.label}>

// Tailwind Theme
<label className="label">
```

### Text Colors
```jsx
// CSS Module
<h1 className={styles.title}>
<p className={styles.description}>

// Tailwind Theme
<h1 className="text-text-primary text-2xl font-bold">
<p className="text-text-secondary">
```

### Badges/Status Indicators
```jsx
// CSS Module
<span className={styles.successBadge}>Active</span>

// Tailwind Theme
<span className="badge-success">Active</span>
<span className="badge-warning">Pending</span>
<span className="badge-danger">Error</span>
```

## Migration Strategy

### Option A: Gradual Migration (Recommended)
1. Keep existing CSS modules working
2. Convert new components to use Tailwind + theme
3. Gradually update old components as you work on them
4. CSS modules can still reference CSS variables

### Option B: Full Migration
1. Replace all CSS module imports with Tailwind classes
2. Delete CSS module files after converting
3. Use theme classes throughout

## Testing Your Integration

1. **Start the dev server:**
   ```bash
   npm run dev
   ```

2. **Verify theme is loading:**
   - Open browser console
   - Check that CSS variables are present on `:root`
   - Theme switcher should appear in your nav

3. **Test theme switching:**
   - Click theme switcher
   - Select different theme
   - Verify all colors update immediately
   - Check localStorage saves preference

4. **Test component updates:**
   - Navigate through all pages
   - Verify themed components look correct
   - Check forms, buttons, cards, badges

## Common Issues

### Issue: Theme not applying
**Solution:** Ensure ThemeProvider wraps your app in main.jsx

### Issue: Tailwind classes not working
**Solution:**
1. Check that `@tailwind` directives are at top of index.css
2. Verify tailwind.config.js is properly configured
3. Restart dev server after config changes

### Issue: Colors in RGB format look wrong
**Solution:** Make sure you're wrapping in `rgb()`:
- ❌ Wrong: `color: var(--text-primary)`
- ✅ Correct: `color: rgb(var(--text-primary))`

### Issue: Custom Tailwind classes not found
**Solution:** Check that class names in tailwind.config.js match CSS variable names

## Next Steps

1. Add theme switcher to your navigation
2. Convert one component to test the system
3. Create your custom theme in themes.js
4. Gradually migrate other components
5. Share your themed PyHammer with your community!

## Example: Complete Button Component

```jsx
// components/Button.jsx
import React from 'react';

const Button = ({
  children,
  variant = 'primary',
  onClick,
  disabled = false,
  type = 'button',
  className = '',
}) => {
  const variantClasses = {
    primary: 'btn-primary',
    secondary: 'btn-secondary',
    success: 'btn-success',
    danger: 'btn-danger',
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${variantClasses[variant]} ${className}`}
    >
      {children}
    </button>
  );
};

export default Button;

// Usage:
// <Button variant="primary" onClick={handleSave}>Save Unit</Button>
// <Button variant="danger" onClick={handleDelete}>Delete</Button>
```

## Resources

- See `THEMING_GUIDE.md` for complete theming documentation
- See `src/components/examples/ThemedComponents.jsx` for component examples
- See `src/themes/themes.js` for theme definitions
- Tailwind CSS docs: https://tailwindcss.com/docs
