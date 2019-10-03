package codility.lesson3complexity;

import jdk.nashorn.internal.parser.JSONParser;
import org.junit.Assert;
import org.junit.Test;

import java.util.Arrays;
import java.util.stream.IntStream;

/**
 * An array A consisting of N different integers is given. The array contains integers in the range [1..(N + 1)], which means that exactly one element is missing.
 *
 * Your goal is to find that missing element.
 *
 * Write a function:
 *
 * class Solution { public int solution(int[] A); }
 *
 * that, given an array A, returns the value of the missing element.
 *
 * For example, given array A such that:
 *
 *   A[0] = 2
 *   A[1] = 3
 *   A[2] = 1
 *   A[3] = 5
 * the function should return 4, as it is the missing element.
 *
 * Write an efficient algorithm for the following assumptions:
 *
 * N is an integer within the range [0..100,000];
 * the elements of A are all distinct;
 * each element of array A is an integer within the range [1..(N + 1)].
 * Copyright 2009–2019 by Codility Limited. All Rights Reserved. Unauthorized copying, publication or disclosure prohibited.
 *
 * My solution : https://app.codility.com/demo/results/trainingENPNVW-SDY/
 * another : https://app.codility.com/demo/results/trainingNTJN66-4KD/
 */
public class PermMissingElem {

    public int solution(int[] A) {

        if (A == null || A.length == 0 || A.length > 100000) {
            return -1;
        }

        Arrays.sort(A);

        return getAsymmetricNumber(1, A);

    }

    private int getAsymmetricNumber(int begin, int[] A) {

        int leftRightSum = begin + begin + A.length;

        if (A.length == 1) {

            return begin == A[0] ? begin + 1 : begin;
        } else {

            int mid = (A.length - 1) / 2;
            int left = A.length % 2 == 0 ? mid : mid - 1;
            int right = mid + 1;

            if (A[left] + A[right] > leftRightSum) {

                if (left == 0) {
                    return A[left] - 1;
                } else {
                    return getAsymmetricNumber(begin, Arrays.copyOfRange(A, 0, right));
                }

            } else if (A[left] + A[right] < leftRightSum) {

                if (right == A.length - 1) {
                    return A[right] + 1;
                } else {
                    return getAsymmetricNumber(A[right] + 1, Arrays.copyOfRange(A, right + 1, A.length));
                }

            } else {
                return leftRightSum / 2;
            }

        }

    }

    @Test
    public void test() {
        int[] a = {2,3,1,5};
        Assert.assertEquals(4, solution(a));
        int[] b = {1};
        Assert.assertEquals(2, solution(b));
        int[] c = {2};
        Assert.assertEquals(1, solution(c));
        int[] d = {1,3};
        Assert.assertEquals(2, solution(d));
    }
}
