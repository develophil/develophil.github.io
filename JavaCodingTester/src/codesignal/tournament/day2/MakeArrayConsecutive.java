package codesignal.tournament.day2;

import org.junit.Test;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

public class MakeArrayConsecutive {

    int[] makeArrayConsecutive(int[] sequence) {

        int min = 10;
        int max = -10;

        Set<Integer> rangeSet = new HashSet<>(Arrays.asList(-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10));

        for (int i = 0; i < sequence.length; i++) {
            int value = sequence[i];
            if (value < min) {
                min = value;
            }
            if (value > max) {
                max = value;
            }
            rangeSet.remove(value);
        }

        return sequence;
    }


    @Test
    public void a() {
        makeArrayConsecutive(new int[]{6, 2, 3, 8});
    }
}
