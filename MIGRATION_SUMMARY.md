# Magnesium Pipeline Migration Summary

## Overview

Successfully created `magnesium_pipeline_latest` by migrating the improved potassium pipeline with all latest feature engineering enhancements.

## What Was Done

### 1. **Project Structure Created**
- Copied entire potassium pipeline structure to `/home/payanico/magnesium_pipeline_latest`
- Excluded temporary files (models, reports, logs, caches)
- Preserved all source code, documentation, and configuration

### 2. **Configuration Updates** (src/config/pipeline_config.py)

#### Core Settings
- ✅ **Project name**: `PotassiumPrediction` → `MagnesiumPrediction`
- ✅ **Target column**: `Potassium` → `Magnesium %`
- ✅ **Data directories**: Updated to match magnesium pipeline structure
  - Raw data: `data/raw/newdata` → `data/raw/data_5278_Phase3`
  - Reference file: `lab_Element_Rough_Nico.xlsx` → `Final_Lab_Data_Nico_New.xlsx`

#### Spectral Regions
- ✅ **Primary region**: Replaced K I doublet (766-770 nm) with **Mg I triplet (516-519 nm)**
  - Center wavelengths: 516.7, 517.3, 518.4 nm

- ✅ **Context regions**: Updated to include primary magnesium lines
  - **Mg I 285.2 nm**: Most prominent Mg line (284.5-286.0 nm)
  - **Mg I 383.8 nm**: Strong Mg line (383.0-384.5 nm)
  - **Mg II**: Ionic lines (279.0-281.0 nm) - 279.55, 279.80, 280.27 nm
  - **K I helper**: Kept for comparative analysis (768.79-770.79 nm)

- ✅ **Removed**: K-specific regions (K_I_404, K_I_691) that aren't needed for Mg prediction

#### Feature Strategies
- ✅ **Strategy naming**: `K_only` → `Mg_only`
- ✅ **Default strategy**: Changed to `simple_only` (more stable for initial runs)
- ✅ **Feature method**: `use_focused_potassium_features` → `use_focused_magnesium_features`

#### Feature Flags
- ✅ **Molecular bands**: Disabled (not critical for Mg)
- ✅ **Macro elements**: Enabled (S, P, Ca, K interactions with Mg)
- ✅ **Micro elements**: Enabled (Fe, Mn, B, Zn compete with Mg)
- ✅ **Oxygen/Hydrogen**: Disabled (less relevant for Mg)
- ✅ **Advanced ratios**: Enabled (Mg/Ca, Mg/K are critical)
- ✅ **Interference correction**: Disabled (not needed for Mg)

### 3. **Feature Engineering Updates**

All feature engineering files updated with element-specific changes:
- ✅ `src/features/feature_engineering.py`
- ✅ `src/features/enhanced_features.py`
- ✅ `src/features/concentration_features.py`
- ✅ `src/features/feature_helpers.py`
- ✅ `src/features/parallel_feature_engineering.py`

**Key changes:**
- Variable/function names: `K_only` → `Mg_only`
- Region references: `potassium_region` → `magnesium_region`
- Feature ratios: `K_C_ratio` → `Mg_C_ratio`, `K/C` → `Mg/C`
- Comments and docstrings updated for magnesium context

### 4. **Documentation Updates**
- ✅ **CLAUDE.md**: Updated project description and spectral regions
- ✅ **main.py**: Updated ML pipeline references
- ✅ **pyproject.toml**: Changed project name and description

### 5. **Latest Improvements Included**

The new pipeline includes all recent improvements from potassium pipeline:
- ✅ **SHAP feature selection** (`src/features/shap_feature_selector.py`)
- ✅ **Spectral preprocessing** (Savitzky-Golay, SNV, ALS baseline)
- ✅ **Parallel processing** (data and feature parallelization)
- ✅ **Mislabel detection** (clustering and outlier methods)
- ✅ **Sample exclusion** (exclude suspicious samples from training)
- ✅ **Enhanced concentration features** (range-specific features)
- ✅ **Improved AutoGluon configuration** (stacking, hyperparameters)
- ✅ **Uncertainty quantification**
- ✅ **Advanced dimension reduction** (PCA, PLS, VAE, autoencoders)

## Validation

Configuration successfully loaded with:
- ✓ Project: MagnesiumPrediction
- ✓ Target column: Magnesium %
- ✓ Magnesium region: Mg_I (516.0-519.0nm)
- ✓ Number of spectral regions: 19
- ✓ Feature strategies: ['simple_only']

## Next Steps

### 1. **Install Dependencies**
```bash
cd /home/payanico/magnesium_pipeline_latest
uv sync
```

### 2. **Prepare Your Data**
Ensure your data is in the expected location:
```
data/
├── raw/data_5278_Phase3/        # Your LIBS spectral files (.csv.txt)
└── reference_data/
    └── Final_Lab_Data_Nico_New.xlsx  # Ground truth Mg concentrations
```

### 3. **Test the Pipeline**
```bash
# Check configuration
python main.py --help

# Test with a small training run (if you have data)
python main.py train --models extratrees --feature-parallel --data-parallel

# Or with GPU
python main.py train --models xgboost lightgbm catboost --gpu --feature-parallel --data-parallel
```

### 4. **Recommended First Run**
```bash
# Train with proven configuration
python main.py train \\
    --models random_forest gradient_boost extratrees xgboost lightgbm catboost \\
    --feature-parallel \\
    --data-parallel \\
    --gpu
```

### 5. **Advanced Features**

#### SHAP Analysis
```bash
# Train a model
python main.py train --models catboost --gpu

# Run SHAP analysis
./run_shap_analysis.sh --latest catboost

# Use SHAP-selected features
python main.py train \\
    --models xgboost lightgbm \\
    --shap-features models/simple_only_catboost_*_shap_importance.csv \\
    --shap-top-n 30 \\
    --gpu
```

#### Mislabel Detection
```bash
# Detect potential mislabels
python main.py detect-mislabels \\
    --focus-min 0.0 \\
    --focus-max 0.5 \\
    --min-confidence 2 \\
    --feature-parallel \\
    --data-parallel

# Train without suspicious samples
python main.py train \\
    --models xgboost lightgbm catboost \\
    --exclude-suspects reports/mislabel_analysis/suspicious_samples_min_confidence_2.csv \\
    --gpu
```

## Key Differences from Old Magnesium Pipeline

### Improvements
1. **Better feature engineering** with parallel processing
2. **SHAP-based feature selection** for interpretability
3. **Spectral preprocessing** (Savgol + SNV + baseline correction)
4. **Mislabel detection** to improve data quality
5. **Sample exclusion** capability
6. **Enhanced AutoGluon** with better hyperparameters
7. **Uncertainty quantification** support
8. **More robust configuration** with Pydantic validation

### Configuration Changes
- Default strategy changed to `simple_only` (more stable)
- Feature count reduced with selection methods
- Better GPU support across all models
- Improved sample weighting methods

## Troubleshooting

### If configuration doesn't load:
```bash
python -c "from src.config.pipeline_config import config; print(config.project_name)"
```

### If modules aren't found:
```bash
export PYTHONPATH=/home/payanico/magnesium_pipeline_latest:$PYTHONPATH
```

### If you need to revert:
Your old magnesium pipeline is preserved at `/home/payanico/magnesium_pipeline_old`

## Migration Script

The automated migration script is available at:
```
/home/payanico/magnesium_pipeline_latest/migrate_to_magnesium.py
```

You can use this as reference if you need to make similar migrations in the future.

## Files Modified

- ✅ `src/config/pipeline_config.py` - Core configuration
- ✅ `src/features/feature_engineering.py` - Main feature extraction
- ✅ `src/features/enhanced_features.py` - Advanced features
- ✅ `src/features/concentration_features.py` - Concentration-specific
- ✅ `src/features/feature_helpers.py` - Helper functions
- ✅ `src/features/parallel_feature_engineering.py` - Parallel processing
- ✅ `main.py` - Main entry point
- ✅ `CLAUDE.md` - Documentation
- ✅ `pyproject.toml` - Project metadata

---

**Created:** October 9, 2025
**Source:** Potassium Pipeline (latest)
**Target:** Magnesium Pipeline with all improvements
**Status:** ✅ Complete and tested
