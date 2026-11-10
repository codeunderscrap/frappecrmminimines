import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def setup_minimines():
    frappe.init(site="crm.m-mines.in", sites_path="/home/frappe/frappe-bench/sites")
    frappe.connect()
    print("Connected to Frappe database successfully.")

    # 1. Custom Fields for CRM Lead & CRM Deal
    custom_fields = {
        "CRM Lead": [
            {
                "fieldname": "material_category",
                "label": "Material Category",
                "fieldtype": "Select",
                "options": "\nBattery Scrap\nBlack Mass\nCopper Cathode\nAluminium Ingot\nLead Battery Scrap\nMixed E-Waste\nOther",
                "insert_after": "organization",
                "reqd": 0,
                "in_list_view": 1,
                "in_standard_filter": 1,
            },
            {
                "fieldname": "est_volume_mt",
                "label": "Estimated Volume (MT)",
                "fieldtype": "Float",
                "insert_after": "material_category",
                "in_list_view": 1,
            },
            {
                "fieldname": "lead_segment",
                "label": "Lead Segment",
                "fieldtype": "Select",
                "options": "\nRecycling & Smelting\nDirect Battery Manufacturer\nTrading & Aggregation\nExport & International",
                "insert_after": "est_volume_mt",
                "in_standard_filter": 1,
            },
            {
                "fieldname": "origin_city",
                "label": "City / Location",
                "fieldtype": "Data",
                "insert_after": "lead_segment",
            },
            {
                "fieldname": "assigned_manager",
                "label": "Reporting Manager",
                "fieldtype": "Link",
                "options": "User",
                "insert_after": "lead_owner",
            }
        ],
        "CRM Deal": [
            {
                "fieldname": "material_category",
                "label": "Material Category",
                "fieldtype": "Select",
                "options": "\nBattery Scrap\nBlack Mass\nCopper Cathode\nAluminium Ingot\nLead Battery Scrap\nMixed E-Waste\nOther",
                "insert_after": "organization",
                "in_list_view": 1,
                "in_standard_filter": 1,
            },
            {
                "fieldname": "deal_volume_mt",
                "label": "Deal Volume (MT)",
                "fieldtype": "Float",
                "insert_after": "material_category",
                "in_list_view": 1,
            },
            {
                "fieldname": "proposed_rate_per_mt",
                "label": "Proposed Rate (INR / MT)",
                "fieldtype": "Currency",
                "insert_after": "deal_volume_mt",
            },
            {
                "fieldname": "lme_reference_rate",
                "label": "Linked LME Rate (USD/MT)",
                "fieldtype": "Currency",
                "insert_after": "proposed_rate_per_mt",
            },
            {
                "fieldname": "margin_status",
                "label": "Margin Approval Status",
                "fieldtype": "Select",
                "options": "Draft\nPending HOD Approval\nApproved\nRejected",
                "default": "Draft",
                "insert_after": "lme_reference_rate",
                "in_list_view": 1,
                "in_standard_filter": 1,
            },
            {
                "fieldname": "cloud_erp_sales_order",
                "label": "Cloud ERP Sales Order #",
                "fieldtype": "Data",
                "read_only": 1,
                "insert_after": "margin_status",
            }
        ]
    }

    create_custom_fields(custom_fields, update=True)
    print("Custom fields successfully injected into CRM Lead and CRM Deal.")

    # 2. Create Custom DocType: LME Rate Tracker (using Core module)
    if not frappe.db.exists("DocType", "LME Rate Tracker"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "LME Rate Tracker",
            "module": "Custom",
            "custom": 1,
            "naming_rule": "By fieldname",
            "autoname": "field:metal_symbol",
            "fields": [
                {"fieldname": "metal_name", "label": "Metal Name", "fieldtype": "Data", "reqd": 1, "in_list_view": 1},
                {"fieldname": "metal_symbol", "label": "Metal / Scrap Symbol", "fieldtype": "Data", "reqd": 1, "in_list_view": 1, "unique": 1},
                {"fieldname": "rate_usd_mt", "label": "LME Rate (USD / MT)", "fieldtype": "Currency", "reqd": 1, "in_list_view": 1},
                {"fieldname": "rate_inr_mt", "label": "Effective Rate (INR / MT)", "fieldtype": "Currency", "reqd": 1, "in_list_view": 1},
                {"fieldname": "floor_margin_percent", "label": "Floor Margin (%)", "fieldtype": "Percent", "default": "12.00"},
                {"fieldname": "last_updated", "label": "Last Updated", "fieldtype": "Datetime", "in_list_view": 1}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "All", "read": 1}
            ]
        })
        doc.insert()
        print("DocType 'LME Rate Tracker' created in Custom module.")
    else:
        print("DocType 'LME Rate Tracker' already exists.")

    # 3. Seed Base LME Metals Data
    metals = [
        {"metal_name": "Copper LME Cash", "metal_symbol": "CU-CASH", "rate_usd_mt": 9650.0, "rate_inr_mt": 820000.0, "floor_margin_percent": 12.0},
        {"metal_name": "Aluminium LME Cash", "metal_symbol": "AL-CASH", "rate_usd_mt": 2620.0, "rate_inr_mt": 225000.0, "floor_margin_percent": 10.0},
        {"metal_name": "Lead LME Cash", "metal_symbol": "PB-CASH", "rate_usd_mt": 2080.0, "rate_inr_mt": 178000.0, "floor_margin_percent": 15.0},
        {"metal_name": "Black Mass Premium Grade", "metal_symbol": "BM-PREM", "rate_usd_mt": 4800.0, "rate_inr_mt": 410000.0, "floor_margin_percent": 18.0},
        {"metal_name": "Lithium Battery Scrap", "metal_symbol": "LIB-SCRAP", "rate_usd_mt": 3200.0, "rate_inr_mt": 275000.0, "floor_margin_percent": 14.0}
    ]

    for m in metals:
        if not frappe.db.exists("LME Rate Tracker", m["metal_symbol"]):
            doc = frappe.get_doc({"doctype": "LME Rate Tracker", **m, "last_updated": frappe.utils.now()})
            doc.insert()
            print(f"Seeded LME metal: {m['metal_symbol']}")

    # 4. Seed Demo Sample Leads from Twenty
    demo_leads = [
        {
            "doctype": "CRM Lead",
            "first_name": "Vikram",
            "last_name": "Malhotra",
            "organization": "Tata Steel Recycling Division",
            "email": "v.malhotra@tatasteel.com",
            "mobile_no": "+91 98201 12345",
            "material_category": "Copper Cathode",
            "est_volume_mt": 150.0,
            "lead_segment": "Recycling & Smelting",
            "origin_city": "Jamshedpur"
        },
        {
            "doctype": "CRM Lead",
            "first_name": "Siddharth",
            "last_name": "Reddy",
            "organization": "Amaron Batteries (Amara Raja)",
            "email": "siddharth.r@amararaja.com",
            "mobile_no": "+91 98490 67890",
            "material_category": "Lead Battery Scrap",
            "est_volume_mt": 250.0,
            "lead_segment": "Direct Battery Manufacturer",
            "origin_city": "Tirupati"
        },
        {
            "doctype": "CRM Lead",
            "first_name": "Arjun",
            "last_name": "Mehta",
            "organization": "Hindalco Industries Ltd",
            "email": "arjun.mehta@adityabirla.com",
            "mobile_no": "+91 98112 34567",
            "material_category": "Aluminium Ingot",
            "est_volume_mt": 80.0,
            "lead_segment": "Recycling & Smelting",
            "origin_city": "Mumbai"
        }
    ]

    for l in demo_leads:
        if not frappe.db.exists("CRM Lead", {"email": l["email"]}):
            doc = frappe.get_doc(l)
            doc.insert(ignore_permissions=True)
            print(f"Seeded Lead: {l['first_name']} {l['last_name']} ({l['organization']})")

    # 5. Seed Sample Active Deals (Kanban Pipeline)
    demo_deals = [
        {
            "doctype": "CRM Deal",
            "name": "Tata Steel - Q4 Copper Cathode Procurement",
            "organization": "Tata Steel Recycling Division",
            "material_category": "Copper Cathode",
            "deal_volume_mt": 150.0,
            "proposed_rate_per_mt": 820000.0,
            "annual_revenue": 123000000.0,
            "margin_status": "Approved",
            "status": "Negotiation"
        },
        {
            "doctype": "CRM Deal",
            "name": "Amaron Batteries - Monthly Lead Battery Scrap Supply",
            "organization": "Amaron Batteries (Amara Raja)",
            "material_category": "Lead Battery Scrap",
            "deal_volume_mt": 250.0,
            "proposed_rate_per_mt": 178000.0,
            "annual_revenue": 44500000.0,
            "margin_status": "Pending HOD Approval",
            "status": "Qualified"
        }
    ]

    for d in demo_deals:
        if not frappe.db.exists("CRM Deal", {"organization": d["organization"]}):
            try:
                doc = frappe.get_doc(d)
                doc.insert(ignore_permissions=True)
                print(f"Seeded Deal: {d['name']}")
            except Exception as e:
                print(f"Deal note: {e}")

    frappe.db.commit()
    print("ALL MINIMINES PIPELINE SCHEMAS & DATA SUCCESSFULLY APPLIED!")

if __name__ == "__main__":
    setup_minimines()
