package hackerrank.warm_up_challenges.no01_sock_merchant;

import org.junit.Assert;
import org.junit.Test;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;
import java.util.stream.IntStream;

public class Solution {


    // Complete the sockMerchant function below.
    static int sockMerchant(int n, int[] ar) {

        final Map<Integer, Integer> pairCountMap = new HashMap<>();

        Arrays.stream(ar)
                .forEach(i -> {
                    if (pairCountMap.keySet().contains(i)) {
                        pairCountMap.put(i, pairCountMap.get(i) + 1);
                    } else {
                        pairCountMap.put(i, 1);
                    }
                });

        return getTotalPairs(pairCountMap);
    }

    private static int getTotalPairs(Map<Integer, Integer> pairCountMap) {
        return pairCountMap.values().stream().map(v -> Double.valueOf(Math.floor(v/2)).intValue()).reduce((i1, i2) -> i1 + i2).orElse(0);
    }

    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) throws IOException {
        BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter(System.getenv("OUTPUT_PATH")));

        int n = scanner.nextInt();
        scanner.skip("(\r\n|[\n\r\u2028\u2029\u0085])?");

        int[] ar = new int[n];

        String[] arItems = scanner.nextLine().split(" ");
        scanner.skip("(\r\n|[\n\r\u2028\u2029\u0085])?");

        for (int i = 0; i < n; i++) {
            int arItem = Integer.parseInt(arItems[i]);
            ar[i] = arItem;
        }

        int result = sockMerchant(n, ar);

        bufferedWriter.write(String.valueOf(result));
        bufferedWriter.newLine();

        bufferedWriter.close();

        scanner.close();
    }

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
