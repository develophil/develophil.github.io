package codesignal.tournament.day1;

import java.util.Arrays;
import java.util.stream.IntStream;

/**
 * Given a rectangular matrix and integers a and b, consider the union of the ath row and the bth (both 0-based) column of the matrix (i.e. all cells that belong either to the ath row or to the bth column, or to both). Return sum of all elements of that union.
 */
public class Lv01_CrossingSum {

    int crossingSum(int[][] matrix, int a, int b) {
/*
        int rowSum = Arrays.stream(matrix[a]).sum();
        int colSum = Arrays.stream(matrix).mapToInt(ints -> ints[b]).sum();
        int intersect = matrix[a][b];

        return rowSum + colSum - intersect;*/


        int colSumExceptAIndex = IntStream.range(0, matrix.length).filter(i -> i != a).map(i -> matrix[i][b]).sum();
        int rowSum = Arrays.stream(matrix[a]).sum();

        return colSumExceptAIndex + rowSum;

    }
}
