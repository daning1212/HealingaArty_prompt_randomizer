import random
import re

# Automatic pose selection contains only body posture and framing.
# Legacy menu entries remain available for saved workflows/manual selection.
PURE_POSES = {
    "세로포즈": [f"{pose}, vertical" for pose in (
        "standing upright, arms relaxed at sides", "standing hands on hips",
        "standing arms folded", "standing hands behind back",
        "standing one hand on hip", "standing arms raised overhead",
        "standing arms extended sideways", "standing elbows bent, palms upward",
        "standing weight on left leg", "standing weight on right leg",
        "standing ankles crossed", "standing feet wide apart",
        "standing side profile", "standing three-quarter turn",
        "standing back view, head turned over shoulder", "standing one knee raised",
        "standing on tiptoes", "standing one arm extended forward",
        "standing hands clasped in front", "standing one hand on chin",
        "standing hands on cheeks", "standing one arm behind head",
        "standing both hands behind head", "standing torso tilted sideways",
        "standing torso leaning slightly forward", "standing shoulders turned",
        "kneeling upright, hands on thighs", "kneeling on one knee",
        "kneeling hands clasped", "squatting hands on knees",
        "squatting arms resting on knees", "sitting upright, knees together",
        "sitting one knee raised", "sitting legs crossed",
        "standing one heel raised", "standing elbows drawn back",
        "standing palms together at chest", "standing one hand on opposite shoulder",
        "standing forearms crossed behind back", "standing one arm raised diagonally",
        "walking forward, arms swinging naturally",
        "walking away, relaxed stride", "walking in side profile",
        "walking diagonally toward camera", "walking with a long stride",
        "walking with small measured steps", "walking on tiptoes",
        "walking with hands behind back", "walking with one hand on hip",
        "walking and turning head sideways", "walking and looking over shoulder",
        "walking with crossed runway steps", "walking with shoulders relaxed",
        "walking with torso turning", "walking mid-step, heel lifting",
        "walking mid-step, front heel touching down",
        "jogging forward, elbows bent", "jogging in side profile",
        "jogging away from camera", "running forward, arms pumping",
        "running in side profile, long stride", "running diagonally",
        "sprinting, torso leaning forward", "running mid-stride, both feet airborne",
        "running with one knee lifted high", "running while turning head sideways",
        "slowing from a run, shortened stride", "standing catching breath, hands on hips",
        "bending forward catching breath, hands on knees",
        "stepping sideways, arms balancing", "stepping backward, one arm extended",
        "pivoting on one foot", "turning around mid-step",
        "skipping forward, one knee lifted", "hopping on one foot",
        "jumping straight upward, arms raised", "jumping with knees bent",
        "jumping with arms and legs spread", "landing from a jump, knees flexed",
        "standing reaching upward with one hand", "standing reaching forward with both hands",
        "standing reaching sideways", "standing waving at shoulder height",
        "standing pointing sideways", "standing pointing upward",
        "standing palms facing outward", "standing shrugging, palms upward",
        "standing brushing hair back with one hand", "standing tucking hair behind ear",
        "standing rubbing the back of neck", "standing rubbing one shoulder",
        "standing covering a yawn with one hand", "standing stretching both arms upward",
        "standing stretching one arm across chest", "standing stretching triceps overhead",
        "standing side stretch, arm curved overhead", "standing torso twist, hands on waist",
        "standing calf stretch, one leg extended back", "standing quad stretch, holding ankle",
        "standing balancing on one leg, arms out",
        "standing ankles together, hips gently shifted",
        "standing torso in a gentle S-curve", "standing hips angled, shoulders facing forward",
        "standing one hand resting at waist, opposite shoulder lowered",
        "standing three-quarter back view, chin turned toward shoulder",
        "standing slight back arch, arms relaxed",
        "standing one knee bent inward, hands behind back",
        "standing one leg extended diagonally, toe pointed",
        "standing shoulders angled, hand resting on opposite upper arm",
        "standing head tilted, one hand resting on collarbone",
        "standing arms loosely crossed at waist",
        "sitting down, knees bending and torso forward",
        "rising from sitting, weight shifting forward",
        "sitting upright, hands resting on thighs",
        "sitting ankles crossed, torso turned sideways",
        "sitting knees together, legs angled sideways",
        "sitting leaning forward, elbows resting on knees",
        "sitting hands clasped between knees",
        "sitting one hand supporting chin, elbow on knee",
        "sitting back straight, shoulders turned",
        "sitting one leg crossed over the other, hands folded",
        "kneeling upright, arms stretched upward",
        "kneeling on one knee, torso turned",
        "kneeling sitting back on heels, hands in lap",
        "lowering onto one knee, arms balancing",
        "rising from kneeling, one foot planted",
        "squatting with heels raised, arms forward",
        "squatting torso turned sideways",
        "standing half squat, hands extended forward",
        "dancing side step, one arm curved overhead",
        "dancing with crossed feet, arms extended",
        "dancing mid-turn, one heel raised",
        "dancing with bent knees, shoulders tilted",
        "ballet first position, arms rounded in front",
        "ballet releve, arms rounded overhead",
        "ballet arabesque, one leg extended backward",
        "standing lunge, arms extended at shoulder height",
        "standing wide stance, one knee bent and opposite leg straight",
        "standing hands together near cheek, head tilted",
        "standing one palm resting over chest",
        "standing loosely hugging own shoulders",
        "studio portrait pose, shoulders square, chin level, hands relaxed",
        "studio portrait pose, torso turned thirty degrees, face toward camera",
        "studio portrait pose, arms loosely folded, shoulders lowered",
        "studio portrait pose, one hand lightly holding opposite wrist",
        "studio portrait pose, hands loosely clasped at waist",
        "studio portrait pose, one hand on hip, other arm relaxed",
        "studio portrait pose, shoulders at different heights, head gently tilted",
        "studio portrait pose, chin resting lightly on knuckles",
        "studio portrait pose, fingers resting gently near jawline",
        "studio portrait pose, side profile with straight posture",
        "studio portrait pose, three-quarter back view, face turned to camera",
        "studio portrait pose, elbows close to body, palms loosely joined",
        "studio portrait pose, seated upright, hands resting on knees",
        "studio portrait pose, seated sideways, torso turned toward camera",
        "studio portrait pose, seated ankles crossed, hands folded in lap",
        "studio portrait pose, leaning slightly forward, forearms on thighs",
        "studio portrait pose, hands behind back, chest open",
        "studio portrait pose, one hand on opposite forearm",
        "studio portrait pose, torso angled, eyes level with camera",
        "studio portrait pose, feet staggered, weight on rear leg",
    )],
    "가로포즈": [f"{pose}, horizontal" for pose in (
        "lying on back, arms at sides", "lying on stomach, chin on hands",
        "lying on left side, knees bent", "lying on right side, legs extended",
        "lying on back, hands behind head", "lying on stomach, feet crossed",
        "lying on side, propped on elbow", "lying on back, knees bent",
        "lying on back, ankles crossed", "lying on side, one knee raised",
        "lying on stomach, forearms supporting torso", "lying curled up",
        "lying on back, one arm overhead", "lying on back, arms extended sideways",
        "lying on stomach, arms extended forward", "lying on side, hand on hip",
        "lying on back, one knee drawn to chest", "lying on side, legs crossed at knees",
        "sitting legs extended forward", "sitting one leg bent, one leg extended",
        "sitting leaning back on hands", "sitting hugging knees",
        "sitting butterfly stretch", "sitting legs extended diagonally",
        "sitting torso twisted sideways", "sitting leaning forward, arms extended",
        "sitting knees bent to one side", "sitting ankles crossed, hands on knees",
        "lying on back, legs raised vertically", "lying on side, upper leg raised",
        "lying on stomach, knees bent and feet raised", "lying on back, hands on abdomen",
        "lying on side, lower arm extended", "lying on back, arms and legs extended",
        "lying on stomach, head turned sideways", "lying on back, knees together tilted sideways",
        "lying on side, knees drawn toward chest", "sitting cross-legged, palms on knees",
        "sitting one knee raised, forearm resting on knee", "lying on back, elbows bent beside head",
        "lying on back, one leg extended and other knee bent",
        "lying on back, fingers interlaced over abdomen",
        "lying on back, palms facing upward beside torso",
        "lying on back, hands resting on ribs",
        "lying on back, one hand behind head and other at side",
        "lying on back, both arms stretched overhead",
        "lying on back, one ankle resting over opposite knee",
        "lying on back, both knees drawn toward chest",
        "lying on back, knees tilted left and arms open",
        "lying on back, knees tilted right and arms open",
        "lying on back, lower legs raised parallel to ground",
        "lying on back, one straight leg raised diagonally",
        "lying on back, shoulders gently lifted",
        "lying on back, head turned toward camera",
        "lying on stomach, hands folded under cheek",
        "lying on stomach, cheek resting on forearm",
        "lying on stomach, chin lifted and elbows beneath shoulders",
        "lying on stomach, one knee bent outward",
        "lying on stomach, one forearm forward and other bent",
        "lying on stomach, hands behind lower back",
        "lying on stomach, one leg lifted slightly",
        "lying on stomach, arms extended sideways",
        "lying on stomach, torso gently twisted to one side",
        "lying on side, head resting on lower arm",
        "lying on side, head supported by hand",
        "lying on side, upper hand resting in front of chest",
        "lying on side, one leg straight and other bent",
        "lying on side, ankles crossed and upper hand at waist",
        "lying on side, shoulders turned slightly toward camera",
        "lying on side, upper arm curved overhead",
        "lying on side, knees stacked and feet together",
        "lying on side, torso forming a gentle curve",
        "reclining on forearms, knees bent together",
        "reclining on one forearm, legs extended diagonally",
        "reclining with one knee raised, opposite leg straight",
        "reclining with ankles crossed, shoulders relaxed",
        "reclining sideways, hand resting on waist",
        "reclining with torso gently arched, elbows supporting weight",
        "sitting legs straight, hands beside hips",
        "sitting legs apart in a gentle stretch, torso upright",
        "sitting cross-legged, hands loosely clasped",
        "sitting cross-legged, torso turned left",
        "sitting cross-legged, torso turned right",
        "sitting hugging one knee, other leg extended",
        "sitting both knees raised, forehead near knees",
        "sitting knees together, arms wrapped around shins",
        "sitting sideways with both legs folded",
        "sitting one leg folded under, other knee raised",
        "sitting leaning back on one hand, other on knee",
        "sitting leaning sideways onto forearm",
        "sitting reaching toward toes with both hands",
        "sitting reaching toward one foot, other knee bent",
        "sitting side stretch, one arm curved overhead",
        "sitting back upright, arms extended sideways",
        "sitting shoulders twisted, one hand behind torso",
        "sitting knees bent, feet flat and hands behind hips",
        "sitting with ankles crossed, chin resting on hand",
        "kneeling leaning forward, arms extended",
        "kneeling curled forward, arms beside legs",
        "kneeling forearms down, hips above knees",
        "kneeling reaching one arm forward",
        "on hands and knees, back neutral",
        "on hands and knees, spine rounded",
        "on hands and knees, chest gently lifted",
        "on hands and knees, opposite arm and leg extended",
        "low lunge, front knee bent and hands beside front foot",
        "forearm plank, body aligned",
        "high plank, arms straight",
        "side plank, upper arm extended upward",
        "side plank, lower knee bent for support",
        "push-up lowered position, elbows bent",
        "push-up raised position, elbows straight",
        "supine bridge, knees bent and hips lifted",
        "supine bridge, one leg extended",
        "seated balance, knees bent and feet lifted",
        "seated balance, arms extended forward",
        "prone back extension, arms beside torso",
        "prone stretch, opposite arm and leg lifted",
        "lying on back, alternating bent knees",
        "lying on back, feet together and knees relaxed outward",
        "lying on side, upper knee opening while feet stay together",
        "lying on back, one arm reaching across torso",
        "lying on stomach, one hand reaching forward",
        "sitting shifting weight onto one hip",
        "rolling from back onto side, knees slightly bent",
        "rising from lying, one elbow supporting torso",
        "lowering from sitting onto one forearm",
        "curling sideways, hands tucked near cheek",
        "lying on side, legs gently staggered",
        "lying on back, elbows wide and hands lightly behind head",
        "reclining with one arm overhead, head turned sideways",
        "sitting legs extended to one side, shoulders turned oppositely",
        "sitting torso angled forward, hands resting loosely on knees",
        "lying on stomach, feet raised and ankles loosely crossed",
        "lying on side, one hand resting on opposite shoulder",
        "sitting legs folded, one arm reaching diagonally upward",
        "lying on back, stretching fingertips and toes in opposite directions",
        "lying on side, forearm across waist and legs extended",
        "reclining with knees together angled sideways",
        "sitting gently leaning forward, chin raised",
    )],
}

GROUP_POSES = {
    "정면 나란히": lambda n: "standing front-facing, hands relaxed" if n == 1 else
        f"all {n} people standing side by side in one row, facing camera, evenly spaced",
    "몸을 살짝 틀기": lambda n: "standing with torso at a three-quarter angle, face toward camera" if n == 1 else
        f"all {n} people standing in one row, each torso slightly angled toward the center, faces toward camera",
    "팔짱 프로필": lambda n: "standing with arms loosely folded, shoulders relaxed" if n == 1 else
        f"all {n} people standing side by side with their own arms loosely folded, clear space between bodies",
    "앉아서 촬영": lambda n: "sitting upright, hands resting on thighs" if n == 1 else
        f"all {n} people sitting side by side, hands resting on their own thighs, every face visible",
    "높낮이 두 줄": lambda n: "sitting with one knee raised, forearm resting on knee" if n == 1 else
        f"{n // 2} people sitting in front and {n - n // 2} people standing behind, staggered faces, exactly {n} people total",
    "완만한 반원": lambda n: "standing with one hand on hip, body turned slightly" if n == 1 else
        f"all {n} people standing in a shallow semicircle, facing camera, no overlapping faces",
    "대각선 배치": lambda n: "standing diagonally, head turned toward camera" if n == 1 else
        f"all {n} people arranged along a shallow diagonal, staggered sideways so every face is visible",
    "함께 걷기": lambda n: "walking naturally toward camera, arms swinging" if n == 1 else
        f"all {n} people walking toward camera side by side, natural alternating strides, evenly spaced",
    "편하게 기대기": lambda n: "standing with weight shifted to one leg, shoulders relaxed" if n == 1 else
        f"all {n} people standing close side by side, shoulders gently leaning toward neighbors, faces unobstructed",
    "손 흔들기": lambda n: "standing and waving one hand beside shoulder" if n == 1 else
        f"all {n} people standing in one row, each waving one hand beside their own shoulder, hands away from faces",
    "뒤돌아보기": lambda n: "standing with back turned, looking toward camera over shoulder" if n == 1 else
        f"all {n} people standing in a staggered row with backs partly turned, each looking over shoulder toward camera",
    "앉아서 몸 틀기": lambda n: "sitting with knees angled sideways, shoulders facing camera" if n == 1 else
        f"all {n} people sitting side by side with knees angled slightly and shoulders facing camera, separate visible faces",
}

class HealingArtyPromptRandomizerV11:
    @classmethod
    def INPUT_TYPES(cls):
        inputs = {
            "required": {
                "시드": ("INT", {"default": -1, "min": -1, "max": 0xffffffffffffffff}),
                "시드_모드": (["고정", "자동"], {"default": "자동"}),
            },
            "optional": {
                "헤어스타일": ([
                    "none", "random",
                    "long hair, straight", "long hair, wavy", "long hair, curly", "long hair, layered",
                    "long hair, with bangs", "long hair, side bangs", "long hair, center part", "long hair, side part",
                    "long hair, hime cut", "long hair, blunt cut", "medium hair, straight", "medium hair, wavy",
                    "medium hair, curly", "medium hair, layered", "medium hair, lob cut", "medium hair, with bangs",
                    "medium hair, side swept", "short hair, bob cut", "short hair, pixie cut", "shoulder length hair, straight",
                    "shoulder length hair, wavy", "collarbone length hair, straight", "collarbone length hair, wavy",
                    "waist length hair, long", "hip length hair, very long", "knee length hair, extreme long",
                    "ponytail, high", "ponytail, low", "ponytail, side", "ponytail, sleek", "ponytail, messy",
                    "ponytail, bubble ponytail", "ponytail, scorpion braid ponytail", "ponytail, wrapped ponytail",
                    "twin tails, high", "twin tails, low", "twin tails, side", "twin tails, drills", "twin tails, curly",
                    "braided ponytail, single", "braided twin tails, double", "bun, high", "bun, low", "bun, messy", "bun, sleek",
                    "bun, space buns", "bun, donut bun", "bun, ballerina bun", "bun, top knot", "bun, double buns", "bun, braided bun", "bun, sock bun",
                    "half up half down, ponytail", "half up half down, bun", "half up half down, braid", "half up half down, bow", "half up half down, twisted",
                    "braid, single", "braid, french braid", "braid, dutch braid", "braid, fishtail braid", "braid, crown braid", "braid, side braid",
                    "braid, milkmaid braid", "braid, waterfall braid", "braid, rope braid", "braid, boxer braids", "braid, four strand braid", "braid, five strand braid",
                    "braid, ladder braid", "braid, snake braid", "braid, mermaid braid", "braid, pull through braid",
                    "hair up, elegant updo", "hair up, messy updo", "hair up, bridal updo", "hair up, vintage updo",
                    "hair up, beehive", "hair up, chignon", "hair up, french twist",
                    "hair down, flowing", "hair down, windswept", "hair down, wet look", "hair down, voluminous",
                    "hair down, sleek", "hair down, tousled", "hair down, bedhead", "hair down, mermaid waves",
                    "hair down, beach waves", "hair down, old hollywood waves",
                    "side swept hair, glamorous", "hair flipped over shoulder, sexy", "hair tucked behind ear, cute",
                    "hair covering one eye, mysterious", "hair blowing in wind, dynamic", "hair in face, sensual",
                    "hair, one side shaved, edgy", "hair, wolf cut", "hair, jellyfish cut", "hair, octopus cut",
                    "pigtails, low", "pigtails, high", "pigtails, braided", "pigtails, curly",
                    "odango, twin buns", "odango, single bun",
                    "hair accessories, ribbon", "hair accessories, headband", "hair accessories, hair clip",
                    "hair accessories, flower crown", "hair accessories, bow", "hair accessories, scrunchie",
                    "hair accessories, hair stick", "hair accessories, tiara", "hair accessories, veil",
                    "hair accessories, bandana", "hair accessories, scarf", "hair accessories, cat ears headband",
                    "black hair, natural", "brown hair, brunette", "blonde hair, golden", "blonde hair, platinum", "red hair, auburn",
                    "red hair, ginger", "pink hair, pastel", "pink hair, hot pink", "blue hair, pastel",
                    "blue hair, electric blue", "purple hair, lavender", "purple hair, violet", "green hair, mint",
                    "silver hair, gray", "white hair, albino", "ombre hair, gradient", "balayage hair, highlights",
                    "two-tone hair, split dye", "rainbow hair, colorful", "streaked hair, highlights",
                    "money piece hair, highlights", "peekaboo hair, hidden color", "dip dye hair", "galaxy hair, colorful"
                ],),
                "헤어스타일_가중치": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 2.0, "step": 0.1}),

                "표정": (["none", "random", "smiling", "expressionless", "winking", "slight smile", "confident look", "surprised", "seductive",
                    "gentle closed-mouth smile", "broad toothy smile", "joyful laughter",
                    "amused smile", "shy smile", "awkward smile", "relieved smile",
                    "proud expression", "hopeful expression", "serene expression",
                    "thoughtful expression", "curious expression", "puzzled expression",
                    "skeptical expression, one eyebrow raised", "shocked expression, wide eyes",
                    "awe-struck expression", "worried expression", "nervous expression",
                    "sad expression", "tearful eyes", "disappointed expression",
                    "lonely expression", "nostalgic expression", "determined expression",
                    "serious expression", "focused expression", "angry expression, furrowed brows",
                    "annoyed expression", "frustrated expression", "pouting",
                    "playful grin", "mischievous smirk", "embarrassed expression",
                    "sleepy expression, heavy eyelids", "tired expression", "bored expression",
                    "unimpressed expression", "tender expression", "grateful expression"],),
                "표정_가중치": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 2.0, "step": 0.1}),

                "의상": ([
                    "none", "random",
                    "school uniform, sailor uniform", "school uniform, blazer uniform", "school uniform, vest uniform",
                    "school uniform, cardigan uniform", "school uniform, summer uniform", "school uniform, winter uniform",
                    "school uniform, gym uniform", "school uniform, ribbon tie", "school uniform, checkered skirt",
                    "school uniform, knee socks uniform", "mini dress, tight bodycon", "mini dress, A-line", "mini dress, slip dress",
                    "mini dress, off-shoulder", "mini dress, halter neck", "mini dress, backless", "mini dress, strapless",
                    "mini dress, lace", "mini dress, satin", "mini dress, velvet", "mini dress, leather", "mini dress, sequin",
                    "mini dress, mesh", "mini dress, cutout sides", "mini dress, high slit", "mini dress, bandage",
                    "mini dress, ruched", "mini dress, wrap", "mini dress, shirt dress", "mini dress, sweater dress",
                    "mini dress, t-shirt dress", "mini dress, tube dress", "mini dress, cami dress", "mini dress, babydoll",
                    "mini dress, peplum", "mini dress, mermaid mini", "mini dress, corset dress", "mini dress, latex mini",
                    "mini dress, vinyl mini", "mini dress, fishnet mini", "mini dress, crochet mini", "evening gown, long slit",
                    "evening gown, mermaid style", "evening gown, ball gown", "cocktail dress, fitted", "cocktail dress, flared",
                    "party dress, glitter", "party dress, feather", "party dress, fringe", "red carpet dress, glamorous",
                    "prom dress, elegant", "wedding guest dress, formal", "club dress, revealing", "club dress, neon",
                    "club dress, mesh panel", "bodycon dress, nightclub", "sequin gown, evening", "velvet gown, evening",
                    "satin gown, evening", "lace gown, evening", "chiffon gown, evening", "halter gown, evening",
                    "one-shoulder gown, evening", "strapless gown, evening", "backless gown, evening", "high-low gown, evening",
                    "tea length dress, evening", "midi dress, evening", "maxi slit dress, evening", "wrap gown, evening",
                    "kimono dress, evening", "cheongsam mini dress", "crop top and mini skirt, sexy", "crop top and hot pants, sexy",
                    "tube top and mini skirt, revealing", "bralette and high waist shorts, sexy", "bustier and pencil skirt, sexy",
                    "off-shoulder top and micro skirt, sexy", "sheer blouse and mini skirt, sexy", "mesh top and leather skirt, sexy",
                    "backless top and tight pants, sexy", "halter top and short shorts, sexy", "tied shirt and mini skirt, sexy",
                    "cropped hoodie and yoga pants, sexy", "cutout top and leather pants, sexy", "lace top and denim shorts, sexy",
                    "satin cami and silk skirt, sexy", "corset top and mini skirt, sexy", "bodysuit and jeans, sexy",
                    "see-through shirt and bralette, sexy", "one-shoulder top and bodycon skirt, sexy", "asymmetric top and slit skirt, sexy",
                    "tube top and leather pants, sexy", "bralette and denim skirt, sexy", "mesh crop top and mini skirt, sexy",
                    "halter neck top and hot pants, sexy", "off-shoulder crop and tight skirt, sexy", "lace bralette and shorts, sexy",
                    "satin tube top and leather skirt, sexy", "backless halter and micro shorts, sexy", "cutout bodysuit and skirt, sexy",
                    "sheer crop top and high waist pants, sexy", "bandage top and bodycon skirt, sexy", "strappy crop and mini skirt, sexy",
                    "bustier top and leather shorts, sexy", "mesh bodysuit and denim skirt, sexy", "one-shoulder crop and hot pants, sexy",
                    "tied front top and slit skirt, sexy", "lace-up top and mini skirt, sexy", "backless crop and yoga pants, sexy",
                    "halter bralette and leather pants, sexy", "off-shoulder bodysuit and shorts, sexy", "see-through blouse and mini skirt, sexy",
                    "cropped sweater and bodycon skirt, sexy", "tube dress top and micro skirt, sexy", "satin halter and tight pants, sexy",
                    "mesh panel top and leather skirt, sexy", "cutout crop and denim shorts, sexy", "strapless top and slit skirt, sexy",
                    "lace crop and hot pants, sexy", "backless bodysuit and mini skirt, sexy", "halter crop and yoga pants, sexy",
                    "off-shoulder lace top and leather skirt, sexy", "sheer bodysuit and shorts, sexy", "bustier crop and tight skirt, sexy",
                    "tube top and high slit skirt, sexy", "mesh bralette and denim skirt, sexy", "one-shoulder mesh top and hot pants, sexy",
                    "cutout halter and micro skirt, sexy", "satin cami and leather pants, sexy", "backless lace top and mini skirt, sexy",
                    "strappy bodysuit and shorts, sexy", "office blouse, white shirt and pencil skirt", "office blouse, silk and tight skirt",
                    "blazer and mini skirt, office", "bodycon office dress, sexy", "pencil dress, office sexy", "wrap dress, office sexy",
                    "shirt dress, office sexy", "button-up tied and skirt, office", "vest and mini skirt, office",
                    "turtleneck and leather skirt, office", "satin blouse and pencil skirt, office", "blazer dress, office sexy",
                    "belted shirt dress, office", "sheer blouse and tight skirt, office", "high slit pencil skirt and blouse, office",
                    "crop blazer and mini skirt, office", "off-shoulder blouse and pencil skirt, office", "bodycon knit dress, office",
                    "lace blouse and leather skirt, office", "halter top and pencil skirt, office", "hoodie crop and shorts, casual sexy",
                    "sweater crop and jeans, casual sexy", "leather jacket and mini dress, sexy", "denim jacket and bodycon dress, sexy",
                    "tank top and leggings, sexy", "ribbed top and yoga pants, sexy", "t-shirt tied and skirt, sexy",
                    "shirt open and bralette, sexy", "knit dress, tight sexy", "sweater dress mini, sexy", "oversized shirt and bike shorts, sexy",
                    "crop knit and leather pants, sexy", "tube top and cargo pants, sexy", "bralette and oversized shirt, sexy",
                    "bodysuit and denim shorts, sexy", "halter crop and sweatpants, sexy", "off-shoulder sweater and mini skirt, sexy",
                    "backless top and jeans, sexy", "mesh t-shirt and biker shorts, sexy", "cropped hoodie and slit skirt, sexy",
                    "satin cami and cardigan, sexy", "lace bodysuit and jeans, sexy", "turtleneck crop and leather skirt, sexy",
                    "cutout sweater and shorts, sexy", "sheer top and denim skirt, sexy", "bustier and sweatpants, sexy",
                    "tube dress and denim jacket, sexy", "slip dress and oversized cardigan, sexy", "corset top and joggers, sexy",
                    "backless dress and leather jacket, sexy", "halter dress and hoodie, sexy", "mini skirt and thigh high socks, sexy",
                    "crop blazer and bralette, sexy", "sheer dress and shorts, sexy", "lace top and leather pants, sexy",
                    "bodysuit and mini skirt, sexy", "t-shirt dress tight, sexy", "off-shoulder crop and jeans, sexy",
                    "mesh hoodie and biker shorts, sexy", "satin slip and denim jacket, sexy", "cutout top and cargo skirt, sexy",
                    "tube top and knit cardigan, sexy", "bralette and leather jacket, sexy", "backless sweater and mini skirt, sexy",
                    "halter top and ripped jeans, sexy", "sheer sweater and leather shorts, sexy", "corset and oversized shirt, sexy",
                    "lace cami and sweatpants, sexy", "crop tank and bodycon skirt, sexy", "off-shoulder bodysuit and denim shorts, sexy",
                    "mesh dress and hoodie, sexy"
                ],),
                "의상_가중치": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 2.0, "step": 0.1}),

                "란제리": ([
                    "none", "random", "lingerie, lace bra and thong set, red", "lingerie, lace bra and panty set, black",
                    "lingerie, satin bra and thong, white", "lingerie, sheer mesh bra and g-string, pink", "lingerie, balconette bra and high waist panty, nude",
                    "lingerie, push-up bra and lace thong, blue", "lingerie, strapless bra and cheeky panty, purple",
                    "lingerie, plunge bra and tanga, emerald", "lingerie, demi cup bra and brazilian panty, wine",
                    "lingerie, bralette and boyshort set, pastel", "lingerie, teddy bodysuit, black lace", "lingerie, teddy bodysuit, red satin",
                    "lingerie, teddy bodysuit, sheer mesh", "lingerie, teddy bodysuit, crotchless", "lingerie, teddy bodysuit, backless",
                    "lingerie, teddy bodysuit, halter neck", "lingerie, teddy bodysuit, strappy", "lingerie, teddy bodysuit, leather",
                    "lingerie, teddy bodysuit, fishnet", "lingerie, teddy bodysuit, floral lace", "lingerie, corset, underbust, black",
                    "lingerie, corset, overbust, red satin", "lingerie, corset, steel boned, white", "lingerie, corset, lace-up front",
                    "lingerie, corset, ribbon lacing", "lingerie, corset, strapless", "lingerie, corset, longline", "lingerie, corset, waspie",
                    "lingerie, corset, brocade", "lingerie, corset, leather", "lingerie, babydoll, sheer chiffon, pink",
                    "lingerie, babydoll, lace trim, black", "lingerie, babydoll, satin, white", "lingerie, babydoll, open cup",
                    "lingerie, babydoll, halter style", "lingerie, babydoll, split side", "lingerie, babydoll, ruffled hem",
                    "lingerie, babydoll, floral embroidery", "lingerie, babydoll, mesh panel", "lingerie, babydoll, crotchless panty",
                    "lingerie, garter belt and stockings, black", "lingerie, garter belt and stockings, red", "lingerie, garter belt and thong set",
                    "lingerie, garter belt, lace, white", "lingerie, garter belt, strappy, pink", "lingerie, suspender belt, satin",
                    "lingerie, thigh high stockings, lace top", "lingerie, thigh high stockings, fishnet", "lingerie, thigh high stockings, sheer",
                    "lingerie, thigh high stockings, back seam", "lingerie, bodystocking, full body, black", "lingerie, bodystocking, crotchless",
                    "lingerie, bodystocking, fishnet", "lingerie, bodystocking, lace pattern", "lingerie, bodystocking, open bust",
                    "lingerie, bodystocking, long sleeve", "lingerie, bodystocking, halter", "lingerie, bodystocking, cutout",
                    "lingerie, bodystocking, floral mesh", "lingerie, bodystocking, strappy harness", "lingerie, strappy harness bra",
                    "lingerie, strappy harness panty", "lingerie, strappy cage bra", "lingerie, strappy body harness",
                    "lingerie, choker and garter set", "lingerie, nipple pasties, rhinestone", "lingerie, nipple pasties, tassel",
                    "lingerie, open cup bra, black lace", "lingerie, shelf bra and thong", "lingerie, cupless bra and g-string",
                    "lingerie, crotchless panty, lace", "lingerie, crotchless panty, satin", "lingerie, crotchless panty, pearl string",
                    "lingerie, crotchless panty, open back", "lingerie, thong, v-string, lace", "lingerie, thong, g-string, mesh",
                    "lingerie, thong, low rise, satin", "lingerie, thong, high cut, leather", "lingerie, thong, strappy side",
                    "lingerie, cheeky panty, lace back", "lingerie, brazilian panty, cutout", "lingerie, tanga panty, sheer",
                    "lingerie, boyshort, lace trim", "lingerie, boyshort, open back", "lingerie, kimono robe, sheer lace",
                    "lingerie, kimono robe, satin", "lingerie, chemise, silk, black", "lingerie, chemise, lace hem, red",
                    "lingerie, chemise, slit side", "lingerie, slip dress, satin, nude", "lingerie, slip dress, lace, white",
                    "lingerie, peignoir set, sheer", "lingerie, bustier and g-string set", "lingerie, bustier, longline, lace",
                    "lingerie, bustier, strapless", "lingerie, merry widow, vintage", "lingerie, merry widow, lace-up",
                    "lingerie, cami set and shorts, satin", "lingerie, bralette and thong, strappy back", "lingerie, lace bodysuit, snap crotch",
                    "lingerie, mesh bodysuit, long sleeve", "lingerie, fishnet bodysuit, cutout", "lingerie, latex bra and panty set",
                    "lingerie, wetlook teddy"
                ],),
                "란제리_가중치": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 2.0, "step": 0.1}),

                "수영복": ([
                    "none", "random", "bikini, basic bikini", "bikini, triangle bikini", "bikini, bandeau bikini",
                    "bikini, halter bikini", "bikini, string bikini", "bikini, high waisted bikini", "bikini, sport bikini",
                    "one piece swimsuit, classic", "one piece swimsuit, cutout", "one piece swimsuit, high leg",
                    "monokini, sexy monokini", "tankini, casual tankini", "micro bikini, revealing", "mesh swimsuit, see-through",
                    "wet swimsuit, sheer", "swim dress, cute", "rash guard, sporty", "wetsuit, tight fit",
                    "competitive swimsuit, athletic", "one piece, athletic", "slingshot bikini, extreme", "micro slingshot bikini",
                    "string slingshot bikini", "V-string slingshot bikini", "G-string slingshot bikini", "thong slingshot bikini",
                    "minimal slingshot bikini", "side-tie slingshot bikini", "halter slingshot bikini", "cross-back slingshot bikini",
                    "one-piece slingshot swimsuit", "monokini slingshot", "cutout slingshot bikini", "mesh slingshot bikini",
                    "fishnet slingshot bikini", "lace slingshot bikini", "satin slingshot bikini", "latex slingshot bikini",
                    "vinyl slingshot bikini", "leather slingshot bikini", "metallic slingshot bikini", "holographic slingshot bikini",
                    "neon slingshot bikini", "transparent slingshot bikini", "wet look slingshot bikini", "oil slingshot bikini",
                    "chain slingshot bikini", "rhinestone slingshot bikini", "sequin slingshot bikini", "strappy slingshot bikini",
                    "minimalist slingshot bikini", "extreme micro slingshot", "barely-there slingshot", "sideboob slingshot bikini",
                    "underboob slingshot bikini", "backless slingshot bikini", "high-cut slingshot bikini", "low-rise slingshot bikini",
                    "adjustable slingshot bikini", "tie-side slingshot bikini", "crisscross slingshot bikini", "strapless slingshot bikini",
                    "asymmetric slingshot bikini", "ruched slingshot bikini", "ribbed slingshot bikini", "ribbed texture slingshot",
                    "crochet slingshot bikini", "knit slingshot bikini", "sheer slingshot bikini", "see-through slingshot bikini",
                    "micro bikini, extreme micro", "micro bikini, string micro", "micro bikini, dental floss bikini", "micro bikini, sheer mesh",
                    "micro bikini, transparent", "micro bikini, metallic finish", "micro bikini, holographic", "micro bikini, neon color",
                    "micro bikini, leopard print", "micro bikini, lace trim", "micro bikini, strappy design", "micro bikini, cutout front",
                    "micro bikini, side tie", "micro bikini, minimal coverage", "micro bikini, barely there", "micro bikini, high cut leg",
                    "micro bikini, underboob style", "micro bikini, sideboob style", "micro bikini, backless", "micro bikini, G-string bottom",
                    "micro bikini, V-string bottom", "micro bikini, T-back bottom", "micro bikini, chain straps", "micro bikini, rhinestone detail",
                    "micro bikini, sequin embellished", "micro bikini, wet look", "micro bikini, oily skin effect", "micro bikini, crochet handmade",
                    "micro bikini, leather look", "micro bikini, latex style"
                ],),
                "수영복_가중치": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 2.0, "step": 0.1}),

                "신발": (["none", "random", "sneakers", "loafers", "boots", "high heels", "sandals", "barefoot"],),
                "신발_가중치": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 2.0, "step": 0.1}),

                "가방": (["none", "random", "backpack", "tote bag", "crossbody bag", "clutch"],),
                "가방_가중치": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 2.0, "step": 0.1}),

                "안경": (["none", "random", "round glasses", "horn-rimmed glasses", "sunglasses"],),
                "안경_가중치": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 2.0, "step": 0.1}),

                "모자": (["none", "random", "baseball cap", "beanie", "beret", "bucket hat"],),
                "모자_가중치": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 2.0, "step": 0.1}),

                "화장": (["none", "random", "natural makeup", "glitter makeup", "smoky makeup", "bare face", "coral makeup"],),
                "화장_가중치": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 2.0, "step": 0.1}),

                "분위기": (["none", "random", "sexy and provocative", "bright and cheerful", "chic", "warm mood", "dreamy", "vintage", "cyberpunk"],),
                "분위기_가중치": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 2.0, "step": 0.1}),

                "실내장소": ([
                    "none", "random", "studio", "white background studio", "black background studio", "bedroom", "hotel room",
                    "bathroom", "living room", "kitchen", "cafe", "library", "bookstore", "office", "classroom", "gym",
                    "yoga studio", "dance studio", "art studio", "music room", "recording studio", "bar", "club", "restaurant",
                    "hotel lobby", "elevator", "corridor", "stairway", "attic", "basement", "garage", "greenhouse"
                ],),
                "실내장소_가중치": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 2.0, "step": 0.1}),

                "실외장소": ([
                    "none", "random", "beach", "sunset beach", "forest", "deep forest", "bamboo forest", "street",
                    "city street", "alley", "rooftop", "city rooftop", "park", "playground", "garden", "flower garden",
                    "cherry blossom street", "mountain", "cliff", "waterfall", "lakeside", "riverside", "field",
                    "flower field", "wheat field", "desert", "snowy field", "countryside", "village", "downtown",
                    "night city", "neon street"
                ],),
                "실외장소_가중치": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 2.0, "step": 0.1}),

                "소품": (["none", "random", "coffee cup", "book", "bouquet", "camera", "cat", "umbrella"],),
                "소품_가중치": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 2.0, "step": 0.1}),

                "추가_태그": ("STRING", {"default": "high quality, detailed, photorealistic, 1girl, adult", "multiline": True}),

                "세로포즈": ([
                    "none", "random", "standing facing forward, vertical", "one hand on hip standing, vertical",
                    "arms crossed standing, vertical", "leaning against wall, vertical", "standing back turned looking back, vertical",
                    "standing one leg raised, vertical", "jumping pose, vertical", "walking pose, vertical", "running pose, vertical",
                    "standing on tiptoes, vertical", "sitting on chair front, vertical", "sitting on chair sideways, vertical",
                    "sitting legs crossed on chair, vertical", "kneeling sitting upright, vertical", "sitting cross-legged on chair, vertical",
                    "sitting leaning on desk, vertical", "squatting looking at camera, vertical", "squatting head down, vertical",
                    "sitting on stairs legs together, vertical", "kneeling on floor upright, vertical", "sitting one knee up, vertical",
                    "sitting holding chair back, vertical", "sitting chin on hand, vertical", "sitting peace sign, vertical",
                    "sitting looking up sky, vertical", "standing side profile, vertical", "standing 45 degree turn, vertical",
                    "standing back view, vertical", "standing waving hand, vertical", "standing flipping hair, vertical",
                    "looking back over shoulder, vertical", "standing arms spread, vertical", "standing one hand in pocket, vertical",
                    "standing both hands in pockets, vertical", "standing hand covering mouth, vertical", "stretching pose standing, vertical",
                    "yoga tree pose, vertical", "ballet pose, vertical", "singing with microphone, vertical", "gun shooting pose, vertical",
                    "sword swinging pose, vertical", "bow shooting pose, vertical", "dancing pose, vertical", "hand heart pose, vertical",
                    "cheek heart pose, vertical", "finger heart, vertical", "peace sign pose, vertical", "thumbs up pose, vertical",
                    "ok sign pose, vertical", "hands covering face, vertical", "hands covering eyes, vertical", "cute hands together, vertical",
                    "hands on cheeks, vertical", "heart above head, vertical", "holding flowers standing, vertical",
                    "holding umbrella standing, vertical", "holding bag standing, vertical", "holding coffee standing, vertical",
                    "holding book standing, vertical", "standing with hip pop, sexy vertical", "leaning against wall seductively, sexy vertical",
                    "standing hand on thigh, sexy vertical", "stretching arms up revealing midriff, sexy vertical", "standing back to camera looking over shoulder, sexy vertical",
                    "standing contrapposto pose, vertical", "standing weight on one leg, vertical", "standing legs crossed, vertical",
                    "standing ankle crossed, vertical", "standing wide stance, vertical", "standing hands on hips, vertical",
                    "standing arms folded, vertical", "standing hand on chin thinking, vertical", "standing scratching head, vertical",
                    "standing adjusting glasses, vertical", "standing fixing tie, vertical", "standing rolling up sleeves, vertical",
                    "standing checking watch, vertical", "standing pointing forward, vertical", "standing saluting pose, vertical",
                    "standing blowing kiss, vertical", "standing shy pose hands behind back, vertical", "standing confident smile, vertical",
                    "standing laughing pose, vertical", "standing surprised hands on face, vertical", "standing cold hugging self, vertical",
                    "standing praying hands, vertical", "standing namaste pose, vertical", "standing victory pose arms up, vertical",
                    "standing rock on pose, vertical", "standing finger gun pose, vertical", "standing call me gesture, vertical",
                    "standing shushing finger on lips, vertical", "standing thinking finger on temple, vertical", "standing come here gesture, vertical",
                    "standing stop hand gesture, vertical", "standing presenting with hand, vertical", "standing holding hat, vertical",
                    "standing holding jacket over shoulder, vertical", "standing holding phone to ear, vertical", "standing texting on phone, vertical",
                    "standing taking selfie, vertical", "standing holding camera, vertical", "standing holding skateboard, vertical",
                    "standing holding guitar, vertical", "standing holding basketball, vertical", "standing holding sword at side, vertical",
                    "standing superhero pose, vertical", "standing power pose hands on hips, vertical", "standing model pose, vertical",
                    "standing fashion pose, vertical", "standing leaning on railing, vertical", "standing leaning on table, vertical",
                    "standing leaning on doorframe, vertical", "standing against tree, vertical", "standing under streetlight, vertical",
                    "standing in doorway, vertical", "standing on balcony, vertical", "standing on stairs looking down, vertical",
                    "standing on top of stairs, vertical", "walking down stairs, vertical", "walking up stairs, vertical",
                    "sitting on bar stool, vertical", "sitting on high chair, vertical", "sitting on counter edge, vertical",
                    "sitting on windowsill, vertical", "sitting on fence, vertical", "sitting on table edge, vertical",
                    "sitting on desk corner, vertical", "sitting on hood of car, vertical", "sitting on park bench, vertical",
                    "kneeling prayer pose, vertical", "kneeling hands clasped, vertical", "kneeling looking up, vertical",
                    "kneeling one knee up, vertical", "half kneeling pose, vertical", "kneeling holding flowers, vertical",
                    "squatting hands on knees, vertical", "squatting asian squat, vertical", "squatting tying shoelace, vertical",
                    "squatting picking flower, vertical", "squatting arms resting on knees, vertical", "warrior pose yoga, vertical",
                    "mountain pose yoga, vertical", "chair pose yoga, vertical", "eagle pose yoga, vertical", "dancer pose yoga, vertical",
                    "standing bow pulling pose, vertical", "standing leg lift ballet, vertical", "standing arabesque pose, vertical",
                    "standing high kick, vertical", "standing martial arts stance, vertical", "standing karate pose, vertical",
                    "standing handstand against wall, vertical", "standing shoulder stretch, vertical", "standing side stretch, vertical",
                    "standing backbend, vertical", "standing hair flip motion, vertical", "standing dress twirl, vertical",
                    "standing skirt holding pose, sexy vertical", "standing leaning back hands on wall, sexy vertical", "standing one shoulder exposed, sexy vertical",
                    "standing biting lip, sexy vertical", "standing running hand through hair, sexy vertical", "standing arching back, sexy vertical",
                    "standing looking down seductive, sexy vertical", "standing pulling on tie, sexy vertical", "standing unbuttoning shirt, sexy vertical",
                    "standing over the shoulder glance, sexy vertical", "standing hip thrust forward, sexy vertical", "standing leg up on wall, sexy vertical",
                    "standing finger tracing collarbone, sexy vertical", "standing wet hair pose, sexy vertical", "standing towel drop pose, sexy vertical",
                    "sitting on chair legs crossed, sexy vertical", "sitting on stool leaning forward, sexy vertical", "sitting on table legs dangling, sexy vertical",
                    "kneeling upright hands on thighs, sexy vertical", "squatting back against wall, sexy vertical", "standing side boob pose, sexy vertical"
                ],),

                "가로포즈": ([
                    "none", "random", "lying on bed front, horizontal", "lying face down on bed, horizontal",
                    "lying on stomach legs raised, horizontal", "lying spread eagle on bed, horizontal",
                    "lying on sofa watching TV, horizontal", "lying on ground looking sky, horizontal", "lying on grass, horizontal",
                    "lying on beach, horizontal", "lying on side S-curve, horizontal", "sitting legs stretched sideways, horizontal",
                    "sitting legs extended, horizontal", "sitting legs spread stretching, horizontal", "sitting one leg bent, horizontal",
                    "sitting leaning back on floor, horizontal", "sitting arms on table, horizontal", "lying on stomach reading book, horizontal",
                    "lying on stomach chin on hands, horizontal", "lying on stomach legs kicking, horizontal", "lying on stomach looking camera, horizontal",
                    "cat pose yoga, horizontal", "downward dog yoga, horizontal", "cobra pose, horizontal", "plank pose, horizontal",
                    "sit-up pose, horizontal", "push-up pose, horizontal", "side plank, horizontal", "bridge pose, horizontal",
                    "lunge pose, horizontal", "squat pose, horizontal", "crawling on all fours, horizontal", "curled up sitting, horizontal",
                    "fetal position curled, horizontal", "curled up lying, horizontal", "lying sideways legs crossed, horizontal",
                    "playing piano pose, horizontal", "drawing pose, horizontal", "using laptop pose, horizontal", "eating pose, horizontal",
                    "riding bicycle pose, horizontal", "lying on bed with arched back, sexy horizontal", "lying on side touching thigh, sexy horizontal",
                    "lying on stomach lifting legs, sexy horizontal", "crawling on bed, sexy horizontal", "lying back with one leg up, sexy horizontal",
                    "lying on back hands behind head, sexy horizontal", "lying sideways finger on lips, sexy horizontal",
                    "lying on stomach looking back, sexy horizontal", "sitting with one leg extended, sexy horizontal",
                    "lying on side propped on elbow, sexy horizontal", "lying on back pulling shirt, sexy horizontal",
                    "prone position looking up, sexy horizontal", "lying on back legs crossed at ankles, horizontal", "lying on side one knee up, horizontal",
                    "lying on stomach feet crossed, horizontal", "lying starfish pose, horizontal", "lying hugging pillow, horizontal",
                    "lying phone in hand, horizontal", "lying reading book on back, horizontal", "lying looking at ceiling, horizontal",
                    "lying side sleeping pose, horizontal", "lying on hammock, horizontal", "lying on picnic blanket, horizontal",
                    "lying on yoga mat stretching, horizontal", "lying on floor exhausted, horizontal", "lying on beach towel, horizontal",
                    "lying on poolside lounger, horizontal", "lying on grass arms behind head, horizontal", "lying on bed hugging knees, horizontal",
                    "lying on side fetal position, horizontal", "lying on back sunbathing, horizontal", "lying on stomach sunbathing, horizontal",
                    "sitting legs crossed on floor, horizontal", "sitting butterfly stretch, horizontal", "sitting straddle stretch, horizontal",
                    "sitting pike stretch, horizontal", "sitting hurdler stretch, horizontal", "sitting cross-legged meditating, horizontal",
                    "sitting lotus pose, horizontal", "sitting seiza pose, horizontal", "sitting w-sit pose, horizontal",
                    "sitting indian style, horizontal", "sitting on floor hugging legs, horizontal", "sitting leaning on wall, horizontal",
                    "sitting leaning on sofa, horizontal", "sitting on floor back against bed, horizontal", "sitting playing guitar on floor, horizontal",
                    "sitting drawing on floor, horizontal", "sitting laptop on lap, horizontal", "sitting eating on floor, horizontal",
                    "sitting picnic pose, horizontal", "sitting building sandcastle, horizontal", "sitting legs in water, horizontal",
                    "child pose yoga, horizontal", "happy baby pose yoga, horizontal", "supine twist yoga, horizontal",
                    "reclined pigeon pose, horizontal", "legs up the wall pose, horizontal", "corpse pose yoga, horizontal",
                    "boat pose on floor, horizontal", "seated forward bend, horizontal", "wide-legged forward bend, horizontal",
                    "kneeling forward stretch, horizontal", "camel pose yoga, horizontal", "bow pose yoga, horizontal",
                    "locust pose yoga, horizontal", "superman pose, horizontal", "swimming kick pose, horizontal",
                    "crawling baby pose, horizontal", "bear crawl pose, horizontal", "leopard crawl pose, horizontal",
                    "crab walk pose, horizontal", "inchworm pose, horizontal", "lying on back making snow angel, horizontal",
                    "lying on stomach sand angel, horizontal", "lying reaching for toes, horizontal", "lying scissor legs, horizontal",
                    "lying bicycle kicks, horizontal", "lying flutter kicks, horizontal", "lying leg raises, horizontal",
                    "lying hip bridge hold, horizontal", "lying pelvic tilt, horizontal", "lying knee to chest, horizontal",
                    "lying figure four stretch, horizontal", "lying spinal twist, horizontal", "lying happy baby stretch, horizontal",
                    "lying on side leg lift, horizontal", "lying on side clamshell, horizontal", "lying on stomach back extension, horizontal",
                    "lying on back arms and legs spread, sexy horizontal", "lying on side arching back, sexy horizontal", "lying on stomach hips raised, sexy horizontal",
                    "lying on back biting finger, sexy horizontal", "lying on side running hand down body, sexy horizontal", "lying on back pulling down strap, sexy horizontal",
                    "lying on stomach looking over shoulder, sexy horizontal", "lying on side hair spread out, sexy horizontal", "lying on back one arm above head, sexy horizontal",
                    "lying on stomach chest pressed down, sexy horizontal", "lying on side legs tangled, sexy horizontal", "lying on back wet shirt, sexy horizontal",
                    "crawling toward camera, sexy horizontal", "lying on back knees bent apart, sexy horizontal", "lying on side hand on hip, sexy horizontal",
                    "lying on stomach pushing up, sexy horizontal", "lying on back arching neck, sexy horizontal", "lying on side legs crossed at knee, sexy horizontal"
                ],),
                "촬영_인원": (["none", "1", "2", "3", "4", "5", "6"],),
                "프로필_단체포즈": (["none", "random", *GROUP_POSES],),
            }
        }
        for name, spec in inputs["optional"].items():
            if isinstance(spec[0], list) and "random" in spec[0]:
                spec[0].insert(2, "순차")
                if name in PURE_POSES:
                    spec[0].extend(pose for pose in PURE_POSES[name] if pose not in spec[0])
        return inputs

    RETURN_TYPES = ("STRING", "STRING", "INT")
    RETURN_NAMES = ("positive_prompt", "세부사항", "사용된_시드")
    FUNCTION = "generate"
    CATEGORY = "HealingArty"

    def generate(self, 시드, 시드_모드="자동", **kwargs):
        if not hasattr(self, "_sequence_positions"):
            self._sequence_positions = {}
        if 시드_모드 == "자동" or 시드 == -1:
            실제_시드 = random.randint(0, 0xffffffffffffffff)
        else:
            실제_시드 = 시드

        rng = random.Random(실제_시드)
        parts = []
        details = []

        options = self.INPUT_TYPES()["optional"]
        count_value = kwargs.get("촬영_인원", "none")
        count = int(count_value) if str(count_value) in ("1", "2", "3", "4", "5", "6") else None
        group_active = count is not None and kwargs.get("프로필_단체포즈", "none") != "none"
        if count is not None:
            parts.append("solo portrait of one adult" if count == 1 else
                         f"group portrait of exactly {count} adults, {count} people total, all faces visible")
            details.append(f"촬영 인원: {count}")
        for key, val in kwargs.items():
            if key.endswith("_가중치") or key in ("추가_태그", "순차_시작번호", "순차_리셋", "촬영_인원"):
                continue
            if group_active and key in ("가로포즈", "세로포즈"):
                continue
            if key == "프로필_단체포즈" and count is None:
                continue
            if key not in options:
                continue
            if val not in [None, "none"]:
                if val in ("random", "순차"):
                    옵션리스트 = PURE_POSES.get(key, [
                        item for item in options[key][0] if item not in ("none", "random", "순차")
                    ])
                    if val == "순차":
                        position = self._sequence_positions.get(key, 0)
                        picked = 옵션리스트[position % len(옵션리스트)]
                        self._sequence_positions[key] = position + 1
                        details.append(f"{key} 순번: {position % len(옵션리스트) + 1}/{len(옵션리스트)}")
                    else:
                        picked = rng.choice(옵션리스트)
                else:
                    picked = val
                if key == "프로필_단체포즈":
                    picked = GROUP_POSES[picked](count)
                weight = kwargs.get(f"{key}_가중치", 1.0)
                parts.append(f"({picked}:{weight:g})" if weight != 1.0 else picked)
                details.append(f"{key}: {picked}")

        추가_태그 = kwargs.get("추가_태그", "")
        if count is not None:
            추가_태그 = re.sub(r"\b1(?:girl|boy|woman|man)\b", "", 추가_태그, flags=re.IGNORECASE)
            if count > 1:
                추가_태그 = re.sub(r"\bsolo\b", "", 추가_태그, flags=re.IGNORECASE)
            추가_태그 = ", ".join(part.strip() for part in 추가_태그.split(",") if part.strip())
        if 추가_태그.strip():
            parts.append(추가_태그.strip())

        positive_prompt = ", ".join(parts) if parts else "1girl"
        세부사항 = f"Seed mode: {시드_모드} | Seed: {실제_시드} | " + " / ".join(details)

        return (positive_prompt, 세부사항, 실제_시드)

    @classmethod
    def IS_CHANGED(cls, 시드, 시드_모드="자동", **kwargs):
        categories = cls.INPUT_TYPES()["optional"]
        has_sequence = any(value == "순차" for key, value in kwargs.items()
                           if key in categories and isinstance(categories[key][0], list))
        if 시드_모드 == "자동" or 시드 == -1 or has_sequence:
            return float("nan")
        return 시드

NODE_CLASS_MAPPINGS = {"HealingArtyPromptRandomizerV11": HealingArtyPromptRandomizerV11}
NODE_DISPLAY_NAME_MAPPINGS = {"HealingArtyPromptRandomizerV11": "HealingArty Prompt Randomizer V11"}
