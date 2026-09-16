import unittest
from updated_prompt_randomizer import HealingArtyPromptRandomizerV11 as Node, POSTURE_POSES, GROUP_POSES


class RandomizerTests(unittest.TestCase):
    def test_sequence_wrap_and_isolation(self):
        for category, pool in POSTURE_POSES.items():
            node = Node()
            values = [node.generate(7, "고정", **{category: "순차"})[0]
                      for _ in range(len(pool) + 1)]
            self.assertEqual(values[:-1], pool)
            self.assertEqual(values[-1], pool[0])
            self.assertEqual(Node().generate(7, "고정", **{category: "순차"})[0], pool[0])

    def test_sequence_pauses_when_category_disabled(self):
        node = Node()
        self.assertEqual(node.generate(0, "고정", 서서포즈="순차")[0], POSTURE_POSES["서서포즈"][0])
        node.generate(0, "고정", 서서포즈="none")
        self.assertEqual(node.generate(0, "고정", 서서포즈="순차")[0], POSTURE_POSES["서서포즈"][1])

    def test_fixed_and_weights(self):
        node = Node()
        args = {"표정": "random", "서서포즈": "random", "표정_가중치": 1.2}
        self.assertEqual(node.generate(42, "고정", **args), node.generate(42, "고정", **args))
        self.assertEqual(node.generate(0, "고정", 표정="smiling", 표정_가중치=1.2)[0],
                         "(smiling:1.2)")
        self.assertEqual(node.generate(0, "고정", 표정="none")[0], "1girl")

    def test_manual_and_independent_categories(self):
        node = Node()
        args = {"표정": "random", "서서포즈": "순차", "앉기포즈": "none", "의상": "none"}
        first = node.generate(42, "고정", **args)[0]
        second = node.generate(42, "고정", **args)[0]
        self.assertNotEqual(first, second)
        self.assertEqual(first.split(", " + POSTURE_POSES["서서포즈"][0])[0],
                         second.split(", " + POSTURE_POSES["서서포즈"][1])[0])
        args["표정"] = "순차"
        self.assertTrue(node.generate(0, "고정", **args)[0].startswith("smiling, "))
        self.assertTrue(node.generate(0, "고정", **args)[0].startswith("expressionless, "))

    def test_cache_and_schema(self):
        value = Node.IS_CHANGED(42, "고정", 서서포즈="순차")
        self.assertNotEqual(value, value)
        schema = Node.INPUT_TYPES()
        self.assertEqual(schema["required"]["시드_모드"][0], ["고정", "자동"])
        self.assertEqual(Node.IS_CHANGED(42, "고정", 추가_태그="순차"), 42)
        self.assertGreater(len(schema["optional"]["표정"][0]), 40)
        for pool in POSTURE_POSES.values():
            self.assertEqual(len(pool), len(set(pool)))
        for spec in schema["optional"].values():
            if isinstance(spec[0], list) and "random" in spec[0]:
                self.assertIn("순차", spec[0])

    def test_group_counts_and_pose_precedence(self):
        for count in range(1, 7):
            for pose in GROUP_POSES:
                prompt = Node().generate(0, "고정", 촬영_인원=str(count),
                    프로필_단체포즈=pose, 서서포즈="순차", 추가_태그="high quality, 1girl, solo, adult")[0]
                self.assertNotIn("1girl", prompt)
                self.assertNotIn(POSTURE_POSES["서서포즈"][0], prompt)
                self.assertIn(GROUP_POSES[pose](count), prompt)
                if count > 1:
                    self.assertIn(f"exactly {count} adults", prompt)
                    self.assertNotIn("solo", prompt)
        node = Node()
        outputs = [node.generate(0, "고정", 촬영_인원="6", 프로필_단체포즈="순차")[0]
                   for _ in range(len(GROUP_POSES) + 1)]
        self.assertEqual(outputs[0], outputs[-1])
        self.assertEqual(len(set(outputs[:-1])), len(GROUP_POSES))

    def test_postures_are_split_and_direction_is_independent(self):
        schema = Node.INPUT_TYPES()["optional"]
        for category in ("서서포즈", "앉기포즈", "누워포즈"):
            self.assertIn(category, schema)
            self.assertGreater(len(POSTURE_POSES[category]), 50)
        prompt = Node().generate(0, "고정", 누워포즈="순차",
                                 이미지방향="portrait orientation, vertical composition")[0]
        self.assertIn(POSTURE_POSES["누워포즈"][0], prompt)
        self.assertIn("portrait orientation, vertical composition", prompt)

    def test_edit_clothing_toggle_and_expanded_clothing(self):
        schema = Node.INPUT_TYPES()["optional"]
        self.assertGreater(len(schema["의상"][0]), 200)
        self.assertGreater(len(schema["란제리"][0]), 120)
        self.assertGreater(len(schema["신발"][0]), 40)
        self.assertGreater(len(schema["팬티스타킹"][0]), 35)
        prompt = Node().generate(0, "고정", 의상제거=True,
                                 의상="plain white t-shirt and blue jeans")[0]
        self.assertIn("remove original clothing completely", prompt)
        self.assertIn("plain white t-shirt and blue jeans", prompt)


if __name__ == "__main__":
    unittest.main()
