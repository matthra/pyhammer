import { useQuery } from '@tanstack/react-query'
import { calculator } from '../api/client'
import useStore from '../store/useStore'
import styles from './Dashboard.module.css'

function Dashboard() {
  const { roster, selectedTarget, assumeCover, assumeHalfRange } = useStore()

  // Calculate metrics when roster or target changes
  const { data: metrics, isLoading } = useQuery({
    queryKey: ['metrics', roster, selectedTarget, assumeCover, assumeHalfRange],
    queryFn: () => {
      if (!selectedTarget || roster.length === 0) return null
      return calculator.calculate(roster, selectedTarget, assumeCover, assumeHalfRange)
    },
    enabled: !!selectedTarget && roster.length > 0,
  })

  const totalPoints = roster.reduce((sum, weapon) => sum + weapon.Pts, 0)
  const unitCount = new Set(roster.map(w => w.UnitID)).size
  const weaponCount = roster.length

  return (
    <div className={styles.dashboard}>
      <div className={styles.header}>
        <h1>PyHammer Dashboard</h1>
        <p>Warhammer 40K Mathematical Analysis Tool</p>
      </div>

      <div className={styles.stats}>
        <div className={styles.statCard}>
          <div className={styles.statValue}>{totalPoints}</div>
          <div className={styles.statLabel}>Total Points</div>
        </div>

        <div className={styles.statCard}>
          <div className={styles.statValue}>{unitCount}</div>
          <div className={styles.statLabel}>Units</div>
        </div>

        <div className={styles.statCard}>
          <div className={styles.statValue}>{weaponCount}</div>
          <div className={styles.statLabel}>Weapons</div>
        </div>

        {metrics && (
          <>
            <div className={styles.statCard}>
              <div className={styles.statValue}>{metrics.total_kills.toFixed(2)}</div>
              <div className={styles.statLabel}>Expected Kills</div>
            </div>

            <div className={styles.statCard}>
              <div className={styles.statValue}>{metrics.avg_cpk.toFixed(2)}</div>
              <div className={styles.statLabel}>Avg CPK</div>
            </div>
          </>
        )}
      </div>

      <div className={styles.quickStart}>
        <h2>Quick Start</h2>
        <div className={styles.steps}>
          <div className={styles.step}>
            <div className={styles.stepNumber}>1</div>
            <div className={styles.stepContent}>
              <h3>Build Your Roster</h3>
              <p>Navigate to the Roster page to add units and weapons</p>
            </div>
          </div>

          <div className={styles.step}>
            <div className={styles.stepNumber}>2</div>
            <div className={styles.stepContent}>
              <h3>Select Targets</h3>
              <p>Choose defensive profiles from the Targets page</p>
            </div>
          </div>

          <div className={styles.step}>
            <div className={styles.stepNumber}>3</div>
            <div className={styles.stepContent}>
              <h3>Analyze Efficiency</h3>
              <p>View CPK, TTK, and lethality metrics in Analysis</p>
            </div>
          </div>

          <div className={styles.step}>
            <div className={styles.stepNumber}>4</div>
            <div className={styles.stepContent}>
              <h3>Visualize Data</h3>
              <p>Explore interactive charts and threat matrices</p>
            </div>
          </div>
        </div>
      </div>

      {isLoading && (
        <div className={styles.loading}>Calculating metrics...</div>
      )}
    </div>
  )
}

export default Dashboard
