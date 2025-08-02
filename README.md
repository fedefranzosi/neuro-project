# Neuro Project

This project demonstrates a simple Dockerized Flask application with a MySQL
backend for storing patient information from a web form. The form collects
details such as name, DNI, health insurance, dates of admission and symptom
onset, and more. Bootstrap is used for styling so it looks polished, similar to
a Google form. The form supports searching Human Phenotype Ontology (HPO)
terms via the public OLS API and saves selected phenotypes in a related table.

## Quick start

1. Install Docker with Docker Compose plugin.
2. Run `docker compose up --build`.
3. Visit `http://localhost:5000` to access the form.

The database schema is recreated each time the stack starts, so any previously
stored data will be cleared.
