package woowabrother;

import org.junit.Assert;
import org.junit.Test;

import java.util.*;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

public class Exam2 {

    private static final String BLANK = " ";
    private static final String BYTE_CODE = "b";
    private static final String NEW_LINE = "\n";

    private TypeAnalyzer typeAnalyzer;
    private StringLoader stringLoader = new StringLoader();

    public String solution(String S) {

        initAnalyzerChain();
        typeAnalyzer.analyze(stringLoader.load(S));

        return typeAnalyzer.print();
    }

    private void initAnalyzerChain() {
        typeAnalyzer = new MusicAnalyzer();
        typeAnalyzer
                .setNextAnalyzer(new ImageAnalyzer())
                .setNextAnalyzer(new MovieAnalyzer())
                .setNextAnalyzer(new OtherAnalyzer());
    }

    class FileInfo {

        private static final String DOT = ".";
        private static final String REGEX_FILE_NAME = "[a-z0-9]+";
        private static final String REGEX_FILE_EXT = "[a-zA-Z\\^\\&\\'\\@\\{\\}\\[\\]\\,\\$\\=\\!\\-\\#\\(\\)\\%\\.\\+\\~\\_";

        private String name;
        private String ext;
        private int bytes;

        public FileInfo(String line) {
            String[] fileInfos = line.split(BLANK);
            separateNameAndExt(fileInfos[0]);
            this.bytes = parseBytes(fileInfos[1]);
        }

        private void separateNameAndExt(String fileFullName) {
            int lastIndexOfDot = fileFullName.lastIndexOf(DOT);
            this.name = fileFullName.substring(0, lastIndexOfDot);
            this.ext = fileFullName.substring(lastIndexOfDot + 1);
        }

        private int parseBytes(String byteString) {
            return Integer.parseInt(byteString.substring(0, byteString.length() - 1));
        }

        public int getBytes() {
            return bytes;
        }

        public String getExt() {
            return ext;
        }
    }

    class StringLoader {

        public List<FileInfo> load(String s) {

            return Arrays.stream(s.split(NEW_LINE))
            .map(FileInfo::new)
            .collect(Collectors.toList())
            ;
        }
    }


    abstract class TypeAnalyzer {

        protected int size;

        protected TypeAnalyzer nextAnalyzer;

        abstract String getExtensionRegex();

        abstract String getTypeStr();

        protected boolean match(FileInfo fileInfo) {
            return Pattern.compile(getExtensionRegex()).matcher(fileInfo.getExt()).find();
        }

        protected void analyze(List<FileInfo> fileInfos) {

            fileInfos.forEach(fileInfo -> {
                if (match(fileInfo)) {
                    size += fileInfo.getBytes();
                }
            });

            fileInfos.removeIf(this::match);

            if (fileInfos.size() > 0 && nextAnalyzer != null) {
                nextAnalyzer.analyze(fileInfos);
            }
        }
        public String print() {
            String result = print("");
            return result.substring(0, result.lastIndexOf(NEW_LINE));
        }
        protected String print(String prefix) {

            String result = prefix + makeRow(getTypeStr(), this.size);

            if (nextAnalyzer != null) {
                return nextAnalyzer.print(result);
            }else{
                return result;
            }
        }

        protected TypeAnalyzer setNextAnalyzer(TypeAnalyzer typeAnalyzer) {
            nextAnalyzer = typeAnalyzer;
            return typeAnalyzer;
        }

        private String makeRow(String type, int size) {
            return type + BLANK + size + BYTE_CODE + NEW_LINE;
        }
    }

    class MusicAnalyzer extends TypeAnalyzer {

        @Override
        String getExtensionRegex() {
            return "(mp3)|(aac)|(flac)";
        }

        @Override
        String getTypeStr() {
            return "music";
        }
    }

    class ImageAnalyzer extends TypeAnalyzer {

        @Override
        String getExtensionRegex() {
            return "(jpg)|(bmp)|(gif)";
        }

        @Override
        String getTypeStr() {
            return "images";
        }
    }
    class MovieAnalyzer extends TypeAnalyzer {

        @Override
        String getExtensionRegex() {
            return "(mp4)|(avi)|(mkv)";
        }

        @Override
        String getTypeStr() {
            return "movies";
        }
    }
    class OtherAnalyzer extends TypeAnalyzer {

        @Override
        String getExtensionRegex() {
            return ".+";
        }

        @Override
        protected boolean match(FileInfo fileInfo) {
            return true;
        }

        @Override
        String getTypeStr() {
            return "other";
        }
    }


    @Test
    public void test() {
        String s = "my.song.mp3 11b\ngreatSong.flac 1000b\nnot3.txt 5b\nvideo.mp4 200b\ngame.exe 100b\nmov!e.mkv 10000b";
        Assert.assertEquals("music 1011b\nimages 0b\nmovies 10200b\nother 105b", solution(s));
    }

}
