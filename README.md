## Pagination in Python

### Introduction
This exercice was part of coursework in Data Engineering Bootcamp from Nashville Software School. The purpose of this exercise is to learn how to access data from an API using pagination in Python. 

### Part 1
Using a sample API, I request a token and authenticate to the API. 

### Part 2
By adding a query string params `offset` and `limit` to the call, I obtain a subset of the results back. 

### Part 3
Once I read data from the API using Python, I save the data to a `.json` file 10 records at a time. I perform line my line string formatting and concatenation to obtain a valid `.json`.

### Part 4 
Finaly, I reformat to write to a `.csv` file still holding only 10 records at a time in memory. The `.csv` is formatted in tabular form. Each column values are stored in double quotes `" "` to prevent ambiguation from `,` within values.
