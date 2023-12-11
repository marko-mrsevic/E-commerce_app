# Django E-commerce App
This Django E-commerce app is a scalable and feature-rich web application that provides a robust platform for online transactions. It incorporates a REST API, user authentication, cart functionality, and secure payment processing using the Stripe payment gateway. The entire application is containerized using Docker, ensuring seamless deployment and scalability.

Technologies Used:

    Python, Django, Django Rest Framework, PostgreSQL, Stripe, Docker

## Installation

Create a .env file in the project root directory and specify the following environment variables:
```.env
POSTGRES_DB=database_name
POSTGRES_USER=username
POSTGRES_PASSWORD=password
POSTGRES_HOST=host
POSTGRES_PORT=5432
```
Run the following command to build Docker images and start containers:
```bash
docker-compose up --build
```
Execute the following command to apply database migrations:
```bash
docker-compose exec web python manage.py migrate
```
## Usage
Once the containers are up and migrations are applied, the Django E-commerce app will be accessible at http://localhost:8000. Explore the API endpoints for user authentication, cart management, and secure payment processing.

## Contributing

Contributions are welcome! Feel free to submit issues, feature requests, or pull requests.

Please make sure to update tests as appropriate.