# Boron Pipeline Configuration Update Summary

## Date: 2025-10-18

## Overview

Successfully configured `pipeline_config.py` for boron (B) prediction based on literature research of LIBS (Laser-Induced Breakdown Spectroscopy) emission lines.

## Literature Research Summary

### Key Boron LIBS Emission Lines

Based on NIST Atomic Spectra Database and peer-reviewed LIBS literature:

1. **B I 249.677 nm, 249.773 nm** (Primary doublet)
   - Strongest boron atomic lines
   - Prone to self-absorption at concentrations > 0.1%
   - UV region requires good UV sensitivity

2. **B I 208.893 nm, 208.959 nm** (Secondary doublet)
   - Less prone to self-absorption
   - Alternative detection method
   - Far UV region

3. **B II 345.128 nm** (Ionized boron)
   - Useful for plasma temperature characterization
   - Visible region, easier detection

4. **BO Molecular Emission**
   - Boron monoxide bands (complex, around 430nm region)
   - Alternative detection method for high concentrations
   - Can reduce self-absorption issues

### Challenges with Boron Detection

- **Limited emission lines**: Boron has very few detectable lines in UV-VIS-NIR range
- **Self-absorption**: 249.7 nm doublet saturates at higher concentrations
- **UV region**: Requires good UV sensitivity and baseline correction
- **Trace element**: Typically 0.001-1.0% concentration (vs K: 1-5%, Mg: 0.5-3%)
- **Interference**: C, O, N lines present in UV region

## Configuration Changes

### 1. Project Metadata
```python
project_name: "BoronPrediction"  # Was: MagnesiumPrediction
target_column: "Boron %"  # Was: "Mg 285.213\n(wt%)"
```

### 2. Concentration Ranges
```python
target_value_min: 0.001  # Was: 0.5 (Boron is trace element)
target_value_max: 1.0    # Was: 5.0 (Lower typical range)
```

### 3. Primary Boron Spectral Region
```python
boron_region: PeakRegion = PeakRegion(
    element="B_I_249",
    lower_wavelength=248.5,
    upper_wavelength=250.8,
    center_wavelengths=[249.677, 249.773]
)
```

### 4. Context Regions (Updated)

Added boron-specific regions:
```python
# Secondary boron doublet (less self-absorption)
B_I_208: 207.8-210.0 nm, centers=[208.893, 208.959]

# Ionized boron (plasma characterization)
B_II_345: 344.0-346.3 nm, center=[345.128]
```

Kept for context:
- C_I, CA_I, CA_II, N_I (UV interference/baseline)
- K_I, Mg_I (elemental correlations)

### 5. Molecular Bands

Added BO molecular emission:
```python
BO_molecular: 429.0-434.0 nm, center=[431.5]
```

Kept UV molecules (relevant for boron region):
- CN violet system
- NH band (336 nm)
- NO band (236 nm - near B lines)

### 6. Feature Configuration Flags

```python
# OPTIMIZED FOR BORON
enable_molecular_bands: True     # BO emission important
enable_macro_elements: True      # Context elements
enable_micro_elements: True      # Removed old B_I from micro_elements
enable_oxygen_hydrogen: True     # BO formation, UV region
enable_advanced_ratios: True     # B/C, B/O critical
enable_spectral_patterns: True   # Self-absorption detection
enable_interference_correction: True   # UV region interference
enable_plasma_indicators: True   # B II for plasma temp

use_focused_boron_features: True  # Was: use_focused_magnesium_features
```

### 7. Feature Strategies

```python
feature_strategies: ["B_only", "simple_only"]  # Was: ["M_only", "simple_only"]
```

**B_only strategy includes:**
- Primary B_I_249 region
- Secondary B_I_208 region
- B_II_345 region
- K_I and Mg_I for context
- C_I for B/C ratio calculation

### 8. Spectral Preprocessing

```python
use_spectral_preprocessing: True
spectral_preprocessing_method: 'full'  # Savgol + SNV + ALS baseline
```

Critical for UV region:
- UV baseline drift correction
- Higher noise in UV
- Atmospheric absorption effects

## Validation Results

Configuration successfully loads:
```
✓ Project: BoronPrediction
✓ Target: Boron %
✓ Primary region: B_I_249 (248.5-250.8nm)
✓ Strategies: ['B_only', 'simple_only']
✓ Total regions: 28
```

## Boron-Specific Considerations

### 1. UV Spectral Range (208-250 nm)
- Requires spectrometer with UV capability
- Higher noise levels
- Stronger atmospheric absorption
- Careful wavelength calibration needed

### 2. Lower Concentration Ranges
- Typical: 0.001-1.0% (vs K: 1-5%, Mg: 0.5-3%)
- Different feature scaling may be needed
- More sensitive to contamination

### 3. Self-Absorption Effects
- 249.7 nm doublet saturates above ~0.1%
- Use 208.9 nm doublet for higher concentrations
- B II 345.1 nm as alternative
- BO molecular emission can reduce self-absorption

### 4. Interference Patterns
- Carbon lines in UV region
- Oxygen and nitrogen emissions
- Careful baseline correction required
- Molecular band interference (CN, NO)

### 5. BO Molecular Emission
- Alternative detection method
- Reduces self-absorption issues
- More complex spectral features
- Requires molecular band extraction

## Recommended Next Steps

### 1. Data Verification
```bash
# Verify your LIBS data covers UV range (208-250 nm)
# Check reference file has "Boron %" column
# Ensure wavelength calibration in UV region
```

### 2. Test Configuration
```bash
# Test with small dataset
python main.py train --models extratrees --strategy B_only --max-samples 100
```

### 3. Verify UV Capability
- Check spectrometer specifications
- Verify UV detection range
- Test baseline correction effectiveness
- Check for UV baseline drift

### 4. Optimize for Boron
```bash
# Start with B_only strategy
python main.py train --models xgboost lightgbm catboost --strategy B_only --gpu

# Then try simple_only
python main.py train --models xgboost lightgbm catboost --strategy simple_only --gpu

# Optimize if needed
python main.py optimize-models --models xgboost lightgbm --strategy B_only --trials 100 --gpu
```

### 5. SHAP Analysis
```bash
# Verify B I lines have high importance
./run_shap_analysis.sh --latest lightgbm
```

Expected top features:
- B_I_249 peak area/height
- B_I_249 FWHM (self-absorption indicator)
- B_I_249 asymmetry (self-absorption)
- B_I_208 peak features (alternative detection)
- B_II_345 (plasma temperature)
- B/C ratio (UV normalization)

## References

### NIST Atomic Spectra Database
- B I lines: 249.677 nm, 249.773 nm, 208.893 nm, 208.959 nm
- B II line: 345.128 nm

### Key Literature
1. "Study of optically thin condition for quantification of trace quantity of boron" - Self-absorption characterization
2. "Determination of boron with molecular emission using LIBS" - BO molecular approach
3. "Highly sensitive analysis of boron and lithium in aqueous solution using dual-pulse LIBS" - Sensitivity enhancement

### LIBS Boron Detection Challenges
- Limited atomic emission lines in UV-VIS-NIR
- Self-absorption in 249.7 nm doublet
- Requires UV-capable spectrometer
- Matrix and self-absorption effects

## Summary of Key Changes

| Aspect | Old (Mg/K) | New (Boron) |
|--------|------------|-------------|
| **Primary Line** | Mg I 516-519 nm (visible) | B I 249.7 nm (UV) |
| **Spectral Region** | Visible (400-800 nm) | UV (208-250 nm) |
| **Concentration Range** | 0.5-5.0% | 0.001-1.0% |
| **Self-Absorption** | Moderate | Strong (>0.1%) |
| **Detection Challenge** | Medium | High (UV, limited lines) |
| **Strategy Name** | Mg_only/M_only | B_only |
| **Feature Method** | use_focused_magnesium_features | use_focused_boron_features |
| **Molecular Bands** | Disabled | Enabled (BO emission) |
| **Interference Correction** | Disabled | Enabled (UV region) |

## Validation Status

- ✅ Configuration file updated
- ✅ Spectral regions configured (literature-based)
- ✅ Concentration ranges adjusted
- ✅ Feature strategies renamed
- ✅ Configuration loads successfully
- ✅ Total 28 spectral regions configured
- ⏳ Pending: Feature engineering code updates
- ⏳ Pending: Test with actual boron LIBS data

## Notes for Future Development

1. **Feature Engineering**: Update `src/features/feature_engineering.py` to recognize `use_focused_boron_features` flag
2. **Self-Absorption Detection**: Implement asymmetry-based self-absorption correction for 249.7 nm doublet
3. **BO Molecular Features**: Consider adding BO band extraction methods
4. **Concentration Range Models**: May need separate models for low (0.001-0.1%) and high (0.1-1.0%) ranges
5. **UV Baseline**: Enhanced baseline correction for UV region may be needed

---

**Configuration File**: `src/config/pipeline_config.py`
**Status**: ✅ Complete and validated
**Next Action**: Update feature engineering code to support boron-specific features
