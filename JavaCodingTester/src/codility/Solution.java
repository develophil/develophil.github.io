package codility;

import org.junit.Assert;
import org.junit.Test;

import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

import static java.util.stream.Collectors.*;

public class Solution {

    public int[] solution(int K, int M, int[] A) {
        // write your code in Java SE 8

        return IntStream.range(0, A.length - K)
                .mapToObj(i -> getIncrementSegmentArray(A, i, K))
                .mapToInt(this::getMaxCountNumber)
                .distinct()
                .toArray();
    }

    private int[] getIncrementSegmentArray(int[] arr, int startIndex, int segmentLength) {
        int[] clone = arr.clone();
        for (int i = startIndex; i < segmentLength + startIndex; i++) {
            clone[i]++;
        }
        return clone;
    }

    private int getMaxCountNumber(int[] numbers) {
        return Arrays.stream(numbers)
                .boxed()
                .collect(
                        groupingBy(Function.identity(), counting()))
                .entrySet().stream()
                .max(Map.Entry.comparingByValue())
                .get().getKey();
    }

    @Test
    public void test() {
        int[] rrr = solution(3,5, new int[]{2,1,3,1,2,2,3});
        for (int i :
                rrr) {
            System.out.println("v : "+i);
        }
//        Assert.assertArrayEquals(new int[]{2, 3}, solution(3,5, new int[]{2,1,3,1,2,2,3}));
//        int[] r = {2,1,3,1,2,2,3};
//        System.out.println(getMaxCountNumber(r));
    }
}
