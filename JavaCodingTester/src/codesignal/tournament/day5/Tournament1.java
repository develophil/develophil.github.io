package codesignal.tournament.day5;

import org.junit.Assert;
import org.junit.Test;

// https://app.codesignal.com/tournaments/tripdqnFnay6vjhrD
public class Tournament1 {
    boolean evenDigitsOnly(int n) {

        return Integer.toString(n).chars()
                .filter(i -> i % 2 != 0)
                .count() == 0;
    }

    String properNounCorrection(String noun) {
        return noun.substring(0, 1).toUpperCase() + noun.substring(1, noun.length()).toLowerCase();
    }

    boolean isLucky(int n) {

        int leftSum = 0, rightSum = 0;

        String nStr = String.valueOf(n);
        int size = nStr.length();

        for (int i = 0; i < size / 2; i++) {
            leftSum += nStr.charAt(i) - '0';
            rightSum += nStr.charAt(size - i -1) - '0';
        }

        return leftSum == rightSum;
    }

    @Test
    public void test() {
        Assert.assertEquals(false, isLucky(10));
        Assert.assertEquals(true, isLucky(1010));
    }

}
