# PythonWeatherApp
Weather App

This application was written in Python while utilizing S3 Buckets, DynamoDB SQL.

User is prompted to select a destination to retrieve current/live weather updates through weather API.
Application is CLI-based and returns all weather information including a photo of the destination that is stored in AWS database.
Each time a user pulls data, it is logged in the database by user, what information was pulled and timestamp of retrieval
