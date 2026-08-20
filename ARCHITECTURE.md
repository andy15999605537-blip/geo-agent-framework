# Geo Agent Framework Architecture

## Overview

Geo Agent Framework is designed as an execution-oriented GEO system.

The core idea is not only to measure AI visibility, but to create a repeatable loop:

```
Brand Knowledge
      ↓
Question Bank
      ↓
AI Engine Sampling
      ↓
Visibility Analysis
      ↓
GEO Diagnosis
      ↓
Execution Tasks
      ↓
Verification Loop
```

## Core Layers

### 1. Knowledge Layer

Contains the information an AI system should understand about a brand:

- Brand facts
- Product information
- Unique advantages
- Trust signals
- Customer scenarios

Typical files:

```
brand_facts.json
```

### 2. Measurement Layer

Collects AI visibility signals:

- Brand mentions
- Ranking position
- Citation sources
- Competitor appearance
- Question-level performance

Inputs:

```
question_bank.json
```

### 3. Diagnosis Layer

Converts observations into actionable findings:

- Missing entity information
- Weak content extraction
- Missing citation sources
- Technical accessibility issues
- Content gaps

### 4. Execution Layer

Transforms diagnosis into tasks:

- Content updates
- Technical fixes
- Authority building
- Distribution actions

Each action should include:

- Reason
- Priority
- Owner
- Acceptance criteria

### 5. Verification Layer

Measures whether execution creates improvement:

```
Before sampling
        ↓
Implementation
        ↓
After sampling
        ↓
Performance comparison
```

## Customization Model

The framework logic stays reusable.

Each company can provide its own:

```
your-brand/
├── brand_facts.json
├── question_bank.json
└── policies/
```

This allows agencies and companies to build different GEO agents on top of the same framework.
