## Task prompt

### Getting times

You are an experienced QA engineer. You are testing a web app that converts times from a base time zone to several other time zones. Given the task below, come up with appropriate times and time zones to test:

<insert task>

### Getting CSV, same chat as previous

Convert this test data to a csv with columns
TestCaseName,BaseTimezone,Time,TargetTimezone,ConvertedTime
There will be multiple rows per case
Format times as YYYY-MM-DD HH:MM

## Form Filling Prompts

### Timezone prompt 1

Write JavaScript to run in the console of a webpage to press a button on that webpage with id "add-zone". I want to press it 20 times

### Timezone prompt 2

That has created a set of boxes with name "targets". Now write JavaScript code to use in the console that will fill the 20 boxes with different time zone names, using IANA standard time zone names

### Time prompt 1

Write JavaScript to run in the console of a webpage to press a button on that webpage with id "add-time". I want to press it 20 times

### Time prompt 2

That has created a set of boxes with name "times". Now write JavaScript code to use in the console that will fill the 20 boxes with different dates and times, in the format "YYYY-MM-DDTHH:MM"

## Convert to Pytest Prompt

You are an experienced QA engineer, testing the python function

convert_times(times, timezones)

Which takes a list of times in a base time zone (as python datetime objects), and a list of time zones (as IANA timezone strings) to convert to.  It produces output of the form

[(base_time1, [converted_first_tz, converted_second_tz, ...]), …]

All output times are strings of the form "YYYY-MM-DD HH:MM:SS"

Create a pytest file making one test per test case from the CSV below:

<copy csv contents>

## Mocking prompt

Create pytest tests for resolve_city_to_tz in conversions.py that mock the calls to the external apis. Mock four different cities, and test that it works as expected for:

- only normal timezones
- only city names
- a mixture of normal timezones and city names

## Story to Tasks Prompt

You are an experienced software QA manager. You are presented with a completed web app based on this agile Epic:

<insert epic>

The user story we are currently working on is:

<insert story>

Please generate appropriate tasks for this story in the same format as this task:

<insert task>

## Generating Stories Prompt

You are an experienced software QA manager. You are presented with a completed web app based on this agile Epic:

<insert epic>

Generate user stories to ensure the app is working as expected. Focus on functionality, don't worry about performance or security. Use the format of this existing story:

<insert story>
