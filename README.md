# textleaks

The text-content companion to `gitleaks`. Where gitleaks scans for credentials and secrets, **textleaks** scans for operator-internal narrative bleeding into your public-facing text: codenames, phase numbers, internal handoff doc references, "earlier in this session," memory observation IDs, your other project's codename slipped into an ADR.

## Why this exists

If you run multiple projects in the same AI coding agent session (Claude Code, Cursor, OpenClaw, etc.) and one or more of them is public OSS, you accumulate a vocabulary of internal-process framing that leaks across the boundary every time you write prose. The patterns aren't credentials. They're cleanups of internal work that read as natural English ("Phase 6 §3 verification revealed..."). Existing secret scanners don't see them, because they're not designed to.

textleaks's starter catalog is a generalization of a real catalog used in production across multiple public OSS repos, with a 15-class taxonomy.

## Install

Install directly from GitHub (PyPI publication pending — the name `textleaks` is reserved but the package is not yet uploaded):

```sh
pip install "git+https://github.com/creatornader/textleaks.git@v0.2.0"
```

Or run as a `pre-commit` hook (see below). The pre-commit framework handles the install for you.

## Use

```sh
textleaks scan                  # scan current directory
textleaks scan src/ docs/       # scan specific paths
textleaks scan --format json    # machine-readable output
textleaks list-classes          # show all classes in the active catalog
textleaks init                  # write a starter textleaks.yaml into the repo
```

Exit code: `0` if clean, `1` if any findings. Wire it into CI to fail PRs that introduce leaks.

## Pre-commit hook

Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/creatornader/textleaks
    rev: v0.2.0
    hooks:
      - id: textleaks
```

The hook runs on every commit and blocks if a finding is added.

## How it works

textleaks ships a starter catalog with 10 generic leak classes baked in (phase numbering, time-of-day narration, agent-memory IDs, session-state framing, etc.). Three classes ship with empty pattern lists because they need your project's specifics:

- **`cross-project-codenames`**: names of OTHER projects you maintain
- **`operator-paths`**: your local username, beyond the generic `/Users/X/` pattern
- **`private-wrapper-services`**: internal services your public code talks to

Run `textleaks init` to scaffold a `textleaks.yaml` in your repo. Add your codenames. Commit. The next `textleaks scan` merges your overrides on top of the starter and flags any new finding.

## The 15-class taxonomy

textleaks's catalog is derived from a 15-class taxonomy of leak patterns observed across multiple private-to-public flips. See [`docs/leak-classes.md`](docs/leak-classes.md) for the prose explanation of each class.

## Roadmap

This is v0.2.0. Planned for v0.3:

- **Vale style integration** for prose-level checks (sentence cadence, narrative tense) that go beyond regex
- **LLM semantic layer** ("Layer B"): for each line a regex flags, an LLM second-opinion judges whether it's a real leak vs a false positive in context
- **`textleaks audit-history`**: scan commit messages and full git history, not just the working tree
- **`textleaks audit-issues`**: scan GitHub issue bodies (the place leaks survive force-pushes)
- **More language ecosystems**: ship `.pre-commit-hooks.yaml` patterns for Husky, lefthook, simple-git-hooks
- **PyPI release** once the rename has settled

If any of these matter to you before they ship, open an issue.

## What it does NOT do

- Does not encrypt files (use `git-crypt` or `git-secret` for that).
- Does not enforce a mirror-repo structure (that's documentation, not code).
- Does not catch credentials (use `gitleaks` + `trufflehog` for that; textleaks runs alongside them, not instead).
- Does not rewrite git history (use `git-filter-repo` for that, after textleaks catches the prose).

## Related tools

textleaks is one layer of a three-tool stack for maintaining public OSS repos with private context:

| Tool | Concern | When to install |
|---|---|---|
| **textleaks** (this tool) | Narrative-leak detection in text CONTENT (prose patterns, codenames) | Anywhere you write text that could leak operator-internal context |
| [**oss-twin**](https://github.com/creatornader/oss-twin) | Structural mirror gate that fails if any path declared private exists in the public tree | When you have a `*-internal` mirror repo |
| [**oss-security-scan**](https://github.com/creatornader/oss-security-scan) | Reusable GitHub Actions workflow (typos + gitleaks + trufflehog + osv-scanner) | Every public OSS repo |

For the full stack wire-up pattern (one repo, all three tools), see [`oss-security-scan/examples/full-stack-starter/`](https://github.com/creatornader/oss-security-scan/tree/main/examples/full-stack-starter).

## Note for repos with prose linters

`textleaks.yaml` lists codenames as REGEX PATTERN VALUES (e.g. `- '\bmyproject\b'`). It defines what to catch, not what to mention. If your repo also runs a prose linter (Vale, an LLM-based audit, etc.), exempt `textleaks.yaml` from those scanners. Otherwise the linter will flag the pattern strings as if they were narrative leaks. Same applies to [`.oss-twin.yaml`](https://github.com/creatornader/oss-twin).

## Renamed from `leakguard`

This package was originally published as `leakguard` (v0.1.x). It was renamed to `textleaks` in v0.2.0 because:

1. `leakguard` on PyPI is an unrelated secret scanner by another author, creating real footgun potential ("I just ran `pip install leakguard` and got the wrong tool").
2. The original framing positioned the tool reactively against gitleaks ("catches what gitleaks misses"). The honest positioning is *complementary*: gitleaks scans for secret-shaped strings, textleaks scans for narrative leaks in text content. Different categories, same security posture.

The GitHub repo URL `creatornader/leakguard` redirects to `creatornader/textleaks`, but you should update your `.pre-commit-config.yaml` to the new URL and hook id when convenient.

## License

Apache 2.0. See [LICENSE](LICENSE).
