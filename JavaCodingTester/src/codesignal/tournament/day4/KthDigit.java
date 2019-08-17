package codesignal.tournament.day4;

import org.junit.Assert;
import org.junit.Test;

import java.util.stream.IntStream;

public class KthDigit {
    int kthDigit(int n, int k) {

        String nStr = String.valueOf(n);

        if(k<1 || k>7 || nStr.length() < k) {
            return -1;
        }

        return nStr.charAt(k - 1) - '0';
    }

    int[] firstReverseTry(int[] arr) {

        if(arr.length == 0)
            return arr;

        int temp = 0;

        temp = arr[0];
        arr[0] = arr[arr.length-1];
        arr[arr.length-1] = temp;

        return arr;
    }

    boolean isIdentityMatrix(int[][] matrix) {

        if (matrix.length == 0 || matrix.length != matrix[0].length) {
            return false;
        }

        for (int i = 0; i < matrix.length; i++) {

            for (int j = 0; j < matrix[0].length; j++) {

                if (matrix[i][j] != (i == j ? 1 : 0)) {
                    return false;
                }
            }
        }
        return true;
    }

    int shapeArea(int n) {
        // n^2 + (n-1)^2 + ... 1

        if(n==1) return 1;

        return IntStream.rangeClosed(n-1, n)
                .map(i -> i*i)
                .reduce(0, (left, right) -> left + right);
    }


    @Test
    public void test() {
//        Assert.assertEquals(kthDigit(578943, 2), 7);
//        Assert.assertArrayEquals(firstReverseTry(new int[]{1,2,3,4}), new int[]{4,2,3,1});
//        Assert.assertArrayEquals(firstReverseTry(new int[]{}), new int[]{});
//        Assert.assertArrayEquals(firstReverseTry(new int[]{1,-10000,10000,4}), new int[]{4,-10000,10000,1});
//        int[][] arrs = {{1,2},{2,1}};
//        int[][] arrs = {{1,0,0},{0,1,0},{0,0,1}};
//        Assert.assertTrue(isIdentityMatrix(arrs));
        Assert.assertEquals(1, shapeArea(1) );
        Assert.assertEquals(5, shapeArea(2) );
        Assert.assertEquals(13, shapeArea(3));
    }
}
