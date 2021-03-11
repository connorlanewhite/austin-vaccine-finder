This will help you find vaccines in Texas. Right now I believe it just does HEB, but can / will do more?

Here's what you'll need to do (and apologies for not being super detailed in all steps - maybe that will come later):
1. Clone this repo
2. Have python
3. Install / have the requirements in `requirements.txt`
4. Locally, change line 37 from `ADDRESS = ""` to `ADDRESS = "<YOUR ADDRESS HERE>"` though you will obviously put your address there. Quick caveats:
    * needs to just be the street address; not cities or states or what have you
    * needs to be fully spelt out "123 Fake Street" not "123 Fake St"
5. Similarly put replace the empty string on line 38 with your zipcode
6. Sign up for [IFTTT](https://ifttt.com/) and also download the mobile app
7. Create an applet (instructions to come soon)
