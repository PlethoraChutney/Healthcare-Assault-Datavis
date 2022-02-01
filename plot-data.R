library(tidyverse)
library(ggforce)
library(extrafont)
loadfonts(device = 'win')

assault_data <- read_csv('all_state_data.csv', col_types = 'cddd')
felony_data <- read_csv('felony-assault.csv', col_types = 'clc')

data <- left_join(assault_data, felony_data, by = 'state') %>% 
  select(-`source/notes`)

data <- data %>% 
  pivot_longer(cols = c('all_healthcare', 'hospitals', 'nursing_and_res_care'), names_to = 'Industry', values_to = 'Assaults')

data %>% 
  drop_na() %>% 
  mutate(is_felony = if_else(is_felony, 'Felony', 'Misdemeanor')) %>% 
  mutate(is_felony = fct_relevel(factor(is_felony), 'Misdemeanor', 'Felony')) %>% 
  mutate(Industry = case_when(
    Industry == 'all_healthcare' ~ 'All Healthcare',
    Industry == 'hospitals' ~ 'Hospitals',
    Industry == 'nursing_and_res_care' ~ 'Nursing and Residential Care'
  )) %>% 
  ggplot(aes(x = is_felony, y = Assaults)) +
  theme_minimal() +
  theme(text = element_text(family = 'Lato')) +
  geom_boxplot(
    color = 'grey',
    outlier.shape = NA
    ) +
  geom_sina(maxwidth = 0.5) +
  facet_grid(cols = vars(Industry)) +
  labs(
    title = 'Assaults per 100 workers in three healthcare industries',
    subtitle = 'Number of illnesses and injuries divided by the total hours worked,\nadjusted to the equivalent of 100 full-time employees',
    y = 'Total Recordable Cases',
    x = element_blank(),
    caption = 'Sources:\nAssault case numbers are 2020 data, from the BLS: https://www.bls.gov/iif/oshstate.htm\nLaw data is from the actual text of laws on the books as of 2014, from onlabor.org, included in github repo\nRich Posert, https://github.com/PlethoraChutney/Healthcare-Assault-Datavis'
  )
ggsave('assault_data.png', width = 8, height = 6)


