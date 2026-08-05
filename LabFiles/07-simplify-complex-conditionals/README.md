# Lab 07: Simplify Complex Conditionals

## Overview
This lab focuses on simplifying deeply nested and complex conditional logic. Learn to identify and refactor nested if-else structures into clearer, more maintainable code using GitHub Copilot.

## Key Objectives
- Identify deeply nested conditional logic
- Simplify nested if-else chains
- Apply guard clause pattern
- Use early returns to reduce nesting depth
- Improve code readability through logic simplification
- Maintain correctness during refactoring

## Lab Structure
```
07-simplify-complex-conditionals/
├── ECommercePricingEngine/       # Complex pricing logic
│   ├── ECommercePricingDemo.cs   # Pricing scenarios (deep nesting)
│   ├── SecurityTest.cs           # Security validation
│   └── obj/                      # Build artifacts
├── LoanApprovalWorkflow/         # Complex approval logic
│   ├── LoanApprovalDemo.cs       # Approval decision tree (8+ levels)
│   ├── SecurityTest.cs           # Validation tests
│   └── obj/                      # Build artifacts
```

## Concepts Demonstrated
- Guard clauses
- Early returns
- Conditional extraction
- Ternary operators (appropriate use)
- Switch expressions
- Strategy pattern application
- Decision table refactoring

## Complex Conditional Patterns

### Pattern 1: Deeply Nested If-Else (8+ Levels)
```csharp
// BEFORE: 8 levels deep
if (condition1)
{
    if (condition2)
    {
        if (condition3)
        {
            if (condition4)
            {
                if (condition5)
                {
                    if (condition6)
                    {
                        if (condition7)
                        {
                            if (condition8)
                            {
                                // Buried logic
                            }
                        }
                    }
                }
            }
        }
    }
}

// AFTER: Guard clauses at top
if (!condition1) return;
if (!condition2) return;
if (!condition3) return;
// ... continue with guard clauses
// Main logic follows naturally
```

### Pattern 2: Complex Boolean Logic
```csharp
// BEFORE: Hard to parse
if ((a && b) || (c && d) || (e && f && !g))
{
    // Complex condition obscures intent
}

// AFTER: Extract to named method
if (IsEligibleForDiscount())
{
    // Clear intent
}

private bool IsEligibleForDiscount()
{
    return (IsPremiumMember() && IsLargeOrder()) ||
           (IsNewCustomer() && HasCoupon()) ||
           (IsLoyalCustomer() && IsSpecialEvent() && !IsBlocked());
}
```

### Pattern 3: Multiple Early Returns vs. Deep Nesting
```csharp
// BEFORE: Single deeply nested path
if (creditScore >= 740)
{
    if (income >= threshold)
    {
        if (employment >= 2)
        {
            approval = ApprovalStatus.Approved;
        }
        else { approval = ApprovalStatus.Declined; }
    }
    else { approval = ApprovalStatus.Declined; }
}
else { approval = ApprovalStatus.Declined; }

// AFTER: Early exits
if (creditScore < 740) return ApprovalStatus.Declined;
if (income < threshold) return ApprovalStatus.Declined;
if (employment < 2) return ApprovalStatus.Declined;
return ApprovalStatus.Approved;
```

## Nesting Depth Guidelines
- **Level 0-2**: Acceptable
- **Level 3-4**: Consider refactoring
- **Level 5+**: Refactor immediately

## Simplification Techniques
1. **Guard Clauses**: Exit early for invalid conditions
2. **Extract Conditions**: Name complex boolean expressions
3. **Replace Nested If with Switch**: For multiple discrete values
4. **Replace Conditional with Polymorphism**: For complex type-based logic
5. **Consolidate Duplicate Conditions**: Remove repeated checks
6. **Decompose Conditionals**: Break into smaller methods

## Getting Started
1. Navigate to the lab directory
2. Open `ECommercePricingDemo.cs` or `LoanApprovalDemo.cs`
3. Review the nested conditional structures
4. Use GitHub Copilot to:
   - Suggest simplification techniques
   - Extract complex conditions
   - Apply guard clause pattern
   - Name extracted methods
5. Test refactored code against original behavior

## Expected Outcomes
- Maximum nesting depth of 3 levels
- Each condition has clear intent
- Guard clauses at function entry
- Named extraction methods for complex logic
- Improved readability without behavioral change
- Easier to test individual conditions

## Real-World Examples from Lab
- **ECommercePricingDemo**: 8+ levels of discount calculation logic
- **LoanApprovalDemo**: 8+ levels of approval decision tree

Each contains complex nested conditions perfect for learning simplification patterns.

## Related Concepts
- Cyclomatic complexity metrics
- Code readability
- Maintainability index
- Decision coverage testing
- Boolean algebra
- Clean Code principles
