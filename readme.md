Pizzeria App
This is a simple Django-based application for a pizzeria that allows customers to create pizza orders with various options, including pizza base, cheese, and toppings. The application also provides order tracking functionality that automatically updates the order status based on the elapsed time.

Setup
Before running the application, you'll need to set up a PostgreSQL database using Docker and install the required dependencies.

Database Setup
We use PostgreSQL as the database for this application. You can set up the database using Docker and the provided docker-compose.yml and init.sql files.

Make sure you have Docker installed on your system.

Navigate to the project directory.

Run the following command to start the PostgreSQL container:
docker-compose up -d
pip install -r requirements.txt



API Endpoints
Add Pizza to Order
Endpoint: /orderpizza/
HTTP Method: POST
Description: Allows a customer to add a pizza to their order by providing details such as the pizza base, cheese, and toppings.
Request Body:
base: ID of the pizza base.
cheese: ID of the cheese.
toppings: List of IDs of selected toppings.
Response: Returns a JSON response with a message indicating whether the pizza was successfully added to the order and the order ID.
Track Order Status
Endpoint: /trackOrderStatus/<int:order_id>/
HTTP Method: GET
Description: Allows customers to track the status of their order based on the order ID.
Response: Returns a JSON response with the order ID and the current status of the order.
Asynchronous Order Status Updates
The application uses Celery for asynchronous task processing to update the order status based on time. The task is defined in tasks.py, and it runs at regular intervals to change the order status as follows:

In the first minute after the order is placed, the status changes from 'Placed' to 'Accepted.'
After 1 minute, the status changes from 'Accepted' to 'Preparing.'
After 3 minutes, the status changes from 'Preparing' to 'Dispatched.'
After 5 minutes, the status reads 'Delivered.'
Docker Containerization
The application and database are containerized using Docker for easy deployment. You can use the provided Dockerfile and docker-compose.yml files to create and run the containers.

Sample Data
The init.sql file contains sample data for pizza bases, cheese, and toppings. You can modify this data as needed for your pizzeria.

Notes
This is a simplified example of a pizzeria application, and it can be extended and customized to meet your specific requirements. Tests have not been included in this README, but they are recommended for ensuring the reliability of the application.

Feel free to reach out if you have any questions or need further assistance with the application. Enjoy your pizza ordering and tracking experience!