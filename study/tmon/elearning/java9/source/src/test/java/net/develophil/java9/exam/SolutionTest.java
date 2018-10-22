package net.develophil.java9.exam;

import org.assertj.core.api.Assertions;
import org.junit.Test;

public class SolutionTest {

	@Test
	public void twoE() throws Exception {
		Assertions.assertThat(new Solution().twoE()).isEqualTo(2184);
	}

	@Test
	public void threeB() throws Exception {
		Assertions.assertThat(new Solution().threeB()).isEqualTo(859);
	}
}