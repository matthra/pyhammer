# Migrating CSS Modules to Theme System

This guide helps you migrate existing CSS Module files to use the new theming system while maintaining compatibility during the transition.

## Migration Strategies

### Strategy A: Hybrid Approach (Recommended for Gradual Migration)

Keep CSS Modules but update them to use CSS variables. This allows you to migrate gradually without breaking existing code.

### Strategy B: Full Tailwind Migration

Replace CSS Modules entirely with Tailwind utility classes and theme component classes.

## Strategy A: Hybrid CSS Modules + CSS Variables

### Before
```css
/* WeaponEditor.module.css */
.container {
  background-color: #1a1f2e;
  border: 1px solid #30363d;
  border-radius: 8px;
  padding: 24px;
}

.title {
  color: #e6edf3;
  font-size: 20px;
  font-weight: 600;
}

.button {
  background-color: #58a6ff;
  color: white;
  padding: 8px 16px;
  border-radius: 6px;
}

.button:hover {
  background-color: #1f6feb;
}
```

### After (Using CSS Variables)
```css
/* WeaponEditor.module.css */
.container {
  background-color: rgb(var(--bg-secondary));
  border: 1px solid rgb(var(--border-color));
  border-radius: var(--radius-md);
  padding: var(--spacing-card);
}

.title {
  color: rgb(var(--text-primary));
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
}

.button {
  background-color: rgb(var(--accent-primary));
  color: white;
  padding: 0.5rem 1rem;
  border-radius: var(--radius-md);
  transition: background-color var(--transition-duration) var(--transition-timing);
}

.button:hover {
  background-color: rgb(var(--accent-hover));
}
```

**Benefits:**
- ✅ No component code changes needed
- ✅ Automatically adapts to theme changes
- ✅ Can migrate at your own pace
- ✅ Easy to convert later to full Tailwind

## Strategy B: Full Tailwind Migration

### Before
```jsx
// WeaponEditor.jsx
import styles from './WeaponEditor.module.css'

function WeaponEditor() {
  return (
    <div className={styles.container}>
      <h2 className={styles.title}>Edit Weapon</h2>
      <button className={styles.button}>Save</button>
    </div>
  )
}
```

### After (Using Tailwind + Theme Classes)
```jsx
// WeaponEditor.jsx
function WeaponEditor() {
  return (
    <div className="bg-bg-secondary border border-border rounded-lg"
         style={{padding: 'var(--spacing-card)'}}>
      <h2 className="text-text-primary text-xl font-semibold">Edit Weapon</h2>
      <button className="btn-primary">Save</button>
    </div>
  )
}
```

**Benefits:**
- ✅ No CSS files to maintain
- ✅ Faster development
- ✅ Smaller bundle size
- ✅ More flexible styling

## Step-by-Step Migration Examples

### Example 1: Card Container

**CSS Module Before:**
```css
.card {
  background: #1a1f2e;
  border: 1px solid #30363d;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.4);
}
```

**Option A - CSS Module with Variables:**
```css
.card {
  background: rgb(var(--bg-secondary));
  border: 1px solid rgb(var(--border-color));
  border-radius: var(--radius-lg);
  padding: var(--spacing-card);
  box-shadow: var(--shadow-md);
}
```

**Option B - Tailwind Classes:**
```jsx
<div className="card" style={{padding: 'var(--spacing-card)'}}>
  {/* or */}
<div className="bg-bg-secondary border border-border rounded-lg shadow-md"
     style={{padding: 'var(--spacing-card)'}}>
```

### Example 2: Buttons

**CSS Module Before:**
```css
.primaryButton {
  background: #58a6ff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
}

.primaryButton:hover {
  background: #1f6feb;
}

.secondaryButton {
  background: #252b3b;
  color: #e6edf3;
  border: 1px solid #30363d;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
}
```

**Option A - CSS Module with Variables:**
```css
.primaryButton {
  background: rgb(var(--accent-primary));
  color: white;
  border: none;
  padding: 0.625rem 1.25rem;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background var(--transition-duration) var(--transition-timing);
}

.primaryButton:hover {
  background: rgb(var(--accent-hover));
}

.secondaryButton {
  background: rgb(var(--bg-tertiary));
  color: rgb(var(--text-primary));
  border: 1px solid rgb(var(--border-color));
  padding: 0.625rem 1.25rem;
  border-radius: var(--radius-md);
  cursor: pointer;
}
```

**Option B - Use Pre-built Classes:**
```jsx
<button className="btn-primary">Primary Action</button>
<button className="btn-secondary">Secondary Action</button>
```

### Example 3: Form Inputs

**CSS Module Before:**
```css
.inputGroup {
  margin-bottom: 20px;
}

.label {
  display: block;
  color: #8b949e;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 6px;
}

.input {
  width: 100%;
  background: #252b3b;
  border: 1px solid #30363d;
  border-radius: 6px;
  padding: 10px 12px;
  color: #e6edf3;
}

.input:focus {
  outline: none;
  border-color: #58a6ff;
  box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.3);
}
```

**Option A - CSS Module with Variables:**
```css
.inputGroup {
  margin-bottom: 1.25rem;
}

.label {
  display: block;
  color: rgb(var(--text-secondary));
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  margin-bottom: 0.375rem;
}

.input {
  width: 100%;
  background: rgb(var(--bg-tertiary));
  border: 1px solid rgb(var(--border-color));
  border-radius: var(--radius-md);
  padding: 0.625rem 0.75rem;
  color: rgb(var(--text-primary));
  transition: all var(--transition-duration) var(--transition-timing);
}

.input:focus {
  outline: none;
  border-color: transparent;
  box-shadow: 0 0 0 2px rgb(var(--accent-primary) / 0.5);
}
```

**Option B - Use Pre-built Classes:**
```jsx
<div style={{marginBottom: '1.25rem'}}>
  <label className="label">Your Label</label>
  <input className="input w-full" />
</div>
```

### Example 4: Status Badges

**CSS Module Before:**
```css
.badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.badgeSuccess {
  background: rgba(63, 185, 80, 0.2);
  color: #3fb950;
  border: 1px solid rgba(63, 185, 80, 0.3);
}

.badgeWarning {
  background: rgba(210, 153, 34, 0.2);
  color: #d29922;
  border: 1px solid rgba(210, 153, 34, 0.3);
}

.badgeDanger {
  background: rgba(248, 81, 73, 0.2);
  color: #f85149;
  border: 1px solid rgba(248, 81, 73, 0.3);
}
```

**Option A - CSS Module with Variables:**
```css
.badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: var(--radius-lg);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
}

.badgeSuccess {
  background: rgb(var(--success) / 0.2);
  color: rgb(var(--success));
  border: 1px solid rgb(var(--success) / 0.3);
}

.badgeWarning {
  background: rgb(var(--warning) / 0.2);
  color: rgb(var(--warning));
  border: 1px solid rgb(var(--warning) / 0.3);
}

.badgeDanger {
  background: rgb(var(--danger) / 0.2);
  color: rgb(var(--danger));
  border: 1px solid rgb(var(--danger) / 0.3);
}
```

**Option B - Use Pre-built Classes:**
```jsx
<span className="badge-success">Success</span>
<span className="badge-warning">Warning</span>
<span className="badge-danger">Danger</span>
```

## Color Conversion Reference

### Hex to RGB Conversion

```
Hex Color        →  RGB Format
#0f1419         →  15 20 25
#1a1f2e         →  26 31 46
#252b3b         →  37 43 59
#e6edf3         →  230 237 243
#8b949e         →  139 148 158
#30363d         →  48 54 61
#58a6ff         →  88 166 255
#1f6feb         →  31 111 235
#3fb950         →  63 185 80
#d29922         →  210 153 34
#f85149         →  248 81 73
```

### Using RGB in CSS

```css
/* Solid color */
color: rgb(var(--text-primary));

/* With opacity */
background: rgb(var(--accent-primary) / 0.2);
color: rgb(var(--text-secondary) / 0.8);
```

## Migration Checklist

### For Each CSS Module File:

- [ ] Identify all hardcoded colors
- [ ] Replace with CSS variable equivalents
- [ ] Convert spacing to use CSS variables
- [ ] Update font sizes to use CSS variables
- [ ] Update border radius to use CSS variables
- [ ] Test component with different themes
- [ ] Verify no visual regressions

### CSS Variable Replacements:

**Colors:**
- `#0f1419`, `#1a1f2e` → `rgb(var(--bg-primary))` or `rgb(var(--bg-secondary))`
- `#252b3b` → `rgb(var(--bg-tertiary))`
- `#e6edf3` → `rgb(var(--text-primary))`
- `#8b949e` → `rgb(var(--text-secondary))`
- `#30363d` → `rgb(var(--border-color))`
- `#58a6ff` → `rgb(var(--accent-primary))`
- `#1f6feb` → `rgb(var(--accent-hover))`
- `#3fb950` → `rgb(var(--success))`
- `#d29922` → `rgb(var(--warning))`
- `#f85149` → `rgb(var(--danger))`

**Spacing:**
- `24px` → `var(--spacing-card)` or `1.5rem`
- `32px` → `var(--spacing-section)` or `2rem`
- `16px` → `var(--spacing-element)` or `1rem`

**Border Radius:**
- `4px` → `var(--radius-sm)`
- `6px`, `8px` → `var(--radius-md)`
- `12px` → `var(--radius-lg)`
- `16px` → `var(--radius-xl)`

**Font Sizes:**
- `12px` → `var(--font-size-xs)`
- `14px` → `var(--font-size-sm)`
- `16px` → `var(--font-size-base)`
- `18px` → `var(--font-size-lg)`
- `20px` → `var(--font-size-xl)`

## Testing After Migration

1. **Visual Test:**
   - Compare before/after screenshots
   - Check all component states (hover, focus, disabled)
   - Verify spacing and alignment

2. **Theme Switching Test:**
   - Switch to each predefined theme
   - Verify component looks good in all themes
   - Check text contrast and readability

3. **Responsive Test:**
   - Test on mobile, tablet, desktop
   - Verify layout doesn't break
   - Check touch targets on mobile

## Common Pitfalls

### ❌ Forgetting `rgb()` wrapper
```css
/* Wrong */
color: var(--text-primary);

/* Correct */
color: rgb(var(--text-primary));
```

### ❌ Using hex instead of RGB
```css
/* Wrong - won't update with themes */
color: #e6edf3;

/* Correct */
color: rgb(var(--text-primary));
```

### ❌ Hardcoding opacity without RGB
```css
/* Wrong */
background: var(--accent-primary);
opacity: 0.2;  /* Affects entire element */

/* Correct */
background: rgb(var(--accent-primary) / 0.2);  /* Only affects background */
```

## Need Help?

- See `THEMING_GUIDE.md` for complete CSS variable reference
- Check `THEME_QUICK_REFERENCE.md` for quick syntax lookup
- Review `src/components/examples/ThemedComponents.jsx` for examples

---

**Take your time with migration - the hybrid approach works great!**
