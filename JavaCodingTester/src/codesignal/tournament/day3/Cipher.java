package codesignal.tournament.day3;

import org.junit.Test;

import java.util.LinkedList;
import java.util.Map;
import java.util.Queue;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class Cipher {
    String substitutionCipherDecryption(String contents, String signature, String encryptedSignature) {

        Map<Integer, Character> decryptMap = getDecryptMap(signature, encryptedSignature);

        return contents.chars().boxed().map(c->decryptMap.get(c).toString()).collect(Collectors.joining());

    }

    private Map<Integer, Character> getDecryptMap(String signature, String encryptedSignature) {

        Queue<Character> lastCharacters = IntStream.rangeClosed((int) 'a', (int) 'z')
                .filter(i -> encryptedSignature.indexOf(i) < 0)
                .collect(LinkedList::new,(characters, value) -> characters.offer(Character.valueOf((char)value)), LinkedList::addAll);

        return IntStream.rangeClosed((int)'a', (int)'z')
                .boxed()
                .collect(
                        Collectors.toMap(
                                k -> {
                                    int index = signature.indexOf(k);

                                    if (index >= 0) {
                                        return (int)encryptedSignature.charAt(index);
                                    } else {
                                        return (int)lastCharacters.poll().charValue();
                                    }
                                },
                                v-> (char) v.intValue()
                        )
                );
    }

    @Test
    public void a() {
//        System.out.println(getDecryptMap("alice", "james"));
        System.out.println(substitutionCipherDecryption("issomtoqmvjts", "alice", "james"));
    }
}
