import os, base64, json, subprocess

OWNER = "chenyang0301"
REPO = "shuyanzhitu"
ROOT = r"C:/Users/10710/WorkBuddy/2026-08-13-15-17-40/website"

EXCLUDE_DIRS = {".git", "_cesium_dl"}
EXCLUDE_FILES = {"upload.py", "set_domain.py", "payload.json", "_gh_payload.json"}
# npm-only entry points, not needed for browser build
SKIP_REL = {"cesium/index.cjs", "cesium/index.js"}

def gh(method, path, body=None):
    cmd = ["gh", "api", path]
    if method != "GET":
        cmd += ["-X", method]
    inp = None
    if body is not None:
        inp = json.dumps(body).encode()
        cmd += ["--input", "-"]
    p = subprocess.run(cmd, input=inp, capture_output=True, timeout=90)
    if p.returncode != 0:
        raise RuntimeError(f"{method} {path} -> {p.stderr.decode()[:400]}")
    out = p.stdout.decode()
    return json.loads(out) if out.strip() else {}

# 1) collect files
files = []
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in EXCLUDE_DIRS]
    for f in fn:
        full = os.path.join(dp, f)
        rel = os.path.relpath(full, ROOT).replace("\\", "/")
        if rel in EXCLUDE_FILES or rel in SKIP_REL:
            continue
        files.append((rel, full))

print(f"collected {len(files)} files", flush=True)

# 2) create blobs
tree_entries = []
failed = []
for i, (rel, full) in enumerate(files):
    with open(full, "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode()
    try:
        r = gh("POST", f"/repos/{OWNER}/{REPO}/git/blobs",
               {"content": b64, "encoding": "base64"})
        tree_entries.append({"path": rel, "mode": "100644",
                             "type": "blob", "sha": r["sha"]})
        if i % 20 == 0:
            print(f"blob {i}/{len(files)} ok", flush=True)
    except Exception as e:
        failed.append((rel, str(e)[:120]))
        print("BLOB FAIL", rel, str(e)[:200], flush=True)

print(f"blobs ok={len(tree_entries)} failed={len(failed)}")

# 3) base tree from current main
ref = gh("GET", f"/repos/{OWNER}/{REPO}/git/refs/heads/main")
base_sha = ref["object"]["sha"]
base_commit = gh("GET", f"/repos/{OWNER}/{REPO}/git/commits/{base_sha}")
base_tree = base_commit["tree"]["sha"]

# 4) create tree
tree = gh("POST", f"/repos/{OWNER}/{REPO}/git/trees",
          {"base_tree": base_tree, "tree": tree_entries})
tree_sha = tree["sha"]

# 5) create commit
commit = gh("POST", f"/repos/{OWNER}/{REPO}/git/commits",
            {"message": "self-host Cesium+Leaflet, switch to Tianditu basemaps (remove foreign CDNs)",
             "tree": tree_sha, "parents": [base_sha]})
commit_sha = commit["sha"]

# 6) update ref
gh("PATCH", f"/repos/{OWNER}/{REPO}/git/refs/heads/main", {"sha": commit_sha})
print("COMMIT_PUSHED", commit_sha)
if failed:
    print("FAILED_FILES:", failed)
print("DONE")
