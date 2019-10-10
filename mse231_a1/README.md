# Gender Homophily on Twitter

### Overview

The proliferation of social media in today’s world allows for a number of novel social questions to be asked, particularly regarding how users interact on digital platforms. In this project, I explore gender homophily on Twitter by analyzing retweet trends between male and female users. Out of interest, I perform this analysis on two different sets of tweets: the randomly selected stream provided by Twitter and a set filtered for the word “Greta” meant to filter for tweets related to Greta Thunberg, the young environmental activist. Below are my approach and results:

### Approach and Strategy

To perform this project, I first streamed both random tweets and filtered tweets from the Twitter API for roughly 34 hours. These tweets were streamed in JSON format and were parsed for basic info such as username, retweeted user, date, and time, all using the python parsing script parse_tweets.py. Once this data was parsed, cleaned, and saved into TSV (tab-separated-value) format, gender analysis could begin. First, I parsed user’s names to identify their prospective first name. In order to do this, I eliminated non-alpha characters such as numbers and emojis, then I extracted the first string in what was remaining under the assumption that this would be the first name of the majority of users.

After identifying a given user’s prospective first name, I used Social Security provided baby names data from 1880 and 2013 to infer its gender. I chose to limit my use of this dataset to only names from 1928 forward, as those would correlate with folks 90 years or younger, which presumably encompasses the majority of Twitter. I did this to ensure the name data I used to infer gender was relevant to the analysis. Next, I aggregated the total occurrences of each unique name and used this to infer a given user’s gender; essentially, for a given user, I asked whether there were more males or females assigned this name. If there have been historically more males with this name, then I labeled that user as male, and if not, female. 

This approach works in this scenario because there are roughly equivalent numbers of males and females in the SSA provided datasets, meaning that it’s good enough to compare raw volume. A more precise approach would have compared the fraction of males with a name to the fraction of females with that name, as this is more robust to variation in sample sizes. To analyze gender homophily, I analysed the proportion of times a given gender retweeted its own gender. I did this using the following formula for each gender:

omophily score for gender x = ((retweets of males by x) - (retweets of females by x)) / total retweets by x

This resulted in a number that ranged from -1 to 1 in which -1 indicated only females were retweeted and 1 indicated only males were retweeted. If females received a negative score, or if males received a positive score, then gender homophily exists to some extent. Once genders were assigned to each twitter user in my dataset, I was able to plot the tweet volume by gender, for each set of tweets. The results are below.

### The Results

*Homophily for all tweets*
<table>
 <thead>
  <tr>
   <th style="text-align:left;"> Gender </th>
   <th style="text-align:left;"> Homophily Score </th>
   <th style="text-align:left;"> Homophily </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> Male </td>
   <td style="text-align:left;"> .34 </td>
   <td style="text-align:left;"> Male </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Female </td>
   <td style="text-align:left;"> .10 </td>
   <td style="text-align:left;"> Male </td>
  </tr>
</tbody>
</table>

*Homophily for filtered tweets*
<table>
 <thead>
  <tr>
   <th style="text-align:left;"> Gender </th>
   <th style="text-align:left;"> Homophily Score </th>
   <th style="text-align:left;"> Homophily </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> Male </td>
   <td style="text-align:left;"> .07 </td>
   <td style="text-align:left;"> Male </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Female </td>
   <td style="text-align:left;"> -.18 </td>
   <td style="text-align:left;"> Female </td>
  </tr>
</tbody>
</table>

Both trends below, for all tweets and tweets about Greta, followed a similar pattern. It appears high tweet volumes picked up around 11 AM and continued until midnight, with quieter traffic in the morning hours likely due to users’ sleep schedules.

![All Tweets](https://github.com/miguelito34/mse_231/blob/master/mse231_a1/all_tweets_plot.jpeg)
![Filtered Tweets](https://github.com/miguelito34/mse_231/blob/master/mse231_a1/filtered_tweets_plot.jpeg)

### Conclusions & Limitations

From this analysis, I believe that homophily is present among males. From the rudimentary analysis, it appears that both females and males retweet males more often than females, however when tweeting about Greta [Thunberg], the story shifts. In this case, females retweet females more often and males, while still retweeting males more often, are doing so at lower rates than usual. I presume this is due to the change in topic, and the fact that Greta is a female, but more analysis would need to be done to be certain.

Further work is needed to build out a more robust way of inferring gender, potentially by analyzing tweets from the user or analyzing their profile photo. As it stands, my current method relies solely on the predicted first name of the user, which itself could be wrong. To that end, a more rigorous way of identifying a user’s first name is needed to increase the accuracy of a users’ inferred gender.

