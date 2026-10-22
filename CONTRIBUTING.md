# Contributing to ঞ (Nya) — Vocal for Local

Thank you for your interest in contributing to **ঞ (Nya)**! Our mission is to make useful online information easily discoverable in Assamese and other regional languages, with grounded AI answers and strict privacy defaults.

---

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please treat all contributors and users with dignity and respect.

---

## Development Workflow

1. **Workspace Setup:**
   - Follow instructions in [README.md](README.md) to set up your Python and Node.js environments.
   - Run frontend tests: `cd apps/web && npm test`
   - Run backend tests: `pytest -v tests/`
   - Run multilingual benchmark: `python evaluation/evaluate.py`

2. **Branching & Commits:**
   - Create focused feature branches (e.g. `feature/assamese-stemming`, `fix/citation-validation`).
   - Write clear, descriptive commit messages.

3. **Code Style & Quality:**
   - Frontend: TypeScript strict mode, clean component separation, Tailwind CSS design system.
   - Backend: PEP 8, type hints, Pydantic data schemas, structured logging.
   - NLP & Transliteration: Ensure any changes to Assamese normalization or phonetic mapping include test cases in `tests/test_nlp.py`.

4. **Privacy Principles:**
   - Never log raw search queries in access logs or persistent storage.
   - Keep search history opt-in only.
   - Anonymize user feedback queries using SHA-256 hashes.

5. **Pull Requests:**
   - Ensure all CI tests pass.
   - Include clear descriptions of the problem solved and test results.
