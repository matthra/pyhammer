import { useQuery } from '@tanstack/react-query'
import { calculator, targets } from '../api/client'
import useStore from '../store/useStore'
import { useState } from 'react'
import styles from './Analysis.module.css'

function Analysis() {
  const { roster, assumeCover, assumeHalfRange, setAssumeCover, setAssumeHalfRange } = useStore()
  const [selectedTargetFilename, setSelectedTargetFilename] = useState(null)

  // Load target lists
  const { data: targetLists } = useQuery({
    queryKey: ['targetLists'],
    queryFn: targets.list,
  })

  // Load selected target list
  const { data: targetListData } = useQuery({
    queryKey: ['targetList', selectedTargetFilename],
    queryFn: () => targets.load(selectedTargetFilename),
    enabled: !!selectedTargetFilename,
  })

  // Calculate metrics for all targets
  const { data: allMetrics, isLoading } = useQuery({
    queryKey: ['allMetrics', roster, targetListData, assumeCover, assumeHalfRange],
    queryFn: async () => {
      if (!targetListData || roster.length === 0) return null

      const results = await Promise.all(
        targetListData.targets.map(async (target) => {
          const response = await calculator.calculate(roster, target, assumeCover, assumeHalfRange)
          return { target: target.Name, ...response }
        })
      )

      return results
    },
    enabled: !!targetListData && roster.length > 0,
  })

  const getGradeColor = (grade) => {
    const colors = {
      S: '#3fb950',
      A: '#58a6ff',
      B: '#d29922',
      C: '#f85149',
      D: '#f85149',
      F: '#8b949e',
    }
    return colors[grade] || colors.F
  }

  return (
    <div className={styles.analysis}>
      <div className={styles.header}>
        <h1>Efficiency Analysis</h1>
        <p>Analyze CPK, TTK, and Lethality metrics</p>
      </div>

      <div className={styles.controls}>
        <div className={styles.controlGroup}>
          <label>Target List</label>
          <select
            value={selectedTargetFilename || ''}
            onChange={(e) => setSelectedTargetFilename(e.target.value)}
          >
            <option value="">Select target list...</option>
            {targetLists?.map((tl) => (
              <option key={tl.filename} value={tl.filename}>
                {tl.name} ({tl.target_count} targets)
              </option>
            ))}
          </select>
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
      </div>

      {isLoading && <div className={styles.loading}>Calculating metrics...</div>}

      {allMetrics && (
        <div className={styles.results}>
          {allMetrics.map((result, idx) => (
            <div key={idx} className={styles.targetSection}>
              <h2>
                {result.target}
                <span className={styles.badge}>
                  {result.total_kills.toFixed(2)} kills @ {result.avg_cpk.toFixed(2)} CPK
                </span>
              </h2>

              <div className={styles.metricsTable}>
                <table>
                  <thead>
                    <tr>
                      <th>Unit</th>
                      <th>Weapon</th>
                      <th>Qty</th>
                      <th>Pts</th>
                      <th>Kills</th>
                      <th>Damage</th>
                      <th>CPK</th>
                      <th>TTK</th>
                      <th>Grade</th>
                    </tr>
                  </thead>
                  <tbody>
                    {result.metrics.map((metric, i) => (
                      <tr key={i}>
                        <td>{metric.Name}</td>
                        <td>{metric.Weapon}</td>
                        <td>{metric.Qty}</td>
                        <td>{metric.Pts}</td>
                        <td>{metric.Kills.toFixed(2)}</td>
                        <td>{metric.Damage.toFixed(2)}</td>
                        <td>{metric.CPK.toFixed(2)}</td>
                        <td>{metric.TTK.toFixed(1)}</td>
                        <td>
                          <span
                            className={styles.grade}
                            style={{ backgroundColor: getGradeColor(metric.CPK_Grade) }}
                          >
                            {metric.CPK_Grade}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          ))}
        </div>
      )}

      {!selectedTargetFilename && (
        <div className={styles.empty}>Select a target list to begin analysis</div>
      )}

      {roster.length === 0 && (
        <div className={styles.empty}>Add units to your roster to see analysis</div>
      )}
    </div>
  )
}

export default Analysis
