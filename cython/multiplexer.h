

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

static bool **generate_data(int bits)
{
    unsigned int i, j, n, n_addr, addr;
    bool **data;

    n = 1 << bits;
    n_addr = floor(log(bits) / log(2));

    data = malloc(n * sizeof(bool *));
    data[0] = malloc((bits + 1) * n * sizeof(bool));
    for (i = 0; i < n; ++i) data[i] = data[0] + i * (bits + 1);

    for (i = 0; i < n; ++i) {
        for (j = 0; j < bits; ++j) data[i][j] = (i & (1 << j)) != 0;

        addr = 0;
        for (j = 0; j < n_addr; ++j) addr += (1 << j) * data[i][j];
        data[i][bits] = data[i][addr + n_addr];
    }

    return data;
}

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

static bool function(char *token, bool *output, int *n_o)
{

    bool q, t, f;
    if (strncmp(token, "if", 2) == 0) {
        q = pop_bit(output, n_o);
        t = pop_bit(output, n_o);
        f = pop_bit(output, n_o);
        return q ? t : f;
    }

    if (strncmp(token, "not", 3) == 0) return !(pop_bit(output, n_o));

    fprintf(stderr, "ERROR: unknown function %s\n", token);
    exit(0);
    return false;
}

static bool is_operater(char *token)
{
    if (strncmp(token, "and", 3) == 0) return true;
    if (strncmp(token, "or", 2) == 0) return true;
    return false;
}

static int operater_precedence(char *token)
{
    if (strncmp(token, "or", 2) == 0) return 1;
    if (strncmp(token, "and", 3) == 0) return 2;
    return 0;
}

static bool operater(char *token, bool a, bool b)
{
if (strncmp(token, "and", 3) == 0) return a && b;
if (strncmp(token, "or", 2) == 0) return a || b;

fprintf(stderr, "ERROR: unknown function %s\n", token);
exit(0);
return false;
}

static bool execute_mul(char *buffer, bool *data)
{
    char *token, **ops, *o1, *o2;
    bool *output, res;
    int n_o, n_q, sz_o, sz_q;;

    sz_o = 8192;
    sz_q = 8192;
    ops = malloc(sz_q * sizeof(char *));
    output = malloc(sz_o * sizeof(bool));
    n_o = n_q = 0;


    for (token = strtok(buffer, " "); token; token = strtok(NULL, " ")) {

        // printf("current dealing with token  --%s-- \n",token );
        // if ((strncmp(token, "s", 1) == 0) ||(strncmp(token, "i", 1) == 0)){
        if (strncmp(token, "i", 1)  == 0){

            // printf("token dealed 1 --%s--\n",token );
            push_bit(data[atoi(token + 1)], &output, &n_o, &sz_o);
        } else if (is_function(token)) {
            // printf("token dealed 2  --%s--\n",token );
            push_op(token, &ops, &n_q, &sz_q);
        } else if (strncmp(token, ",", 1) == 0) {

            // printf("token dealed 3 --%s--\n",token );
            while (strncmp(peek_op(ops, n_q), "(", 1) != 0) {
                token = pop_op(ops, &n_q);
                if (is_operater(token)) {
                    push_bit(operater(token, pop_bit(output, &n_o), pop_bit(output, &n_o)), &output, &n_o, &sz_o);
                } else {
                    push_bit(function(token, output, &n_o), &output, &n_o, &sz_o);
                }
            }
        } else if (is_operater(token)) {

            // printf("token dealed 4 --%s--\n",token );
            o1 = token;
            while (peek_op(ops, n_q) && is_operater(peek_op(ops, n_q))) {
                o2 = peek_op(ops, n_q);
                if (operater_precedence(o1) <= operater_precedence(o2)) {
                    push_bit(operater(pop_op(ops, &n_q), pop_bit(output, &n_o), pop_bit(output, &n_o)), &output, &n_o, &sz_o);
                } else {
                    break;
                }
            }
            push_op(o1, &ops, &n_q, &sz_q);
        } else if (strncmp(token, "(", 1) == 0) {

            // printf("token dealed  5 --%s--\n",token );
            push_op(token, &ops, &n_q, &sz_q);
        } else if (strncmp(token, ")", 1) == 0) {
            while (strncmp(peek_op(ops, n_q), "(", 1) != 0) {
                token = pop_op(ops, &n_q);
                if (is_operater(token)) {
                    push_bit(operater(token, pop_bit(output, &n_o), pop_bit(output, &n_o)), &output, &n_o, &sz_o);
                } else {
                    push_bit(function(token, output, &n_o), &output, &n_o, &sz_o);
                }
            }

            token = pop_op(ops, &n_q); /* pop the left bracket */

            if (peek_op(ops, n_q) && is_function(peek_op(ops, n_q))) {
                push_bit(function(pop_op(ops, &n_q), output, &n_o), &output, &n_o, &sz_o);
            }
        } else {
            fprintf(stderr, "ERROR: unknown symbol: %s\n", token);
            exit(EXIT_FAILURE);
        }
    }

    while ((token = pop_op(ops, &n_q))) {
        // printf("round --%s--\n",token );
        if (is_operater(token)) {
            push_bit(operater(token, pop_bit(output, &n_o), pop_bit(output, &n_o)), &output, &n_o, &sz_o);
        } else {
            push_bit(function(token, output, &n_o), &output, &n_o, &sz_o);
        }
    }

    res = output[0];

    free(output);
    free(ops);

//    printf("%s\n",btoa(res) );
    return res;
}

static int measure(char *ind, bool **X, int n, int b)
{
    int i;
    bool q, r;
    int score;
    char *buffer;

//    if (!ind->mapped) return n;

    score = 0;
    for (i = 0; i < n; ++i) {
        buffer = malloc(strlen(ind) + 1);
        strcpy(buffer, ind);

        q = X[i][b];
        r = execute_mul(buffer, X[i]);
        // q is real, r is prediction, if prediction is correct, get one score.

        score += (q == r) ? 1 : 0;

        free(buffer);
    }

    return (1 << b) - score;
    // return 2^n -score to make this a minimize problem
}



int evaluate_multiplexer(char *solution, int input_size){
    int i;
    struct details details;

    details.b = input_size + (1<<input_size);
    details.n = 1 << details.b;
    details.data = generate_data(details.b);

    return measure(solution,details.data, details.n, details.b);
}