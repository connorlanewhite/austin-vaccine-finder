This will help you find vaccines in Texas. Right now I believe it just does HEB, but can / will do more?

Here's what you'll need to do (and apologies for not being super detailed in all steps - maybe that will come later)

## How to Setup
1. Clone this repo
2. Have python
3. Install / have the requirements in `requirements.txt`
    * not neccesarily sure who the audience would be for this particular instruction, but you can do this with `pip install -r requirements.txt`
5. Locally, change line 37 from `ADDRESS = ""` to `ADDRESS = "<YOUR ADDRESS HERE>"` though you will obviously put your address there. Quick caveats:
    * needs to just be the street address; not cities or states or what have you
    * needs to be fully spelt out "123 Fake Street" not "123 Fake St"
6. Similarly put replace the empty string on line 38 with your zipcode
7. Sign up for [IFTTT](https://ifttt.com/) and also download the mobile app
8. Create an applet with two steps. 
    * <img width=400 src="https://user-images.githubusercontent.com/13944198/110836281-7cadba00-8265-11eb-82dc-1a6779c84f6f.png">
    * If: Receive a web request (webhooks)
    * Then: Send a rich notification from the IFTTT app
9. Set the event_name as appts_available for the web request
    * <img width=400 src="https://user-images.githubusercontent.com/13944198/110836446-abc42b80-8265-11eb-940f-b30f9f0a822c.png">
10. Set the values for the rich notification as in image3: value1 is brand, value2 is city, value3 is the brand’s url
    * <img width=400 src="https://user-images.githubusercontent.com/13944198/110836459-b1ba0c80-8265-11eb-9a9d-9f643625b1af.png">
11. After creating the webhook, navigate to "my applets"
12. Click on your applet
13. Hit the little webhook icon (not the bell) and then hit "documentation" in the top right
14. Copy the text that's after "Your key is:" as pictured
    * <img width="247" alt="image" src="https://user-images.githubusercontent.com/13944198/110837255-9c91ad80-8266-11eb-829c-f059c7451463.png">
15. Replace line 36's empty string with that copied text... but you know, still in the quotes

## How to run it
1. Make sure you're logged in on your mobile app
2. Run `python vax.py` from the repo's folder
