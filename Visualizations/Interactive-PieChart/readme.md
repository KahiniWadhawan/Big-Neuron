## Pie charts 

#### Author - Tanvi Parikh

#### Purpose
To display results of sentiment analysis obtained from IBM Tone Analyzer. The pie charts will b used to depict the sentence-level sentiment analysis of each tweet. 

![alt tag](https://github.com/CUBigDataClass/Big-Neuron/blob/Tanvi-branch/Visualizations/Interactive-PieChart/Sentence-level-pipeline.png)

 - **top100tweets algorithm** will pull the top 100 tweets for that candidate based on time-range specified.
 - **tone.json** is given out by IBM Tone analyser. 
 - **amcharts_JSON.py** will crunch *tone.json* into 3 files  in a format acceptable by Amcharts. 
   - emotion.json
   - social.json
   - writing.json
 - **Concerns:** 
    - should the 3 json files(per tweet) be stored locally or dumped into cassandra and then retrieved as per need. 
 - **Steps:** (Need modification) User selects 'X' candidate, 'a-b' date range > 
     - `top100tweets pulls tweets from cassandra `
     - `tone.json for all 100 from IBM` (how many firehoses needed?)
     - `amcharts_json.py creates 3 files per tone.json`

#### Technologies 
 - D3.js
 - CSS

#### Screenshots
1. PieChart from External JSON using **D3.js**
![alt text](https://github.com/CUBigDataClass/Big-Neuron/blob/Tanvi-branch/Visualizations/Interactive-PieChart/screenshots/pie-chart2.png "Logo Title Text 1")

***

2. PieChart from External JSON using **Amcharts & DataLoader plugin**
![alt text](https://github.com/CUBigDataClass/Big-Neuron/blob/Tanvi-branch/Visualizations/Interactive-PieChart/screenshots/final_emotiontone.png "Logo Title Text 2")

***

3. Double-columned pie-charts from External JSON using **Amcharts & DataLoader plugin**
![alt text](https://github.com/CUBigDataClass/Big-Neuron/blob/Tanvi-branch/Visualizations/Interactive-PieChart/screenshots/final_colors.png "Logo Title Text 2")

***

