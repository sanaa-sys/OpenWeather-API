# project

Openweather Command Manual

NAME:
		openweather - Weather forecast program

SYNOPSIS:
		openweather -api="{API token}" -city="{city name},{country code}" -time -temp="{celsius or fahrenheit}"
		openweather -api="{API token}" -city="{city ID}" -pressure -cloud
		openweather -api="{API token}" -city="{lat},{lon}" - humidity - wind
		openweather -api="{API token}" -city="{zip code},{country code}" -sunrise -sunset
		openweather -help

DESCRIPTION:
		A python script that fetches weather information from the openweathermap API and returns current weather information to the user

EXECUTION INSTRUCTIONS:
		1. Open a terminal window
		2. Navigate to directory that contails openweather.py using the change directory command, e.g [cd Documents/openweather.py_folder]
		3. Run openweather program by entering "python3 openweather" with valid arguments. e.g[python3 openweather.py -api"abc123" -city="Clayton,AU" -temp="celsius"]

ARGUMENTS:
    MANDATORY ARGUMENTS:
		-api	    The -api argument, is a mandatory argument which provides the program with the API key required for Openweathermap API requests
	
	MUTUALLY EXCLUSIVE ARGUMENTS:
		-city	    The -city argument, provides the program with a city to search the weather
		-cid	    The -cid argument, provides the program with a city ID code to search the weather (Openweathermap recommends calls to API by city ID to get unambiguous result for your city)
		-gc         The -gc argument, provides the program with geographical latitude and longitude to search the weather
		-z          The -z argument, procides the program with a city's zip code and country code to search the weather
		
	OPTIONAL ARGUMENTS (AT LEAST ONE MUST BE SPECIFIED):
	    -time       The -time argument, allows the user to print the time which the weather forecast was fetched in the location's local time
	    -temp       The -temp argument, must be followed by either "celsius" or "fahrenheit", prints the minimum and maximum temperature of the location in the specified units. -temp is set to "celsius" by default if not specified
	    -pressure   The -pressure argument, allows the user to print the air pressure information at the location
	    -cloud      The -cloud argument, allows the user to print the density of clouds information at the location
	    -humidity   The -humidity argument, allows the user to print the humidity information at the location
	    -wind       The -wind argument, allows the user to print the wind speed and wind direction information at the location. Units for wind speed is set to meters/sec by default unless -temp="fahrenheit", then it will be shown in miles/hour
        -sunrise    The -sunset argument, allows the user to print the time of sunrise at the location
        -sunset     The -sunset argument, allows the user to print the time of sunrise at the location
        
    HELP ARGUMENTS
        -help       The -help argument, if provided, overwrites any other arguments provided and prints a list of arguments and their functionality
        
EXCEPTIONS:

        1.          A RUNTIME ERROR EXCEPTION WILL BE RAISED IF USER PROVIDES MORE THAN ONE LOCATION ARGUMENT. E.G "python3 openweather.py -api"abc123" -city="Clayton,AU" -z="3800,AU" -time"
        2.          A RUNTIME ERROR EXCEPTION WILL BE RAISED IF USER DOES NOT PROVIDE ANY LOCATION ARGUMENT. E.G "python3 openweather.py -api"abc123" -time"
        3.          AN ERROR WILL BE THROWN IF THE USER DOES NOT PROVIDE ANY API TOKEN. E.G "python3 openweather.py -city="Clayton,AU" -time"
        4.          A VALUE ERROR EXCEPTION WILL BE RAISED IF USER PROVIDES A -temp ARGUMENT OTHER THAN "celsius" OR "fahrenheit". E.G "python3 openweather.py -api"abc123" -city="Clayton,AU" -temp="kelvin""
        5.          A RUNTIME ERROR EXCEPTION WILL BE RAISED IF A USER DOES NOT PROVIDE ANY WEATHER PARAMETER ARGUMENT. E.G E.G "python3 openweather.py -api"abc123" -city="Clayton,AU""
        6.          A RUNTIME ERROR EXCEPTION WILL BE RAISED IF THE API REQUEST COULD NOT BE FUFILLED. THE API STATUS CODE WILL BE PRINTED FOR DEBUGGING PURPOSES
	

COMMON API STATUS CODE:
        200 :       API REQUEST IS SUCCESSFUL AND FUFILLED
        401 :       API KEY IS INVALID
        404 :       API REQUEST COULD NOT BE FUFILLED DUE TO LOCATION ARGUMENT ERROR (INVALID CITY NAME, INVALID CITY ID, INVALID COORDINATES OR INVALID ZIP CODE)
        429 :       API CALLS EXCEEDED THE LIMIT OF 60 CALLS PER MINUTE

AUTHOR:
		AYESHA ALI
		MONASH UNIVERSITY, AUSTRALIA
		VERSION 1	:	17 OCTOBER 2019
