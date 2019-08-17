package codesignal.tournament.day2;

import org.junit.Test;

import java.util.Arrays;
import java.util.stream.IntStream;

public class MatrixTransposition {
/*

    int[][] matrixTransposition(int[][] matrix) {

        int[][] transMatrix = new int[matrix[0].length][matrix.length];

        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[i].length; j++) {
                transMatrix[j][i] = matrix[i][j];
            }
        }

        return transMatrix;

    }
*/

    int[][] matrixTransposition(int[][] matrix) {

        return IntStream.range(0, matrix[0].length)
                .mapToObj(i -> IntStream.range(0, matrix.length).map(j -> matrix[j][i]).toArray())
                .toArray(int[][]::new);

    }

    @Test
    public void am() {
        System.out.println(Arrays.deepToString(matrixTransposition(new int[][]{{1, 1, 3}, {2, 1, 1}})));
    }
}
