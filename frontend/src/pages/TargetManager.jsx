import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { targets } from '../api/client'
import useStore from '../store/useStore'
import toast from 'react-hot-toast'
import { Plus, Save, Trash2, Copy } from 'lucide-react'
import styles from './TargetManager.module.css'

function TargetManager() {
  const queryClient = useQueryClient()
  const { targetList, setTargetList, setSelectedTarget, setTargetListFilename } = useStore()
  const [editingIndex, setEditingIndex] = useState(null)
  const [filename, setFilename] = useState('')
  const [selectedListFilename, setSelectedListFilename] = useState('')

  const { data: targetLists } = useQuery({ queryKey: ['targets'], queryFn: targets.list })

  // Auto-load default list on mount
  useEffect(() => {
    if (targetLists && targetLists.length > 0 && targetList.length === 0) {
      const defaultList = targetLists.find(list => list.filename === 'default')
      if (defaultList) {
        loadMutation.mutate('default')
      }
    }
  }, [targetLists])

  const loadMutation = useMutation({
    mutationFn: targets.load,
    onSuccess: (data) => {
      setTargetList(data.targets)
      setTargetListFilename(data.filename)
      setFilename(data.filename)
      setSelectedListFilename(data.filename)
      toast.success(`Loaded ${data.filename}`)
    },
  })

  const saveMutation = useMutation({
    mutationFn: ({ filename, targets }) => targets.save(filename, targets),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries(['targets'])
      setFilename(variables.filename)
      setSelectedListFilename(variables.filename)
      toast.success('Saved')
    },
  })

  const deleteMutation = useMutation({
    mutationFn: targets.delete,
    onSuccess: () => {
      queryClient.invalidateQueries(['targets'])
      setTargetList([])
      setFilename('')
      setSelectedListFilename('')
      toast.success('List deleted')
    },
  })

  const handleListChange = (e) => {
    const selectedFile = e.target.value
    if (selectedFile) {
      loadMutation.mutate(selectedFile)
    } else {
      setTargetList([])
      setFilename('')
      setSelectedListFilename('')
    }
  }

  const handleNewList = () => {
    setTargetList([])
    setFilename('')
    setSelectedListFilename('')
    toast.success('Started new list')
  }

  const handleCopyList = () => {
    if (!filename) {
      toast.error('No list loaded to copy')
      return
    }
    const newFilename = `${filename}_copy`
    setFilename(newFilename)
    setSelectedListFilename('')
    toast.success('List copied - click Save to save the copy')
  }

  const handleDeleteList = () => {
    if (!filename) {
      toast.error('No list selected')
      return
    }
    if (confirm(`Delete list "${filename}"?`)) {
      deleteMutation.mutate(filename)
    }
  }

  const handleSave = () => {
    if (!filename.trim()) {
      toast.error('Please enter a filename')
      return
    }
    saveMutation.mutate({ filename: filename.trim(), targets: targetList })
  }

  const handleNewTarget = () => {
    setTargetList([...targetList, { Name: 'New Target', Pts: 20, T: 4, W: 2, Sv: '3+', Inv: '', FNP: '', Stealth: 'N', UnitSize: 5 }])
    setEditingIndex(targetList.length)
  }

  const handleDeleteTarget = (index) => {
    if (confirm('Delete this target?')) {
      setTargetList(targetList.filter((_, i) => i !== index))
      if (editingIndex === index) setEditingIndex(null)
    }
  }

  const handleUpdate = (index, field, value) => {
    const updated = [...targetList]
    updated[index] = { ...updated[index], [field]: value }
    setTargetList(updated)
  }

  return (
    <div className={styles.manager}>
      <div className={styles.header}>
        <h1>Target Manager</h1>
        <p>Manage defensive target profiles</p>
      </div>

      <div className={styles.listControls}>
        <div className={styles.listSelector}>
          <label>Target List:</label>
          <select value={selectedListFilename} onChange={handleListChange} className={styles.listDropdown}>
            <option value="">-- New List --</option>
            {targetLists?.map((list) => (
              <option key={list.filename} value={list.filename}>
                {list.name} ({list.target_count} targets)
              </option>
            ))}
          </select>
        </div>

        <div className={styles.filenameInput}>
          <label>Filename:</label>
          <input type="text" value={filename} onChange={(e) => setFilename(e.target.value)} placeholder="Enter filename..." />
        </div>

        <div className={styles.listActions}>
          <button onClick={handleNewList} className={styles.btnSecondary}><Plus size={18} />New List</button>
          <button onClick={handleCopyList} className={styles.btnSecondary} disabled={!filename}><Copy size={18} />Copy</button>
          <button onClick={handleSave} className={styles.btnSuccess} disabled={!filename || targetList.length === 0}><Save size={18} />Save</button>
          <button onClick={handleDeleteList} className={styles.btnDanger} disabled={!selectedListFilename}><Trash2 size={18} />Delete List</button>
        </div>
      </div>

      {targetList.length > 0 && (
        <div className={styles.listSummary}>
          <h3>Targets in List ({targetList.length})</h3>
          <div className={styles.targetSummaryGrid}>
            {targetList.map((target, index) => (
              <div key={index} className={styles.targetSummaryCard}>{target.Name} - T{target.T} W{target.W} Sv{target.Sv}</div>
            ))}
          </div>
        </div>
      )}

      <div className={styles.targetDetails}>
        <div className={styles.detailsHeader}>
          <h3>Target Details</h3>
          <button onClick={handleNewTarget} className={styles.btnPrimary}><Plus size={18} />Add Target</button>
        </div>

        <div className={styles.targetList}>
          {targetList.map((target, index) => (
            <div key={index} className={styles.targetCard}>
              <div className={styles.targetCardHeader}>
                <div className={styles.targetInfo}>
                  <h4>{target.Name}</h4>
                  <p>T{target.T} W{target.W} Sv{target.Sv} • {target.Pts}pts • Unit Size: {target.UnitSize}</p>
                </div>
                <div className={styles.targetCardActions}>
                  <button onClick={() => setEditingIndex(editingIndex === index ? null : index)} className={styles.btnSecondary}>{editingIndex === index ? 'Close' : 'Edit'}</button>
                  <button onClick={() => handleDeleteTarget(index)} className={styles.btnDanger}><Trash2 size={16} /></button>
                </div>
              </div>

              {editingIndex === index && (
                <div className={styles.targetEditor}>
                  <div className={styles.editorGrid}>
                    <div className={styles.formGroup}><label>Name</label><input type="text" value={target.Name} onChange={(e) => handleUpdate(index, 'Name', e.target.value)} /></div>
                    <div className={styles.formGroup}><label>Points</label><input type="number" value={target.Pts} onChange={(e) => handleUpdate(index, 'Pts', parseInt(e.target.value))} /></div>
                    <div className={styles.formGroup}><label>Toughness (T)</label><input type="number" value={target.T} min="1" max="14" onChange={(e) => handleUpdate(index, 'T', parseInt(e.target.value))} /></div>
                    <div className={styles.formGroup}><label>Wounds (W)</label><input type="number" value={target.W} min="1" max="30" onChange={(e) => handleUpdate(index, 'W', parseInt(e.target.value))} /></div>
                    <div className={styles.formGroup}><label>Save (Sv)</label><select value={target.Sv} onChange={(e) => handleUpdate(index, 'Sv', e.target.value)}><option>2+</option><option>3+</option><option>4+</option><option>5+</option><option>6+</option><option>7+</option></select></div>
                    <div className={styles.formGroup}><label>Invuln (Inv)</label><select value={target.Inv} onChange={(e) => handleUpdate(index, 'Inv', e.target.value)}><option value="">None</option><option>4+</option><option>5+</option><option>6+</option></select></div>
                    <div className={styles.formGroup}><label>Feel No Pain (FNP)</label><select value={target.FNP} onChange={(e) => handleUpdate(index, 'FNP', e.target.value)}><option value="">None</option><option>4+</option><option>5+</option><option>6+</option></select></div>
                    <div className={styles.formGroup}><label>Stealth</label><select value={target.Stealth} onChange={(e) => handleUpdate(index, 'Stealth', e.target.value)}><option value="N">No</option><option value="Y">Yes</option></select></div>
                    <div className={styles.formGroup}><label>Unit Size</label><input type="number" value={target.UnitSize} min="1" onChange={(e) => handleUpdate(index, 'UnitSize', parseInt(e.target.value))} /></div>
                  </div>
                </div>
              )}
            </div>
          ))}

          {targetList.length === 0 && (
            <div className={styles.empty}><p>No targets in this list. Click "Add Target" to start building your target list.</p></div>
          )}
        </div>
      </div>
    </div>
  )
}

export default TargetManager
