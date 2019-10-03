package woowabrother;

import org.junit.Assert;
import org.junit.Test;

import java.util.Arrays;

public class Exam3 {
    public int solution(int[] A) {

        if (A.length == 0 || A.length > 100000) {
            return 0;
        }

        Arrays.sort(A);

        for (int i = A.length - 1; i >= 0; i--) {
            for (int value : A) {
                if (A[i] < 0 || value > 0 || value > A[i] * -1) {
                    break;
                } else if (value == A[i] * -1) {
                    return A[i];
                }
            }
        }

        return 0;
    }

    @Test
    public void test() {
        Assert.assertEquals(3, solution(new int[]{3,2,-2,5,-3}));
        Assert.assertEquals(1, solution(new int[]{1,1,2,-1,2,-1}));
        Assert.assertEquals(0, solution(new int[]{1,2,3,-4}));
        Assert.assertEquals(0, solution(new int[]{1000000001}));
        Assert.assertEquals(0, solution(new int[]{-1000000001}));
        Assert.assertEquals(0, solution(new int[0]));
    }
}
