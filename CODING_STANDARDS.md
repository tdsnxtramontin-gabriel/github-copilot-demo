# Coding Standards & Comment Guidelines

This document establishes standardized commenting and documentation practices across all labs to ensure consistency and clarity.

## Comment Types and Formats

### 1. XML Documentation Comments (C#)

Used for public APIs, classes, and methods. These generate IntelliSense and documentation.

```csharp
/// <summary>
/// Brief description of what this does.
/// </summary>
/// <param name="parameter">Description of parameter</param>
/// <returns>Description of return value</returns>
public void MethodName(string parameter)
{
    // Implementation
}
```

**Example:**
```csharp
/// <summary>
/// Validates applicant financial data for security and completeness
/// </summary>
/// <param name="applicant">The applicant to validate</param>
/// <returns>True if applicant data is valid, false otherwise</returns>
private bool IsValidApplicantData(Applicant applicant)
{
    // Implementation
}
```

### 2. Docstrings (Python)

Used for modules, classes, and functions. Generates documentation and type hints.

```python
def function_name(parameter: str) -> bool:
    """
    Brief description of what this does.
    
    Args:
        parameter: Description of the parameter
        
    Returns:
        Description of the return value
        
    Raises:
        ValueError: When input is invalid
    """
    # Implementation
```

**Example:**
```python
def validate_applicant_data(applicant: Applicant) -> bool:
    """
    Validates applicant financial data for security and completeness.
    
    Args:
        applicant: The applicant object to validate
        
    Returns:
        True if applicant data is valid, false otherwise
    """
    # Implementation
```

### 3. Section Comments

Mark major logical sections within methods/functions:

```csharp
// SECURITY: Input validation to prevent null reference attacks
if (user == null)
{
    throw new ArgumentNullException(nameof(user), "User cannot be null");
}

// DATA PROCESSING: Calculate base discount from membership tier
decimal baseDiscount = CalculateBaseDiscount(user.Membership);

// BUSINESS LOGIC: Apply seasonal event multipliers
if (order.ActiveEvent == SeasonalEvent.BlackFriday)
{
    baseDiscount *= 1.5m;
}
```

### 4. Inline Comments

Explain complex logic or non-obvious decisions:

```csharp
// Cap coupon value at 50% to maintain profit margins
decimal couponValue = Math.Min(50, order.Coupon.Value);

// Check if 2+ years of employment to establish stability
if (applicant.EmploymentYears >= 2)
{
    // Process qualified applicant
}
```

### 5. Security Annotations

Mark all security-sensitive code clearly:

```csharp
// SECURITY: Bounds checking to prevent overflow attacks
private const decimal MAX_DISCOUNT_PERCENT = 95m;

// SECURITY: Safe division to prevent division by zero
private double SafeDivide(double numerator, double denominator)
{
    if (Math.Abs(denominator) < 0.01)
        return 0;
    
    return numerator / denominator;
}
```

## Comment Standards by Category

### Security-Related
```
// SECURITY: [Description of security measure]
/// <summary>Security: [Purpose of validation]</summary>
```

### Performance-Related
```
// PERFORMANCE: [Optimization rationale]
/// <summary>Optimized for: [Specific use case]</summary>
```

### Business Logic
```
// BUSINESS LOGIC: [Explanation of complex calculation]
// Level N: [Nested condition explanation]
```

### TODO/FIXME
```
// TODO: [Future enhancement]
// FIXME: [Known issue with workaround]
// HACK: [Temporary solution with explanation]
```

## Level Hierarchy for Complex Conditions

For deeply nested conditionals, use level annotations:

```csharp
// Level 1: Credit Score Primary Assessment
if (applicant.CreditScore >= 740)
{
    // Level 2: Income Verification and Stability
    if (applicant.VerifiedIncome >= applicant.AnnualIncome * 0.95)
    {
        // Level 3: Employment Stability
        if (applicant.EmploymentStatus == EmploymentType.Salaried)
        {
            // Level 4: Debt Service Coverage
            if (applicant.DebtToIncomeRatio <= 0.36)
            {
                // Process approval
            }
        }
    }
}
```

## Do's and Don'ts

### ✅ DO:
- Write clear, concise comments
- Explain *why*, not just *what* (code shows what)
- Use consistent terminology
- Mark security and performance concerns
- Keep comments synchronized with code
- Use professional, active voice

### ❌ DON'T:
- State the obvious: `i++; // increment i`
- Leave outdated comments
- Write novels; keep it brief
- Use profanity or sarcasm
- Comment bad code; refactor it instead
- Use abbreviations without explanation

## Examples

### Bad Comment:
```csharp
// iterate through users
foreach (var user in users)
{
    // check if active
    if (user.IsActive)
    {
        // do something
        ProcessUser(user);
    }
}
```

### Good Comment:
```csharp
// BUSINESS LOGIC: Process only active users for monthly billing
foreach (var user in users)
{
    if (user.IsActive)
    {
        ProcessUser(user);
    }
}
```

## Documentation Links

- **C# XML Documentation**: https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/xmldoc/
- **Python Docstrings**: https://www.python.org/dev/peps/pep-0257/
- **Clean Code**: Robert C. Martin's "Clean Code" Chapter 4
- **Code Comments**: https://refactoring.guru/refactoring/techniques/extract-method

## Enforcement

- Code reviews should validate comment quality
- IDE formatters should enforce spacing and structure
- Documentation generation tools validate XML/docstring format
- Comments should be treated as code; maintain them carefully

## Lab-Specific Conventions

### Labs 01-04 (Python)
- Use docstrings for all functions
- Use section comments for major logic blocks
- Include type hints in all function signatures

### Labs 05-09 (C#)
- Use XML documentation for public types
- Use level annotations for nested conditions
- Mark all security-related code explicitly
- Include meaningful variable names to reduce comment need

---

**Remember:** Good comments enable future maintainers (including your future self) to understand not just what code does, but why it does it that way.
