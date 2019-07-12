package hackerrank.warm_up_challenges.no03_jumping_on_the_clouds;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

public class Solution {

    static class Game {

        private static final int MAX_SIZE = 100;
        private int[] clouds;
        private int jumpCount;

        public Game(int[] c) {
            this.clouds = c;
        }

        public void play() {

            for (int i = 0; i < clouds.length - 1; i += getJumpStep(i)) {
                jumpCount++;
            }
        }

        private int getJumpStep(int i) {

            int result = MAX_SIZE;

            try {

                int next = clouds[i + 1];
                int next2 = clouds[i + 2];

                if (next2 == 0) {
                    result = 2;

                } else if (next2 == 1) {
                    if (next == 0) {
                        result = 1;
                    }
                }

            } catch (ArrayIndexOutOfBoundsException ignored) {
            }
            return result;
        }

        public int getJumpCount() {
            return this.jumpCount;
        }
    }

    // Complete the jumpingOnClouds function below.
    static int jumpingOnClouds(int[] c) {
        Game game = new Game(c);
        game.play();
        return game.getJumpCount();
    }

    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) throws IOException {
        BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter(System.getenv("OUTPUT_PATH")));

        int n = scanner.nextInt();
        scanner.skip("(\r\n|[\n\r\u2028\u2029\u0085])?");

        int[] c = new int[n];

        String[] cItems = scanner.nextLine().split(" ");
        scanner.skip("(\r\n|[\n\r\u2028\u2029\u0085])?");

        for (int i = 0; i < n; i++) {
            int cItem = Integer.parseInt(cItems[i]);
            c[i] = cItem;
        }

        int result = jumpingOnClouds(c);

        bufferedWriter.write(String.valueOf(result));
        bufferedWriter.newLine();

        bufferedWriter.close();

        scanner.close();
    }
}