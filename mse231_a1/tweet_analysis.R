## Setup

### Libraries
if (!require(tidyverse)) install.packages("tidyverse")
library(tidyverse)
if (!require(lubridate)) install.packages("lubridate")
library(lubridate)
if (!require(scales)) install.packages("scales")
library(scales)

###  Parameters
all_tweets_pathname <- "all_tweets_clean.tsv"
filtered_tweets_pathname <- "filtered_tweets_clean.tsv"
female_names_url <- "https://5harad.com/mse125/assets/hw1/female_names.tsv.gz"
male_names_url <- "https://5harad.com/mse125/assets/hw1/male_names.tsv.gz"

## Load Data
all_tweets <-
  all_tweets_pathname %>%
  read_tsv(quote = " ")

filtered_tweets <-
  filtered_tweets_pathname %>% 
  read_tsv()

female_names <-
  female_names_url %>% 
  read_tsv()

male_names <-
  male_names_url %>% 
  read_tsv()

## Functions

### find_gender function
find_gender <- function(data) {
  
  data %>% 
    
    # String manipulation to isolate first names
    mutate_if(
      is.character, 
      str_replace_all,
      pattern = "[^[:alpha:]+[:space:]]", # Gets rid of non-alpha characters
      replacement = ""
    ) %>% 
    mutate_if(
      is.character,
      str_extract,
      pattern = "^[:alpha:]+" # Extracts first string
    ) %>%
    mutate_if(
      is.character,
      str_to_lower # Normalizes names to lowercase for easier joining
    ) %>%
    
    # Gives each row a unique key so that they can later be brought back
    # togther
    mutate(pair_key = as.integer(rownames(.))) %>% 
    
    # Gathers the names to minimize the amount of processing needed when
    # inferring gender, connects each name to counts, and infers gender based
    # on the formula explained above
    gather(key = "user_type", value = "name", username, og_poster) %>%
    left_join(male_names, by = "name") %>% 
    left_join(female_names, by = "name") %>% 
    mutate_at(
      vars(contains("total")),
      replace_na,
      replace = 0
    ) %>% 
    mutate(
      gender_p = (total_male - total_female)/(total_male + total_female),
      est_gender = case_when(
        gender_p < 0 ~ "female",
        gender_p == 0 ~ sample(c("female", "male"), replace = TRUE, size = 1),
        gender_p > 0 ~ "male",
        TRUE ~ "unknown"
      )
    ) %>% 
    select(-total_male, -total_female) %>% 
    
    # Collects newly created data and then spreads it out so that further
    # analysis can be done, keeping interacting user pairs together
    unite(col = "info", name, gender_p, est_gender) %>% 
    spread(key = "user_type", value = "info") %>%
    separate(
      username, 
      into = c("user_name", "user_gender_p", "user_est_gender"), 
      sep = "_"
    ) %>% 
    separate(
      og_poster, 
      into = c("og_name", "og_gender_p", "og_est_gender"), 
      sep = "_"
    ) %>% 
    select(
      date, time, user_name, og_name, user_est_gender, og_est_gender,
      user_gender_p, og_gender_p
    )
  
}

## Data Prep

### Prep Gender Data
male_names <-
  male_names %>% 
  filter(year >= 1928 & year <= 2014) %>% 
  mutate(name = name %>% str_to_lower()) %>% 
  group_by(name) %>% 
  summarise(total_male = sum(count, na.rm = TRUE))

female_names <-
  female_names %>% 
  filter(year >= 1928 & year <= 2014) %>% 
  mutate(name = name %>% str_to_lower()) %>% 
  group_by(name) %>% 
  summarise(total_female = sum(count, na.rm = TRUE))

### Prep Tweet Data
filtered_tweets_gen <- find_gender(filtered_tweets)
all_tweets_gen <- find_gender(all_tweets)

## Analysis

### Gender Trends Over Time

#### Tweet Volume by Gender for All Tweets
all_tweets_plot <-
  all_tweets_gen %>% 
  filter(user_est_gender != "unknown") %>% 
  count(date, time, user_est_gender, name = "tweets") %>% 
  arrange(date, time, user_est_gender) %>% 
  transmute(
    user_est_gender = user_est_gender %>% str_to_title(), 
    tweets, 
    datetime = ymd_hms(str_c(date, time))
  ) %>% 
  ggplot(aes(datetime, tweets, color = user_est_gender)) +
  geom_line() +
  scale_x_datetime(
    breaks = "3 hours",
    date_labels = "%a, %b%e %I%p"
  ) +
  scale_y_continuous(
    labels = comma_format()
  ) +
  labs(
    title = "Tweet Volume by Gender for All Tweets",
    x = NULL,
    y = "Tweet Volume",
    caption = "Data collected from Twitter over 24 hours."
  ) +
  theme_minimal() +
  theme(
    legend.title = element_blank(),
    legend.position = "bottom",
    axis.text.x.bottom = element_text(angle = 45, hjust = 1)
  )

all_tweets_plot

ggsave(plot = all_tweets_plot, file = "all_tweets_plot.pdf", width = 8, height = 5)

#### Tweet Volume by Gender for Tweets About Greta Thunberg
filtered_tweets_plot <-
  filtered_tweets_gen %>% 
  filter(user_est_gender != "unknown") %>% 
  count(date, time, user_est_gender, name = "tweets") %>% 
  arrange(date, time, user_est_gender) %>% 
  transmute(
    user_est_gender = user_est_gender %>% str_to_title(), 
    tweets, 
    datetime = ymd_hms(str_c(date, time))
  ) %>% 
  ggplot(aes(datetime, tweets, color = user_est_gender)) +
  geom_line() +
  scale_x_datetime(
    breaks = "3 hours",
    date_labels = "%a, %b%e %I%p"
  ) +
  scale_y_continuous(
    labels = comma_format()
  ) +
  labs(
    title = "Tweet Volume by Gender for Tweets About Greta Thunberg",
    x = NULL,
    y = "Tweet Volume",
    caption = "Data collected from Twitter over 24 hours."
  ) +
  theme_minimal() +
  theme(
    legend.title = element_blank(),
    legend.position = "bottom",
    axis.text.x.bottom = element_text(angle = 45, hjust = 1)
  )

filtered_tweets_plot

ggsave(plot = filtered_tweets_plot, file = "filtered_tweets_plot.pdf", width = 8, height = 5)

### Homophily

#### Gender Homophily in All Tweets
all_tweets_gen %>% 
  filter(user_est_gender != "unknown" & og_est_gender != "unknown") %>% 
  count(user_est_gender, og_est_gender, name = "total") %>% 
  spread(key = "og_est_gender", value = "total") %>% 
  mutate(
    bias = (male - female)/(male + female),
    homophily = ifelse(bias < 0, "female", "male"),
    male_likelihood = (male - female)/male
  )

#### Gender Homophily in Tweets About Greta Thunberg
filtered_tweets_gen %>% 
  filter(user_est_gender != "unknown" & og_est_gender != "unknown") %>% 
  count(user_est_gender, og_est_gender, name = "total") %>% 
  spread(key = "og_est_gender", value = "total") %>% 
  mutate(
    bias = (male - female)/(male + female),
    homophily = ifelse(bias < 0, "female", "male"),
    male_likelihood = (male - female)/male
  )