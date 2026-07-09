import random
import time

class HealingArtyPromptRandomizerV11:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "시드": ("INT", {"default": -1, "min": -1, "max": 0xffffffffffffffff}),
                "랜덤_모드": (["고정", "완전랜덤"], {"default": "완전랜덤"}),
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

                "표정": (["none", "random", "smiling", "expressionless", "winking", "slight smile", "confident look", "surprised", "seductive"],),
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
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "INT")
    RETURN_NAMES = ("positive_prompt", "세부사항", "사용된_시드")
    FUNCTION = "generate"
    CATEGORY = "HealingArty"

    def generate(self, 시드, 랜덤_모드, **kwargs):
        if 랜덤_모드 == "완전랜덤" or 시드 == -1:
            실제_시드 = random.randint(0, 0xffffffffffffffff)
        else:
            실제_시드 = 시드

        rng = random.Random(실제_시드)
        parts = []
        details = []

        for key, val in kwargs.items():
            if key.endswith("_가중치") or key == "추가_태그":
                continue
            if val not in [None, "none"]:
                if val == "random":
                    옵션리스트 = self.INPUT_TYPES()["optional"][key][0][2:]
                    picked = rng.choice(옵션리스트)
                else:
                    picked = val
                parts.append(picked)
                details.append(f"{key}: {picked}")

        추가_태그 = kwargs.get("추가_태그", "")
        if 추가_태그.strip():
            parts.append(추가_태그.strip())

        positive_prompt = ", ".join(parts) if parts else "1girl"
        세부사항 = f"Seed: {실제_시드} | " + " / ".join(details)

        return (positive_prompt, 세부사항, 실제_시드)

    @classmethod
    def IS_CHANGED(cls, 시드, 랜덤_모드, **kwargs):
        if 랜덤_모드 == "완전랜덤" or 시드 == -1:
            return time.time()
        return 시드

NODE_CLASS_MAPPINGS = {"HealingArtyPromptRandomizerV11": HealingArtyPromptRandomizerV11}
NODE_DISPLAY_NAME_MAPPINGS = {"HealingArtyPromptRandomizerV11": "HealingArty Prompt Randomizer V11"}
