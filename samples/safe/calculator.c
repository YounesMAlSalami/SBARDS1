/*
 * Simple Calculator Program
 * 
 * This is a safe C program that implements a basic calculator.
 * It performs addition, subtraction, multiplication, and division.
 * 
 * Author: Security Researcher
 * Date: May 15, 2025
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

#define MAX_INPUT 100
#define VERSION "1.0.0"

// Function prototypes
void print_welcome();
void print_help();
double calculate(double a, double b, char operator);
int is_valid_operator(char operator);
int get_input(char *input, int max_size);
void process_input(const char *input);
void clear_screen();

int main() {
    char input[MAX_INPUT];
    int running = 1;
    
    print_welcome();
    
    while (running) {
        printf("\nEnter calculation (or 'help', 'clear', 'exit'): ");
        if (get_input(input, MAX_INPUT) == 0) {
            continue;
        }
        
        // Check for commands
        if (strcmp(input, "exit") == 0 || strcmp(input, "quit") == 0) {
            running = 0;
            printf("Goodbye!\n");
            continue;
        } else if (strcmp(input, "help") == 0) {
            print_help();
            continue;
        } else if (strcmp(input, "clear") == 0) {
            clear_screen();
            continue;
        }
        
        // Process calculation
        process_input(input);
    }
    
    return 0;
}

// Print welcome message
void print_welcome() {
    printf("*************************************************\n");
    printf("*                                               *\n");
    printf("*            Simple Calculator v%s            *\n", VERSION);
    printf("*                                               *\n");
    printf("*************************************************\n");
    printf("\nThis is a safe calculator program with no malicious code.\n");
    printf("Type 'help' for instructions or 'exit' to quit.\n");
}

// Print help information
void print_help() {
    printf("\nSimple Calculator Help:\n");
    printf("------------------------\n");
    printf("Enter calculations in the format: number operator number\n");
    printf("For example: 5 + 3\n\n");
    printf("Supported operators:\n");
    printf("  + : Addition\n");
    printf("  - : Subtraction\n");
    printf("  * : Multiplication\n");
    printf("  / : Division\n");
    printf("  %% : Modulus (remainder)\n");
    printf("  ^ : Exponentiation\n\n");
    printf("Commands:\n");
    printf("  help  : Display this help message\n");
    printf("  clear : Clear the screen\n");
    printf("  exit  : Exit the calculator\n");
}

// Perform calculation
double calculate(double a, double b, char operator) {
    switch (operator) {
        case '+':
            return a + b;
        case '-':
            return a - b;
        case '*':
            return a * b;
        case '/':
            if (b == 0) {
                printf("Error: Division by zero\n");
                return 0;
            }
            return a / b;
        case '%':
            if (b == 0) {
                printf("Error: Modulus by zero\n");
                return 0;
            }
            return fmod(a, b);
        case '^':
            return pow(a, b);
        default:
            printf("Error: Invalid operator\n");
            return 0;
    }
}

// Check if operator is valid
int is_valid_operator(char operator) {
    return (operator == '+' || operator == '-' || operator == '*' || 
            operator == '/' || operator == '%' || operator == '^');
}

// Get user input safely
int get_input(char *input, int max_size) {
    if (fgets(input, max_size, stdin) == NULL) {
        printf("Error reading input\n");
        return 0;
    }
    
    // Remove newline character if present
    size_t len = strlen(input);
    if (len > 0 && input[len - 1] == '\n') {
        input[len - 1] = '\0';
    }
    
    return 1;
}

// Process user input for calculation
void process_input(const char *input) {
    double a, b, result;
    char operator;
    int items_read;
    
    // Parse input
    items_read = sscanf(input, "%lf %c %lf", &a, &operator, &b);
    
    if (items_read != 3) {
        printf("Error: Invalid input format. Expected 'number operator number'\n");
        return;
    }
    
    if (!is_valid_operator(operator)) {
        printf("Error: Invalid operator '%c'\n", operator);
        return;
    }
    
    // Perform calculation
    result = calculate(a, b, operator);
    
    // Display result
    printf("Result: %.6g\n", result);
}

// Clear the screen
void clear_screen() {
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif
    print_welcome();
}
