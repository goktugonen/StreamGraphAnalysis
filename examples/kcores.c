/**
 * @file examples/kcores.c
 * @brief Example program on how to compute k-cores
 */

#include "../StreamGraphAnalysis.h"
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char **argv) {
        const char *path = argc > 1 ? argv[1] : "../data/tests/S.sga";
        // Load the stream into memory
        SGA_StreamGraph sg = SGA_StreamGraph_from_file(path);
        SGA_Stream st      = SGA_FullStreamGraph_from(&sg);

        // Compute all k-cores
        for (size_t k = 1;; k++) {
                SGA_Cluster k_core = SGA_Stream_k_core(&st, k);

                if (k_core.nodes.length == 0) {
                        SGA_Cluster_destroy(k_core);
                        printf("K-core for k=%zu is empty\n", k);
                        break;
                }

                String str = SGA_Cluster_to_string(&k_core);
                printf("K-core for k=%zu: %s\n", k, str.data);
                String_destroy(str);
                SGA_Cluster_destroy(k_core);
        }

        SGA_FullStreamGraph_destroy(st);
        SGA_StreamGraph_destroy(sg);
        exit(EXIT_SUCCESS);
}
