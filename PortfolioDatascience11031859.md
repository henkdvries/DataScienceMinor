# DataScienceMinor
### Portfolio for the Data Science Minor

Table of Contents
==================

# Introduction
---
For the minor Applied Data Science at the Hague University of Applied Sciences I, Lennart van Koppen, will look back at the the work I did for the minor and reflect on that. 

## project
Our project is Ortho Eyes, which is a project with the LUMC, specifically with the laboratory of Kinematics and Neuromechanics(LK&N). We did research on how and with what data science methods we could help make a diagnosis of Musculoskeletal Disorders (MSD), specifically Rotator Cuff tears, easier for physicians. 

The LUMC has patients with various degrees of Rotater Cuff tears, that have been classified by physicians. The data from these patients are movements in forms of multiple exercises. These exercises were measured with a system called the Flock of Birds, which uses a magnetic field generator and magnetic sensors to measure the movement of bones. 

This resulted in the following research question:

_To what extend and in what way, can different supervised data science techniques be used on kinematic recordings to contribute to a more valid and more reliable diagnosis, made by a doctor, on shoulder disability_

We worked on a classification model to classify patients into different patients groups depending on severity of their Rotator Cuff tears. The patient groups are pre-determined by physicians of the LUMC. 

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

[Script can be found here](/Fingerprinting/DataScience/filespotting.py "script located here")
### Visualizing Data
At this point I wanted to manually go through all the files which means I needed a way to visualize the exercises in a way so I could compare the same labeled exercises from multiple patients.
#### Manually Finding Wrongly Named Files
Because I didn't want to spend to much time in filling in the data or clicking through the different plots of the exercises I went on to create a dynamic visualizer to plot all the exercises and patient dynamically, which I could loop through with simple key board shortcuts. I also added a way to register all the wrongly named files to a single json file. 
![Chunkfinder](/images/Dynamicvis.png)
[Script can be found here](/DynamicVisualizer/plot.py "script located here")

---
# Predictive Analytics

## Model Evaluation
---
# Research
## Desk Research
As I have stated earlier, I spent alot of time looking for usefull research papers that could support our own research. While it was difficult to find specific papers that relate to our 
## Paper
I wrote or rewrote large parts of the paper, I  
>The use of machine learning in the medical field started in the 1990’s (D. Douglas Miller, 2018).With the increase of data and processing power in the 21st century, this became a more usable tool. Since 2010 there has been a sharp rise in companies, investing in machine learning and artificial intelligence with the purpose of supporting the medical field.  
>
>While most machine learning focuses on Radiology, Oncology, Cardiology and Pathology, the focus of Computer-Assisted-Diagnosis (CAD) lies in image processing and assessing bio markers. The Laboratory for Kinematics and Neuromechanics (LK&N) in the Leiden University Medical Center (LUMC) (Sylvia A. Stegeman, 2016) (C.G.M.Meskers, 1998) is searching for new tools to support doctors in diagnosing Musculoskeletal Disorders (MSD) that are not found within these areas. This research is a follow up on previous researches done by the students of the minor Applied Data Science at the Hague University of Applied Sciences and the LK&N (Kasper van der Hoofd, 2019) as to find new ways to diagnose Rotator Cuff tears using machine learning.  
>
---
# Presentations
---
# Reflection
