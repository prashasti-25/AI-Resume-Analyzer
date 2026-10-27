# data/

- `skills_master.csv` — the shared skill vocabulary used by both:
  - `resume_parser/skill_extractor.py` (extracting skills from an uploaded resume)
  - `ml/predict.py` (matched/missing skill detection against a job description)

  Both parts of the project read this SAME file, so they always agree on
  what counts as a "skill". Add new skills as new rows (`skill,category`)
  — no code changes needed elsewhere.

No other dataset is required. `ml/train.py` generates its own synthetic
training data on the fly for the optional supervised classifier (see
`ml/train.py`'s docstring for why: no real labeled resume/JD dataset
exists publicly, and hand-labeling one is out of scope for this project).
