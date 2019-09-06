

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include <unistd.h>

#include <float.h>
#include <math.h>
#include <string.h>

#include <sys/time.h>
//#include "share_func.h"



static bool **generate_data_parity(int bits)
{
    unsigned int i, j, n, sum;
    bool **data;

    n = 1 << bits;

    data = malloc(n * sizeof(bool *));
    data[0] = malloc((bits + 1) * n * sizeof(bool));
    for (i = 0; i < n; ++i) data[i] = data[0] + i * (bits + 1);

    for (i = 0; i < n; ++i) {
        sum = 0;
        for (j = 0; j < bits; ++j) if ((data[i][j] = (i & (1 << j)) != 0)) sum++;
        data[i][bits] = (sum % 2) == 0;
    }

    return data;
}







static bool function_parity(char *token, bool *output, int *n_o)
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

static bool is_operator_parity(char *token)
{
    if (strncmp(token, "and", 3) == 0) return true;
    if (strncmp(token, "or", 2) == 0) return true;

    if (strncmp(token, "nand", 4) == 0) return true;
    if (strncmp(token, "nor", 3) == 0) return true;

    if (strncmp(token, "xor", 3) == 0) return true;
    if (strncmp(token, "nxor", 4) == 0) return true;

    return false;
}

static int operator_parity_precedence(char *token)
{
    if (strncmp(token, "or", 2) == 0) return 1;
    if (strncmp(token, "nor", 2) == 0) return 1;
    if (strncmp(token, "xor", 3) == 0) return 2;
    if (strncmp(token, "nxor", 4) == 0) return 2;
    if (strncmp(token, "and", 3) == 0) return 3;
    if (strncmp(token, "nand", 3) == 0) return 3;
    return 0;
}

static bool operator_parity(char *token, bool a, bool b)
{
    if (strncmp(token, "and", 3) == 0) return a && b;
    if (strncmp(token, "or", 2) == 0) return a || b;

    if (strncmp(token, "nand", 4) == 0) return !(a && b);
    if (strncmp(token, "nor", 3) == 0) return !(a || b);

    if (strncmp(token, "xor", 3) == 0) return !(a && b) && (a || b);
    if (strncmp(token, "nxor", 4) == 0) return (a && b) || !(a || b);

    fprintf(stderr, "ERROR: unknown function %s\n", token);
    exit(0);
    return false;
}

static bool execute_parity(char *buffer, bool *data)
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
        if (strncmp(token, "b", 1) == 0) {
            push_bit(data[atoi(token + 1)], &output, &n_o, &sz_o);
        } else if (is_function(token)) {
            push_op(token, &ops, &n_q, &sz_q);
        } else if (strncmp(token, ",", 1) == 0) {
            while (strncmp(peek_op(ops, n_q), "(", 1) != 0) {
                token = pop_op(ops, &n_q);
                if (is_operator_parity(token)) {
                    push_bit(operator_parity(token, pop_bit(output, &n_o), pop_bit(output, &n_o)), &output, &n_o, &sz_o);
                } else {
                    push_bit(function_parity(token, output, &n_o), &output, &n_o, &sz_o);
                }
            }
        } else if (is_operator_parity(token)) {
            o1 = token;
            while (peek_op(ops, n_q) && is_operator_parity(peek_op(ops, n_q))) {
                o2 = peek_op(ops, n_q);
                if (operator_parity_precedence(o1) <= operator_parity_precedence(o2)) {
                    push_bit(operator_parity(pop_op(ops, &n_q), pop_bit(output, &n_o), pop_bit(output, &n_o)), &output, &n_o, &sz_o);
                } else {
                    break;
                }
            }
            push_op(o1, &ops, &n_q, &sz_q);
        } else if (strncmp(token, "(", 1) == 0) {
            push_op(token, &ops, &n_q, &sz_q);
        } else if (strncmp(token, ")", 1) == 0) {
            while (strncmp(peek_op(ops, n_q), "(", 1) != 0) {
                token = pop_op(ops, &n_q);
                if (is_operator_parity(token)) {
                    push_bit(operator_parity(token, pop_bit(output, &n_o), pop_bit(output, &n_o)), &output, &n_o, &sz_o);
                } else {
                    push_bit(function_parity(token, output, &n_o), &output, &n_o, &sz_o);
                }
            }

            token = pop_op(ops, &n_q); /* pop the left bracket */

            if (peek_op(ops, n_q) && is_function(peek_op(ops, n_q))) {
                push_bit(function_parity(pop_op(ops, &n_q), output, &n_o), &output, &n_o, &sz_o);
            }
        } else {
            fprintf(stderr, "ERROR: unknown symbol: %s\n", token);
            exit(EXIT_FAILURE);
        }
    }

    while ((token = pop_op(ops, &n_q))) {
        if (is_operator_parity(token)) {
            push_bit(operator_parity(token, pop_bit(output, &n_o), pop_bit(output, &n_o)), &output, &n_o, &sz_o);
        } else {
            push_bit(function_parity(token, output, &n_o), &output, &n_o, &sz_o);
        }
    }

    res = output[0];

    free(output);
    free(ops);

    return res;
}

static int measure_parity(char *ind, bool **X, int n, int b)
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
        r = execute_parity(buffer, X[i]);
        // q is real, r is prediction, if prediction is correct, get one score.

        score += (q == r) ? 1 : 0;

        free(buffer);
    }

    return (1 << b) - score;
    // return 2^n -score to make this a minimize problem
}



int evaluate_parity(char *solution, int input_size){
    int i;
    struct details details;

    details.b = input_size ;
    details.n = 1 << details.b;
    details.data = generate_data_parity(details.b);

    return measure_parity(solution,details.data, details.n, details.b);
}