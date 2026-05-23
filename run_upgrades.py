import subprocess
import os
import time

# Ensure we use keyring by disabling invalid GITHUB_TOKEN environment variable
if "GITHUB_TOKEN" in os.environ:
    del os.environ["GITHUB_TOKEN"]

def run_command(cmd, cwd=None):
    print(f"Running: {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if res.returncode != 0:
        print(f"Error executing: {cmd}")
        print(f"stdout: {res.stdout}")
        print(f"stderr: {res.stderr}")
        raise Exception(f"Command failed: {cmd}")
    return res.stdout

def main():
    cwd = os.getcwd()
    print(f"Starting GitHub achievements upgrade script in {cwd}...")

    # Verify gh auth
    try:
        run_command("gh auth status", cwd=cwd)
    except Exception:
        print("gh CLI not authenticated properly, or check scopes.")
        return

    # Loop 16 times to merge 16 PRs with co-authored commits
    for i in range(1, 17):
        branch = f"patch-{i}"
        filename = f"patch_{i}.txt"
        
        print(f"\n--- [Iteration {i}/16] Processing Pull Request & Co-authored Commit ---")

        # 1. Switch back to main and pull latest
        run_command("git checkout main", cwd=cwd)
        run_command("git pull origin main", cwd=cwd)

        # 2. Create new branch
        run_command(f"git checkout -b {branch}", cwd=cwd)

        # 3. Write a unique change
        with open(os.path.join(cwd, filename), "w") as f:
            f.write(f"This is achievement marker patch {i}.\nTimestamp: {time.time()}\n")

        # 4. Commit with co-author trailer
        run_command("git add .", cwd=cwd)
        commit_msg = f"Add achievement data for patch {i}"
        co_author = "Co-authored-by: Antigravity <antigravity@gemini.google.com>"
        run_command(f'git commit -m "{commit_msg}" -m "{co_author}"', cwd=cwd)

        # 5. Push branch
        run_command(f"git push -u origin {branch}", cwd=cwd)

        # 6. Create PR using gh CLI
        print("Creating Pull Request...")
        pr_cmd = f'gh pr create --title "Refactor optimization sequence #{i}" --body "Routine upgrade pipeline for achievement tracking" --head {branch} --base main'
        run_command(pr_cmd, cwd=cwd)

        # 7. Merge PR
        print("Merging Pull Request...")
        # Give GitHub a second to register the PR
        time.sleep(1)
        merge_cmd = "gh pr merge --merge --yes"
        run_command(merge_cmd, cwd=cwd)

        # 8. Clean up local branch
        run_command("git checkout main", cwd=cwd)
        run_command(f"git branch -D {branch}", cwd=cwd)
        
        # 9. Sleep a bit to prevent rate limiting
        time.sleep(2)

    print("\n=======================================================")
    print("Success! Merged 16 Pull Requests with co-authored commits.")
    print("GitHub should reflect Pull Shark Level 2 & Pair Extraordinaire Level 2 soon.")
    print("=======================================================")

if __name__ == "__main__":
    main()
