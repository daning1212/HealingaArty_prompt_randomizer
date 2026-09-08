import unittest
from updated_prompt_randomizer import HealingArtyPromptRandomizerV11 as Node, PURE_POSES


class RandomizerTests(unittest.TestCase):
    def test_sequence_wrap_and_isolation(self):
        for category, pool in PURE_POSES.items():
            node = Node()
            values = [node.generate(-1, "순차", **{category: "random"})[0]
                      for _ in range(len(pool) + 1)]
            self.assertEqual(values[:-1], pool)
            self.assertEqual(values[-1], pool[0])
            self.assertEqual(Node().generate(-1, "순차", **{category: "random"})[0], pool[0])

    def test_reset_start_and_mode_switch(self):
        node = Node()
        args = {"세로포즈": "random", "순차_시작번호": 3, "순차_리셋": 0}
        self.assertEqual(node.generate(0, "순차", **args)[0], PURE_POSES["세로포즈"][2])
        self.assertEqual(node.generate(0, "순차", **args)[0], PURE_POSES["세로포즈"][3])
        args["순차_리셋"] = 1
        self.assertEqual(node.generate(0, "순차", **args)[0], PURE_POSES["세로포즈"][2])
        node.generate(0, "고정", 표정="random")
        self.assertEqual(node.generate(0, "순차", **args)[0], PURE_POSES["세로포즈"][2])

    def test_fixed_and_weights(self):
        node = Node()
        args = {"표정": "random", "세로포즈": "random", "표정_가중치": 1.2}
        self.assertEqual(node.generate(42, "고정", **args), node.generate(42, "고정", **args))
        self.assertEqual(node.generate(0, "고정", 표정="smiling", 표정_가중치=1.2)[0],
                         "(smiling:1.2)")
        self.assertEqual(node.generate(0, "고정", 표정="none")[0], "1girl")

    def test_manual_and_independent_categories(self):
        node = Node()
        args = {"표정": "smiling", "세로포즈": "random", "가로포즈": "none"}
        self.assertTrue(node.generate(0, "순차", **args)[0].startswith("smiling, "))
        args["표정"] = "random"
        self.assertTrue(node.generate(0, "순차", **args)[0].startswith("smiling, "))
        self.assertTrue(node.generate(0, "순차", **args)[0].startswith("expressionless, "))

    def test_cache_and_schema(self):
        value = Node.IS_CHANGED(42, "순차")
        self.assertNotEqual(value, value)
        schema = Node.INPUT_TYPES()
        self.assertIn("순차", schema["required"]["랜덤_모드"][0])
        self.assertGreater(len(schema["optional"]["표정"][0]), 40)
        for pool in PURE_POSES.values():
            self.assertEqual(len(pool), len(set(pool)))


if __name__ == "__main__":
    unittest.main()
