---
name: code-review
description: Systematic approach to reviewing code quality and best practices
version: 1.0.0
author: DB-GPT Team
skill_type: coding
tags: [code, review, quality]
allowed-tools: 
license: MIT
---

# Code Review Skill

## When to Use
- User requests code review
- Need to evaluate code quality
- Looking for bugs or issues
- Checking for best practices
- Assessing security vulnerabilities
- Reviewing performance considerations

## Code Review Checklist

### Functionality
- [ ] Does the code implement the required features?
- [ ] Are edge cases handled properly?
- [ ] Does it handle errors gracefully?
- [ ] Are there any obvious bugs?

### Code Quality
- [ ] Is the code readable and well-structured?
- [ ] Are variable and function names descriptive?
- [ ] Is there unnecessary code duplication?
- [ ] Are comments clear and helpful?

### Performance
- [ ] Are there any performance bottlenecks?
- [ ] Are data structures chosen appropriately?
- [ ] Are there inefficient loops or operations?
- [ ] Is caching appropriate?

### Security
- [ ] Are there any security vulnerabilities?
- [ ] Is user input properly validated?
- [ ] Are sensitive data handled correctly?
- [ ] Are there injection risks?

### Best Practices
- [ ] Does it follow language conventions?
- [ ] Are common patterns used appropriately?
- [ ] Is the code modular and reusable?
- [ ] Are dependencies managed properly?

## Review Structure

### 1. Summary
- Brief overview of what the code does
- Overall impression
- Key strengths and weaknesses

### 2. Issues by Category

#### Critical Issues
```markdown
**Issue**: [Brief description]
**Location**: [File:Line]
**Impact**: [Why this matters]
**Suggestion**: [How to fix]
```

#### Style and Convention Issues
```markdown
**Issue**: [Brief description]
**Location**: [File:Line]
**Suggestion**: [How to fix]
```

#### Optimization Opportunities
```markdown
**Opportunity**: [Brief description]
**Location**: [File:Line]
**Current**: [Current approach]
**Suggested**: [Better approach]
**Impact**: [Expected improvement]
```

#### Best Practices
```markdown
**Suggestion**: [Improvement]
**Location**: [File:Line]
**Reason**: [Why this is better]
```

### 3. Positive Feedback
- Well-implemented features
- Good practices observed
- Notable strengths

### 4. Recommendations
- Prioritized list of improvements
- Long-term suggestions
- Additional resources

## Common Patterns to Check

### Python
- Use list comprehensions appropriately
- Follow PEP 8 guidelines
- Use context managers (`with` statements)
- Implement `__str__` and `__repr__`
- Use type hints
- Handle exceptions properly
- Avoid mutable default arguments

### JavaScript/TypeScript
- Use `const` and `let` instead of `var`
- Use arrow functions appropriately
- Handle promises correctly
- Avoid implicit globals
- Use modern ES6+ features
- Properly scope variables

### SQL
- Use parameterized queries
- Index common query columns
- Avoid SELECT *
- Use appropriate JOIN types
- Handle NULL values correctly
- Optimize subqueries

## Security Checks

### Input Validation
```python
# Bad
user_input = request.form.get('data')
# Direct use without validation

# Good
user_input = request.form.get('data', '').strip()
if not is_valid_input(user_input):
    raise ValueError("Invalid input")
```

### SQL Injection
```python
# Bad
query = f"SELECT * FROM users WHERE name = '{name}'"

# Good
query = "SELECT * FROM users WHERE name = %s"
cursor.execute(query, (name,))
```

### XSS Prevention
```python
# Bad
return f"<div>{user_content}</div>"

# Good
from markupsafe import escape
return f"<div>{escape(user_content)}</div>"
```

## Code Review Principles

1. **Be Constructive**: Focus on improvement, not criticism
2. **Be Specific**: Point to exact locations and issues
3. **Provide Context**: Explain why something is a problem
4. **Offer Solutions**: Suggest how to fix issues
5. **Be Thorough**: Don't miss important issues
6. **Be Timely**: Review code while it's fresh
7. **Be Respectful**: Consider the author's perspective

## Performance Considerations

### Time Complexity
- Identify O(n²) operations that could be O(n log n) or O(n)
- Check nested loops
- Look for unnecessary repeated computations

### Space Complexity
- Check for memory leaks
- Consider using generators instead of lists
- Release resources when done

### Database Queries
- N+1 query problems
- Missing indexes
- Unnecessary joins
- Fetching too much data

## Example Review Output

```markdown
# Code Review: user_authentication.py

## Summary
The code implements user authentication with JWT tokens. Overall, it's well-structured
but has some security concerns and opportunities for improvement.

## Critical Issues

**Issue**: Hardcoded secret key
**Location**: Line 15
**Impact**: Security vulnerability - JWT secret should be in environment
**Suggestion**: Move to `os.environ.get('JWT_SECRET_KEY')`

**Issue**: SQL injection vulnerability
**Location**: Line 42
**Impact**: Attackers could execute arbitrary SQL
**Suggestion**: Use parameterized queries

## Style and Convention Issues

**Issue**: Missing type hints
**Location**: Functions throughout
**Suggestion**: Add type hints for better IDE support and documentation

## Optimization Opportunities

**Opportunity**: Repeated password hashing
**Location**: Line 58
**Current**: Hashing password on every validation
**Suggested**: Cache hashed password or use constant-time comparison
**Impact**: Performance improvement for authentication

## Positive Feedback
- Good error handling overall
- Clean function separation
- Good use of logging

## Recommendations (Prioritized)
1. Fix security vulnerabilities immediately
2. Add comprehensive tests
3. Add type hints throughout
4. Consider using a password hashing library
5. Add rate limiting
```

## Resources

- [PEP 8 - Style Guide](https://peps.python.org/pep-0008/)
- [Clean Code](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
- [Effective Java](https://www.amazon.com/Effective-Java-Joshua-Bloch/dp/0134685997)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
