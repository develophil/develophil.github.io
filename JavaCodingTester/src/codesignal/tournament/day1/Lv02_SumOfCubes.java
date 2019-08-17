package codesignal.tournament.day1;

import java.util.stream.IntStream;

public class Lv02_SumOfCubes {

    /**
     * 1000
     *
     * Find the sum of cubes of all integers starting from 1 up to the given integer n, inclusive.
     *
     * Example
     *
     * For n = 3, the output should be
     * sumOfCubes(n) = 36.
     *
     * Because 13 + 23 + 33 = 1 + 8 + 27 = 36.
     *
     * Input/Output
     *
     * [execution time limit] 3 seconds (java)
     *
     * [input] integer n
     *
     * Guaranteed constraints:
     * 1 ≤ n ≤ 10.
     *
     * [output] integer
     *
     * [Java] Syntax Tips
     *
     * // Prints help message to the console
     * // Returns a string
     * //
     * // Globals declared here will cause a compilation error,
     * // declare variables inside the function instead!
     * String helloWorld(String name) {
     *     System.out.println("This prints to the console when you Run Tests");
     *     return "Hello, " + name;
     * }
     */
    int sumOfCubes(int n) {



        return IntStream.rangeClosed(1, n).map(i -> (int) Math.pow(i, n)).sum();
    }
}
