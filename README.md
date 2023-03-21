
<h1>Student Management API</h1>


<p>This is a RESTful API for managing student data. It allows you to create, read, update, and delete student records. The API is built with Python and Flask, and uses a PostgreSQL database to store student data.</p>
    <h2>Installation</h2>
     <ol>
      <li>Clone the repository to your local machine.</li>
      <li>Create a virtual environment and activate it.</li>
      <li>Install the required packages using <code>pip install -r requirements.txt</code>.</li>
      <li>Set the app  by running <code>set FLASK_APP=API </code> for windows and <code> export FLASK_APP=API</code> for MAC or linux.</li>
      <li>Set up the database by running <code>flask shell </code> in the terminal.</li>
      <li>Start the server by running <code>runserver.py </code>.</li>
    </ol>


<h2>Usage</h2>
    <p>The API provides the following endpoints:</p>
    <ul>
      <li><code>POST /auth/login</code>: roue for login .</li>
      <li><code>POST /auth/signup</code>: roue for signup .</li>
       e.t.c
    </ul>
   


<p>To use the API, send HTTP requests to the appropriate endpoints using a tool like <code>Insomnia</code> or <code>Postman</code>. The API returns responses in JSON format.</p>
    <h2>Authentication</h2>
    <p>The API requires authentication to access any of the endpoints. To authenticate, send a POST request to the <code>/auth</code> endpoint with your credentials in the request body. You will receive a JWT token in the response, which you can use to access the other endpoints.</p>
    <h2>Security</h2>
    <p>The API uses JWT tokens for authentication and authorization. All requests to the API must include a valid JWT token in the <code>Authorization</code> header. The API also uses Flask-SQLAlchemy to protect against SQL injection attacks.</p>
    <h2>MAIN USAGE</h2>
    <P> This API can be used majorly for rgistering courses, students and taking their grade and in return gives the performance of student by returning the cgpa of requested student</p>
