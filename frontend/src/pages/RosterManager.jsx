import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { rosters } from '../api/client'
import useStore from '../store/useStore'
import toast from 'react-hot-toast'
import { Plus, Save, Trash2, Upload } from 'lucide-react'
import WeaponEditor from '../components/WeaponEditor'
import styles from './RosterManager.module.css'

function RosterManager() {
  const queryClient = useQueryClient()
  const { roster, rosterFilename, setRoster, setRosterFilename, addWeapon, deleteUnit } = useStore()
  const [selectedUnitId, setSelectedUnitId] = useState(null)
  const [showNewUnitForm, setShowNewUnitForm] = useState(false)

  // Load roster list
  const { data: rosterList } = useQuery({
    queryKey: ['rosters'],
    queryFn: rosters.list,
  })

  // Load roster mutation
  const loadMutation = useMutation({
    mutationFn: rosters.load,
    onSuccess: (data) => {
      setRoster(data.weapons)
      setRosterFilename(data.filename)
      toast.success(`Loaded ${data.filename}`)
    },
    onError: () => toast.error('Failed to load roster'),
  })

  // Save roster mutation
  const saveMutation = useMutation({
    mutationFn: ({ filename, weapons }) => rosters.save(filename, weapons),
    onSuccess: (_, variables) => {
      setRosterFilename(variables.filename)
      queryClient.invalidateQueries(['rosters'])
      toast.success('Roster saved')
    },
    onError: () => toast.error('Failed to save roster'),
  })

  // Delete roster mutation
  const deleteMutation = useMutation({
    mutationFn: rosters.delete,
    onSuccess: () => {
      queryClient.invalidateQueries(['rosters'])
      toast.success('Roster deleted')
    },
    onError: () => toast.error('Failed to delete roster'),
  })

  const handleNewUnit = () => {
    const newWeapon = {
      UnitID: crypto.randomUUID(),
      Name: 'New Unit',
      Qty: 1,
      Pts: 0,
      Weapon: 'New Weapon',
      Range: 24,
      A: 1,
      BS: 3,
      S: 4,
      AP: 0,
      D: 1,
      Blast: 'N',
      Melta: 0,
      RapidFire: 0,
      TwinLinked: 'N',
      Lethal: 'N',
      Dev: 'N',
      Torrent: 'N',
      CritHit: 6,
      CritWound: 6,
      Sustained: 0,
      FNP: '',
      ProfileID: '',
    }
    addWeapon(newWeapon)
    setSelectedUnitId(newWeapon.UnitID)
    setShowNewUnitForm(false)
  }

  const handleSave = () => {
    const filename = rosterFilename || `roster_${Date.now()}.json`
    saveMutation.mutate({ filename, weapons: roster })
  }

  const handleDeleteUnit = (unitId) => {
    if (confirm('Delete this unit and all its weapons?')) {
      deleteUnit(unitId)
    }
  }

  // Group weapons by unit
  const units = roster.reduce((acc, weapon) => {
    if (!acc[weapon.UnitID]) {
      acc[weapon.UnitID] = {
        id: weapon.UnitID,
        name: weapon.Name,
        qty: weapon.Qty,
        pts: weapon.Pts,
        weapons: [],
      }
    }
    acc[weapon.UnitID].weapons.push(weapon)
    return acc
  }, {})

  return (
    <div className={styles.manager}>
      <div className={styles.header}>
        <div>
          <h1>Roster Manager</h1>
          <p>Build and edit your army roster</p>
        </div>

        <div className={styles.actions}>
          <button onClick={handleNewUnit} className={styles.btnPrimary}>
            <Plus size={20} />
            New Unit
          </button>
          <button onClick={handleSave} className={styles.btnSuccess} disabled={roster.length === 0}>
            <Save size={20} />
            Save Roster
          </button>
        </div>
      </div>

      <div className={styles.content}>
        <div className={styles.sidebar}>
          <h3>Saved Rosters</h3>
          <div className={styles.rosterList}>
            {rosterList?.map((r) => (
              <div key={r.filename} className={styles.rosterItem}>
                <div
                  className={styles.rosterInfo}
                  onClick={() => loadMutation.mutate(r.filename)}
                >
                  <div className={styles.rosterName}>{r.name}</div>
                  <div className={styles.rosterStats}>
                    {r.total_points} pts • {r.unit_count} units
                  </div>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    if (confirm(`Delete ${r.filename}?`)) {
                      deleteMutation.mutate(r.filename)
                    }
                  }}
                  className={styles.btnIcon}
                >
                  <Trash2 size={16} />
                </button>
              </div>
            ))}
          </div>
        </div>

        <div className={styles.main}>
          <div className={styles.unitList}>
            <h3>Units ({Object.keys(units).length})</h3>

            {Object.values(units).map((unit) => (
              <div key={unit.id} className={styles.unitCard}>
                <div className={styles.unitHeader}>
                  <div>
                    <h4>{unit.name}</h4>
                    <p>
                      {unit.qty}x @ {unit.pts} pts • {unit.weapons.length} weapon(s)
                    </p>
                  </div>
                  <div className={styles.unitActions}>
                    <button
                      onClick={() => setSelectedUnitId(selectedUnitId === unit.id ? null : unit.id)}
                      className={styles.btnSecondary}
                    >
                      {selectedUnitId === unit.id ? 'Collapse' : 'Edit'}
                    </button>
                    <button onClick={() => handleDeleteUnit(unit.id)} className={styles.btnDanger}>
                      <Trash2 size={16} />
                    </button>
                  </div>
                </div>

                {selectedUnitId === unit.id && (
                  <div className={styles.weaponsList}>
                    {unit.weapons.map((weapon, idx) => (
                      <WeaponEditor key={idx} weapon={weapon} unitId={unit.id} weaponIndex={idx} />
                    ))}
                  </div>
                )}
              </div>
            ))}

            {roster.length === 0 && (
              <div className={styles.empty}>
                <p>No units in roster. Click "New Unit" to start building.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default RosterManager
