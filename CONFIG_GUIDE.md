# Configuration Guide for Quality Validation

## Quick Start

### Process a Single File
```yaml
# conf/state/state_1.yaml
directory_path: "../data/sample_2026-05-21_14-30/"
files:
  - "geo_example.rdf"
```

Then run:
```bash
python src/main.py
```

### Process All Files in Directory
```yaml
# conf/state/state_1.yaml
directory_path: "../data/sample_2026-05-21_14-30/"
files: []  # Empty list = process all matching files
```

### Process with Include/Exclude Patterns
```yaml
# conf/state/state_1.yaml
directory_path: "../data/sample_2026-05-21_14-30/"
files: []

file_filter:
  extensions: [".rdf"]
  include_patterns: ["geo_"]      # Only process files starting with "geo_"
  exclude_patterns: ["test_"]     # Skip files starting with "test_"
```

---

## Configuration Structure

### Input Configuration

**Specific Files (files list populated):**
```yaml
directory_path: "../data/sample_2026-05-21_14-30/"
files:
  - "geo_open-data-brandenburg.rdf"
  - "geo_gdi-de.rdf"
  - "non_geo_land-schleswig-holstein.rdf"
```

**All Files (files list empty):**
```yaml
directory_path: "../data/sample_2026-05-21_14-30/"
files: []  # Triggers directory scanning with patterns
```

### File Filtering

Only applies when `files` list is **empty**:

```yaml
file_filter:
  # File extensions to include
  extensions: [".rdf"]

  # Include patterns: process only files matching these (filename prefix)
  include_patterns: []
    # Leave empty to include all
    # - "geo_"          # Include only geo_ files
    # - "non_geo_"      # Include non_geo_ files

  # Exclude patterns: skip files matching these (filename prefix)
  exclude_patterns: []
    # Leave empty to exclude none
    # - "test_"         # Skip test_ files
```

**Examples:**
- Process all `.rdf` files:
  ```yaml
  files: []
  file_filter:
    include_patterns: []
    exclude_patterns: []
  ```

- Process only geo datasets:
  ```yaml
  files: []
  file_filter:
    include_patterns: ["geo_"]
  ```

- Process geo and non-geo, skip test files:
  ```yaml
  files: []
  file_filter:
    include_patterns: ["geo_", "non_geo_"]
    exclude_patterns: ["test_"]
  ```

### Output Configuration

```yaml
output_dir: "outputs/"  # Root directory for all runs
```

**Output Structure:**
```
outputs/
└── run_2026-05-21_14-30-45/          # Timestamp-based run directory
    ├── metadata.json                 # Run configuration & input info
    ├── run_summary.json              # Aggregated stats across all files
    ├── geo_example/
    │   ├── result.json               # Complete validation result
    │   ├── summary.json              # Score, grade, by_dimension
    │   └── details.json              # Indicator-level breakdown
    └── non_geo_example/
        ├── result.json
        ├── summary.json
        └── details.json
```

---

## Full Configuration Reference

```yaml
# Directory containing RDF files to process
directory_path: "../data/sample_2026-05-21_14-30/"

# Files to process (if empty: scan directory with patterns)
files: []
  # - "filename_1.rdf"
  # - "filename_2.rdf"

# File filtering (only used if files list is empty)
file_filter:
  extensions: [".rdf"]
  include_patterns: []   # Filename prefixes to include
  exclude_patterns: []   # Filename prefixes to exclude

# Output directory for results
output_dir: "outputs/"

# Language configuration
language: "de"  # "de" or "en"

# Pipeline stages
pipeline:
  load_data: true
  static_analysis: true
  quality_validation: true
  semantic_analysis: true

# LLM configuration
llm:
  model: "anthropic/claude-sonnet-4.5"
  temperature: 0.0
  max_tokens: 50000

# Logging
logging:
  level: "DEBUG"   # "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
  verbose: true

# Quality scoring
quality:
  max_workers: 4
  dimension_weights:
    findability: 0.1
    accessibility: 0.3
    reusability: 0.3
    expressiveness: 0.3
  indicator_weights:
    find_keywords_count: 1.5
    find_theme_valid: 1.0
```

---

## Common Workflows

### Validate One File
```yaml
files:
  - "my_dataset.rdf"
```

### Batch: All Geo Files
```yaml
files: []
file_filter:
  include_patterns: ["geo_"]
```

### Batch: All Non-Geo Files
```yaml
files: []
file_filter:
  include_patterns: ["non_geo_"]
```

### Batch: Everything Except Test Files
```yaml
files: []
file_filter:
  exclude_patterns: ["test_"]
```

### Batch: Multiple Include Patterns
```yaml
files: []
file_filter:
  include_patterns: ["geo_", "non_geo_"]
  exclude_patterns: ["draft_", "old_"]
```

---

## Command Line Overrides

```bash
# Override directory
python src/main.py directory_path="../another_dir/"

# Override output directory
python src/main.py output_dir="my_outputs/"

# Override logging level
python src/main.py logging.level="INFO"

# Multiple overrides
python src/main.py \
  directory_path="../data/sample_2026-05-21/" \
  output_dir="results/" \
  logging.level="WARNING"
```

---

## Troubleshooting

**"Directory does not exist"**
- Check that `directory_path` is correct
- Use paths relative to project root

**"No files to process"**
- If using `files` list: verify filenames exist
- If using patterns: check `include_patterns` and `exclude_patterns`
- Run with `logging.level: "DEBUG"` to see what files were found

**"Output directory missing"**
- Check that `output_dir` is writable
- Directory will be created automatically if parent exists
