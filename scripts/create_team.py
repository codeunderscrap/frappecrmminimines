import frappe

frappe.init(site="crm.m-mines.in", sites_path="/home/frappe/frappe-bench/sites")
frappe.connect()

users = [
    {
        "email": "itadmin@m-mines.com",
        "first_name": "IT",
        "last_name": "Admin",
        "roles": ["System Manager", "CRM Manager", "Sales Manager"]
    },
    {
        "email": "itassociate@m-mines.com",
        "first_name": "IT",
        "last_name": "Associate",
        "roles": ["CRM User", "Sales User"]
    },
    {
        "email": "spokeops@m-mines.com",
        "first_name": "Spoke",
        "last_name": "Operations",
        "roles": ["CRM User", "Sales User"]
    }
]

for u in users:
    if not frappe.db.exists("User", u["email"]):
        doc = frappe.get_doc({
            "doctype": "User",
            "email": u["email"],
            "first_name": u["first_name"],
            "last_name": u["last_name"],
            "enabled": 1,
            "send_welcome_email": 0
        })
        doc.insert(ignore_permissions=True)
        # set default temporary password
        from frappe.utils.password import update_password
        update_password(u["email"], "MiniMines@2026")
        
        for r in u["roles"]:
            if frappe.db.exists("Role", r):
                doc.add_roles(r)
        print(f"Created user: {u['email']} (Password: MiniMines@2026)")
    else:
        print(f"User {u['email']} already exists.")

frappe.db.commit()
print("All team users successfully registered with login access!")
