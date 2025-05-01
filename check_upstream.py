import subprocess
import datetime
import os

REPO_DIR = "."  # Current directory
RENDER_SCRIPT = "convert_tex_to_rst.py"  # Update if your render script has a different name
LOG_FILE = "update_log.txt"

def run_cmd(cmd, cwd=REPO_DIR):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip()

def fetch_upstream():
    run_cmd("git fetch upstream")

def get_incoming_changes():
    out, _ = run_cmd("git diff --name-only HEAD..upstream/main")
    return [line for line in out.splitlines() if line]

def merge_upstream():
    run_cmd("git merge upstream/main --no-edit")

def render_docs():
    print(">>> Rendering docs...")
    out, err = run_cmd(f"python {RENDER_SCRIPT}")
    if err:
        print(">>> Render script errors:\n", err)
    else:
        print(">>> Render script complete.")

def commit_and_push():
    run_cmd("git add .")
    out, err = run_cmd('git commit -m "Auto-sync: merged upstream changes and re-rendered docs"')
    if "nothing to commit" not in out.lower():
        print(">>> Committing and pushing changes...")
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
    print("=== Checking for upstream updates ===")
    fetch_upstream()
    changed_files = get_incoming_changes()

    if changed_files:
        print(">>> Incoming changes found:")
        for f in changed_files:
            print(f" - {f}")
        merge_upstream()
        render_docs()
        commit_and_push()
    else:
        print(">>> No upstream changes detected.")

    log_update(changed_files)

if __name__ == "__main__":
    main()
