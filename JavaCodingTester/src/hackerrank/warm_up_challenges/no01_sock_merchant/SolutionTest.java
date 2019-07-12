package hackerrank.warm_up_challenges.no01_sock_merchant;

import org.junit.Assert;
import org.junit.Test;

import java.util.stream.IntStream;

import static hackerrank.warm_up_challenges.no01_sock_merchant.Solution.sockMerchant;

public class SolutionTest {

    @Test
    public void test1() {
        int result = sockMerchant(9, new int[]{10, 20, 20, 10, 10, 30, 50, 10, 20});
        Assert.assertEquals(3, result);
    }

    @Test
    public void test2() {
        int result = sockMerchant(10, new int[]{1,1,3,1,2,1,3,3,3,3});
        Assert.assertEquals(4, result);
    }
    @Test
    public void min() {
        int result = sockMerchant(1, new int[]{1});
        Assert.assertEquals(0, result);
    }
    @Test
    public void max() {
        int n = 100;
        final int value = 100;
        int[] ar = IntStream.range(1, 101).map(i -> value).toArray();
        int result = sockMerchant(n, ar);
        Assert.assertEquals(50, result);
    }
}
