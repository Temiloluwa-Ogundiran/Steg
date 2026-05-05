# TODO
- [x] Add report/ to .gitignore and commit.
- [x] Back up report/ and rewrite history to remove it from all refs.
- [x] Restore local report/ and force-push rewritten history.
- [x] Verify report/ is ignored and history cleanup completed.

## Performance + warning fixes
- [x] Add a model-load warning filter in SteganoGAN.load.
- [x] Warm the model at FastAPI startup to remove per-request load overhead.
- [x] Use torch inference optimizations for encode/decode paths.
- [x] Add optional CPU thread tuning via env for server deployments.
- [ ] Verify warnings no longer appear per request and measure response times.

### Notes
- Tests: `python -m pytest tests/webapp/test_services.py -v` (system Python) passed.

# Review
- [x] Verified `git check-ignore -v report` shows ignore rule.
- [x] Verified `git log --all -- report/ --oneline` produced no output.
