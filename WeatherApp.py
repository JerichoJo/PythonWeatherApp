import boto3
import requests
from datetime import datetime
import sys
import time

client = boto3.resource('dynamodb')


def menu():
    print("\n*** Welcome to the top city weather application ***\n\n",
          "Please enter a selection of the following cities:\n",
          "1) London, UK\n",
          "2) Paris, FR\n",
          "3) New York City, NY\n",
          "4) Moscow, RU\n",
          "5) Dubai, UAE\n",
          "6) Tokyo, JP\n",
          "7) To exit Program"
        )
    user_location = input("\nYour Selection: ")
        
    # IF statements guiding input for API output and input validation
    if user_location == "1":
        user_location = "London"
    elif user_location == "2":
        user_location = "Paris"
    elif user_location =="3":
        user_location = "New York City"
    elif user_location == "4":
        user_location = "Moscow"
    elif user_location == "5":
        user_location = "Dubai"
    elif user_location == "6":
        user_location = "Tokyo"
    elif user_location == "7":
        print("\nThank you for using the top city weather application!\n",
                  "Goodbye!"
                )
        sys.exit(0)
    else:
        print("\nPlease enter a valid response")
        menu()
        
    pull_photo(user_location)
    run(user_location)
            

def pull_photo(user_location):
    # Re-formatting string for proper filepath
    formatted_user_selection = user_location.lower() + ".jpg"
    # Bucket name and file names
    BUCKET_NAME = 'cityphotos'
    BUCKET_FILE_NAME = formatted_user_selection
    LOCAL_FILE_NAME = formatted_user_selection
    # Assigning boto3 client and bucket to download file
    s3 = boto3.client('s3')
    s3.download_file(BUCKET_NAME, BUCKET_FILE_NAME, LOCAL_FILE_NAME)
    # Output for successful download
    print("\n",formatted_user_selection, "has been downloaded!\n")
    

def put_weather_data(user_location, temperature, feel_like_temperature, humidity_level, weather_status, wind_status, date_and_time):
    # Verifying Database
    dynamodb = boto3.resource('dynamodb')
    # Assigning table to table variable for put-items
    table = dynamodb.Table("StoringWeatherData")
    response = table.put_item(
        # Item properties to put
        Item={
            'City': user_location,
            'Temperature': str(temperature),
            'Feels-Like': str(feel_like_temperature),
            'Humidity': humidity_level,
            'Weather': weather_status,
            'Wind': str(wind_status),
            'Date-Time': date_and_time
        }
        )
    # Confirmation of successful backup
    print(" \n* This search has been automatically backed up into the DynamoDB table. *\n")
    
    
def run(user_location):
    # variables storing API and user input
    api_key = '318cb6c74953673955580b7a077462d7'
    
    # Full link to API
    full_api = "http://api.openweathermap.org/data/2.5/weather?q=" + user_location + "&units=imperial" + "&appid=" + api_key
        
    # Pull request for API key
    link_to_api = requests.get(full_api)
        
    # Storing API pull results
    request_results = link_to_api.json()
        
    # IF statement validating user input and handling 404 error
    if request_results['cod'] == '404':
        print("You have entered an invalid location: {}, Enter a valid city.".format(user_location))
    else:
        # Assigning variables for weather status pulled from JSON
        temperature = (request_results['main']['temp'])
        feel_like_temperature = (request_results['main']['feels_like'])
        humidity_level = request_results['main']['humidity']
        weather_status = request_results['weather'][0]['description']
        wind_status = request_results['wind']['speed']
        date_and_time = datetime.now().strftime("%d %b %y | %I:%M%S %p")
        # Output weather results
        print("Weather Status for {} at {}".format(user_location.upper(), date_and_time))
        
        print("\nThe current temperature is: {:.2f} degrees F".format(temperature))
        print("The 'feel-like' temperature is: {:.2f} degrees F".format(feel_like_temperature))
        print("The current weather status is: ", weather_status)
        print("The current humidity level is: {}%".format(humidity_level))
        print("The wind speed status is: ", wind_status, 'MPH')
            
            
        # Run storing function
        put_weather_data(user_location, temperature, feel_like_temperature, humidity_level, weather_status, wind_status, date_and_time)
        
    time.sleep(5)
    menu()
    
    
menu()
