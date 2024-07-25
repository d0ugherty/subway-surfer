# Train Information
![traininfo](https://github.com/user-attachments/assets/15c8942c-7154-4c66-a771-1efcece8b2e1)

# Next to Arrive
![Screenshot from 2024-07-25 12-18-28](https://github.com/user-attachments/assets/cb26cc8c-1f30-4d9c-963f-c53c193d3a11)




# What is this?

A passenger information system built using the Django web framework. 

So far it includes train information boards, real-time locations, and fare calculation.

Services: SEPTA Regional Rail, SEPTA Subway-Surface Trolleys, and NJ Transit Commuter Rail*.

I would like to extend this to other agencies with available data.

*Real-time data for NJ Transit is currently unavailable so static GTFS data is used.

# Why?

About a year and a half ago, I started a similar project using vanilla JS, HTML, and CSS. I really didn't know what I was doing when it came to setting up a database and ended up over engineering the whole thing. I built out C# models and controllers for the backend so I could use the GTFS data which I stored in a SQL database. I learned a lot, but it made the project bigger than it had to be and the relational database wasn't very...well, relational.

After learning about Django, it seemed like an appropriate set of tools to build this with. Outside of school, this would be my first time using any sort of framework. 

# How does it work?

This uses SEPTA's REST API for real-time information. For static information, it uses GTFS data stored in a SQLite database.

Since this is a transactional application (send request, retrieve objects, process the data, and render it), it uses the Django ORM for querying against the database. The queries are relatively simple so raw SQL doesn't seem necessary. However, I have been using SQL for troubleshooting inside the database.

