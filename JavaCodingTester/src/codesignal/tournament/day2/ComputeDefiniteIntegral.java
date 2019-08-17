package codesignal.tournament.day2;

import org.junit.Test;

import java.util.stream.IntStream;

public class ComputeDefiniteIntegral {

    double computeDefiniteIntegral(int l, int r, int[] p) {

        return Math.round((calc(r, p) - calc(l, p))*100)/100.0;
    }

    private double calc(int val, int[] p) {
        return IntStream.rangeClosed(1, p.length)
                .mapToDouble(i -> (p[i-1] * Math.pow(val, i - 1)) * val / i).sum();
    }


    @Test
    public void a() {
        System.out.println(computeDefiniteIntegral(-1, 2, new int[]{0, 0, 0, 1}));
        System.out.println(computeDefiniteIntegral(-150, 150, new int[]{1,1,1,1,1,1,1,1}));
    }
}
