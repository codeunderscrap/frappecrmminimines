import frappe

frappe.init(site="crm.m-mines.in", sites_path="/home/frappe/frappe-bench/sites")
frappe.connect()

orgs = [
    {"doctype": "CRM Organization", "organization_name": "Tata Steel Recycling Division"},
    {"doctype": "CRM Organization", "organization_name": "Amaron Batteries (Amara Raja)"},
    {"doctype": "CRM Organization", "organization_name": "Hindalco Industries Ltd"}
]

created_org_map = {}
for o in orgs:
    existing = frappe.db.get_value("CRM Organization", {"organization_name": o["organization_name"]})
    if not existing:
        doc = frappe.get_doc(o)
        doc.insert(ignore_permissions=True)
        created_org_map[o["organization_name"]] = doc.name
        print("Created Organization:", o["organization_name"], "->", doc.name)
    else:
        created_org_map[o["organization_name"]] = existing

deals = [
    {
        "doctype": "CRM Deal",
        "organization": created_org_map["Tata Steel Recycling Division"],
        "material_category": "Copper Cathode",
        "deal_volume_mt": 150.0,
        "proposed_rate_per_mt": 820000.0,
        "annual_revenue": 123000000.0,
        "margin_status": "Approved"
    },
    {
        "doctype": "CRM Deal",
        "organization": created_org_map["Amaron Batteries (Amara Raja)"],
        "material_category": "Lead Battery Scrap",
        "deal_volume_mt": 250.0,
        "proposed_rate_per_mt": 178000.0,
        "annual_revenue": 44500000.0,
        "margin_status": "Pending HOD Approval"
    }
]

for d in deals:
    if not frappe.db.exists("CRM Deal", {"organization": d["organization"]}):
        doc = frappe.get_doc(d)
        doc.insert(ignore_permissions=True)
        print("Created Deal for:", d["organization"])

frappe.db.commit()
print("Deals and Orgs successfully populated!")
