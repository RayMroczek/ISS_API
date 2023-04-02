#import requests to make API calls:
import requests
#from the datetime module, import datetime class:
from datetime import datetime
#for emailing yourself - not using this time though
#import smtplib

#making it more fun:
print("""\
 .    '                   .  "   '
            .  .  .                 '      '
    "`       .   .
                                     '     '
  .    '      _______________
          ==c(___(o(______(_()
                  \=\
                   )=\
                  //|\\
                 //|| \\
                // ||  \\
               //  ||   \\
              //         \\

                    """)

#getting sun up and sun down times for fam:
my_lat = 33.933380
my_lng = -78.030724

print("Welcome to the International Space Station (ISS) Spotter App!\n")

#choosing hard-coded values:
parents = input("Are you Shirley? Enter Y or N: ")

if parents != 'Y':
  print(f"You can find your latitude and longitude here: \n https://www.latlong.net/\nThen, paste it in here - don't forget to include any minuses.\n")
  ask_lat = float(input("What is your latitude? "))
  ask_lng = float(input("What is your longitude? "))


def iss_is_above():
  #get ISS location
  ISS_response = requests.get(url="http://api.open-notify.org/iss-now.json")
  #make sure API call was successful with raise_for_status:
  ISS_response.raise_for_status()
  #get the actual data:
  data = ISS_response.json()
  #print(f'full response: {data}')
  #print(f'retrieve just the key position and associated values: {data["iss_position"]}')
  latitude = float(data["iss_position"]["latitude"])
  longitude = float(data["iss_position"]["longitude"])
  #create a tuple with latitude and longitude:
  #iss_position = (latitude, longitude)
  #check if the ISS latitude and longitude are within +/-5 of your hard-coded location:
  if (parents == 'Y' and (my_lat-5 <= latitude <= my_lat+5 and my_lng-5 <= longitude <= my_lng+5)) or (parents != 'Y' and (ask_lat-5 <= latitude <= ask_lat+5 and ask_lng-5 <= longitude <= ask_lng+5)):
    print("The ISS is in the sky above you!")
  else:
    print("It's not above you right now - the ISS has other places to be. Check back in later!")
    

def its_dark_outside ():
  #request the sunrise and sunset times, in UTC, for your hard-coded location:
  response_sun=requests.get(f'https://api.sunrise-sunset.org/json?lat={my_lat}&lng={my_lng}&formatted=0')
  my_loc = response_sun.json()
  #print(my_loc)
  #retrieve specific UTC time values out of the dictionary:
  #use split to get just the hour! and convert it to an integer for comparison.
  sunrise = int(my_loc["results"]["sunrise"].split("T")[1].split(":")[0])
  sunset = int(my_loc["results"]["sunset"].split("T")[1].split(":")[0])
  #get current UTC time, converted to an hour to make it comparable to our hours above.
  time_now = datetime.now().hour
  if time_now >= sunset or time_now <= sunrise:
    print("\nIt's dark enough to be able to see the International Space Station.")
  else:
    print("\nIt's not dark enough to see the International Space Station.")

its_dark_outside()
iss_is_above()


#not adding emailing functionality.
print("\nThanks for visiting! I'll add some notification function at a later time.")

#reminders on response codes:
#response codes tell us if the request succeeded or not. 404... doesn't exist!
#response starting with 100... hold on 
#response starting with 200... here you go, you should be getting the response you expected
#response starting with 300... Go away! you probs don't have permission.
#response starting with 400... you screwed up / the thing you're looking for doesn't exist
#response 401 - you are not authorized to access this data
#response starting with 500... "I" screwed up (server, website something down/not working)
#and more! https://www.webfx.com/web-development/glossary/http-status-codes/