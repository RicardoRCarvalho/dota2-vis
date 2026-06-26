# Dota2-Vis

This repository contains the dataset information and baseline experiments associated with our SBGames 2026 paper:

* *Computer Vision for MOBA Analytics: A Dataset and Baseline for Visibility Analysis in Dota 2* [[arXiv]](https://arxiv.org/abs/2606.26970)

The project introduces **Dota2-Vis**, a video-based dataset and baseline pipeline for visibility analysis in professional Dota 2 matches. Instead of relying only on structured match data, such as drafts, logs, replays, or public APIs, this work investigates how computer vision can be used to estimate what each team could actually see during a match.

The dataset and baseline are designed to support research on MOBA analytics, esports performance analysis, minimap understanding, and visibility-centered game analytics.

## Code

The source code will be made available soon.

## Data

Dota2-Vis contains two complementary components:

1. **Manually annotated minimap images**, used to train and evaluate player-icon detectors.
2. **Full-match gameplay videos from The International 2025**, recorded from both Radiant and Dire perspectives.

The dataset was built to support the extraction of opponent-visible player presence over time. This enables analyses at different levels, including players, heroes, roles, teams, match stages, and match outcomes.

### Match Videos

The video component contains all 144 matches from **The International 2025**, recorded twice: once from the Radiant perspective and once from the Dire perspective.

In total, the dataset includes:

* 144 professional Dota 2 matches;
* 288 Full HD videos;
* both team perspectives for every match;
* fixed recording resolution of 1920 × 1080 pixels.

These videos are used to estimate when each player is visible from the opposing team’s perspective.

### Minimap Annotations

The annotation component contains **2,477 manually annotated minimap images** collected from professional matches that were not part of The International 2025, reducing overlap between training data and the matches analyzed in the paper.

Each minimap image has resolution **240 × 240 pixels** and was annotated with bounding boxes for player-related minimap elements.

The final annotation protocol includes **21 classes**:

* 10 player classes, one for each player in the match;
* 10 clone classes, one for each player;
* 1 `Other` class for non-player minimap elements that may affect detection, such as pings.

The predefined split is:

* 1,670 training images;
* 407 validation images;
* 400 test images.

## Baseline

We provide baseline experiments using YOLO11 variants for player-icon detection on Dota 2 minimaps.

The evaluated models include:

* YOLO11n;
* YOLO11s;
* YOLO11m;
* YOLO11l;
* YOLO11x.

Among the evaluated variants, **YOLO11l** achieved the best overall trade-off, with:

* Precision: 0.974;
* Recall: 0.906;
* F-score: 0.939;
* mAP50:95: 0.729.

The trained detector is then used to estimate opponent-visible map presence over time.

## How to Obtain the Dataset

Dataset access instructions will be made available soon.

## Citation

If you use our code or dataset in your research, please cite our paper:

* R. R. Carvalho, E. Oliveira, L. B. M. Kummer, E. C. Paraiso, R. Laroca, “Computer Vision for MOBA Analytics: A Dataset and Baseline for Visibility Analysis in Dota 2,” in *Simpósio Brasileiro de Jogos e Entretenimento Digital (SBGames)*, 2026. [[arXiv]](https://arxiv.org/abs/2606.26970)

```bibtex
@inproceedings{carvalho2026computer,
  title = {Computer Vision for {MOBA} Analytics: A Dataset and Baseline for Visibility Analysis in {Dota}~2},
  author = {R. {Carvalho} and E. {Oliveira} and L. B. M. {Kummer} and E. C. {Paraiso} and R. {Laroca}},
  year = {2026},
  month = {Sept},
  booktitle = {Simpósio Brasileiro de Jogos e Entretenimento Digital (SBGames)},
  pages = {1-12},
  doi = {},
  issn = {}
}
```

## Contact

Please contact Ricardo Carvalho ([ricardo.rcarvalho@ppgia.pucpr.br](mailto:ricardo.rcarvalho@ppgia.pucpr.br)) with questions or comments.
