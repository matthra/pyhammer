import React, { useState } from 'react';
import { Shield, Zap, Target, Settings } from 'lucide-react';

/**
 * Example Components Demonstrating the Theming System
 *
 * These examples show different ways to use the theming system:
 * 1. Using Tailwind utility classes with CSS variables
 * 2. Using custom component classes from index.css
 * 3. Using CSS variables directly in inline styles
 */

/**
 * Example 1: Card with Tailwind Utilities
 * Uses Tailwind classes that reference CSS variables
 */
export const ThemedCard = ({ title, children, icon: Icon }) => {
  return (
    <div className="bg-bg-secondary border border-border rounded-lg p-card shadow-md hover:shadow-lg transition-shadow">
      <div className="flex items-center gap-3 mb-4">
        {Icon && (
          <div className="w-10 h-10 rounded-lg bg-accent-primary/20 flex items-center justify-center">
            <Icon size={20} className="text-accent-primary" />
          </div>
        )}
        <h3 className="text-lg font-semibold text-text-primary">{title}</h3>
      </div>
      <div className="text-text-secondary">
        {children}
      </div>
    </div>
  );
};

/**
 * Example 2: Button with Custom Classes
 * Uses the pre-defined button classes from index.css
 */
export const ThemedButtons = () => {
  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-text-primary">Button Variants</h3>
      <div className="flex flex-wrap gap-3">
        <button className="btn-primary">
          Primary Button
        </button>
        <button className="btn-secondary">
          Secondary Button
        </button>
        <button className="btn-success">
          Success Button
        </button>
        <button className="btn-danger">
          Danger Button
        </button>
        <button className="btn-primary" disabled>
          Disabled Button
        </button>
      </div>
    </div>
  );
};

/**
 * Example 3: Form with Themed Inputs
 * Demonstrates form elements using the theming system
 */
export const ThemedForm = () => {
  const [formData, setFormData] = useState({
    unitName: '',
    unitType: '',
    attacks: '',
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className="card p-card">
      <h3 className="text-lg font-semibold text-text-primary mb-4 flex items-center gap-2">
        <Settings size={20} />
        Unit Configuration
      </h3>
      <form className="space-y-4">
        <div>
          <label htmlFor="unitName" className="label">
            Unit Name
          </label>
          <input
            id="unitName"
            name="unitName"
            type="text"
            className="input w-full"
            placeholder="Enter unit name"
            value={formData.unitName}
            onChange={handleChange}
          />
        </div>

        <div>
          <label htmlFor="unitType" className="label">
            Unit Type
          </label>
          <select
            id="unitType"
            name="unitType"
            className="select w-full"
            value={formData.unitType}
            onChange={handleChange}
          >
            <option value="">Select type...</option>
            <option value="infantry">Infantry</option>
            <option value="vehicle">Vehicle</option>
            <option value="monster">Monster</option>
          </select>
        </div>

        <div>
          <label htmlFor="attacks" className="label">
            Number of Attacks
          </label>
          <input
            id="attacks"
            name="attacks"
            type="number"
            className="input w-full"
            placeholder="0"
            value={formData.attacks}
            onChange={handleChange}
          />
        </div>

        <div className="flex gap-3 pt-2">
          <button type="submit" className="btn-primary">
            Save Unit
          </button>
          <button type="button" className="btn-secondary">
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

/**
 * Example 4: Badge System
 * Demonstrates status badges with different colors
 */
export const ThemedBadges = () => {
  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-text-primary">Status Badges</h3>
      <div className="flex flex-wrap gap-3">
        <span className="badge-success">Active</span>
        <span className="badge-warning">Pending</span>
        <span className="badge-danger">Critical</span>
        <span className="badge-info">Info</span>
      </div>
    </div>
  );
};

/**
 * Example 5: Stats Grid
 * Shows a grid of statistics using theme colors
 */
export const ThemedStatsGrid = () => {
  const stats = [
    { label: 'Total Units', value: '24', icon: Shield, color: 'accent-primary' },
    { label: 'Avg Damage', value: '8.4', icon: Zap, color: 'warning' },
    { label: 'Hit Rate', value: '67%', icon: Target, color: 'success' },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
      {stats.map((stat, index) => (
        <div
          key={index}
          className="bg-bg-secondary border border-border rounded-lg p-4 hover:bg-bg-tertiary transition-colors"
        >
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-text-secondary">{stat.label}</span>
            <stat.icon size={18} className={`text-${stat.color}`} />
          </div>
          <div className={`text-2xl font-bold text-${stat.color}`}>
            {stat.value}
          </div>
        </div>
      ))}
    </div>
  );
};

/**
 * Example 6: Using CSS Variables Directly
 * Sometimes you need direct access to CSS variables
 */
export const DirectCSSVariables = () => {
  return (
    <div
      style={{
        backgroundColor: 'rgb(var(--bg-tertiary))',
        border: '2px solid rgb(var(--accent-primary))',
        borderRadius: 'var(--radius-lg)',
        padding: 'var(--spacing-card)',
        color: 'rgb(var(--text-primary))',
      }}
    >
      <h3 style={{ fontSize: 'var(--font-size-xl)', marginBottom: '1rem' }}>
        Direct CSS Variables
      </h3>
      <p style={{ color: 'rgb(var(--text-secondary))' }}>
        This component uses CSS variables directly in inline styles,
        which is useful for dynamic styling or when Tailwind classes aren't sufficient.
      </p>
    </div>
  );
};

/**
 * Example 7: Complete Example Page
 * Combines all examples into a demo page
 */
export const ThemeExamplesPage = () => {
  return (
    <div className="min-h-screen bg-bg-primary p-6 space-y-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-text-primary mb-2">
          PyHammer Theming System Examples
        </h1>
        <p className="text-text-secondary mb-8">
          Demonstrating various components using the centralized theme system
        </p>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <ThemedCard title="Welcome to PyHammer" icon={Shield}>
            This card demonstrates the theming system using Tailwind utilities
            that reference CSS variables. Change the theme to see it update automatically.
          </ThemedCard>

          <div className="space-y-6">
            <ThemedButtons />
            <ThemedBadges />
          </div>
        </div>

        <div className="mt-6">
          <ThemedStatsGrid />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
          <ThemedForm />
          <DirectCSSVariables />
        </div>
      </div>
    </div>
  );
};

export default ThemeExamplesPage;
