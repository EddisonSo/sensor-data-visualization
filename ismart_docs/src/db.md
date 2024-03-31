## ORM
ORM was chosen to be used in this project due to the relatively simple queries that will be done and the simplistic nature of utilizing an ORM to objectify retrieved queries from the DB.

We first define our models within the differnet domains (Sensor, SensorData).

Then manipulating the differnet objects is as simple as querying the database by an object's id, modifying the retrieved object and commiting the changes back to the database.

## Sessions
Sessions allow us to manage transaction to ensure that multiple writers do not cause inconsistencies within the database. For more detail regarding this probem, online sources on readers-writers can give more insight on common issues concurrent applications encounter. 

We utilize session to ensure atomic transactions. That is, a group of operations on a single object is guaranteed to be completed altogether.

This is one of the advantages of utilizing PostgreSQL over other databases such as MongoDB that focuses more on eventual consistency over strong consistency.
