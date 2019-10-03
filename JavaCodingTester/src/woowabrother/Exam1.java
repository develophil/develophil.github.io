package woowabrother;

import org.junit.Assert;
import org.junit.Test;

import java.util.Arrays;

public class Exam1 {

    private static final String IMPOSSIBLE = "IMPOSSIBLE";

    public String solution(int U, int L, int[] C) {

        if (outOfRange(U) || outOfRange(L) || outOfLength(C) || invalidSum(U, L, C)) {
            return IMPOSSIBLE;
        }

        StringBuilder upperSb = new StringBuilder(100000);
        StringBuilder lowerSb = new StringBuilder(100000);

        for (int sum : C) {

            if (sum < 0 || sum > 2) {
                return IMPOSSIBLE;
            }

            if (sum == 2) {
                U = addOne(U, upperSb);
                L = addOne(L, lowerSb);

            } else if (sum == 1) {
                if (U >= 1) {
                    U = addOne(U, upperSb);
                    addZero(lowerSb);
                } else if (L >= 1) {
                    L = addOne(L, lowerSb);
                    addZero(upperSb);
                }
            } else {
                addZero(upperSb);
                addZero(lowerSb);
            }
        }

        return String.join(",", upperSb.toString(), lowerSb.toString());
    }

    private static boolean invalidSum(int U, int L, int[] C) {
        return U + L != Arrays.stream(C).sum();
    }

    private static boolean outOfLength(int[] c) {
        return c.length < 1 || c.length > 100000;
    }

    private static boolean outOfRange(int n) {
        return n < 0 || n > 100000;
    }

    private static void addZero(StringBuilder sb) {
        sb.append("0");
    }

    private static int addOne(int sum, StringBuilder upperSb) {
        upperSb.append("1");
        sum -= 1;
        return sum;
    }


    @Test
    public void test() {
        Assert.assertEquals("11100,10001", solution(3, 2, new int[]{2,1,1,0,1}));
        Assert.assertEquals("1010,1010", solution(2, 2, new int[]{2,0,2,0}));
        Assert.assertEquals("IMPOSSIBLE", solution(2, 3, new int[]{0,0,1,1,2}));
        Assert.assertEquals("0,0", solution(0, 0, new int[]{0}));
        Assert.assertEquals("1,1", solution(1, 1, new int[]{2}));
        Assert.assertEquals("10,01", solution(1, 1, new int[]{1,1}));
        Assert.assertEquals("IMPOSSIBLE", solution(100001, 3, new int[]{0,0,1,1,2}));
        Assert.assertEquals("IMPOSSIBLE", solution(1, 1, new int[]{3}));
    }

}
