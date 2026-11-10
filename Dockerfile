FROM frappe/bench:latest

USER frappe
WORKDIR /home/frappe

# Initialize frappe-bench with Frappe v15 and CRM v15 stable branch
RUN bench init --skip-redis-config-generation --frappe-branch version-15 --python python3.11 frappe-bench \
    && cd frappe-bench \
    && bench get-app --branch version-15 --resolve-deps crm

WORKDIR /home/frappe/frappe-bench

EXPOSE 8000
CMD ["bench", "start"]
