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

_To what extend and in what way, can different data science techniques be used on kinematic recordings to contribute to a more valid and more reliable diagnosis, made by a doctor, on shoulder disability_

We worked on a classification model to classify patients into different patients groups depending on severity of their Rotator Cuff tears. The patient groups are pre-determined by physicians of the LUMC. 

### Structure
For the structure of the project we used scrum to divide epics into smaller tasks. I setup the Azure DevOps enviroment where we both have are scrumboard but also our repository. We did weekly and bi-weekly sprints depending on the stage of the project to guide the team from the starting epics towards smaller task that could be completed within a sprint. 

---
# Python for Datascience
As Software Engineering student I had experience with python for a couple of years. Although I thought I knew the most from the early parts of the Datacamp Courses, I was suprised to see there is plenty of more to learn. I had experience with the certain libraries like numpy but didn't know the inner workings until I started learning it with Data Camp. Furthermore, I didn't have much experience with most Data Science libraries, but they were explained pretty well with the Datacamp courses. 
## Datacamp
Here is an overview of my Datacamp assesments
![DatacampAssesments](/images/Datacamp.png)
---
# Pre-Processing Data
For pre-processing data I was messing around with the data and using some newly learned libraries from the datacamp courses and practicising my newly learned skills from datacamp. Furthermore I spent the most time in finding a way to fingerprint exercise for the purpose of finding wrongly named exercise files. Because the fingerprinting took too long I eventually resorted to manually spitting through the data with a self created tool to check all patients/exercises for wrongly named files. 
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
For the predictive analytics I mostly worked on the model evaluation.

## Model Evaluation
For the model evaluations I searched on what good model evaluations are besides the explained group of accuracy, preciscion, recall and the F1 score. 

I found the following model evaluations that could be usefull to get a more in depth evaluation beside the standard group I learned about within the lessons.
* Matthews Correlation Coefficient (MCC): this evaluation is a measure of quality of a classification. It is a balanced measure that isn't influenced by imbalanced datasets. It takes the full spectrum of the confusion matrix to create a correlation coefficient between the predicted and observed classifications. Where a +1 score is a perfect observed vs predicted classification, 0 no better than random predictions and -1 indicates complete disagreement between observed vs predicted classification. 
* Logaritmic Loss: Log Loss gives more nuanced view of the predictions because it takes into account the uncertainty of the prediction based on how much it varies from the true label. 

I wrote code so the model returns a set of model evaluations, which eventually get added the the configuration the model runs. the last part wasn't written by me, I just focused on the model evaluations. Below is an example of a finished configuration with the different model evaluations in it. 

```json
"Accuracy": 0.6959537572254335,
"LogLoss": 1.3907332369374026,
"MCC": 0.592299585950794,
"RMSE": 0.5514038835323583,
"RMSLE": 0.16069798344358124,
"ConfusionMatrix": [
[
    [604,5],
    [2,254]
 ],
[
    [407,42],
    [221,195]
],
[
    [456,216],
    [40,153]
]
]
```

In the actual research paper we just used the accuracy, precision and recall. This is because the group wanted to use these evaluations because they weren't certain about how to interpret them.

![ConfusionMatrix](/1/figuur1.png "confusion matrix of the best result" )

I had a hard time evaluation the results because patient group 2 was falsely predicting patient group 3 (PG) as PG2 in large amounts. But vice versa this was not the case. Which is weird because PG3 has smaller amount of patients and therefore data. Which made me think it should have been reversed because the model has less training data and therefor isn't capable of understanding the difference better. Because of the results in PG2 is lowered the precision of PG3, even though it had no trouble of differentiation between the other PG's.   

The result created more questions about the validity of the model and the data, without knowing precisely where to expect. My advice to the next group would be to try a more complex model,to see if these problems still persist with PG2, if that is still the case there should be another look at the data. 



---
# Research
## Desk Research
To get a good feel for the domain of our research I spent alot of time reading research papers about machine learning within the medical field, how motion of shoulders work and these shoulder motions can be translated to data that can be used for machine learning. I summed up a list of interesting research papers I found during my desk research.


1. D. Douglas Miller, E. W. (2018). Artificial Intelligence in Medical Practice: The. The American Journal of Medicine, 129/133.
 - This paper describes the use of AI in medical practice. It shows that since the 90's slowly more AI has been used within the field of medicine. Thus confirming 

2. Phadke, V., Braman, J. P., LaPrade, R. F., & Ludewig, P. M. (2011). Comparison of glenohumeral motion using different rotation sequences. Journal of Biomechanics, 44(4), 700–705. https://doi.org/10.1016/j.jbiomech.2010.10.042
 - This paper describes a problem we could run into with our data regarding the humerus and the issue with working with Euler angles to represent movement, it is called Gimbal Lock. This is where in Euler space, one axis rotates 90 degrees, which it then lines up with another axis, therefor removing one degree of freedom. This was also neccesary to understand how the axis notations worked for 3D visualization, This was also written in the paper that was used by the LUMC to translate the data into medical terms. 

## Paper
I wrote or rewrote large parts of the paper, for example the introduction below. I worked the last couple of day almost 12 hours per days on the research paper. 

>The use of machine learning in the medical field started in the 1990’s (D. Douglas Miller, 2018).With the increase of data and processing power in the 21st century, this became a more usable tool. Since 2010 there has been a sharp rise in companies, investing in machine learning and artificial intelligence with the purpose of supporting the medical field.  
>
>While most machine learning focuses on Radiology, Oncology, Cardiology and Pathology, the focus of Computer-Assisted-Diagnosis (CAD) lies in image processing and assessing bio markers. The Laboratory for Kinematics and Neuromechanics (LK&N) in the Leiden University Medical Center (LUMC) (Sylvia A. Stegeman, 2016) (C.G.M.Meskers, 1998) is searching for new tools to support doctors in diagnosing Musculoskeletal Disorders (MSD) that are not found within these areas. This research is a follow up on previous researches done by the students of the minor Applied Data Science at the Hague University of Applied Sciences and the LK&N (Kasper van der Hoofd, 2019) as to find new ways to diagnose Rotator Cuff tears using machine learning.  
>

We worked in a way so we all wrote keypoints to all the subjects and iteratively write the keypoints into paragraph. Since I was one of the only persons to work out these keypoints thuesday into actual paragraphs I wrote larges parts of the paper, specifically the introduction, result, discussion, conclusion and some parts in techniques. Not all my written parts stayed the same, other teammembers have rewrote my texts aswell since we continued to update the paper to the latest version. 

---
# Presentations
During the minor I gave multiple presentations, everytime I gave the presentation I created the powerpoint togather with my co-presenter. 

---
# Reflection
## Own Contribution Evaluation
### Situation
To evaluate the results of all the configurations the model ran, we needed a way to compare different results on a deeper level then average. 
### Task
I took upon myself the task of figuring out what model evaluations we could use and how we could use them.
### Actions
I did a lot of research into different model evaluation past the ones we got during the lessons. Based on what i've learned from this I implemented the evaluations I deemed important.
### Results
The result was in the end the model evaluations I picked weren't used in our paper. 
### Reflection
The results made me doubt myself why I wasn't able to bring over the reasons why I picked these evaluations and wasn't able to bring over the information I learned. The next time this situation arises I will try better in sharing my knowlegde in the subject. Furthermore, there were some model evaluation even I didn't look at (RMSE/RMSLE), this means I should keep it more simple, don't spend time in subjects I'm not sure about. Also try to taylor the evaluations needed for the data/model. Some evaluation have a good purpose in different types of data or other types of model.  
## Learned Objectives Evaluation
### Situation
For the most part of the project I was lagging behind in the data preperation/shaping and running the model. 
### Task
I was tasked with understanding the model and the way the data was shaped by last years group. 
### Actions
I did work on data shaping and running models. Although I was lagging behind other group members.
### Results
This resulted in that I had to catch up a lot all the time since people made big progress in preparing the data and training the model, while I was still struggling to do some simpler data shaping and trying train some other models.
### Reflection
When I look back at this, I always see myself getting distracted with ideas, other ways to enrich or shape the data. And getting stuck in a place where I want to do something without having the prior knowlegde needed to go where I am thinking about. I see it is not logical to go from point a to g without taking the steps in between. In the future I should hold my thoughts about crazy ideas and start slowly building my knowlegde to a point where I can actually realize my ideas instead of losing them because I have no clue how to get there. This means I should use smaller steps in the learning proces to make sure I understand what I need to do to go where my ideas lead me. 
## Group Evaluation
### Situation
As a group we are working togather to tackle big epics to finish our project.
### Task
The task neccesary for this was to split up all encompassing epics to a bitsize bits where can work on and finish in a short notice.
### Actions
To get these bitsize steps we discussed plenty on how we should fill the scrumboard. Also we should reflect on the earlier created tasks and issues to see if they are still valid.
### Results
This resulted in a agile working environment. Where we took what wee needed to do on sprint by sprint basis, within a general plan to reach a goal.
### Reflection
Although it went fine for the most part, I should for one not be a scrum master. I already have issues with being structured and not being able to provide a certain amount of structure to the group influences the rest aswell. Luckily other people picked up on this, creating a step by step plan on how to reach our goals and maintaining this on the scrumboard. In the end it all worked out fine but I think some annoyance could have been avoided if I was able to say that I'm not the person for the job.
