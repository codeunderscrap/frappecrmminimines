import json, os, glob

assets_file = "/home/frappe/frappe-bench/sites/assets/assets.json"
css_dir = "/home/frappe/frappe-bench/sites/assets/frappe/dist/css/"

with open(assets_file, "r") as f:
    data = json.load(f)

# Update website.bundle.css
website_files = [f for f in os.listdir(css_dir) if f.startswith("website.bundle.") and f.endswith(".css") and not f.endswith(".map")]
if website_files:
    latest = max(website_files, key=lambda x: os.path.getmtime(os.path.join(css_dir, x)))
    data["website.bundle.css"] = "/assets/frappe/dist/css/" + latest
    print("Mapped website.bundle.css ->", latest)

# Update login.bundle.css
login_files = [f for f in os.listdir(css_dir) if f.startswith("login.bundle.") and f.endswith(".css") and not f.endswith(".map")]
if login_files:
    latest = max(login_files, key=lambda x: os.path.getmtime(os.path.join(css_dir, x)))
    data["login.bundle.css"] = "/assets/frappe/dist/css/" + latest
    print("Mapped login.bundle.css ->", latest)

# Update desk.bundle.css
desk_files = [f for f in os.listdir(css_dir) if f.startswith("desk.bundle.") and f.endswith(".css") and not f.endswith(".map")]
if desk_files:
    latest = max(desk_files, key=lambda x: os.path.getmtime(os.path.join(css_dir, x)))
    data["desk.bundle.css"] = "/assets/frappe/dist/css/" + latest
    print("Mapped desk.bundle.css ->", latest)

with open(assets_file, "w") as f:
    json.dump(data, f, indent=2)

print("assets.json updated successfully!")
