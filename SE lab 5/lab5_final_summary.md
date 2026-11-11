# Lab 5 — Static Code Analysis: Final Summary

## Project
Public Transit Fare Calculator

## Objective
Use Pylint, Bandit, and Flake8 to identify code-quality, security, and formatting issues in `fare_calculator.py`, then improve the code and rerun the tools.

## Final results

| Analysis tool | Initial result | Final result |
|---|---:|---:|
| Pylint | 5.80/10 | 10.00/10 |
| Bandit | 5 findings | 0 findings |
| Flake8 | 20 violations | 0 violations |

## Commands used

```bash
python fare_calculator.py
python -m pylint fare_calculator.py
python -m bandit -r fare_calculator.py
python -m flake8 fare_calculator.py
```

## Conclusion
After the corrections, Pylint reported 10.00/10, Bandit reported no issues, and Flake8 produced no violations. The program also ran successfully. The test output still showed a negative travel-card balance and floating-point precision in a top-up calculation; these behaviours should be checked against the required fare-system rules.

## Reflection questions
The four reflection questions were not present in the supplied handout. Add answers after obtaining the exact questions from the instructor or course platform.
