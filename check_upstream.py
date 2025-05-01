import subprocess
import datetime

REPO_DIR = "."
LOG_FILE = "update_log.txt"

def run_cmd(cmd, cwd=REPO_DIR):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip()

def fetch_upstream():
    print(">>> Fetching upstream...")
    run_cmd("git fetch upstream")

def get_upstream_changes():
    out, _ = run_cmd("git diff --name-only HEAD..upstream/main")
    return [line for line in out.splitlines() if line]

def merge_upstream():
    print(">>> Merging upstream/main into local main...")
    out, err = run_cmd("git merge upstream/main --no-edit")
    print(out)
    if err:
        print(">>> Merge stderr:\n", err)

def commit_and_push():
    print(">>> Committing and pushing merged changes...")
    run_cmd("git add .")
    out, _ = run_cmd('git commit -m "Auto-sync: merged upstream changes"')
    if "nothing to commit" not in out.lower():
        run_cmd("git push origin main")
    else:
        print(">>> Nothing new to commit.")

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

def main():
    print("=== Auto-sync with upstream (no render) ===")
    fetch_upstream()
    changed_files = get_upstream_changes()

    if changed_files:
        print(">>> Upstream updates detected:")
        for f in changed_files:
            print(f" - {f}")
        merge_upstream()
        commit_and_push()
    else:
        print(">>> No upstream changes found.")

    log_update(changed_files)

if __name__ == "__main__":
    main()
