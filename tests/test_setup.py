#!/usr/bin/env python3
"""
Quick setup verification script
Run this to check if the migration is ready to use
"""

import sys
import subprocess
from pathlib import Path

def check_command(cmd, name):
    """Check if a command exists"""
    try:
        subprocess.run([cmd, '--version'], capture_output=True, check=True)
        print(f"✅ {name} is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"❌ {name} is NOT installed")
        return False

def check_file(path, description):
    """Check if a file exists"""
    if Path(path).exists():
        print(f"✅ {description} exists")
        return True
    else:
        print(f"❌ {description} NOT FOUND")
        return False

def check_directory(path, description):
    """Check if a directory exists"""
    if Path(path).is_dir():
        print(f"✅ {description} exists")
        return True
    else:
        print(f"❌ {description} NOT FOUND")
        return False

def main():
    print("🔨 PyHammer Setup Verification\n")

    checks = []

    # Check required software
    print("📦 Checking required software...")
    checks.append(check_command('python', 'Python'))
    checks.append(check_command('node', 'Node.js'))
    checks.append(check_command('npm', 'npm'))
    checks.append(check_command('docker', 'Docker'))

    print("\n📁 Checking backend structure...")
    checks.append(check_directory('backend', 'Backend directory'))
    checks.append(check_file('backend/main.py', 'Backend main.py'))
    checks.append(check_file('backend/models.py', 'Backend models.py'))
    checks.append(check_file('backend/requirements.txt', 'Backend requirements.txt'))
    checks.append(check_directory('backend/routers', 'Backend routers'))

    print("\n📁 Checking frontend structure...")
    checks.append(check_directory('frontend', 'Frontend directory'))
    checks.append(check_file('frontend/package.json', 'Frontend package.json'))
    checks.append(check_file('frontend/vite.config.js', 'Vite config'))
    checks.append(check_file('frontend/index.html', 'Frontend index.html'))
    checks.append(check_directory('frontend/src', 'Frontend src directory'))

    print("\n📁 Checking original PyHammer files...")
    checks.append(check_directory('src/engine', 'Calculator engine'))
    checks.append(check_file('src/engine/calculator.py', 'Calculator'))
    checks.append(check_directory('src/data', 'Data layer'))
    checks.append(check_directory('roster_configs', 'Roster configs'))
    checks.append(check_directory('target_configs', 'Target configs'))

    print("\n🐳 Checking Docker setup...")
    checks.append(check_file('docker-compose.yml', 'Docker Compose file'))
    checks.append(check_file('Dockerfile.backend', 'Backend Dockerfile'))
    checks.append(check_file('frontend/Dockerfile', 'Frontend Dockerfile'))

    print("\n📚 Checking documentation...")
    checks.append(check_file('README_MIGRATION.md', 'Migration guide'))
    checks.append(check_file('QUICKSTART.md', 'Quick start guide'))
    checks.append(check_file('MIGRATION_SUMMARY.md', 'Migration summary'))

    print("\n" + "="*50)

    passed = sum(checks)
    total = len(checks)

    print(f"\n✅ Passed: {passed}/{total} checks")

    if passed == total:
        print("\n🎉 Setup is complete! You're ready to go!")
        print("\n📋 Next steps:")
        print("   1. Run: docker-compose up")
        print("   2. Open: http://localhost:3000")
        print("   3. Check API docs: http://localhost:8000/docs")
        return 0
    else:
        print("\n⚠️ Some checks failed. Review the output above.")
        print("\n💡 Tips:")
        if not check_command('python', ''):
            print("   - Install Python 3.11+")
        if not check_command('node', ''):
            print("   - Install Node.js 18+")
        if not check_command('docker', ''):
            print("   - Install Docker (optional but recommended)")
        return 1

if __name__ == '__main__':
    sys.exit(main())
