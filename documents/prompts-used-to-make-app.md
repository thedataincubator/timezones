## Prompts used to generate this app

This was a lot of back-and-forth with copilot, at least partially because I was seeing what it can do. I didn't commit after each one, I waited until I had something working (so usually a few prompts to get there) between commits. I have added some comments that are not part of the prompt to give context where it isn't clear, these are in italics

1. I want to build a flask app in Python that will create a webpage where a user can input a number of time zones and a time, and get that time in each of the time zones.
1. let's run it and see how it looks
1. Let's save our current progress to a git repo
1. Let's do some more work on the app. It's coming along, but let's change the base timezone to also allow users to type to find their timezone
1. run it so we can see how it's working
1. There's a bug: if there's a blank timezone slot, you get a server error. It should just ignore blank timezones
1. run it, I'll test it
1. Instead of ignoring unknown timezones, we should produce a line in the output indicating that the timezone was unrecognized
1. sure 
    1. _copilot asked me if it should test if it fixed the bug_
1. stop. Run the app, let me test it 
    1. _it was trying to do too much to test it_
1. Let's make some changes: Don't put the UTC default in the base timezone box, and make one of the rows in the output the base time zone. Also, remove the title in the output
1. let's save this in our github
1. cancel. Save this in our local git 
    1. _I said github, it tried to set up a github connection_
1. Let's make this more useful. Allow a user to enter multiple times to convert
1. Rearrange the output to be a grid, with the rows being the different times and the columns the different time zones
1. For the printed times in the output, only write the date and time (don't write the time zone in the cells in the grid - it's repetitive)
1. For the inputs, I want people to be able to enter a city and have it look up the time zone for them (so they could enter "San Francsico" or "Mumbai, India" or "Frederick, MD"). Don't do the lookup live, allow them to enter a city and then convert it when the output is generated. Use a free API to look things up if possible
1. run the app
1. The city and timezone entries should use the same box, they shouldn't have separate lists
    1. _the inital solution it came up with was two sets of input boxes: timezones and cities_
1. I'm getting "unrecoginzed location" for every city I try
    1. _I realized that it was just an issue of a missing username while copilot was "fixing" it by rewriting everything in a way that broke things_
1. Undo whatever you just did
1. You broke everything we did in the last hour
    1. _The code that was basically working was completely overwritten - I hadn't done a git commit since I foolishly assumed that my statement about the error would lead to testing rather than rewriting code_
1. just stop
    1. _Copilot assumed the last instruction meant "reset to our last git commit" and tried to wipe out even more of the work_
1. go back to using geonames.org for city lookup
    1. _This basically got us back to where we were before, though with some differences_
1. This is now basically working. But I'd like to use bootstrap to make it look nicer
1. That's looking better, but the boxes added by "add time" and "add target" are not as wide as the ones present by default, it looks weird
1. better, but now the button to remove the added time or target is gray instead of red, and is extending on to the next line
1. That made things worse. Now the added times and targets are too narrow again, and their buttons are gray. They don't need to be red, they just need to match the default ones
1. Ok, that's working. Now I want to set up tests. What kind of inputs should we be testing for?
    1. _I was expecting it to generate a list of big-picture test cases, like "near daylight savings time" or "crossing midnight" or something about weird time zones. Which it basically did, as a bullet list of things to test. It asked if it should make `pytest` code for all of that_
1. yes
1. There's a prompt missing from my history: I switched to the `weekday` branch here and asked it to print the weekday as well as the date, but I don't have the exact wording
1. This is displaying the weekday in the base timezone, I need it for each timezone - conversions will often push into the next day
1. _I switched back to the main branch, I'm abandoning the weekday one for the moment_
1. Instead of displaying the results on a separate page, have them display at the bottom of the input page. Maintain the filled out time and timezone boxes, but please minimize how much javascript you use
1. Make a nicer readme for the project. Make sure to have:
    - a short introduction to what it does
    - how to use the app
    - how to setup and run it (including geonames for the city lookup)
    - the project structure
    - troubleshooting tips (like timezone format, what to do if city lookup fails, etc)
    - Any other useful notes for potential users
1. _I did some hand-editing to get things better arranged and to break the big monolith in app.py up a bit_