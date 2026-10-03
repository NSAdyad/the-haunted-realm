"""Prepare a reviewable deployment scope AFTER final passing local checks.

This helper reads Git/configuration and project files; it never stages, commits,
pushes, contacts GitHub, or changes runtime/protected files. Generated inventory
files are local audit artifacts and are deliberately excluded from the commit.

Usage (supply actual final result paths):
  python prepare_deployment_manifest.py --test-results work/.../results.json \
      --test-results work/.../presentation-results.json
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
JSON_OUTPUT = WORK / "deployment-candidate-files.json"
MD_OUTPUT = WORK / "exact-deployment-scope.md"
COMMIT_MESSAGE = "Integrate Haunted Realm shell and classroom presentation mode"
EXPECTED_REMOTE = "https://github.com/NSAdyad/the-haunted-realm.git"


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", "-c", "core.quotepath=false", *args], cwd=ROOT
    ).decode("utf-8")


def git_paths(*args: str) -> set[str]:
    return set(git(*args).split("\0")) - {""}


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def resolve_local(value: str, base: Path) -> Path | None:
    value = value.strip()
    if not value or value.startswith(("#", "data:", "blob:")):
        return None
    if re.match(r"(?:[a-z]+:)?//", value, re.I):
        raise AssertionError(f"Unexpected external runtime dependency: {value}")
    value = re.split(r"[?#]", value, maxsplit=1)[0]
    assert not value.startswith("/"), f"Root-absolute asset may break Pages prefix: {value}"
    result = (base / value).resolve()
    assert ROOT == result or ROOT in result.parents, f"Path escapes project: {value}"
    return result


def require_exact_file(path: Path) -> None:
    assert path.is_file(), f"Required candidate file missing: {relative(path)}"
    cursor = ROOT
    for segment in path.relative_to(ROOT).parts:
        assert segment in {child.name for child in cursor.iterdir()}, (
            f"Case mismatch in deployment path: {relative(path)}"
        )
        cursor /= segment
    assert path.stat().st_size < 100 * 1024 * 1024, (
        f"Candidate file exceeds GitHub file limit: {relative(path)}"
    )


class EntryReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references: list[str] = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        key = "href" if tag == "link" else "src"
        if tag in {"link", "script", "img", "source", "audio", "video"} and values.get(key):
            self.references.append(values[key])


def runtime_closure() -> set[str]:
    pending = [ROOT / "index.html", ROOT / "src/presentation.js"]
    result: set[str] = set()
    while pending:
        path = pending.pop()
        name = relative(path)
        if name in result:
            continue
        require_exact_file(path)
        result.add(name)
        references: list[tuple[str, Path]] = []
        if path.suffix == ".html":
            parser = EntryReferences()
            parser.feed(path.read_text(encoding="utf-8"))
            references.extend((value, path.parent) for value in parser.references)
        elif path.suffix == ".css":
            source = path.read_text(encoding="utf-8")
            references.extend(
                (value.strip(), path.parent)
                for value in re.findall(r"url\(\s*['\"]?([^)'\"]+)", source)
            )
        elif path.suffix == ".js":
            source = path.read_text(encoding="utf-8")
            imports = re.findall(
                r"(?:\bfrom\s*|\bimport\s*(?:\(\s*)?)['\"]([^'\"]+)['\"]", source
            )
            for value in imports:
                assert value.startswith("."), f"Unexpected bare runtime import: {value}"
                references.append((value, path.parent))
            # Registry paths intentionally resolve against the site's root.
            references.extend(
                (value, ROOT)
                for value in re.findall(r"['\"]((?:work|outputs|assets)/[^'\"\n]+)['\"]", source)
            )
        for value, base in references:
            resolved = resolve_local(value, base)
            if resolved is not None:
                pending.append(resolved)
    return result


def record(name: str, tracked: set[str], changed: set[str], staged: set[str]) -> dict:
    path = ROOT / name
    require_exact_file(path)
    return {
        "path": name,
        "bytes": path.stat().st_size,
        "sha256": sha(path),
        "git_state": "UNTRACKED" if name not in tracked else (
            "MODIFIED" if name in changed or name in staged else "TRACKED_UNCHANGED"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--test-results", action="append", required=True,
                        help="Actual final passing JSON result; repeat for each required suite.")
    args = parser.parse_args()

    closure = runtime_closure()
    newest_runtime = max((ROOT / name).stat().st_mtime_ns for name in closure)
    test_records = []
    for value in args.test_results:
        path = (ROOT / value).resolve()
        require_exact_file(path)
        data = read_json(path)
        tests = data.get("tests", [])
        assert tests and all(test.get("status", "").upper() == "PASS" for test in tests), (
            f"Final suite contains absent/non-passing checks: {relative(path)}"
        )
        assert data.get("failed", 0) == 0, f"Failing suite: {relative(path)}"
        for key in ("errors", "badRequests", "consoleErrors", "pageErrors", "networkErrors"):
            assert not data.get(key), f"Unresolved {key}: {relative(path)}"
        assert path.stat().st_mtime_ns >= newest_runtime, (
            f"Runtime changed after test results; rerun required suite: {relative(path)}"
        )
        test_records.append({"path": relative(path), "checks": len(tests), "sha256": sha(path)})

    verification_path = WORK / "protected-and-source-verification.json"
    require_exact_file(verification_path)
    verification = read_json(verification_path)
    assert verification.get("all_protected_unchanged") is True, "Protected verification failed"
    assert not verification.get("pre_existing_missing"), "Existing files are missing"
    assert not verification.get("existing_image_changes"), "Existing image content changed"
    assert verification_path.stat().st_mtime_ns >= newest_runtime, "Protected audit is stale"

    expected = dict(read_json(WORK / "before-snapshot.json")["protected_expected"])
    navigation = read_json(ROOT / "outputs/the-haunted-realm-navigation-approved-assets.json")
    for asset in navigation["assets"]:
        expected["outputs/" + asset["file"]] = asset["sha256"]
    images = read_json(ROOT / "outputs/the-haunted-realm-navigation-images-approved.json")
    for asset in images["approved_images"].values():
        expected[asset["file"]] = asset["sha256"]
    actual = {name: sha(ROOT / name) for name in expected}
    assert actual == expected, "Protected source hash mismatch: STOP"
    assert verification["protected_hashes_after"] == actual, "Recorded protected audit differs"
    assert verification["protected_count"] == len(actual), "Protected audit count differs"

    branch = git("branch", "--show-current").strip()
    remote = git("config", "--local", "--get", "remote.origin.url").strip()
    upstream = git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}").strip()
    assert branch == "main" and remote == EXPECTED_REMOTE and upstream == "origin/main", (
        "Existing repository/branch connection differs; STOP before deployment preparation"
    )
    head = git("rev-parse", "HEAD").strip()
    github_evidence_path = WORK / "github-read-only-verification.json"
    require_exact_file(github_evidence_path)
    github_evidence = read_json(github_evidence_path)
    assert github_evidence["repository"] == "NSAdyad/the-haunted-realm", "GitHub evidence repository differs"
    assert github_evidence["default_branch"] == "main", "GitHub evidence branch differs"
    assert github_evidence["visibility"] == "public", "GitHub evidence visibility differs"
    assert github_evidence["authenticated_login"] == "NSAdyad", "GitHub evidence account differs"
    assert github_evidence["remote_main_commit"] == head, "Remote read evidence differs from local HEAD"
    assert not github_evidence.get("mutations_performed"), "Expected a read-only GitHub evidence record"
    tracked = git_paths("ls-files", "-z")
    untracked = git_paths("ls-files", "--others", "--exclude-standard", "-z")
    changed = git_paths("diff", "--name-only", "-z")
    staged = git_paths("diff", "--cached", "--name-only", "-z")
    assert not staged, "Staged changes exist; do not silently replace another staging decision"

    scope = set(closure)
    scope.add("assets/navigation/asset-lineage.json")
    for asset in images["approved_images"].values():
        scope.update([asset["file"], asset["approval_record"], asset["appearance_reference"]])
        scope.update(asset.get("appearance_reference_hashes", {}))
        if asset.get("existing_desktop_review_reference"):
            scope.add(asset["existing_desktop_review_reference"])
    scope.update({
        "AGENTS.md",
        "docs/the-haunted-realm-development-workflow.md",
        "docs/the-haunted-realm-integrated-shell-and-cumulative-workflow.md",
        "docs/the-haunted-realm-local-integrated-shell-report-v1.md",
        "docs/the-haunted-realm-user-inspection-and-presentation-workflow.md",
        "docs/the-haunted-realm-home-presentation-correction-report-v1.md",
        "outputs/the-haunted-realm-local-integrated-shell-status.md",
        "outputs/the-haunted-realm-home-presentation-validation-candidate.md",
        "outputs/the-haunted-realm-navigation-current-design-status.md",
        "outputs/the-haunted-realm-navigation-images-approved.json",
        "outputs/the-haunted-realm-navigation-images-complete-set-approval.md",
        "outputs/the-haunted-realm-hotel-transylvania-navigation-artwork-approval.md",
        "work/local-integrated-shell-v1/test-failures.md",
        "work/local-integrated-shell-v1/test_shell.cjs",
        "work/local-integrated-shell-v1/test_supplemental.cjs",
        "work/local-integrated-shell-v1/serve_local.py",
        "work/local-integrated-shell-v1/prepare_runtime_assets.py",
        "work/local-integrated-shell-v1/audit_before.py",
        "work/local-integrated-shell-v1/audit_after.py",
        "work/local-integrated-shell-v1/before-snapshot.json",
        relative(WORK / "before-snapshot.json"),
        relative(WORK / "failure-ledger.md"),
        relative(verification_path),
        relative(github_evidence_path),
    })
    # Preserve the source algorithms, their required hash/source baselines and
    # final passed results. Re-running the complete file-preservation audit also
    # requires the original local archives intentionally excluded from deployment;
    # this is not a claim of a self-contained clean-clone/CI audit environment.
    # Do not include PNG runs or failed result runs.
    scope.update(relative(path) for pattern in ("*.py", "*.cjs") for path in WORK.glob(pattern))
    scope.update(item["path"] for item in test_records)
    audit_notes = WORK / "presentation-audit-notes.md"
    if audit_notes.is_file():
        scope.add(relative(audit_notes))
    for name in scope:
        require_exact_file(ROOT / name)
    unexpected_changes = sorted(changed - scope)
    assert not unexpected_changes, f"Tracked modifications outside reviewed scope: {unexpected_changes}"

    candidate = sorted(scope & (untracked | changed | staged))
    unchanged = sorted(scope & tracked - changed - staged)
    outputs = {relative(JSON_OUTPUT), relative(MD_OUTPUT)}
    excluded = sorted((untracked | outputs) - scope)
    manifest = {
        "status": "READY FOR CONTROLLED GITHUB DEPLOYMENT — AWAITING USER APPROVAL",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "repository": "NSAdyad/the-haunted-realm",
        "remote": remote,
        "branch": branch,
        "upstream": upstream,
        "head_before_commit": head,
        "github_read_verification": github_evidence,
        "github_read_verification_source": relative(github_evidence_path),
        "pages": {
            "source": "main / (root)",
            "evidence": "User's current explicit configuration and local infrastructure records; connector does not expose Pages settings GET. This helper performs no network requests.",
            "url": "https://nsadyad.github.io/the-haunted-realm/",
            "current_remote_main_read_verification": "VERIFIED by recorded read-only connector result; matches local HEAD",
            "new_commit_and_deployment_verification": "PENDING later explicit push approval",
        },
        "proposed_commit_message": COMMIT_MESSAGE,
        "actions_performed": ["Read project files", "Read local Git configuration/status", "Write local review inventories"],
        "actions_not_performed": ["Stage", "Commit", "Push", "Remote request", "Pages configuration change", "Deploy"],
        "test_evidence": test_records,
        "protected_count": len(actual),
        "protected_hashes": actual,
        "candidate_count": len(candidate),
        "candidate_files": [record(name, tracked, changed, staged) for name in candidate],
        "runtime_closure_count": len(closure),
        "runtime_closure": [record(name, tracked, changed, staged) for name in sorted(closure)],
        "unchanged_scope_files_already_tracked": unchanged,
        "all_existing_tracked_files_retained_count": len(tracked),
        "all_existing_tracked_files_retained": sorted(tracked),
        "excluded_untracked_count": len(excluded),
        "excluded_untracked_files": excluded,
        "exclusion_policy": "Preserve locally. No deletions, untracking or wholesale work/outputs ignores. Generated inventories are local approval artifacts, excluded to avoid self-referential hashes.",
        "git_status_porcelain": git("status", "--porcelain=v1", "--untracked-files=all"),
        "authentication": "Read-only GitHub connector authenticated as NSAdyad, per the recorded verification. This helper makes no authentication or network requests.",
        "audit_reproduction_requirements": "Source scripts and both required baseline snapshots are included. Complete file-preservation reruns require the retained original local archives; those excluded images/reviews are not deleted. Browser tests require the documented local Edge/Playwright runtime. This is not a self-contained clean-clone/CI setup.",
        "known_unresolved_non_blocking_items": [
            "Final supernatural Landing Page activity-name lettering",
            "Door to Darkness larger-scene bill/departure cue",
            "Hotel Transylvania larger Landing Page guest/interior observations",
            "Final navigation geometry pending live/device validation",
            "Physical phone/tablet/classroom projector and other browser validation",
        ],
    }
    lines = [
        "# READY FOR CONTROLLED GITHUB DEPLOYMENT — AWAITING USER APPROVAL", "",
        "This is an exact local review inventory. No staging, commit, push, deployment or Pages change occurred. This preparation helper makes no network requests; the earlier read-only GitHub evidence is recorded separately.", "",
        f"Existing repository: `{manifest['repository']}`. Branch: `{branch}`. Tracking: `{upstream}`.", "",
        f"Proposed commit: **{COMMIT_MESSAGE}**", "",
        f"Recorded read-only GitHub connector verification ({github_evidence['checked_date']}): public repository, default main, authenticated NSAdyad, remote main `{github_evidence['remote_main_commit']}` matches local HEAD. This helper makes no network requests.", "",
        "Pages source is main / (root), per the user's current explicit configuration and local records; connector Pages settings GET is unavailable. New-commit/deployment verification remains pending after explicit push approval.", "",
        f"Final test evidence: {sum(item['checks'] for item in test_records)} passing checks across {len(test_records)} result files. Protected hashes: {len(actual)}/{len(actual)} match.", "",
        f"## Exact candidate files ({len(candidate)})", "",
        "| Path | Git state | Bytes | SHA-256 |", "|---|---|---:|---|",
    ]
    lines.extend(f"| `{item['path']}` | {item['git_state']} | {item['bytes']} | `{item['sha256']}` |" for item in manifest["candidate_files"])
    lines.extend(["", f"## Existing runtime files already tracked and unchanged ({len(closure & tracked - changed - staged)})", ""])
    lines.extend(f"- `{name}`" for name in sorted(closure & tracked - changed - staged))
    lines.extend(["", f"## Exact untracked exclusions ({len(excluded)})", "", "All remain preserved locally. Existing tracked review files remain in Git; none will be deleted or untracked.", ""])
    lines.extend(f"- `{name}`" for name in excluded)
    lines.extend(["", "## Audit reproduction", "", manifest["audit_reproduction_requirements"], ""])
    lines.extend(["", "## Remaining validation", ""])
    lines.extend(f"- {item}" for item in manifest["known_unresolved_non_blocking_items"])
    lines.extend(["", "STOP. Actual commit/push requires the user's later explicit approval.", ""])
    JSON_OUTPUT.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"status": manifest["status"], "candidate_count": len(candidate), "runtime_closure_count": len(closure), "protected_count": len(actual), "excluded_untracked_count": len(excluded), "outputs": [relative(JSON_OUTPUT), relative(MD_OUTPUT)]}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
