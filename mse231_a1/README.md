# Gender Homophily on Twitter

### Overview

The proliferation of social media in today’s world allows for a number of novel social questions to be asked, particularly regarding how users interact on digital platforms. In this project, I explore gender homophily on Twitter by analyzing retweet trends between male and female users. Out of interest, I perform this analysis on two different sets of tweets: the randomly selected stream provided by Twitter and a set filtered for the word “Greta” meant to filter for tweets related to Greta Thunberg, the young environmental activist. Below are my approach and results:

### Approach and Strategy

To perform this project, I first stream both random tweets and filtered tweets from the Twitter API for roughly 34 hours. Our filtered tweets included those with the name Greta - a reference to the environmental activist [Greta Thunberg](https://en.wikipedia.org/wiki/Greta_Thunberg). These tweets were streamed in JSON format and were parsed for basic info such as username, retweeted user, date, and time using parse_tweets.py. Once this data was parsed, gender analysis could begin. First, I parsed user’s screen names to identify their prospective first name. In order to do this, I eliminated non-alpha characters such as numbers and emojis, then extracted the first string in what was remaining under the assumption that this would be the real first name of the majority of users.

After identifying a given user’s prospective first name, I used Social Security provided baby names data from 1880 and 2013 to infer its gender. We chose to limit our use of this dataset to only names from 1928 forward, as I assumed Twitter users weren’t born prior to this. Next, I aggregated the total occurrences of each unique name and used this to infer a given user’s gender; essentially, for a given user, I asked whether there were more males or females assigned to this name. If there have been historically more males with this name, I labeled that user as a male, and if not, a female. 

This approach works in this scenario because there are roughly equal numbers of males and females in the SSA provided data, meaning that it’s good enough to compare raw volume of names and not proportion, as another analysis might do. To analyze gender homophily, I analyzed the actual proportion of times a given gender retweeted its own gender and compared this to the expected proportion if no homophily existed.

![equations](https://github.com/miguelito34/mse_231/blob/master/mse231_a1/homophily_equations.jpeg)

Using these two values, I can determine if a given gender shows homophily by taking the actual proportion for retweets of females (females would be y above) minus the expected proportion. If the result is positive, it means that gender x retweeted females more often than expected. Thus, using this test, homophily is determined by a positive result for females and a negative result for males. We see this in the tables below.

### The Results

*Homophily for all tweets*
<table>
 <thead>
  <tr>
   <th style="text-align:left;"> Gender </th>
   <th style="text-align:left;"> Female Proportion </th>
   <th style="text-align:left;"> Homophily Exists? </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> Female </td>
   <td style="text-align:left;"> 6.18% </td>
   <td style="text-align:left;"> Yes </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Male </td>
   <td style="text-align:left;"> -5.86% </td>
   <td style="text-align:left;"> Yes </td>
  </tr>
</tbody>
</table>

*Homophily for filtered tweets*
<table>
 <thead>
  <tr>
   <th style="text-align:left;"> Gender </th>
   <th style="text-align:left;"> Female Proportion </th>
   <th style="text-align:left;"> Homophily Exists? </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> Female </td>
   <td style="text-align:left;"> 20.44% </td>
   <td style="text-align:left;"> Yes </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Male </td>
   <td style="text-align:left;"> 7.47% </td>
   <td style="text-align:left;"> No </td>
  </tr>
</tbody>
</table>

Both trends below, for all tweets and tweets about Greta, followed a similar pattern. It appears high tweet volumes picked up around 11 AM and continued until midnight, with quieter traffic in the morning hours likely due to users’ sleep schedules. Among all tweets, it appears men tend to tweet more than women. In tweets about Greta, women tweeted more for a small period.

![All Tweets](https://github.com/miguelito34/mse_231/blob/master/mse231_a1/all_tweets_plot.jpeg)
![Filtered Tweets](https://github.com/miguelito34/mse_231/blob/master/mse231_a1/filtered_tweets_plot.jpeg)

### Conclusions & Limitations

Based on our analysis, it appears that in general cases, both men and women demonstrate homophily. This is likely due to the fact that they share a gender and are thus more likely to interact with each other. Notably, when only considering tweets about Greta Thunberg, homophily drastically increases for females and completely disappears for males. This is likely due to the fact that Greta is a female environmental activist and at the forefront of a lot of news regarding her position as such. Thus, I expected female users to engage with the topic more.

Further work is needed to build out a more robust way of inferring gender, potentially by analyzing tweets from the user or analyzing their profile photo. As it stands, our current method relies solely on the predicted first name of the user, which itself could be wrong. To that end, a more rigorous way of identifying a user’s first name is needed to increase the accuracy of a users’ inferred gender.


