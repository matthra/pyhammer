import { Outlet, Link, useLocation } from 'react-router-dom'
import { Home, List, Target, BarChart3, TrendingUp } from 'lucide-react'
import styles from './Layout.module.css'

function Layout() {
  const location = useLocation()

  const navItems = [
    { path: '/', label: 'Dashboard', icon: Home },
    { path: '/roster', label: 'Roster', icon: List },
    { path: '/targets', label: 'Targets', icon: Target },
    { path: '/analysis', label: 'Analysis', icon: TrendingUp },
    { path: '/charts', label: 'Charts', icon: BarChart3 },
  ]

  return (
    <div className={styles.layout}>
      <nav className={styles.sidebar}>
        <div className={styles.logo}>
          <h1>PyHammer</h1>
          <p>Mathhammer Analysis</p>
        </div>

        <ul className={styles.navList}>
          {navItems.map((item) => {
            const Icon = item.icon
            const isActive = location.pathname === item.path

            return (
              <li key={item.path}>
                <Link
                  to={item.path}
                  className={`${styles.navLink} ${isActive ? styles.active : ''}`}
                >
                  <Icon size={20} />
                  <span>{item.label}</span>
                </Link>
              </li>
            )
          })}
        </ul>
      </nav>

      <main className={styles.main}>
        <Outlet />
      </main>
    </div>
  )
}

export default Layout
