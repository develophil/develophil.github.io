package codility.lesson6sorting;

import java.util.function.Predicate;
import java.util.Arrays;
import java.util.stream.IntStream;

/**
 * A non-empty array A consisting of N integers is given. The product of triplet (P, Q, R) equates to A[P] * A[Q] * A[R] (0 ≤ P < Q < R < N).
 *
 * For example, array A such that:
 *
 *   A[0] = -3
 *   A[1] = 1
 *   A[2] = 2
 *   A[3] = -2
 *   A[4] = 5
 *   A[5] = 6
 * contains the following example triplets:
 *
 * (0, 1, 2), product is −3 * 1 * 2 = −6
 * (1, 2, 4), product is 1 * 2 * 5 = 10
 * (2, 4, 5), product is 2 * 5 * 6 = 60
 * Your goal is to find the maximal product of any triplet.
 *
 * Write a function:
 *
 * class Solution { public int solution(int[] A); }
 *
 * that, given a non-empty array A, returns the value of the maximal product of any triplet.
 *
 * For example, given array A such that:
 *
 *   A[0] = -3
 *   A[1] = 1
 *   A[2] = 2
 *   A[3] = -2
 *   A[4] = 5
 *   A[5] = 6
 * the function should return 60, as the product of triplet (2, 4, 5) is maximal.
 *
 * Write an efficient algorithm for the following assumptions:
 *
 * N is an integer within the range [3..100,000];
 * each element of array A is an integer within the range [−1,000..1,000].
 * Copyright 2009–2019 by Codility Limited. All Rights Reserved. Unauthorized copying, publication or disclosure prohibited.
 */
public class MaxProductOfThree {

    Predicate<int[]> checkArrayLengthRange = (arr) -> (arr.length < 3 || arr.length > 100000);
    Predicate<Integer> checkValuesRange = (i) -> i < -1000 || i > 1000;

    public int solution(int[] A) {

        try {
            asserts(A, checkArrayLengthRange, "정수 배열 길이의 범위는 3이상 100,000이하입니다.");

            final int[] sorted = Arrays.stream(A)
//                    .peek((i) -> asserts(i, checkValuesRange, "배열 요소의 값의 범위는 -1,000이상 1,000이하입니다."))
                    .sorted().toArray();

            int result = IntStream.rangeClosed(1, 3).reduce(1, (product, i) -> product * sorted[sorted.length - i]);

            result = replaceIfnegativeProductValueBiggerThanResult(sorted, result);

            return result;
        } catch (Exception e) {
            // exception logging
            return 0;
        }
    }

    private int replaceIfnegativeProductValueBiggerThanResult(int[] A, int result) {
        if (existMoreTwoNegative(A)) {
            int negativeProductValue = A[0] * A[1] * A[A.length - 1];

            if (negativeProductValue > result) {
                result = negativeProductValue;
            }
        }
        return result;
    }

    private boolean existMoreTwoNegative(int[] A) {
        return A[0] < 0 && A[1] < 0;
    }

    private void asserts(int[] A, Predicate<int[]> check, String errMsg) {
        if (check.test(A)) {
            throw new IllegalArgumentException(errMsg);
        }
    }

    private void asserts(int A, Predicate<Integer> check, String errMsg) {
        if (check.test(A)) {
            throw new IllegalArgumentException(errMsg);
        }
    }

}
