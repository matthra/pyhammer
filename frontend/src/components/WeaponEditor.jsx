import { useState } from 'react'
import useStore from '../store/useStore'
import styles from './WeaponEditor.module.css'

function WeaponEditor({ weapon, unitId, weaponIndex }) {
  const { updateWeapon } = useStore()
  const [localWeapon, setLocalWeapon] = useState(weapon)

  const handleChange = (field, value) => {
    const updated = { ...localWeapon, [field]: value }
    setLocalWeapon(updated)
    updateWeapon(unitId, weaponIndex, { [field]: value })
  }

  return (
    <div className={styles.editor}>
      <div className={styles.grid}>
        <div className={styles.field}>
          <label>Unit Name</label>
          <input
            type="text"
            value={localWeapon.Name}
            onChange={(e) => handleChange('Name', e.target.value)}
          />
        </div>

        <div className={styles.field}>
          <label>Weapon</label>
          <input
            type="text"
            value={localWeapon.Weapon}
            onChange={(e) => handleChange('Weapon', e.target.value)}
          />
        </div>

        <div className={styles.field}>
          <label>Qty</label>
          <input
            type="number"
            value={localWeapon.Qty}
            onChange={(e) => handleChange('Qty', parseInt(e.target.value) || 1)}
            min="1"
          />
        </div>

        <div className={styles.field}>
          <label>Pts</label>
          <input
            type="number"
            value={localWeapon.Pts}
            onChange={(e) => handleChange('Pts', parseInt(e.target.value) || 0)}
            min="0"
          />
        </div>

        <div className={styles.field}>
          <label>Range</label>
          <input
            type="text"
            value={localWeapon.Range}
            onChange={(e) => handleChange('Range', e.target.value)}
            placeholder="24 or M"
          />
        </div>

        <div className={styles.field}>
          <label>Attacks</label>
          <input
            type="text"
            value={localWeapon.A}
            onChange={(e) => handleChange('A', e.target.value)}
            placeholder="1 or D6"
          />
        </div>

        <div className={styles.field}>
          <label>BS/WS</label>
          <input
            type="number"
            value={localWeapon.BS}
            onChange={(e) => handleChange('BS', parseInt(e.target.value) || 3)}
            min="2"
            max="6"
          />
        </div>

        <div className={styles.field}>
          <label>Strength</label>
          <input
            type="number"
            value={localWeapon.S}
            onChange={(e) => handleChange('S', parseInt(e.target.value) || 4)}
            min="1"
            max="14"
          />
        </div>

        <div className={styles.field}>
          <label>AP</label>
          <input
            type="number"
            value={localWeapon.AP}
            onChange={(e) => handleChange('AP', parseInt(e.target.value) || 0)}
            min="-6"
            max="0"
          />
        </div>

        <div className={styles.field}>
          <label>Damage</label>
          <input
            type="text"
            value={localWeapon.D}
            onChange={(e) => handleChange('D', e.target.value)}
            placeholder="1 or D6"
          />
        </div>

        <div className={styles.field}>
          <label>Blast</label>
          <select value={localWeapon.Blast} onChange={(e) => handleChange('Blast', e.target.value)}>
            <option value="N">No</option>
            <option value="Y">Yes</option>
          </select>
        </div>

        <div className={styles.field}>
          <label>Melta</label>
          <input
            type="number"
            value={localWeapon.Melta}
            onChange={(e) => handleChange('Melta', parseInt(e.target.value) || 0)}
            min="0"
            max="6"
          />
        </div>

        <div className={styles.field}>
          <label>Rapid Fire</label>
          <input
            type="number"
            value={localWeapon.RapidFire}
            onChange={(e) => handleChange('RapidFire', parseInt(e.target.value) || 0)}
            min="0"
            max="6"
          />
        </div>

        <div className={styles.field}>
          <label>Twin-Linked</label>
          <select
            value={localWeapon.TwinLinked}
            onChange={(e) => handleChange('TwinLinked', e.target.value)}
          >
            <option value="N">No</option>
            <option value="Y">Yes</option>
          </select>
        </div>

        <div className={styles.field}>
          <label>Lethal Hits</label>
          <select value={localWeapon.Lethal} onChange={(e) => handleChange('Lethal', e.target.value)}>
            <option value="N">No</option>
            <option value="Y">Yes</option>
          </select>
        </div>

        <div className={styles.field}>
          <label>Dev Wounds</label>
          <select value={localWeapon.Dev} onChange={(e) => handleChange('Dev', e.target.value)}>
            <option value="N">No</option>
            <option value="Y">Yes</option>
          </select>
        </div>
      </div>
    </div>
  )
}

export default WeaponEditor
