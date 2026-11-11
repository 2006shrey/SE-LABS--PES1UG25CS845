# Lab 5 — Reflection

**Project:** Public Transit Fare Calculator  
**Topic:** Static Code Analysis using Pylint, Bandit, and Flake8

*Note: The supplied lab handout asks students to answer reflection questions but does not include the exact questions. The following are suggested reflection prompts and answers based on the work completed. Replace them if your instructor provides specific questions.*

## 1. What did you learn from using Pylint, Bandit, and Flake8?

I learned that different static analysis tools check different aspects of a program. Pylint checks code quality and readability, Bandit identifies possible security problems, and Flake8 checks Python formatting and style. Using all three gave me a better understanding of how to review Python code.

## 2. What problems did you find and fix in the program?

The original program had several issues, including an unused import, a mutable default argument, an MD5 checksum, unsafe XML parsing, and an SSH configuration that automatically trusted unknown host keys. I also corrected naming, documentation, and formatting problems. These changes improved the code quality and security checks.

## 3. How did static analysis improve your code?

Static analysis helped me identify problems without having to find every issue by running the program. After making corrections, Pylint improved from 5.80/10 to 10.00/10, Bandit reported no issues, and Flake8 reported no violations. This showed me that static analysis is useful for improving code quality, security, and consistency.

## 4. Why is static code analysis important in software development?

Static code analysis is important because it can detect potential bugs, security weaknesses, and style problems early in development. Fixing these issues early can make software easier to maintain, safer, and more reliable. It also helps developers follow consistent coding standards.

