# Rida Research Hunter — Summer 2027

Personal, low-cost research opportunity agent for a Vanderbilt mechanical-engineering sophomore seeking U.S. Summer 2027 opportunities.

## Search focus

Medical/surgical/miniature/soft robotics, microrobotics, medical devices, mechatronics, electromechanical systems, microfabrication, microelectronics, MEMS, flexible electronics, sensors/actuators, nanotechnology, biomedical imaging, computer vision, signal processing, Fourier/image/sound analysis.

## What it does

1. Searches job APIs and web search for research programs, internships and relevant university opportunities.
2. Deduplicates results in SQLite.
3. Uses OpenAI only on a capped number of new opportunities per run.
4. Scores technical fit, international-student eligibility, realistic getability, career value and interest alignment.
5. Searches for faculty/lab pages related to high-scoring universities/opportunities.
6. Scores whether a cold email to a professor is likely to help.
7. Sends email alerts above the configured threshold.
8. Publishes a static dashboard to `docs/index.html`.
9. Runs every 30 minutes via GitHub Actions.

## Secrets

Required: `OPENAI_API_KEY`, `ADZUNA_APP_ID`, `ADZUNA_APP_KEY`, `CANDIDATE_PROFILE_JSON`.
Optional: `RESEND_API_KEY`, `RESEND_FROM`, `ALERT_EMAIL`, `BRAVE_SEARCH_API_KEY`.

Never commit a real API key or the private candidate profile to a public repository.

## Local

Create `.env`, create `profile.json` from the provided profile, then:

`pip install -r requirements.txt`

`python -m app.pipeline`

`python generate_static.py`

`uvicorn app.main:app --reload`

## GitHub

The workflow is in `.github/workflows/hunt.yml`. GitHub scheduled workflows use POSIX cron and run on the default branch; GitHub supports schedules as often as every 5 minutes. The project uses every 30 minutes.

For a public repository, keep `profile.json` out of the repository and use the `CANDIDATE_PROFILE_JSON` secret. The generated dashboard is intentionally sanitized and contains opportunity/professor information, not the candidate's private profile.
