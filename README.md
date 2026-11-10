# MiniMines Frappe CRM (`crm.m-mines.in`)

Production repository for MiniMines CRM deployment on Hostinger KVM VPS, integrated with Coolify / Traefik reverse proxy.

## Architecture & Features
- **Frontend & App:** Frappe CRM v15 (Vue 3, Tailwind CSS, Frappe UI)
- **Backend:** Frappe Framework v15 (Python 3.11, MariaDB 10.6, Redis 7)
- **Reverse Proxy:** Coolify Traefik with automated Let's Encrypt SSL (`https://crm.m-mines.in`)
- **Isolation:** Resource-capped Docker Compose stack (< 1.2 GB total RAM footprint)

## Repository Structure
```
├── docker-compose.yml          # Production Docker Compose definition
├── Dockerfile                  # Frappe Bench + CRM v15 image build definition
├── entrypoint.sh               # Container startup script (scheduler & web server)
├── init_site.sh                # Initial site bootstrap script
├── traefik/
│   └── crm-minimines.yaml      # Traefik dynamic router config for crm.m-mines.in
└── scripts/
    ├── setup_minimines_crm.py  # Custom fields (Material Category, Volume MT, LME links) & DocTypes
    ├── seed_orgs.py            # Sample B2B Organizations and active Pipeline Deals
    ├── create_team.py          # Role-based team user provisioner (HOD, Manager, Associate)
    └── sync_assets.py          # Static asset bundle hash synchronizer (prevents FOUC)
```

## Quick Start on VPS
```bash
# Clone repository
git clone https://github.com/codeunderscrap/frappecrmminimines.git /root/internal-tools/frappe-crm
cd /root/internal-tools/frappe-crm

# Start services
docker compose up -d

# Initialize site & custom MiniMines schemas
bash init_site.sh
```
