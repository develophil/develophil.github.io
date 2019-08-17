package codesignal.tournament.day1;

import java.util.Arrays;
import java.util.stream.IntStream;
import java.util.stream.Stream;

/**
 * You are given two strings s and t of the same length, consisting of uppercase English letters. Your task is to find the minimum number of "replacement operations" needed to get some anagram of the string t from the string s. A replacement operation is performed by picking exactly one character from the string s and replacing it by some other character.
 *
 * Example
 *
 * For s = "AABAA" and t = "BBAAA", the output should be
 * createAnagram(s, t) = 1;
 * For s = "OVGHK" and t = "RPGUC", the output should be
 * createAnagram(s, t) = 4.
 */
public class Lv04_CreateAnagram {
    int createAnagram(String s, String t) {

        String target = t;

        return s.chars().mapToObj(c -> (char)c).mapToInt(c -> {
            if (target.indexOf(c) > 0) {
                target.replace(c+"", "");
                return 0;
            } else {
                return 1;
            }
        }).sum();




    }
}
