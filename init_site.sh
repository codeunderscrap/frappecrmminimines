#!/bin/bash
export MYSQL_HOME=/home/frappe/frappe-bench/sites
bench new-site crm.minimines.com     --db-name crm_minimines     --db-password mm_crm_user_sec2026     --db-root-password mm_crm_root_db_sec2026     --db-host crm-db     --admin-password Admin@MiniMines2026     --install-app crm     --force
