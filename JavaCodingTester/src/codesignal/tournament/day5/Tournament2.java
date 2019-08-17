package codesignal.tournament.day5;

import org.junit.Assert;
import org.junit.Test;

import java.util.Arrays;
import java.util.stream.IntStream;

// https://app.codesignal.com/tournaments/f6gBXnRR9BjZLRxEz
public class Tournament2 {

    boolean isLuckyNumber(int n) {
        return !String.valueOf(n).chars()
                .filter(i -> !(i - '0' == 4 || i - '0' == 7))
                .findAny().isPresent();
    }

    @Test
    public void test1() {
        isLuckyNumber(47);
    }

    int arrayMinimumAboveBound(int[] inputArray, int bound) {

        return Arrays.stream(inputArray)
                .filter(i -> i > bound)
                .min()
                .orElse(0);
    }

    @Test
    public void test2() {
        Assert.assertEquals(2, arrayMinimumAboveBound(new int[]{1, 4, 10, 5, 2}, 1));
        Assert.assertEquals(-2, arrayMinimumAboveBound(new int[]{-3,-40,5,10,-2}, -3));
    }

    int giftSafety(String gift) {

        return (int) IntStream.range(0, gift.length() - 2)
                .filter(i -> gift.charAt(i) == gift.charAt(i + 1) || gift.charAt(i + 1) == gift.charAt(i + 2) || gift.charAt(i + 2) == gift.charAt(i))
                .count();
    }

    @Test
    public void test3() {
        Assert.assertEquals(1, giftSafety("doll"));
        Assert.assertEquals(5, giftSafety("aaaaaaa"));
    }

    /**
     * its length is at least 5 characters;
     * it contains at least one capital letter;
     * it contains at least one small letter;
     * it contains at least one digit.
     * @param inputString
     * @return
     */
    boolean passwordCheck(String inputString) {

        if (inputString.length() < 5) return false;

        return containsLetterRange(inputString, 'A', 'Z')
                && containsLetterRange(inputString, 'a', 'z')
                && containsLetterRange(inputString, '0', '9');

    }

    private boolean containsLetterRange(String inputString, char start, char end) {
        return inputString.chars()
                .filter(i -> i >= start && i <= end)
                .findAny().isPresent();
    }


    @Test
    public void testcontainsletterrange() {
        Assert.assertEquals(false, passwordCheck("my.password123"));

    }
}
