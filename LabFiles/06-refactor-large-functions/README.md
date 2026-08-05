# Lab 06: Refactor Large Functions

## Overview
This lab demonstrates how to identify and refactor large, complex functions into smaller, more maintainable units. Learn to break down monolithic methods using GitHub Copilot while maintaining functionality and improving readability.

## Key Objectives
- Identify functions that are too large (>50 lines)
- Extract logical units into separate functions
- Apply Single Responsibility Principle
- Improve code readability and testability
- Maintain functionality during refactoring
- Use meaningful function names to document intent

## Lab Structure
```
06-refactor-large-functions/
├── ECommerceOrderProcessing/     # E-commerce order handling
│   ├── src/                      # Source code
│   │   ├── ECommerce.Console/    # CLI application
│   │   ├── ECommerce.ApplicationCore/  # Business logic
│   │   └── ECommerce.Infrastructure/   # Data access
│   └── tests/                    # Unit tests
├── ServerLogAnalysisUtility/     # Log analysis tool
│   ├── Program.cs
│   ├── LogAnalyzer.cs
│   └── OutputFormatter.cs
```

## Concepts Demonstrated
- Method extraction
- Function decomposition
- Cyclomatic complexity reduction
- Scope and parameter optimization
- Return type simplification
- Guard clauses
- Helper method patterns

## Large Function Patterns to Refactor

### Pattern 1: Multiple Responsibilities
```csharp
// BEFORE: One function doing many things
public void ProcessOrder(Order order)
{
    // Validation (20+ lines)
    // Calculation (15+ lines)
    // Update database (10+ lines)
    // Send notification (10+ lines)
}

// AFTER: Separated concerns
public void ProcessOrder(Order order)
{
    ValidateOrder(order);
    CalculateTotal(order);
    UpdateDatabase(order);
    SendNotification(order);
}
```

### Pattern 2: Deep Nesting
```csharp
// BEFORE: Nested conditionals
if (condition1)
{
    if (condition2)
    {
        if (condition3)
        {
            // Deep logic
        }
    }
}

// AFTER: Guard clauses
if (!condition1) return;
if (!condition2) return;
if (!condition3) return;
// Execute logic
```

### Pattern 3: Complex Logic
Extract calculations into helper functions with clear names that document intent.

## Getting Started
1. Navigate to the lab directory
2. Open projects in your IDE
3. Review the main program files
4. Use GitHub Copilot to:
   - Suggest function decomposition opportunities
   - Extract helper methods
   - Simplify conditional logic
   - Improve variable naming
5. Run tests to ensure refactoring maintains behavior

## Refactoring Steps
1. **Identify** functions exceeding 50 lines
2. **Analyze** to find logical sections
3. **Extract** each section into a new method
4. **Name** extracted methods to describe their purpose
5. **Test** to verify functionality is preserved
6. **Iterate** to improve readability further

## Expected Outcomes
- Smaller functions (20-30 lines maximum)
- Each function has single responsibility
- Improved code maintainability
- Better test coverage capability
- Clear, descriptive function names
- Reduced cyclomatic complexity

## Refactoring Techniques
- **Extract Method**: Move code to new function
- **Replace Temp with Query**: Calculate values on demand
- **Introduce Parameter Object**: Group related parameters
- **Replace Conditional with Polymorphism**: Use inheritance instead of if-else
- **Simplify Boolean Logic**: Extract complex conditions

## Related Concepts
- Clean Code principles
- SOLID principles (especially SRP)
- Cyclomatic complexity
- Code metrics
- Refactoring patterns
- Unit testing
