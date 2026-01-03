# Website Content Staging

Staging repository for public-facing figure summaries to be merged into `blalterman.github.io`.

## Purpose

This repository contains:
- **Figure summaries**: Public-friendly explanations of research figures
- **Guidelines**: Writing standards for maintaining consistent voice

The content is staged here for review before integration with the main website repository.

## Structure

```
for-website/
├── public/
│   └── data/
│       └── figure_summaries/
│           └── {paper_id}/
│               └── figure_summaries.json
├── .claude/
│   └── guidelines/
│       ├── public_summaries.md
│       └── figure_summary_workflow.md
└── README.md
```

## Content Summary

### Figure Summaries (10 papers, ~86 figures)

| Paper ID | Figures | Topic |
|----------|---------|-------|
| Alterman_2018_ApJ_864_112 | 9 | Alpha/proton beam comparison |
| Alterman_2019_ApJL_879_L6 | 6 | He abundance correction |
| s11207-021-01801-9 | 6 | SWEAP overview |
| Alterman_2023_ApJ_952_42 | 11 | A_He in switchbacks |
| Alterman_2024_ApJL_964_L31 | 4 | Collisional age study |
| aa51550-24 | 8 | Heavy ion abundances |
| Alterman_2025_ApJL_982_L40 | 13 | Alfvenicity correlation |
| aa54299-25 | 3 | Phase space evolution |
| Alterman_2025_ApJL_984_L64 | 4 | Alpha drift temperature |
| Alterman_2026_ApJL_996_L12 | 25 | Collisional regime |

### JSON Schema (figure_summaries.json)

```json
{
  "paper_id": "Alterman_2018_ApJ_864_112",
  "paper_title": "A Comparison of...",
  "paper_doi": "https://doi.org/10.3847/...",
  "metadata": {
    "version": "1.0",
    "figures_count": 9,
    "target_audience": "scientifically_literate_public"
  },
  "figures": [
    {
      "figure_id": "fig_1",
      "short_title": "Three Ion Populations...",
      "summary": {
        "what_we_see": "...",
        "the_finding": "...",
        "why_it_matters": "..."
      },
      "keywords": ["Faraday cup", "charge flux", ...]
    }
  ]
}
```

## Integration with blalterman.github.io

### Manual Merge Procedure

1. Review content in this repository
2. Copy `public/data/figure_summaries/` to website's data directory
3. Update website components to consume new data
4. Test locally
5. Commit to website repository

### Future Automation

Consider:
- Git submodule linking
- GitHub Actions for automatic sync
- API endpoint for dynamic loading

## Guidelines

The `.claude/guidelines/` directory contains:
- **public_summaries.md**: Voice and style guidelines for public writing
- **figure_summary_workflow.md**: Process for creating new summaries

## Related Repositories

- **research-corpus**: Source papers and figures
- **paper-writer**: Writing evaluation tools
- **professional-identity**: Career materials
- **blalterman.github.io**: Target website (separate integration)
