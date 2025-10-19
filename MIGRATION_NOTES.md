# Boron Pipeline Migration Notes

This project was created from the Potassium Pipeline and adapted for Boron detection.

## Changes Made

### 1. Automated Updates
- All references to "potassium"/"magnesium" changed to "boron"
- Element symbol changed from "K"/"Mg" to "B"
- Project name and metadata updated
- Spectral regions updated for B detection

### 2. Spectral Regions
Updated from K/Mg spectral lines to B spectral lines:
- **Original K regions**: 766-770nm (K I doublet), 404nm (K I)
- **Original Mg regions**: 516-519nm (Mg I triplet), 285nm (Mg I), 383nm (Mg I)
- **New B regions**: 249.0-250.5nm (B I doublet), 208.0-210.0nm (B I lines)

Common B LIBS lines for reference:
- B I: 249.68 nm, 249.77 nm (primary doublet - strongest)
- B I: 208.89 nm, 208.96 nm (secondary doublet)

## Manual Tasks Required

### 1. Data Preparation
- [ ] Update reference Excel files with B concentration values
- [ ] Ensure spectral data covers B wavelength regions (UV range: 208-250 nm)
- [ ] Verify data file naming conventions

### 2. Configuration Updates
- [ ] Review `src/config/pipeline_config.py` for B-specific settings
- [ ] Adjust concentration ranges (typical B ranges may differ from K/Mg)
- [ ] Update outlier detection thresholds if needed
- [ ] Configure UV spectral range settings

### 3. Model Tuning
- [ ] Adjust hyperparameter ranges for B concentration prediction
- [ ] Update sample weighting if B distribution differs from K/Mg
- [ ] Consider different model architectures if needed
- [ ] Tune for potentially lower concentration ranges

### 4. Validation
- [ ] Verify spectral peak extraction works for B lines (UV range)
- [ ] Test with sample B data
- [ ] Validate model performance metrics
- [ ] Check UV baseline correction effectiveness

### 5. Cloud Deployment
- [ ] Update GCP project settings if using different project
- [ ] Modify bucket names in cloud configurations
- [ ] Update Docker image names

## Quick Start

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Prepare your B data**:
   - Place spectral files in `data/raw/`
   - Add reference Excel with B concentrations
   - Ensure spectrometer covers UV range (208-250 nm)

3. **Update spectral regions** (if needed):
   Edit `src/config/pipeline_config.py` to match your LIBS setup

4. **Train models**:
   ```bash
   python main.py train --gpu --data-parallel --feature-parallel
   python main.py autogluon --gpu --data-parallel --feature-parallel
   ```

5. **Deploy**:
   ```bash
   ./deploy/local-deploy.sh build
   ./deploy/gcp_deploy.sh all
   ```

## Important Files to Review

1. `src/config/pipeline_config.py` - Main configuration (check B spectral regions)
2. `src/features/feature_engineering.py` - Feature extraction
3. `src/spectral_extraction/peak_extraction.py` - Peak detection
4. `config/cloud_config.yml` - Cloud deployment settings

## Boron-Specific Considerations

### UV Spectral Range
- Boron lines are in UV (208-250 nm) vs visible (K, Mg)
- May require different baseline correction strategies
- Higher noise levels in UV region
- Potential for stronger atmospheric absorption

### Concentration Ranges
- Boron is typically present in lower concentrations than K/Mg
- Expected range: 0.001% - 1.0% (vs K: 1-5%, Mg: 0.5-3%)
- May need different feature scaling approaches

### Interference Considerations
- Carbon lines may interfere in UV region
- Oxygen and nitrogen lines present
- Careful wavelength selection important

## Support

For questions about the original potassium pipeline, refer to the source project.
For B-specific adaptations, document changes in this file.
