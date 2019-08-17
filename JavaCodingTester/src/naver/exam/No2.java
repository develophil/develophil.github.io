package naver.exam;

import org.junit.Test;

import java.util.*;

public class No2 {

    public int solution(int A, int B) {
        // write your code in Java SE 8

        int maxCount = 0;
        Map<Integer, Integer> countSumMap = new HashMap<>();

        for (int i = A; i <= B; i++) {

            int intSqrt = getIntSqrt(i);

            if (intSqrt > 2) {
                int count = countSumMap.getOrDefault(intSqrt, solution(intSqrt, intSqrt));
                if (count > maxCount) {
                    maxCount = count + 1;
                    countSumMap.put(i, maxCount);
                }
            }
        }

        return maxCount;

    }

    public static int getIntSqrt(int num) {

        double sqrt = Math.sqrt(num);
        return sqrt == (int) sqrt ? (int) sqrt : -1;
    }

    @Test
    public void test() {

//        System.out.println(getRepeatedSqrtCount(6561));
//        System.out.println(solution(2,1000000000));
        System.out.println(solution(6000,7000));
//        System.out.println(solution(6561,6561));
//        System.out.println(calcSqrt(17));
//        System.out.println(calcSqrt(16));
    }

    @Test
    public void name() {
        System.out.println(3 % 2);
    }
}
