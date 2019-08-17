package codesignal.tournament.day1;

import org.junit.Assert;
import org.junit.Test;

public class Lv04_CreateAnagramTest {

    @Test
    public void sumOfCubes() {
        Assert.assertEquals(1, new Lv04_CreateAnagram().createAnagram("AABAA", "BBAAA"));
        Assert.assertEquals(4, new Lv04_CreateAnagram().createAnagram("OVGHK", "RPGUC"));
    }

}