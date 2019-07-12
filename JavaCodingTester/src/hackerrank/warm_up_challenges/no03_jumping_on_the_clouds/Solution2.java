package hackerrank.warm_up_challenges.no03_jumping_on_the_clouds;

public class Solution2 {

    // Complete the jumpingOnClouds function below.
    static int jumpingOnClouds(int[] c) {

        int jumpCount = 0;

        try {
            for (int i = 0, next = 0, next2 = 0; i < c.length - 1; i++) {

                next = c[i + 1];
                next2 = c[i + 2];

                if (next == 1 && next2 == 1) {
                    break;
                }

                if (next2 == 0) {
                    i++;
                }

                jumpCount++;
            }

        } catch (Exception igored) {
            jumpCount++;
        }

        return jumpCount;
    }
}