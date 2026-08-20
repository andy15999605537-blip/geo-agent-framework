# Geo Agent Framework Overview

```
                 Brand Facts
                     |
                     v
              Question Bank
                     |
                     v
             AI Engine Sampling
                     |
                     v
             GEO Diagnosis
                     |
                     v
            Execution Workflow
                     |
                     v
              Verification Loop
```

The framework separates reusable GEO logic from brand-specific data.

## Framework Layer

- Sampling engines
- Audit rules
- Task generation
- Verification workflows

## Brand Layer

- Company facts
- Products
- Buyer questions
- Industry rules

This separation allows one framework to power multiple GEO agents.

## Why this architecture

The framework separates reusable GEO execution logic from brand-specific knowledge.

This enables:

- One GEO engine supporting multiple brands
- Different industries using different question banks
- Custom diagnosis rules without changing the core system
- Repeatable verification after implementation
