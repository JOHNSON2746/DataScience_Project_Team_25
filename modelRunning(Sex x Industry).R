df <- read.csv('/Users/zigeliang/Desktop/All/Data Science 2025S1/DS Project 1/datasets & Rmodel/testing_syn_salary(age x industry).csv')
summary(df)

# find the categorical vars 
# we also need to treat YEAR as the categorical var \
# becasue we want to compare the income between different time period
df$Sex <- as.factor(df$Sex)
df$Industry <- as.factor(df$Industry)
df$Year<- as.factor(df$Year)

# treat INCOME as a numerical value 
df$Median.Income.per.year <- as.numeric(gsub(",", "", df$Median.Income.per.year))
 
#1: run simple linear reg
basic.reg <- lm(Median.Income.per.year ~ Industry + Sex + Year, data = df)
summary(basic.reg)

#2: run linear reg sex * industry
reg.sex.x.industry <- lm(Median.Income.per.year ~ Industry * Sex + Year, data = df)
summary(reg.sex.x.industry)

# run linear reg sex * industry without year
reg.sex.x.industry.2 <- lm(Median.Income.per.year ~ Industry * Sex, data = df)
summary(reg.sex.x.industry.2)

#4 run two-way avowa (Sex * industry + Year)
two.anova.model.1 <- aov(Median.Income.per.year ~ Sex * Industry + Year, data = df)
summary(two.anova.model.1)

#5 run two-way avowa (Sex * industry)
two.anova.model.2<- aov(Median.Income.per.year ~ Sex * Industry, data = df)
summary(two.anova.model.2)


# compute sum of square to see the degree of influence of each features to the income
ss_total <- sum(9.561e+10, 6.686e+09, 4.271e+09, 4.441e+08)
industry_pct <- 9.561e+10 / ss_total
industry_pct
sex_pct <- 6.686e+09 / ss_total
sex_pct
interaction_pct <- 4.271e+09 / ss_total
interaction_pct






