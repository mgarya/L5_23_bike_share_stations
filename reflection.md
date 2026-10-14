# Reflection — Lab 5: Static Code Analysis

> **Important:** The repository README refers to four reflection questions in the lab handout, but the handout itself is not included in the repository. These are draft answers covering likely learning outcomes. Replace or rearrange them to match the exact questions in your handout.

## 1. What did the static-analysis tools help identify?

Pylint helped identify code-quality and maintainability problems, including naming conventions, missing documentation, unused variables, and unclear function behavior. Flake8 highlighted PEP 8 formatting and style violations. Bandit helped review security-sensitive patterns, particularly unsafe SQL construction and use of non-cryptographic randomness for a PIN. The tools complement one another because each focuses on somewhat different classes of problems.

## 2. Which issue was most important, and why?

The SQL query built through string concatenation was the most important security issue. Station names were inserted directly into SQL, so unusual or malicious input could alter the statement, and ordinary names containing quotes could cause failures. Replacing concatenation with parameterized queries separates SQL instructions from values and makes input handling safer.

## 3. How were the issues fixed, and how was behavior preserved?

I replaced SQL string concatenation with parameterized statements, used `secrets` for PIN generation, removed the mutable default list, checked for missing database rows, and removed the broad exception handler that hid reset errors. I also renamed functions to snake_case, added docstrings, removed an unused variable, and made unsuccessful bike rentals return `False`. I retained the core operations: station registration, bike rental, PIN generation, full-station lookup, station reset, and bike availability checking. I ran the program and the analysis tools again after making the changes.

## 4. What did you learn, and what are the limitations of static analysis?

Static analysis can detect suspicious patterns before a program is used, but a warning is not automatically a real bug and a clean report does not prove that software is correct or secure. Tools may miss logical errors and runtime edge cases. Tests and manual code review are still needed. In this exercise, combining tool output with review of the functions helped identify both style issues and behavior/security risks.
