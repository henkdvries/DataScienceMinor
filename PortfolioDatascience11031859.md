# DataScienceMinor
### Portfolio for the Data Science Minor

Table of Contents
==================

# Introduction
---
For the minor Applied Data Science at the Hague University of Applied Sciences I, Lennart van Koppen, will look back at the the work I did for the minor and reflect on that. 

---
# Domain
---
# Python for Datascience
As Software Engineering student I had experience with python for a couple of years. Although I thought I knew the most from the early parts of the Datacamp Courses, I was suprised to see there is plenty of more to learn. I had experience with the certain libraries like numpy but didn't know the inner workings until I started learning it with Data Camp. Furthermore, I didn't have much experience with most Data Science libraries, but they were explained pretty well with the Datacamp courses. 
## Datacamp
Here is an overview of my Datacamp assesments
![DatacampAssesments](/images/Datacamp.png)
---
# Pre-Processing Data
For pre-processing data I was messing around with the data and using some newly learned libraries from the datacamp courses and practicising my newly learned skills from datacamp. Furthermore I spent the most time in finding a way to fingerprint exercise for the purpose of finding wrongly named exercise files. Because the fingerprinting took to long I eventually resorted to manually spitting through the data with a self created tool to check all patients/exercises for wrongly named files. 
## Data Exploration
For data exploration I mostly used the newly learned libraries like Pandas and Seaborn to plot exercises and understand the way the data is shaped. 
## Finding wrongly name CSV files
Because we wanted to decrease the number of assumptions made on the data we determined we also must check if the data is what is says it is. Eventually we got labeled data, which means we wanted to check if the labeling is correct. I worked on this part to find a way to figure out if the labeling of the CSV files for the exercises is correct. 
### Fingerprinting
The first solution I had in mind was to use fingerprinting to find the characteristics of an exercise, by means of finding a finperprint. I had the idea of splitting the exercise in chunks, based on direction of movement. Where the movement was positive, negative or stayed neutral (within a certain range). The first step was to find the chunks based on the type of movement. To actually use fingerprinting I would need a way to transform the chunks into characteristics that could be used for fingerprinting. What I had in mind was using the chunk count, the smoothnes of the curve, the derivative of the formula for the line per chunk. 

As seen in the result below, I wasn't able to refine the chunk finder to a point that I could actually use it. The colours represent the direction, with red being down and blue going up. As you can see it didn't got that right. In the end I spent alot of time working on a non functioning tool.
![Chunkfinder](/images/FoundChunks.png)
### Visualizing Data
At this point I wanted to manually go through all the files which means I needed a way to visualize the exercises in a way so I could compare the same labeled exercises from multiple patients.
#### Manually Finding Wrongly Named Files
Because I didn't want to spend to much time in filling in the data or clicking through the different plots of the exercises I went on to create a dynamic visualizer to plot all the exercises and patient dynamically, which I could loop through with simple key board shortcuts. I also added a way to register all the wrongly named files to a single json file. 

---
# Predictive Analytics

## Model Evaluation
---
# Research
---
## Desk Research
## Paper
---
# Presentations
---
# Reflection
