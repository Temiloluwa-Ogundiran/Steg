# TODO
- [x] Add report/ to .gitignore and commit.
- [x] Back up report/ and rewrite history to remove it from all refs.
- [x] Restore local report/ and force-push rewritten history.
- [x] Verify report/ is ignored and history cleanup completed.

# Review
- [x] Verified `git check-ignore -v report` shows ignore rule.
- [x] Verified `git log --all -- report/ --oneline` produced no output.
