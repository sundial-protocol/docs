import subprocess
import datetime

# Directory where the Git commands will run (assumes script is in repo root)
REPO_DIR = "."

# Log file to record sync activity and any updated files
LOG_FILE = "update_log.txt"

# Utility to run shell commands and capture output/errors
def run_cmd(cmd, cwd=REPO_DIR):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip()

# Fetch latest changes from upstream remote
def fetch_upstream():
    print(">>> Fetching upstream...")
    run_cmd("git fetch upstream")

# Get list of changed files between local HEAD and upstream main branch
def get_upstream_changes():
    out, _ = run_cmd("git diff --name-only HEAD..upstream/main")
    return [line for line in out.splitlines() if line]

# Merge upstream/main into local branch (no manual editing allowed)
def merge_upstream():
    print(">>> Merging upstream/main into local main...")
    out, err = run_cmd("git merge upstream/main --no-edit")
    print(out)
    if err:
        print(">>> Merge stderr:\n", err)

# Add, commit, and push any newly merged changes to origin/main
def commit_and_push():
    print(">>> Committing and pushing merged changes...")
    run_cmd("git add .")
    out, _ = run_cmd('git commit -m "Auto-sync: merged upstream changes"')
    if "nothing to commit" not in out.lower():
        run_cmd("git push origin main")
    else:
        print(">>> Nothing new to commit.")

# Log the result of the update (time + file list) into a text file
def log_update(changed_files):
    now = datetime.datetime.now().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(f"{now} — Upstream changes:\n")
        if changed_files:
            for file in changed_files:
                f.write(f" - {file}\n")
        else:
            f.write(" - No changes\n")
        f.write("\n")

# === Main script workflow ===
def main():
    print("=== Auto-sync with upstream (no render) ===")
    fetch_upstream()

    # Step 1: Capture current HEAD to later compare if anything changed
    old_head, _ = run_cmd("git rev-parse HEAD")

    # Step 2: Check if there are any upstream changes
    changed_files = get_upstream_changes()
    if not changed_files:
        print(">>> No upstream changes found.")
        log_update([])
        return

    print(">>> Upstream updates detected:")
    for f in changed_files:
        print(f" - {f}")

    # Step 3: Merge updates into local branch
    merge_upstream()

    # Step 4: Identify actual file changes after merge by comparing commit hashes
    new_files_raw, _ = run_cmd(f"git diff --name-only {old_head} HEAD")
    new_files = [f for f in new_files_raw.splitlines() if f]

    if new_files:
        print(">>> Incoming files changed during merge:")
        for f in new_files:
            print(f" - {f}")
    else:
        print(">>> Merge completed but no actual changes.")

    # Step 5: Commit and push if necessary
    commit_and_push()

    # Step 6: Log update details
    log_update(new_files)

# Entry point for standalone execution
if __name__ == "__main__":
    main()
