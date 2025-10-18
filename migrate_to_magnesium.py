#!/usr/bin/env python3
"""
Automated migration script to convert potassium pipeline to magnesium pipeline.
This script updates all necessary files to adapt the pipeline for magnesium analysis.
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple

def update_pipeline_config(file_path: Path) -> None:
    """Update pipeline_config.py with magnesium-specific settings."""
    print(f"Updating {file_path}...")

    with open(file_path, 'r') as f:
        content = f.read()

    # Replace project name
    content = content.replace('project_name: str = "PotassiumPrediction"', 'project_name: str = "MagnesiumPrediction"')

    # Replace target column
    content = content.replace('target_column: str = "Potassium"', 'target_column: str = "Magnesium %"')

    # Replace header comment
    content = content.replace(
        'Centralized Configuration Management for the Potassium Prediction ML Pipeline.',
        'Centralized Configuration Management for the Magnesium Prediction ML Pipeline.'
    )

    # Replace comments about concentration ranges
    content = re.sub(
        r'# Based on potassium concentration ranges \(typical values\)',
        '# Based on magnesium concentration ranges (typical values)',
        content
    )
    content = re.sub(r'15% K - low end', '15% Mg - low end', content)
    content = re.sub(r'35% K - high end', '35% Mg - high end', content)
    content = re.sub(r'45% K - very high', '45% Mg - very high', content)

    # Replace potassium_region with magnesium_region
    content = re.sub(
        r'# Literature-verified Potassium LIBS spectral lines:.*?# Updated for potassium: K I doublet at 766\.49, 769\.90 nm \(strongest lines\)\s+potassium_region:',
        '''# Literature-verified Magnesium LIBS spectral lines:
    # According to NIST and LIBS literature:
    # - 285.2 nm: Most prominent Mg I line (resonance line)
    # - 383.8 nm: Strong Mg I line
    # - 516.7-518.4 nm: Mg I triplet (516.7, 517.3, 518.4 nm)
    # - 279.5-280.3 nm: Mg II ionic lines (279.55, 279.80, 280.27 nm)

    # Primary magnesium region - Mg I triplet around 517 nm
    magnesium_region:''',
        content,
        flags=re.DOTALL
    )

    # Replace the potassium_region PeakRegion with magnesium_region
    content = re.sub(
        r'potassium_region: PeakRegion = PeakRegion\(\s+element="K_I", lower_wavelength=765\.0, upper_wavelength=771\.0, center_wavelengths=\[766\.49, 769\.90\]\)',
        'magnesium_region: PeakRegion = PeakRegion(\n        element="Mg_I", lower_wavelength=516.0, upper_wavelength=519.0, center_wavelengths=[516.7, 517.3, 518.4])',
        content
    )

    # Update context_regions to remove K-specific lines and add/update Mg lines
    # This is complex, so we'll do it in parts

    # Remove K_I_404 and K_I_691 regions
    content = re.sub(
        r'\s+# Additional potassium lines.*?PeakRegion\(element="K_I_691".*?\],\),\n',
        '',
        content,
        flags=re.DOTALL
    )

    # Update comments about keeping magnesium lines to make them primary
    content = re.sub(
        r'# Keep magnesium lines for context and potential interference detection',
        '# Primary magnesium spectral lines',
        content
    )

    # Update Mg lines - ensure they have proper widths
    content = re.sub(
        r'PeakRegion\(element="Mg_I_285", lower_wavelength=283\.5, upper_wavelength=286\.5, center_wavelengths=\[285\.2\]\),  # WIDENED: 1\.5→3\.0 nm',
        'PeakRegion(element="Mg_I_285", lower_wavelength=284.5, upper_wavelength=286.0, center_wavelengths=[285.2]),',
        content
    )

    content = re.sub(
        r'PeakRegion\(element="Mg_I_383", lower_wavelength=382\.0, upper_wavelength=385\.0, center_wavelengths=\[383\.8\]\),  # WIDENED: 1\.5→3\.0 nm',
        'PeakRegion(element="Mg_I_383", lower_wavelength=383.0, upper_wavelength=384.5, center_wavelengths=[383.8]),',
        content
    )

    content = re.sub(
        r'PeakRegion\(element="Mg_II", lower_wavelength=278\.0, upper_wavelength=281\.5, center_wavelengths=\[279\.55, 279\.80, 280\.27\]\),  # WIDENED: 2\.0→3\.5 nm \(3 peaks\)',
        'PeakRegion(element="Mg_II", lower_wavelength=279.0, upper_wavelength=281.0, center_wavelengths=[279.55, 279.80, 280.27]),',
        content
    )

    # Remove phosphorus region comment
    content = re.sub(
        r'\s+# Phosphorous region - kept from original pipeline for reference and comparative feature engineering\s+PeakRegion\(element="P_I_secondary".*?\],\),\n',
        '',
        content
    )

    # Add K_I_help region to context_regions for comparative analysis
    if 'K_I_help' not in content:
        # Add K line as helper after N_I_help
        content = re.sub(
            r'(PeakRegion\(element="N_I_help",.*?\],\),)\n',
            r'\1\n        PeakRegion(element="K_I_help", lower_wavelength=768.79, upper_wavelength=770.79, center_wavelengths=[769.79]),\n',
            content
        )

    # Update feature configuration comments
    content = re.sub(
        r'# Feature configuration flags - OPTIMIZED FOR POTASSIUM',
        '# Feature configuration flags - OPTIMIZED FOR MAGNESIUM',
        content
    )
    content = re.sub(
        r'enable_molecular_bands: bool = False   # CN/NH/NO bands can indicate organic matter affecting K',
        'enable_molecular_bands: bool = False   # CN/NH/NO bands can indicate organic matter affecting Mg',
        content
    )
    content = re.sub(
        r'enable_macro_elements: bool = True    # S, P, Ca, Mg - critical for K interactions',
        'enable_macro_elements: bool = True    # S, P, Ca, K - critical for Mg interactions',
        content
    )
    content = re.sub(
        r'enable_micro_elements: bool = True    # Fe, Mn, B, Zn - compete with K uptake',
        'enable_micro_elements: bool = True    # Fe, Mn, B, Zn - compete with Mg uptake',
        content
    )
    content = re.sub(
        r'enable_oxygen_hydrogen: bool = True   # H/O ratios affect K compounds',
        'enable_oxygen_hydrogen: bool = False   # H/O ratios affect Mg compounds',
        content
    )
    content = re.sub(
        r'enable_advanced_ratios: bool = True   # K/Ca, K/Mg, K/P ratios are critical',
        'enable_advanced_ratios: bool = True   # Mg/Ca, Mg/K ratios are critical',
        content
    )
    content = re.sub(
        r'enable_spectral_patterns: bool = True # Peak shapes help identify K compounds',
        'enable_spectral_patterns: bool = True # Peak shapes help identify Mg compounds',
        content
    )
    content = re.sub(
        r'enable_interference_correction: bool = True  # Fe/Mn can interfere with K lines',
        'enable_interference_correction: bool = False  # Fe/Mn can interfere with Mg lines',
        content
    )

    # Update feature generation method
    content = re.sub(
        r'# Potassium feature generation method\s+use_focused_potassium_features:',
        '# Magnesium feature generation method\n    use_focused_magnesium_features:',
        content
    )
    content = re.sub(
        r'use_focused_potassium_features: bool = True  # If True, uses focused features; if False, uses original features',
        'use_focused_magnesium_features: bool = True  # If True, uses focused features; if False, uses original high-magnesium features',
        content
    )

    # Update enhanced spectral regions comment
    content = re.sub(
        r'# Enhanced spectral regions for crop potassium prediction',
        '# Enhanced spectral regions for crop magnesium prediction',
        content
    )

    # Update macro_elements comment
    content = re.sub(
        r'# Note: Primary K lines.*?# Additional K lines for macro analysis if needed:.*?# PeakRegion\(element="K_I_404_macro".*?\],\),',
        '# Note: Primary Mg lines are already defined in magnesium_region and context_regions\n        # to avoid duplication. If needed for macro_elements analysis, uncomment below:\n        # PeakRegion(element="Mg_I_macro", lower_wavelength=516.0, upper_wavelength=519.0, center_wavelengths=[516.7, 517.3, 518.4]),\n        # PeakRegion(element="Mg_II_macro", lower_wavelength=279.0, upper_wavelength=281.0, center_wavelengths=[279.55, 279.80, 280.27]),',
        content,
        flags=re.DOTALL
    )

    # Update get_regions_for_strategy method
    content = re.sub(
        r'if strategy == "K_only":.*?# Only K regions \+ C for K_C_ratio\s+k_regions = \[self\.potassium_region\].*?return k_regions',
        '''if strategy == "Mg_only":
            # Only Mg regions + C for Mg_C_ratio
            mg_regions = [self.magnesium_region]
            mg_regions.extend([r for r in self.context_regions if r.element.startswith("Mg_I") or r.element.startswith("Mg_II")])
            # Add C_I for Mg_C_ratio calculation
            c_region = next((r for r in self.context_regions if r.element == "C_I"), None)
            if c_region:
                mg_regions.append(c_region)
            return mg_regions''',
        content,
        flags=re.DOTALL
    )

    # Update all_regions property
    content = re.sub(
        r'regions = \[self\.potassium_region\] \+ self\.context_regions',
        'regions = [self.magnesium_region] + self.context_regions',
        content
    )

    # Update feature_strategies
    content = re.sub(
        r'#feature_strategies: List\[str\] = \["K_only", "simple_only", "full_context"\]\s+feature_strategies: List\[str\] = \["K_only"\]',
        '#feature_strategies: List[str] = ["Mg_only", "simple_only", "full_context"]\n    feature_strategies: List[str] = ["simple_only"]',
        content
    )

    # Update raw data directory default
    content = re.sub(
        r'_raw_data_dir=str\(BASE_PATH / "data" / "raw" / "newdata"\)',
        '_raw_data_dir=str(BASE_PATH / "data" / "raw" / "data_5278_Phase3")',
        content
    )

    # Update reference data path
    content = re.sub(
        r'_reference_data_path=str\(BASE_PATH / "data" / "reference_data" / "lab_Element_Rough_Nico\.xlsx"\)',
        '_reference_data_path=str(BASE_PATH / "data" / "reference_data" / "Final_Lab_Data_Nico_New.xlsx")',
        content
    )

    # Update raw_data_dir_path property defaults
    content = re.sub(
        r'return Path\(self\.__dict__\.get\(\'_raw_data_dir\', f\'\{get_base_path\(\)\}/data/raw/newdata\'\)\)',
        'return Path(self.__dict__.get(\'_raw_data_dir\', f\'{get_base_path()}/data/raw/data_5278_Phase3\'))',
        content,
        count=2
    )

    # Update reference_data_path property defaults
    content = re.sub(
        r'return Path\(self\.__dict__\.get\(\'_reference_data_path\', f\'\{get_base_path\(\)\}/data/reference_data/lab_Element_Rough_Nico\.xlsx\'\)\)',
        'return Path(self.__dict__.get(\'_reference_data_path\', f\'{get_base_path()}/data/reference_data/Final_Lab_Data_Nico_New.xlsx\'))',
        content,
        count=2
    )

    with open(file_path, 'w') as f:
        f.write(content)

    print(f"✓ Updated {file_path}")

def update_feature_files(base_dir: Path) -> None:
    """Update feature engineering files to replace K with Mg."""
    print("\nUpdating feature engineering files...")

    feature_files = [
        'src/features/feature_engineering.py',
        'src/features/enhanced_features.py',
        'src/features/concentration_features.py',
        'src/features/feature_helpers.py',
        'src/features/parallel_feature_engineering.py',
    ]

    replacements = [
        # Variable and function names
        (r'K_only', 'Mg_only'),
        (r'k_only', 'mg_only'),
        (r'potassium_region', 'magnesium_region'),
        (r'use_focused_potassium_features', 'use_focused_magnesium_features'),

        # Comments and docstrings
        (r'Potassium-specific', 'Magnesium-specific'),
        (r'potassium-specific', 'magnesium-specific'),
        (r'potassium concentration', 'magnesium concentration'),
        (r'Potassium concentration', 'Magnesium concentration'),
        (r'K concentration', 'Mg concentration'),

        # Feature names
        (r'K_C_ratio', 'Mg_C_ratio'),
        (r'K/C', 'Mg/C'),

        # Keep K_I as is when it refers to specific spectral lines
        # But replace references to K as the element
    ]

    for file_rel_path in feature_files:
        file_path = base_dir / file_rel_path
        if not file_path.exists():
            print(f"⚠ Skipping {file_path} (not found)")
            continue

        print(f"Updating {file_path}...")

        with open(file_path, 'r') as f:
            content = f.read()

        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)

        with open(file_path, 'w') as f:
            f.write(content)

        print(f"✓ Updated {file_path}")

def update_main_py(file_path: Path) -> None:
    """Update main.py with magnesium references."""
    print(f"\nUpdating {file_path}...")

    with open(file_path, 'r') as f:
        content = f.read()

    replacements = [
        (r'Potassium Prediction ML Pipeline', 'Magnesium Prediction ML Pipeline'),
        (r'potassium prediction', 'magnesium prediction'),
        (r'Potassium concentration', 'Magnesium concentration'),
        (r'potassium concentration', 'magnesium concentration'),
    ]

    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

    with open(file_path, 'w') as f:
        f.write(content)

    print(f"✓ Updated {file_path}")

def update_claude_md(file_path: Path) -> None:
    """Update CLAUDE.md documentation for magnesium."""
    print(f"\nUpdating {file_path}...")

    with open(file_path, 'r') as f:
        content = f.read()

    # Replace project overview
    content = re.sub(
        r'This is a machine learning pipeline for predicting potassium concentration from LIBS',
        'This is a machine learning pipeline for predicting magnesium concentration from LIBS',
        content,
        flags=re.IGNORECASE
    )

    content = re.sub(
        r'potassium percentage',
        'magnesium percentage',
        content,
        flags=re.IGNORECASE
    )

    # Replace feature strategy descriptions
    content = re.sub(
        r'- \*\*K_only\*\*: Focus on potassium spectral regions.*?\)',
        '- **Mg_only**: Focus on magnesium spectral regions (516-519nm and 279-286nm)',
        content,
        flags=re.DOTALL
    )

    # Replace spectral regions in feature engineering description
    content = re.sub(
        r'\(766-770nm and 404nm for potassium\)',
        '(516-519nm and 279-286nm for magnesium)',
        content
    )

    # Replace neural network loss description
    content = re.sub(
        r'MagnesiumLoss',
        'MagnesiumLoss',
        content
    )

    # No need to replace - already says MagnesiumLoss in potassium pipeline

    with open(file_path, 'w') as f:
        f.write(content)

    print(f"✓ Updated {file_path}")

def update_pyproject_toml(file_path: Path) -> None:
    """Update pyproject.toml with magnesium project information."""
    print(f"\nUpdating {file_path}...")

    with open(file_path, 'r') as f:
        content = f.read()

    replacements = [
        (r'name = "potassium-prediction-pipeline"', 'name = "magnesium-prediction-pipeline"'),
        (r'description = ".*?"', 'description = "LIBS-based magnesium concentration prediction pipeline"'),
    ]

    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)

    with open(file_path, 'w') as f:
        f.write(content)

    print(f"✓ Updated {file_path}")

def main():
    """Main migration function."""
    print("=" * 60)
    print("Magnesium Pipeline Migration Script")
    print("=" * 60)

    base_dir = Path(__file__).parent

    # Update pipeline configuration
    update_pipeline_config(base_dir / 'src/config/pipeline_config.py')

    # Update feature engineering files
    update_feature_files(base_dir)

    # Update main.py
    update_main_py(base_dir / 'main.py')

    # Update CLAUDE.md
    update_claude_md(base_dir / 'CLAUDE.md')

    # Update pyproject.toml
    update_pyproject_toml(base_dir / 'pyproject.toml')

    print("\n" + "=" * 60)
    print("✓ Migration completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review the changes in the updated files")
    print("2. Test configuration loading: python main.py --help")
    print("3. If you have data, try a test training run")

if __name__ == '__main__':
    main()
