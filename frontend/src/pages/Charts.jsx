import Plot from 'react-plotly.js'
import { useQuery } from '@tanstack/react-query'
import { visualizations, targets } from '../api/client'
import useStore from '../store/useStore'
import { useState } from 'react'
import styles from './Charts.module.css'

function Charts() {
  const { roster, assumeCover, assumeHalfRange } = useStore()
  const [selectedTargetFilename, setSelectedTargetFilename] = useState(null)
  const [chartType, setChartType] = useState('threat_matrix')

  const { data: targetLists } = useQuery({
    queryKey: ['targetLists'],
    queryFn: targets.list,
  })

  const { data: targetListData } = useQuery({
    queryKey: ['targetList', selectedTargetFilename],
    queryFn: () => targets.load(selectedTargetFilename),
    enabled: !!selectedTargetFilename,
  })

  const { data: chartData, isLoading } = useQuery({
    queryKey: ['chart', chartType, roster, targetListData, assumeCover, assumeHalfRange],
    queryFn: async () => {
      if (!targetListData || roster.length === 0) return null

      const response = await visualizations.generateChart(
        chartType,
        roster,
        targetListData.targets,
        assumeCover,
        assumeHalfRange,
        'plotly_dark'
      )

      return response.chart_json
    },
    enabled: !!targetListData && roster.length > 0,
  })

  return (
    <div className={styles.charts}>
      <div className={styles.header}>
        <h1>Interactive Charts</h1>
        <p>Visualize efficiency and threat analysis</p>
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
                {tl.name}
              </option>
            ))}
          </select>
        </div>

        <div className={styles.controlGroup}>
          <label>Chart Type</label>
          <select value={chartType} onChange={(e) => setChartType(e.target.value)}>
            <option value="threat_matrix">Threat Matrix</option>
            <option value="efficiency_curve">Efficiency Curve</option>
            <option value="ttk_heatmap">TTK Heatmap</option>
            <option value="unit_comparison">Unit Comparison</option>
          </select>
        </div>
      </div>

      {isLoading && <div className={styles.loading}>Generating chart...</div>}

      {chartData && (
        <div className={styles.chartContainer}>
          <Plot
            data={chartData.data}
            layout={{
              ...chartData.layout,
              autosize: true,
              paper_bgcolor: '#1a1f2e',
              plot_bgcolor: '#1a1f2e',
              font: { color: '#e6edf3' },
            }}
            config={{ responsive: true }}
            style={{ width: '100%', height: '600px' }}
          />
        </div>
      )}

      {!selectedTargetFilename && (
        <div className={styles.empty}>Select a target list to generate charts</div>
      )}
    </div>
  )
}

export default Charts
