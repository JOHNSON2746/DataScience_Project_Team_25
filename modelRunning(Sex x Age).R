df <- read.csv('/Users/zigeliang/Desktop/All/Data Science 2025S1/DS Project 1/datasets & Rmodel/testing_syn_salary(age x gender)2.csv')
df <- df[, colSums(is.na(df)) < nrow(df)]

# find the categorical vars 
# we also need to treat YEAR as the categorical var \
# becasue we want to compare the income between different time period
df$SEX <- as.factor(df$SEX)
df$Age.GROUP <- as.factor(df$Age.GROUP)
df$YEAR <- as.factor(df$YEAR)

# treat INCOME as a numerical value 
df$INCOME <- as.numeric(gsub(",", "", df$INCOME))

colnames(df)

# Run linear Reg (without interaction)
basic.reg <- lm(INCOME ~ SEX + Age.GROUP + YEAR, data = df)
summary(basic.reg)

# linear reg (sex * Age.GROUP )
interact.sex.age <- lm(INCOME ~ SEX * Age.GROUP + YEAR, data = df)
summary(interact.sex.age)

# Two-way anova (with interaction)
two.anova.model <- aov(INCOME ~ SEX * Age.GROUP, data = df)
summary(two.anova.model)


# Age + Sex regression, used to generate the income for Syn dataset 
reg <- lm(INCOME ~ SEX + Age.GROUP, data = df)
summary(reg)

reg$coefficients

# Age * Sex regression
reg.age.sex <- lm(INCOME ~ SEX*Age.GROUP, data = df)
summary(reg.age.sex)
