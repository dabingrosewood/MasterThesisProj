#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include <unistd.h>

#include <float.h>
#include <math.h>
#include <string.h>

#include <sys/time.h>


#define btoa(x) ((x)?"true":"false")
struct details {
    bool **data;

    int n;
    int b;
};

static void free_data(bool **data)
{
    free(data[0]);
    free(data);
}

static void push_bit(bool val, bool **stack, int *n, int *s)
{
    if (*n >= *s) {
        while (*s <= *n) *s *= 2;
        *stack = realloc(*stack, *s * sizeof(bool));
    }

    (*stack)[(*n)++] = val;
}

static bool pop_bit(bool *stack, int *n)
{
    if (*n == 0) {
        fprintf(stderr, "ERROR: no bits on stack to pop.\n");
        exit(EXIT_FAILURE);
    }

    return stack[--(*n)];
}

static void push_op(char *op, char ***stack, int *n, int *s)
{
    if (*n >= *s) {
        while (*s <= *n) *s *= 2;
        *stack = realloc(*stack, *s * sizeof(char *));
    }

    (*stack)[(*n)++] = op;
}

static char *peek_op(char **stack, int n)
{
    return (n == 0) ? NULL : stack[n - 1];
}

static char *pop_op(char **stack, int *n)
{
    return ((*n) == 0) ? NULL : stack[--(*n)];
}

static bool is_function(char *token)
{
    if (strncmp(token, "if", 2) == 0) return true;
    if (strncmp(token, "not", 3) == 0) return true;
    return false;
}
