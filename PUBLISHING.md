# Publishing guide

This project uses Semantic Versioning and publishes immutable releases from GitHub release tags.

## One-time PyPI setup

1. Create and verify the maintainer account on PyPI and enable two-factor authentication.
2. Confirm that `text-to-music-prompt-structurer` is available and create a pending Trusted Publisher for:
   - Owner: `edujbarrios`
   - Repository: `text-to-music-prompt-structurer`
   - Workflow: `release.yml`
   - Environment: `pypi`
3. Create a protected GitHub environment named `pypi` and require manual approval.
4. Optionally repeat the configuration on TestPyPI with the `testpypi` environment.

No long-lived PyPI API token is required.

## Release checklist

1. Ensure CI passes on `main`.
2. Update the version in `pyproject.toml` and `text_to_music_prompt_structurer/__init__.py`.
3. Move relevant entries from `Unreleased` into a dated changelog section.
4. Open and merge a release preparation pull request.
5. Create a GitHub release whose tag exactly matches the package version with a `v` prefix, such as `v0.1.0`.
6. Review and approve the protected `pypi` deployment.
7. Install the published package into a new environment and run a CLI smoke test.

PyPI does not allow replacing a file for an existing version. If a release is defective, publish a new patch version.

## Local verification

```bash
python -m pip install --upgrade build twine
python -m pytest
ruff check .
ruff format --check .
python -m build
python -m twine check dist/*
```

Then install the wheel into a clean virtual environment and run:

```bash
text-to-music-prompt "dreamy jazz at 90 bpm"
```

