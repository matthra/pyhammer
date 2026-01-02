import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import RosterManager from './pages/RosterManager'
import TargetManager from './pages/TargetManager'
import Analysis from './pages/Analysis'
import Charts from './pages/Charts'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="roster" element={<RosterManager />} />
        <Route path="targets" element={<TargetManager />} />
        <Route path="analysis" element={<Analysis />} />
        <Route path="charts" element={<Charts />} />
      </Route>
    </Routes>
  )
}

export default App
