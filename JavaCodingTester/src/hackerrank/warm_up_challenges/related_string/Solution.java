package hackerrank.warm_up_challenges.related_string;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;
import java.util.stream.IntStream;

public class Solution {

    private static final char CHECK_CHARACTER = 'a';

    // Complete the repeatedString function below.
    static long repeatedString(String s, long n) {

        final int strLength = s.length();

        final long remainder = Math.floorMod(n, strLength);
        final long times = Math.floorDiv(n, strLength);

        return IntStream.range(0, strLength)
                .filter(i -> s.charAt(i) == CHECK_CHARACTER)
                .mapToLong((i) -> {
                    long cnt = times;
                    if (i < remainder) {
                        cnt++;
                    }
                    return cnt;
                })
                .sum();
    }

    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) throws IOException {
        BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter(System.getenv("OUTPUT_PATH")));

        String s = scanner.nextLine();

        long n = scanner.nextLong();
        scanner.skip("(\r\n|[\n\r\u2028\u2029\u0085])?");

        long result = repeatedString(s, n);

        bufferedWriter.write(String.valueOf(result));
        bufferedWriter.newLine();

        bufferedWriter.close();

        scanner.close();
    }
}

