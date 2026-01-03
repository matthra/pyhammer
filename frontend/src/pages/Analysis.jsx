import { useQuery } from '@tanstack/react-query'
import { calculator, targets, rosters } from '../api/client'
import useStore from '../store/useStore'
import { useState } from 'react'
import toast from 'react-hot-toast'
import { RefreshCw } from 'lucide-react'
import styles from './Analysis.module.css'

// CPK Grade colors based on grading.py
const GRADE_COLORS = {
  S: '#2196F3', // Blue - Elite
  A: '#00D084', // Green - Excellent
  B: '#4CAF50', // Light Green - Good
  C: '#FFC107', // Yellow - Average
  D: '#FF9800', // Orange - Below Average
  E: '#FF5722', // Deep Orange - Poor
  F: '#F44336', // Red - Ineffective
}

const GRADE_THRESHOLDS = {
  S: 1.0,
  A: 1.5,
  B: 2.0,
  C: 2.5,
  D: 3.0,
  E: 3.5,
}

function getCPKGrade(cpk) {
  if (cpk <= 0 || cpk >= 999) return 'F'
  if (cpk <= GRADE_THRESHOLDS.S) return 'S'
  if (cpk <= GRADE_THRESHOLDS.A) return 'A'
  if (cpk <= GRADE_THRESHOLDS.B) return 'B'
  if (cpk <= GRADE_THRESHOLDS.C) return 'C'
  if (cpk <= GRADE_THRESHOLDS.D) return 'D'
  if (cpk <= GRADE_THRESHOLDS.E) return 'E'
  return 'F'
}

function Analysis() {
  const { roster, assumeCover, assumeHalfRange, setAssumeCover, setAssumeHalfRange } = useStore()
  const [selectedRosterFilename, setSelectedRosterFilename] = useState(null)
  const [selectedTargetFilename, setSelectedTargetFilename] = useState(null)
  const [activeRoster, setActiveRoster] = useState([])
  const [activeTargets, setActiveTargets] = useState([])
  const [matrixData, setMatrixData] = useState(null)
  const [isCalculating, setIsCalculating] = useState(false)
  const [hoveredCell, setHoveredCell] = useState(null)
  const [viewMode, setViewMode] = useState('matrix') // 'matrix' or 'list'

  // Load available rosters
  const { data: rosterList } = useQuery({
    queryKey: ['rosters'],
    queryFn: rosters.list,
  })

  // Load target lists
  const { data: targetLists } = useQuery({
    queryKey: ['targetLists'],
    queryFn: targets.list,
  })

  // Handle roster selection
  const handleRosterChange = async (filename) => {
    setSelectedRosterFilename(filename)
    if (!filename) {
      setActiveRoster(roster)
      return
    }
    try {
      const data = await rosters.load(filename)
      setActiveRoster(data.weapons)
      toast.success(`Loaded roster: ${filename}`)
    } catch (error) {
      toast.error('Failed to load roster')
      console.error(error)
    }
  }

  // Handle target list selection
  const handleTargetChange = async (filename) => {
    setSelectedTargetFilename(filename)
    if (!filename) {
      setActiveTargets([])
      return
    }
    try {
      const data = await targets.load(filename)
      setActiveTargets(data.targets)
      toast.success(`Loaded targets: ${filename}`)
    } catch (error) {
      toast.error('Failed to load targets')
      console.error(error)
    }
  }

  // Calculate threat matrix
  const calculateMatrix = async () => {
    const weaponsToUse = activeRoster.length > 0 ? activeRoster : roster

    if (!weaponsToUse || weaponsToUse.length === 0) {
      toast.error('No roster available')
      return
    }
    if (!activeTargets || activeTargets.length === 0) {
      toast.error('No targets loaded')
      return
    }

    setIsCalculating(true)
    try {
      const response = await calculator.calculateMultiTarget(
        weaponsToUse,
        activeTargets,
        assumeCover,
        assumeHalfRange
      )
      setMatrixData(response)
      toast.success('Analysis complete')
    } catch (error) {
      toast.error('Calculation failed')
      console.error('Calculation error:', error)
    } finally {
      setIsCalculating(false)
    }
  }

  // Group roster by units
  const weaponsToDisplay = activeRoster.length > 0 ? activeRoster : roster
  const units = weaponsToDisplay.reduce((acc, weapon) => {
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
    <div className={styles.analysis}>
      <div className={styles.header}>
        <div>
          <h1>Threat Matrix Analysis</h1>
          <p>Analyze your roster's effectiveness against different targets</p>
        </div>
      </div>

      {/* Controls */}
      <div className={styles.controls}>
        <div className={styles.selectors}>
          <div className={styles.selector}>
            <label>Roster</label>
            <select
              value={selectedRosterFilename || ''}
              onChange={(e) => handleRosterChange(e.target.value)}
            >
              <option value="">Use Current Roster ({Object.keys(units).length} units)</option>
              {rosterList?.map((r) => (
                <option key={r.filename} value={r.filename}>
                  {r.name} ({r.total_points}pts, {r.unit_count} units)
                </option>
              ))}
            </select>
          </div>

          <div className={styles.selector}>
            <label>Target List</label>
            <select
              value={selectedTargetFilename || ''}
              onChange={(e) => handleTargetChange(e.target.value)}
            >
              <option value="">Select targets...</option>
              {targetLists?.map((t) => (
                <option key={t.filename} value={t.filename}>
                  {t.name} ({t.target_count} targets)
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className={styles.toggles}>
          <label className={styles.checkbox}>
            <input
              type="checkbox"
              checked={assumeCover}
              onChange={(e) => setAssumeCover(e.target.checked)}
            />
            <span>Assume Cover (+1 Sv)</span>
          </label>

          <label className={styles.checkbox}>
            <input
              type="checkbox"
              checked={assumeHalfRange}
              onChange={(e) => setAssumeHalfRange(e.target.checked)}
            />
            <span>Assume Half Range (Melta/RF)</span>
          </label>
        </div>

        <button
          onClick={calculateMatrix}
          disabled={isCalculating || !weaponsToDisplay.length || !activeTargets.length}
          className={styles.btnCalculate}
        >
          <RefreshCw size={20} className={isCalculating ? styles.spinning : ''} />
          {isCalculating ? 'Calculating...' : 'Calculate Matrix'}
        </button>
      </div>

      {/* Grade Legend */}
      {matrixData && (
        <div className={styles.legend}>
          <h3>CPK Grade Scale (Cost Per Kill)</h3>
          <div className={styles.grades}>
            {Object.entries(GRADE_THRESHOLDS).map(([grade, threshold]) => (
              <div key={grade} className={styles.gradeItem}>
                <div
                  className={styles.gradeColor}
                  style={{ backgroundColor: GRADE_COLORS[grade] }}
                />
                <div className={styles.gradeLabel}>
                  <strong>{grade}</strong>
                  <span>≤{threshold.toFixed(1)}</span>
                </div>
              </div>
            ))}
            <div className={styles.gradeItem}>
              <div className={styles.gradeColor} style={{ backgroundColor: GRADE_COLORS.F }} />
              <div className={styles.gradeLabel}>
                <strong>F</strong>
                <span>&gt;{GRADE_THRESHOLDS.E.toFixed(1)}</span>
              </div>
            </div>
          </div>
          <p className={styles.legendNote}>Lower CPK = More Efficient. Hover cells for details.</p>
        </div>
      )}

      {/* Threat Matrix Grid */}
      {matrixData && (
        <div className={styles.matrixContainer}>
          <div className={styles.gridWrapper}>
            <table className={styles.matrix}>
              <thead>
                <tr>
                  <th className={styles.cornerCell}>Unit \ Target</th>
                  {activeTargets.map((target) => (
                    <th key={target.Name} className={styles.targetHeader}>
                      <div className={styles.targetName}>{target.Name}</div>
                      <div className={styles.targetStats}>
                        T{target.T} W{target.W} {target.Sv}
                        {target.Inv && ` ${target.Inv}++`}
                        {target.FNP && ` FNP${target.FNP}`}
                      </div>
                      <div className={styles.targetPoints}>{target.Pts}pts</div>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {Object.values(units).map((unit) => (
                  <tr key={unit.id}>
                    <td className={styles.unitCell}>
                      <div className={styles.unitName}>{unit.name}</div>
                      <div className={styles.unitStats}>
                        {unit.qty}x @ {unit.pts}pts
                      </div>
                    </td>
                    {activeTargets.map((target) => {
                      const targetResults = matrixData.results?.[target.Name]
                      const metrics = targetResults?.metrics
                      const results = metrics?.filter((m) => m.UnitID === unit.id)

                      if (!results || results.length === 0) {
                        return (
                          <td key={target.Name} className={styles.noData}>
                            -
                          </td>
                        )
                      }

                      // Take best CPK from all weapon profiles
                      const bestResult = results.reduce((best, curr) =>
                        curr.CPK < best.CPK ? curr : best
                      )

                      const grade = getCPKGrade(bestResult.CPK)
                      const color = GRADE_COLORS[grade]

                      return (
                        <td
                          key={target.Name}
                          className={styles.dataCell}
                          style={{ backgroundColor: color }}
                          onMouseEnter={() =>
                            setHoveredCell({ unit: unit.name, target: target.Name, results })
                          }
                          onMouseLeave={() => setHoveredCell(null)}
                        >
                          <div className={styles.cpkValue}>{bestResult.CPK.toFixed(2)}</div>
                          <div className={styles.gradeTag}>{grade}</div>
                          <div className={styles.killsValue}>
                            {bestResult.Kills.toFixed(2)} kills
                          </div>
                        </td>
                      )
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Hover Tooltip */}
          {hoveredCell && (
            <div className={styles.tooltip}>
              <h4>{hoveredCell.unit} vs {hoveredCell.target}</h4>
              {hoveredCell.results.map((result, idx) => (
                <div key={idx} className={styles.tooltipItem}>
                  <div className={styles.weaponName}>{result.Weapon}</div>
                  <div className={styles.tooltipStats}>
                    <span>CPK: <strong>{result.CPK.toFixed(2)}</strong> ({result.CPK_Grade})</span>
                    <span>Kills: <strong>{result.Kills.toFixed(2)}</strong></span>
                    <span>Damage: <strong>{result.Damage.toFixed(1)}</strong></span>
                    <span>TTK: <strong>{result.TTK.toFixed(1)}</strong> activations</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Empty State */}
      {!matrixData && (
        <div className={styles.empty}>
          {!weaponsToDisplay.length && <p>Add units to your roster to begin analysis</p>}
          {!activeTargets.length && weaponsToDisplay.length > 0 && (
            <p>Select a target list and click Calculate Matrix to begin analysis</p>
          )}
        </div>
      )}
    </div>
  )
}

export default Analysis
