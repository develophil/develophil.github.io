package hackerrank.warm_up_challenges.related_string;

import org.junit.Assert;
import org.junit.Test;

import java.util.stream.IntStream;

import static hackerrank.warm_up_challenges.related_string.Solution.repeatedString;

public class SolutionTest {

    @Test
    public void test() {
        long result = repeatedString("aba", 10);
        Assert.assertEquals(7, result);
    }
    @Test
    public void test1() {

        long max = Double.valueOf(Math.pow(10, 12)).longValue();

        long result = repeatedString("a", max);
        Assert.assertEquals(max, result);
    }
    @Test
    public void test2() {

        long max = Double.valueOf(Math.pow(10, 12)).longValue();

        long result = repeatedString("b", max);
        Assert.assertEquals(0, result);
    }
    @Test
    public void test3() {
        long result = repeatedString("a", 1);
        Assert.assertEquals(1, result);
    }
    @Test
    public void test4() {
        long result = repeatedString(new String(new char[100]).replace("\0", "a"), 10);
        Assert.assertEquals(10, result);
    }
}