package codesignal.arcade.intro;

import org.junit.Assert;
import org.junit.Test;

import java.util.LinkedList;
import java.util.Queue;
import java.util.stream.IntStream;

public class Lv2 {


    int makeArrayConsecutive2(int[] statues) {

        int min = 20;
        int max = 0;

        for (int i : statues) {
            min = Math.min(min, i);
            max = Math.max(max, i);
        }

        int betweenMinMaxNumbers = max - min - 1;

        return betweenMinMaxNumbers - (statues.length - 2);
    }

    boolean almostIncreasingSequence(int[] sequence) {

        boolean isAlreadyPass = false;

        for (int i = 1; i < sequence.length; i++) {
            if (sequence[i] <= sequence[i-1]) {
                if (isAlreadyPass) {
                    return false;
                } else {
                    isAlreadyPass = true;
                    if (i == 1 || i == sequence.length - 1) {
                        continue;
                    }
                    if (sequence[i] <= sequence[i - 2] && sequence[i + 1] <= sequence[i - 1]) {
                        return false;
                    }
                }
            }
        }

        return true;
    }

    int matrixElementsSum(int[][] matrix) {
        return IntStream.range(0, matrix[0].length)
                .map(value -> getSumBeforeZero(matrix, value))
                .sum();
    }

    private int getSumBeforeZero(int[][] matrix, int value) {
        int sum = 0;
        for (int i = 0; i < matrix.length; i++) {
            if (matrix[i][value] != 0) {
                sum += matrix[i][value];
            } else {
                break;
            }
        }
        return sum;
    }


    @Test
    public void test1() {

        int[] arr = {6, 2, 3, 8};
        Assert.assertEquals(3, makeArrayConsecutive2(arr));
    }

    @Test
    public void test2() {

        int[] arr = {1,3,2,1};
        Assert.assertEquals(false, almostIncreasingSequence(arr));
        int[] arr2 = {1,3,2};
        Assert.assertEquals(true, almostIncreasingSequence(arr2));
        int[] arr3 = {1,1};
        Assert.assertEquals(true, almostIncreasingSequence(arr3));
        int[] arr4 = {1,2,1,2};
        Assert.assertEquals(false, almostIncreasingSequence(arr4));
        int[] arr5 = {10, 1, 2, 3, 4, 5};
        Assert.assertEquals(true, almostIncreasingSequence(arr5));
        int[] arr6 = {1, 1, 2, 3, 4, 4};
        Assert.assertEquals(false, almostIncreasingSequence(arr6));
        int[] arr7 = {1, 2, 5, 3, 5};
        Assert.assertEquals(true, almostIncreasingSequence(arr7));
    }

    @Test
    public void test3() {
        int[][] arr = {{0,1,1,2},{0,5,0,0},{2,0,3,3}};
        Assert.assertEquals(9, matrixElementsSum(arr));
    }

    @Test
    public void test4() {

        Queue<Integer> queue = new LinkedList<>();

        queue.add(1);
        queue.offer(4);
        queue.offer(5);
        queue.offer(2);


        for (int i = 0; i < 3; i++) {
            System.out.println(queue.poll());
        }

        System.out.println(queue.size());

    }


}
