# Evaluation Summary
- Total tables: **7**; flagged for drill-down: **6**.
- Mean TVD (overall / flagged): **0.1348 / 0.1488**.
- Thresholds used: TVD_mean>0.06, MaxAbsDev>0.08, zero/only rates ≥10%, direction bias ≥70%.

## Likely Causes (counts of affected tables)
- Label alignment / enumeration (only-in-sample ≥10%): **1**
- Missing support / rare categories (zero-coverage ≥10%): **0**
- Directional bias (≥70% of nontrivial gaps move same way): **0**
- Global miscalibration (high TVD without coverage issues): **5**

## Top Tables to Address
- **sector_gender_transformed_v3.csv** | tvd_mean=0.2745, max_abs_dev_max=0.3006 | reason=tvd_mean>0.06 & max_abs_dev_max>0.08 | suggested=label_alignment_normalization, priority=High
- **industry_gender_transformed_v3.csv** | tvd_mean=0.2092, max_abs_dev_max=0.0790 | reason=tvd_mean>0.06 | suggested=genderwise_calibration_raking, priority=High
- **age_gender_transformed_v3.csv** | tvd_mean=0.1390, max_abs_dev_max=0.0549 | reason=tvd_mean>0.06 | suggested=genderwise_calibration_raking, priority=High
- **arrivalGroup_gender_transformed.csv** | tvd_mean=0.1027, max_abs_dev_max=0.1052 | reason=tvd_mean>0.06 & max_abs_dev_max>0.08 | suggested=genderwise_calibration_raking, priority=High
- **visaGroup_gender_transformed.csv** | tvd_mean=0.0976, max_abs_dev_max=0.0625 | reason=tvd_mean>0.06 | suggested=genderwise_calibration_raking, priority=High

## Next Steps (from auto plan)
- See `modification_plan.csv` for per-(table, gender, feature) nudges (`suggested_delta_pp`, in pp).
- Process

## Note on Income Granularity
- Targets with gender × income were marginalized over income to match gender-only comparisons. If large, consistent gaps persist across many tables, consider upgrading to P(c|g,i) for finer calibration.