"""Generate redirects for agent-platform → agents rename and insert into vercel.json."""
import json
import os

agents_dir = "src/content/docs/agents"
redirects = []

for root, dirs, files in os.walk(agents_dir):
    for f in files:
        if not f.endswith(".mdx"):
            continue
        path = os.path.join(root, f)
        rel = os.path.relpath(path, agents_dir)
        slug = rel.replace("/index.mdx", "").replace(".mdx", "")
        if slug == "index":
            old_url = "/agent-platform/"
            new_url = "/agents/"
        else:
            old_url = f"/agent-platform/{slug}/"
            new_url = f"/agents/{slug}/"
        redirects.append({"source": old_url, "destination": new_url, "statusCode": 308})

redirects.sort(key=lambda r: r["source"])
print(f"Generated {len(redirects)} redirects")

with open("vercel.json", "r") as fh:
    data = json.load(fh)

existing_sources = {r["source"] for r in data.get("redirects", [])}
new_redirects = [r for r in redirects if r["source"] not in existing_sources]
skipped = len(redirects) - len(new_redirects)
print(f"{len(new_redirects)} new redirects to add (skipping {skipped} duplicates)")

data["redirects"] = new_redirects + data["redirects"]

with open("vercel.json", "w") as fh:
    json.dump(data, fh, indent=2)
print("vercel.json updated")
