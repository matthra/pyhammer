# PyHammer Documentation

Comprehensive documentation for all PyHammer features, implementations, and design decisions.

## 📚 Documentation Index

### Core Features

#### **[UX_REFACTOR_V0.3.9.md](UX_REFACTOR_V0.3.9.md)** - Latest UX Improvements
- **Version**: v0.3.9
- **Summary**: Major UX refactor with global configuration sidebar
- **Features**:
  - Sidebar reorganized as global config hub
  - Half range toggle for Melta/Rapid Fire weapons
  - Consolidated import/export controls
  - Removed single-profile view (edge case)
- **Status**: ✅ Production-ready, fully tested

#### **[GRADING_SYSTEM.md](GRADING_SYSTEM.md)** - CPK Grading Engine
- **Summary**: Letter-grade efficiency system (S to F tier)
- **Features**:
  - Dynamic thresholds per target type
  - Color-coded visual indicators
  - CPK (Cost Per Kill) metric
- **Status**: ✅ Core feature, fully integrated

### Weapon Keywords

#### **[BLAST_KEYWORD.md](BLAST_KEYWORD.md)** - Blast Implementation
- **Summary**: Area-of-effect weapons that scale with target unit size
- **Mechanics**:
  - ≤5 models: No change
  - 6-10 models: Minimum attacks
  - 11+ models: Maximum attacks
- **Test Results**: +71% damage vs large units
- **Status**: ✅ Production-ready

#### **[NEW_KEYWORDS_IMPLEMENTATION.md](NEW_KEYWORDS_IMPLEMENTATION.md)** - Keyword System
- **Summary**: Implementation of Torrent, Twin-Linked, and FNP keywords
- **Covered Keywords**:
  - **Torrent**: Auto-hit (ignores BS)
  - **Twin-Linked**: Reroll wound rolls
  - **Feel No Pain (FNP)**: Final damage reduction
- **Status**: ✅ Production-ready

#### **[COVER_TOGGLE.md](COVER_TOGGLE.md)** - Cover Mechanics
- **Summary**: Global toggle for +1 save bonus
- **Mechanics**:
  - Applies +1 to armor save (3+ → 2+)
  - Minimum save of 2+
  - 50% damage reduction (3+ to 2+)
- **Use Case**: Tournament scenarios, realistic terrain simulation
- **Status**: ✅ Production-ready

### UI/UX Documentation

#### **[UI_IMPROVEMENTS.md](UI_IMPROVEMENTS.md)** - Early UI Enhancements
- **Summary**: Initial Streamlit UI improvements
- **Features**:
  - Master-detail unit editor
  - Sidebar navigation
  - Improved roster management
- **Status**: ✅ Historical reference (superseded by v0.3.9)

#### **[KILLS_TAB_UPGRADE.md](KILLS_TAB_UPGRADE.md)** - Lethality Tab
- **Summary**: Enhanced "Kills" tab with better visualization
- **Features**:
  - Dead models display
  - Color-coded efficiency
  - Sortable columns
- **Status**: ✅ Integrated into main UI

### Integration Documentation

#### **[STREAMLIT_GRADING_INTEGRATION.md](STREAMLIT_GRADING_INTEGRATION.md)** - UI Grading Integration
- **Summary**: Integration of CPK grading system into Streamlit UI
- **Features**:
  - Color-coded efficiency metrics
  - Visual grade indicators
  - Tooltip explanations
- **Status**: ✅ Fully integrated

#### **[COMPLETE_GRADING_INTEGRATION.md](COMPLETE_GRADING_INTEGRATION.md)** - Full Grading System
- **Summary**: Complete implementation of grading across all tabs
- **Features**:
  - Threat matrix integration
  - CPK tab enhancements
  - Efficiency curve grading
- **Status**: ✅ Production-ready

## 📖 Reading Guide

### For New Contributors
1. Start with **UX_REFACTOR_V0.3.9.md** to understand current architecture
2. Read **GRADING_SYSTEM.md** to understand efficiency metrics
3. Review **NEW_KEYWORDS_IMPLEMENTATION.md** for keyword system

### For Feature Implementation
1. Check relevant keyword documentation (BLAST, COVER, etc.)
2. Review **UX_REFACTOR_V0.3.9.md** for global settings patterns
3. Follow established testing patterns (see `../tests/README.md`)

### For Bug Fixes
1. Identify affected feature in documentation
2. Review implementation details
3. Check test coverage in `../tests/`

## 🗂️ Documentation Categories

### By Feature Type
- **Global Settings**: UX_REFACTOR_V0.3.9.md, COVER_TOGGLE.md
- **Weapon Keywords**: BLAST_KEYWORD.md, NEW_KEYWORDS_IMPLEMENTATION.md
- **UI/UX**: UI_IMPROVEMENTS.md, KILLS_TAB_UPGRADE.md
- **Metrics**: GRADING_SYSTEM.md, COMPLETE_GRADING_INTEGRATION.md

### By Version
- **v0.3.9**: UX_REFACTOR_V0.3.9.md (latest)
- **v0.3.8**: COVER_TOGGLE.md, BLAST_KEYWORD.md
- **v0.3.x**: GRADING_SYSTEM.md, NEW_KEYWORDS_IMPLEMENTATION.md
- **Earlier**: UI_IMPROVEMENTS.md (historical)

## 🔄 Documentation Standards

When creating new documentation:

1. **File Naming**: Use UPPERCASE_WITH_UNDERSCORES.md format
2. **Structure**:
   - Overview section
   - Implementation details
   - Test results
   - Use cases
   - Files modified
   - Status/version info
3. **Code Examples**: Include relevant code snippets with file paths and line numbers
4. **Test Coverage**: Document test files and results
5. **Status Tags**: Mark as ✅ Production-ready, 🚧 In Progress, or 📝 Draft

## 📊 Documentation Statistics

- **Total Documents**: 9
- **Production Features**: 9
- **Test Coverage**: 100% (26 tests across all features)
- **Last Updated**: v0.3.9 (2025-12-31)

## 🔗 Related Documentation

- **Test Documentation**: `../tests/README.md`
- **Main README**: `../README.md`
- **Source Code**: `../src/`

---

**Tip**: Use GitHub's file search (press `t`) or your editor's fuzzy finder to quickly locate specific documentation.
