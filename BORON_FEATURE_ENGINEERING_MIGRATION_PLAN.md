# Boron Feature Engineering Migration Plan

## Executive Summary

**Problem**: The pipeline configuration has been updated for boron prediction, but the feature engineering code still contains 102 references to magnesium/potassium that need to be migrated to boron.

**Impact**: Current state will cause feature generation failures or incorrect features when using the `B_only` strategy.

**Solution**: Systematic migration of all feature engineering modules to use boron-specific nomenclature and logic.

---

## Analysis Results

### Files Requiring Updates

| File | Old Element References | Priority |
|------|----------------------|----------|
| `concentration_features.py` | 28 | HIGH |
| `feature_helpers.py` | 25 | HIGH |
| `feature_engineering.py` | 21 | HIGH |
| `parallel_feature_engineering.py` | 21 | HIGH |
| `enhanced_features.py` | 6 | MEDIUM |
| `feature_selector.py` | 1 | LOW |

**Total References to Update**: 102

---

## Migration Strategy

### Phase 1: Core Feature Generation (HIGH PRIORITY)

#### 1.1 Update `feature_helpers.py` (25 references)

**Functions to Rename:**
```python
# OLD → NEW
generate_high_magnesium_features() → generate_high_boron_features()
generate_focused_magnesium_features() → generate_focused_boron_features()
```

**Ratio Variables to Update:**
```python
# OLD → NEW
MgC_ratio → B_C_ratio  # Boron-to-Carbon ratio
Mg_O_ratio → B_O_ratio  # Boron-to-Oxygen ratio
K_Mg_ratio → K_B_ratio  # Potassium-to-Boron ratio (K as context)
```

**Feature Names to Update:**
- `Mg_I_*` → `B_I_*` (boron atomic lines)
- `Mg_II_*` → `B_II_*` (ionized boron lines)
- All "magnesium" strings in comments → "boron"

**Physics Context Changes:**
```python
# OLD (Magnesium physics)
# Magnesium in plants: structural component, chlorophyll center
# Typical range: 0.5-3.0%
# Key lines: 285 nm, 383 nm, 516-519 nm

# NEW (Boron physics)
# Boron in plants: micronutrient, cell wall structure
# Typical range: 15-35% (based on your data analysis)
# Key lines: 249.7 nm (doublet), 208.9 nm (doublet), 345.1 nm (B II)
```

---

#### 1.2 Update `feature_engineering.py` (21 references)

**Import Changes:**
```python
# Line 18-19: OLD
from src.features.feature_helpers import (
    generate_high_magnesium_features,
    generate_focused_magnesium_features,
)

# NEW
from src.features.feature_helpers import (
    generate_high_boron_features,
    generate_focused_boron_features,
)
```

**Strategy Check Updates:**
```python
# Line 359: OLD
if self.strategy == "Mg_only" or self.strategy == "M_only":
    mg_regions = [self.config.magnesium_region]

# NEW
if self.strategy == "B_only":
    b_regions = [self.config.boron_region]
```

**Region References:**
```python
# OLD
self.config.magnesium_region
self.config.context_regions  # Check if these include Mg_I_285, Mg_I_383

# NEW
self.config.boron_region  # B_I_249 (primary doublet)
self.config.context_regions  # Should include B_I_208, B_II_345
```

**Configuration Flag:**
```python
# Line 442: OLD
if self.config.use_focused_magnesium_features:
    full_features_df, _ = generate_focused_magnesium_features(...)

# NEW
if self.config.use_focused_boron_features:
    full_features_df, _ = generate_focused_boron_features(...)
```

**Feature Filtering for B_only Strategy:**
```python
# Lines 700-714: OLD logic
if self.strategy == "Mg_only" or self.strategy == "M_only":
    # Include all Mg_I and Mg_II features
    selected_names = [
        name for name in all_names
        if "Mg" in name or "magnesium" in name.lower()
    ]
    # Always add Mg_C_ratio

# NEW logic
if self.strategy == "B_only":
    # Include all B_I and B_II features
    selected_names = [
        name for name in all_names
        if "B_I" in name or "B_II" in name or "boron" in name.lower()
    ]
    # Always add B_C_ratio (critical boron indicator)
    if "B_C_ratio" not in selected_names and "B_C_ratio" in all_names:
        selected_names.append("B_C_ratio")
    # Add B_O_ratio if available (boron-oxygen interaction)
    if "B_O_ratio" not in selected_names and "B_O_ratio" in all_names:
        selected_names.append("B_O_ratio")
```

**Key Peak Reference:**
```python
# Line 430: OLD
if "Mg_I_peak_0" not in base_features.columns:
    raise ValueError("Mg_I_peak_0 not found...")

# NEW
if "B_I_peak_0" not in base_features.columns:
    raise ValueError("B_I_peak_0 not found. Ensure boron (B_I) region is properly defined...")
```

---

#### 1.3 Update `parallel_feature_engineering.py` (21 references)

Similar changes to `feature_engineering.py`:
- Update imports
- Update strategy checks (`Mg_only`/`M_only` → `B_only`)
- Update region references
- Update configuration flag checks
- Update comments and logging

---

### Phase 2: Enhanced Features (MEDIUM PRIORITY)

#### 2.1 Update `concentration_features.py` (28 references)

**Key Changes:**
```python
# Concentration-specific features for boron
# OLD: Low/medium/high magnesium ranges (0.5-3.0%)
# NEW: Boron ranges based on data (15-35%)

# Range definitions
LOW_BORON = 15.0-20.0%
MEDIUM_BORON = 20.0-28.0%
HIGH_BORON = 28.0-35.0%

# Self-absorption features (critical for boron!)
# B I 249.7 nm doublet shows strong self-absorption above ~25%
# Add asymmetry features to detect self-absorption
```

**Boron-Specific Considerations:**
1. **Self-absorption**: The 249.7 nm doublet is prone to self-absorption at higher concentrations
2. **UV region effects**: More baseline drift, higher noise
3. **Limited emission lines**: Only 2 main atomic lines (249.7 nm, 208.9 nm) vs Mg's 3+ lines
4. **Alternative detection**: B II 345.1 nm and BO molecular bands

---

#### 2.2 Update `enhanced_features.py` (6 references)

**Key Changes:**
- Update element-specific comments
- Update ratio calculations for boron context
- Consider adding BO (boron monoxide) molecular features if relevant

---

### Phase 3: Minor Updates (LOW PRIORITY)

#### 3.1 Update `feature_selector.py` (1 reference)

Minor docstring or comment update.

---

## Boron-Specific Feature Engineering Considerations

### 1. Self-Absorption Detection (NEW FEATURE)

Boron's 249.7 nm doublet shows strong self-absorption at concentrations above ~25%. Add features:

```python
# Asymmetry features for self-absorption detection
'B_I_249_asymmetry': peak_asymmetry_score,
'B_I_249_doublet_ratio': ratio_of_two_lines,  # Should be ~1:1 without absorption
'B_I_249_FWHM': full_width_half_maximum,  # Increases with self-absorption
```

### 2. Boron-Specific Ratios

```python
# Primary ratios for boron
'B_C_ratio': B_intensity / C_intensity,  # Carbon normalization
'B_O_ratio': B_intensity / O_intensity,  # Oxygen context
'B_N_ratio': B_intensity / N_intensity,  # Nitrogen context
'B_II_B_I_ratio': B_II_345 / B_I_249,   # Plasma temperature indicator
```

### 3. UV Region Features

```python
# UV-specific considerations
'UV_baseline_drift': baseline_curvature_in_UV,
'UV_noise_level': std_dev_in_baseline_regions,
'atmospheric_absorption': O2_absorption_features,  # ~200-250 nm
```

### 4. Alternative Detection Methods

```python
# When primary line saturates
'B_I_208_intensity': secondary_doublet_features,  # Less self-absorption
'B_II_345_intensity': ionized_boron_features,     # Plasma characterization
'BO_molecular_band': molecular_emission_features,  # ~430 nm region
```

---

## Testing Strategy

### Test 1: Configuration Validation
```bash
python -c "from src.config.pipeline_config import config; \
print('Boron region:', config.boron_region.element); \
print('Use focused boron:', config.use_focused_boron_features); \
print('Strategies:', config.feature_strategies)"
```

### Test 2: Feature Helper Functions
```bash
python -c "from src.features.feature_helpers import \
generate_high_boron_features, generate_focused_boron_features; \
print('Boron functions imported successfully')"
```

### Test 3: Feature Engineering Import
```bash
python -c "from src.features.feature_engineering import SpectralFeatureEngineering; \
print('Feature engineering imported successfully')"
```

### Test 4: B_only Strategy Test
```bash
# Test with small dataset
uv run python main.py train \
    --models ridge \
    --strategy B_only \
    --max-samples 10 \
    --feature-parallel \
    --data-parallel
```

### Test 5: Full Training Test
```bash
# Full test with GPU
uv run python main.py train \
    --models xgboost lightgbm catboost \
    --strategy B_only \
    --gpu \
    --feature-parallel \
    --data-parallel
```

---

## Implementation Checklist

### Core Files (Must Complete)
- [ ] `feature_helpers.py` - Function renames and ratio updates
- [ ] `feature_engineering.py` - Import and strategy logic updates
- [ ] `parallel_feature_engineering.py` - Parallel processing updates
- [ ] `concentration_features.py` - Range and feature updates

### Enhanced Features (Should Complete)
- [ ] `enhanced_features.py` - Minor updates for boron context

### Optional (Nice to Have)
- [ ] `feature_selector.py` - Minor comment updates
- [ ] Add boron-specific self-absorption features
- [ ] Add UV region quality indicators
- [ ] Add BO molecular band features

### Testing
- [ ] Configuration loads without errors
- [ ] Feature helper functions import correctly
- [ ] B_only strategy generates expected features
- [ ] Full training pipeline runs successfully
- [ ] Generated features match expected boron nomenclature

---

## Risk Assessment

### High Risk Items
1. **Function signature changes** in `feature_helpers.py` - Could break imports
2. **Strategy logic** in `feature_engineering.py` - Core feature extraction
3. **B_I_peak_0 reference** - Critical for feature validation

### Mitigation Strategies
1. Update all imports simultaneously
2. Test feature extraction with small dataset first
3. Verify feature names in output before full training
4. Keep backup of original files

---

## Expected Outcomes

### Before Migration
- ❌ `B_only` strategy fails with "magnesium_region" AttributeError
- ❌ Features generated with wrong element names (Mg instead of B)
- ❌ Incorrect ratio calculations (Mg_C instead of B_C)
- ❌ Misleading feature importance (magnesium features for boron data)

### After Migration
- ✅ `B_only` strategy extracts boron-specific features
- ✅ Feature names reflect boron nomenclature (B_I_*, B_II_*, B_C_ratio)
- ✅ Correct concentration ranges (15-35% instead of 0.001-1.0%)
- ✅ Boron-specific features (self-absorption detection, UV baseline)
- ✅ Accurate feature importance analysis
- ✅ Better model performance due to correct feature engineering

---

## Timeline Estimate

| Phase | Tasks | Estimated Time |
|-------|-------|----------------|
| Phase 1.1 | Update feature_helpers.py | 30 minutes |
| Phase 1.2 | Update feature_engineering.py | 30 minutes |
| Phase 1.3 | Update parallel_feature_engineering.py | 20 minutes |
| Phase 2.1 | Update concentration_features.py | 20 minutes |
| Phase 2.2 | Update enhanced_features.py | 10 minutes |
| Phase 3.1 | Update feature_selector.py | 5 minutes |
| Testing | Run all tests | 15 minutes |
| **TOTAL** | | **~2 hours** |

---

## Next Steps

1. **Review this plan** with the team/user
2. **Backup current files** before making changes
3. **Start with Phase 1.1** (feature_helpers.py) - highest impact
4. **Test incrementally** after each phase
5. **Validate feature names** in output files
6. **Document any boron-specific insights** discovered during migration

---

**Status**: Plan complete, ready for implementation
**Priority**: HIGH - Blocks B_only strategy functionality
**Complexity**: Medium - Systematic search-and-replace with logic verification
**Impact**: High - Enables correct boron feature engineering

---

*Document created: 2025-10-18*
*For: Boron Concentration Prediction Pipeline*
*Migration: Magnesium → Boron*
