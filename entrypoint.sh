#!/bin/bash
export MYSQL_HOME=/home/frappe/frappe-bench/sites
bench --site crm.m-mines.in set-config developer_mode 0
bench --site crm.m-mines.in enable-scheduler
exec bench start
