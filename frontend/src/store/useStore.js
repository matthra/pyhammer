import { create } from 'zustand'

/**
 * Global state management using Zustand
 * Replaces Streamlit's session_state with proper React state
 */
const useStore = create((set, get) => ({
  // Current roster
  roster: [],
  rosterFilename: null,

  // Target settings
  selectedTarget: null,
  targetList: [],
  targetListFilename: null,

  // Global settings
  assumeCover: false,
  assumeHalfRange: false,

  // UI state
  selectedUnitId: null,

  // Actions
  setRoster: (roster) => set({ roster }),
  setRosterFilename: (filename) => set({ rosterFilename: filename }),

  addWeapon: (weapon, unitId = null) => set((state) => {
    // If unitId is provided, inherit Name, Qty, Pts from existing unit weapons
    if (unitId) {
      const existingWeapon = state.roster.find(w => w.UnitID === unitId)
      if (existingWeapon) {
        weapon = {
          ...weapon,
          UnitID: unitId,
          Name: existingWeapon.Name,
          Qty: existingWeapon.Qty,
          Pts: existingWeapon.Pts
        }
      }
    }
    return { roster: [...state.roster, weapon] }
  }),

  updateWeapon: (unitId, weaponIndex, updates) => set((state) => ({
    roster: state.roster.map((weapon, idx) =>
      weapon.UnitID === unitId && idx === weaponIndex
        ? { ...weapon, ...updates }
        : weapon
    )
  })),

  updateUnitAttributes: (unitId, updates) => set((state) => ({
    roster: state.roster.map((weapon) =>
      weapon.UnitID === unitId
        ? { ...weapon, ...updates }
        : weapon
    )
  })),

  deleteWeapon: (unitId, weaponIndex) => set((state) => ({
    roster: state.roster.filter((weapon, idx) =>
      !(weapon.UnitID === unitId && idx === weaponIndex)
    )
  })),

  deleteUnit: (unitId) => set((state) => ({
    roster: state.roster.filter((weapon) => weapon.UnitID !== unitId),
    selectedUnitId: state.selectedUnitId === unitId ? null : state.selectedUnitId
  })),

  setSelectedTarget: (target) => set({ selectedTarget: target }),
  setTargetList: (targets) => set({ targetList: targets }),
  setTargetListFilename: (filename) => set({ targetListFilename: filename }),

  setAssumeCover: (value) => set({ assumeCover: value }),
  setAssumeHalfRange: (value) => set({ assumeHalfRange: value }),

  setSelectedUnitId: (unitId) => set({ selectedUnitId: unitId }),

  // Helper: Get weapons for a specific unit
  getUnitWeapons: (unitId) => {
    const state = get()
    return state.roster.filter((weapon) => weapon.UnitID === unitId)
  },

  // Helper: Get unique units
  getUnits: () => {
    const state = get()
    const unitMap = new Map()

    state.roster.forEach((weapon) => {
      if (!unitMap.has(weapon.UnitID)) {
        unitMap.set(weapon.UnitID, {
          UnitID: weapon.UnitID,
          Name: weapon.Name,
          Qty: weapon.Qty,
          Pts: weapon.Pts,
          weaponCount: 0,
        })
      }
      const unit = unitMap.get(weapon.UnitID)
      unit.weaponCount++
    })

    return Array.from(unitMap.values())
  },
}))

export default useStore
