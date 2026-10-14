"""script.txt の各 "# scene:" ブロック(登場順)に対応する画像生成プロンプト。

各ブロックはショットのリストで、ブロックが長い場合は約12秒ごとに次のショットへ切り替える。
人物の見た目をそろえるため、キャラクターの描写は定数で共通化している。
"""

NOAH = "a thin 10-year-old American boy (male child) with a short boyish haircut, light-brown hair and blue eyes"
SARAH = "a 40-year-old American woman (adult mother, mature face, fine wrinkles) with shoulder-length brown hair, wearing a cardigan, tired kind face"
TAKA = "a 68-year-old Japanese fireworks craftsman, tanned face, short gray-streaked hair, thick arms, navy work clothes with rolled sleeves"
SATO = "a Japanese male doctor in his 40s with glasses and a white coat, calm expression"
BENNETT = "an American male doctor in his 50s with a white coat and gray hair"
STYLE = "cinematic photograph, realistic, natural lighting, shallow depth of field, 35mm film look"

BLOCKS = [
    # 1 title
    [f"{NOAH} lying in a white hospital bed looking out the window, IV stand, soft daylight"],
    # 2 midwest
    ["small quiet town in the American Midwest, factory and corn fields, wooden houses, golden hour"],
    # 3 scan_us
    [f"{BENNETT} showing a brain MRI scan on a monitor, serious face, dim consultation room"],
    # 4 noah_room
    [f"{NOAH} sitting on the floor of his small bedroom watching Japanese anime on an old TV, anime posters on the wall, night",
     f"{NOAH} and {SARAH} hugging in a modest American living room"],
    # 5 airplane
    ["passenger airplane flying above white clouds, blue sky, view from window"],
    # 6 tokyo
    ["crowded Shibuya scramble crossing in Tokyo in hot summer, many people, bright signs",
     f"{NOAH} in a wheelchair with {SARAH} looking tired in a crowded Tokyo street, summer heat"],
    # 7 workshop
    [f"{TAKA} sitting in his old wooden fireworks workshop, round firework shells on shelves"],
    # 8 lanterns
    [f"{TAKA} handing a red paper lantern to {NOAH} in a wheelchair on a narrow Japanese town street, festival preparation",
     f"{NOAH} smiling shyly while holding a red paper lantern, Japanese town street"],
    # 9 hospital_wall
    [f"{NOAH} lying in a Japanese hospital bed at night, looking at a window that shows only the wall of the next building, faint colored light"],
    # 10 scan_compare
    [f"{SATO} comparing two brain MRI images side by side on a monitor, focused, hospital office",
     "two brain MRI scans displayed side by side on a light box, close-up"],
    # 11 fireworks
    ["huge round Japanese fireworks bursting over a river at night, crowd silhouettes on the riverbank, reflections on water"],
    # 12 ct_chart
    ["modern CT scanner in a clean Japanese clinic room, white and bright"],
    # 13 clinic_jp
    ["small Japanese neighborhood clinic waiting room, clean and calm",
     "Japanese radiologist operating a CT scanner from a control room"],
    # 14 midwest
    ["small American Midwest town with a factory chimney and fields, overcast sky",
     f"{SARAH} working in a factory line, wearing a work uniform"],
    # 15 dawn
    [f"{SARAH} leaving a small wooden house at 5 am before dawn, dark blue sky",
     f"{SARAH} working as a cashier in a supermarket at night, tired",
     f"{NOAH} sleeping in his bed at night, his mother gently touching his hair"],
    # 16 noah_room
    [f"{NOAH} alone in his bedroom watching anime on an old TV at night, Japanese anime posters on wall",
     f"{NOAH} looking at a poster of a Japanese countryside landscape, dreaming expression",
     f"{NOAH} and {SARAH} talking on a sofa in summer evening light"],
    # 17 midwest_spring
    [f"{NOAH} holding his head with a headache, sitting at a kitchen table in the morning",
     f"{NOAH} dropping a glass of milk in the kitchen, shattered glass",
     f"{NOAH} looking dazed in an American school classroom",
     f"{SARAH} looking worried at {NOAH}"],
    # 18 hospital_us
    [f"{NOAH} falling down at the front door of a house, {SARAH} rushing to him",
     "large American hospital exterior, daytime",
     f"{BENNETT} speaking seriously to {SARAH} in a hospital consultation room"],
    # 19 scan_us
    [f"{BENNETT} pointing at a brain MRI image on a monitor, {SARAH} listening in shock",
     f"{SARAH} with tears in her eyes, hands over mouth, hospital room",
     f"{BENNETT} slowly shaking his head, serious"],
    # 20 parking
    [f"{SARAH} crying alone in her car in a hospital parking lot, forehead on the steering wheel, sunset"],
    # 21 living_room
    [f"the small back of {NOAH} sitting on a sofa watching anime on TV, seen from behind",
     f"{SARAH} collapsing to her knees in the doorway of a living room, devastated"],
    # 22 kitchen_table
    [f"{SARAH} and {NOAH} sitting at a wooden kitchen table, serious talk, warm lamp light",
     f"{NOAH} staring down at the wood grain of the table, quiet and sad",
     f"{SARAH} holding her son's hand across the table, unable to speak"],
    # 23 noah_room_dark
    [f"{NOAH} curled up in bed in a dark bedroom, curtains closed",
     f"{SARAH} standing outside her son's closed bedroom door, hand on the door"],
    # 24 kitchen_night
    [f"{SARAH} washing dishes at a kitchen sink at night, seen from behind",
     f"{NOAH} standing in the kitchen at night looking straight at his mother, determined",
     f"{SARAH} turning around at the sink with wet hands, shocked",
     f"{SARAH} hugging {NOAH} tightly in the kitchen at night, crying"],
    # 25 kitchen_table
    [f"{SARAH} looking at bank statements and a calculator at the kitchen table at night",
     f"{BENNETT} handing documents to {SARAH} in a hospital office"],
    # 26 airplane
    [f"{NOAH} looking out of an airplane window with excitement, {SARAH} next to him"],
    # 27 airport
    [f"{NOAH} and {SARAH} arriving at Narita airport arrival hall, holding hands",
     f"Japanese airport staff crouching to talk kindly to {NOAH} in a wheelchair",
     f"{SARAH} pushing {NOAH} in a wheelchair through a bright Japanese airport"],
    # 28 tokyo
    [f"{NOAH} in a wheelchair laughing in Akihabara with anime billboards, {SARAH} smiling",
     "busy Tokyo street with Japanese signs, strong summer sun and heat haze",
     f"{NOAH} sweating and tired in the Tokyo summer heat"],
    # 29 hotel
    [f"{NOAH} lying in a hotel bed with a headache, curtains closed, {SARAH} sitting beside him",
     f"{SARAH} talking with a Japanese hotel receptionist woman who spreads out a map on the counter"],
    # 30 riverside
    ["small Japanese countryside train station in summer, cicadas, blue sky",
     "wide river and grassy embankment in a small Japanese town, summer blue sky, low houses",
     f"{NOAH} squinting happily in the wind on a Japanese river embankment"],
    # 31 lanterns
    ["Japanese townspeople hanging rows of red paper lanterns on bamboo poles along a narrow street",
     "traditional small Japanese inn with a noren curtain at the entrance"],
    # 32 inn_evening
    [f"{TAKA} preparing festival decorations in front of a traditional Japanese inn at dusk",
     f"{TAKA} glancing at {NOAH} in a wheelchair, gruff expression"],
    # 33 lanterns
    [f"{NOAH} in a wheelchair holding a red paper lantern, surprised face",
     f"{TAKA} assembling bamboo poles while {NOAH} hands him lanterns",
     f"{NOAH} talking excitedly to {SARAH} on the way back to the inn at dusk"],
    # 34 inn_night
    [f"{TAKA} standing at the entrance of a Japanese inn at night holding a small paper bag"],
    # 35 senko
    [f"close-up of a senko hanabi sparkler with tiny orange sparks in the dark",
     f"{NOAH} holding a senko hanabi sparkler in a Japanese garden at night, face lit by orange sparks",
     f"{TAKA} smiling softly in the dark lit by a sparkler",
     f"{NOAH} looking at {TAKA} with shining eyes at night"],
    # 36 festival_morning
    [f"{NOAH} in a dark blue children's yukata looking at himself in a mirror in a Japanese tatami room, morning light"],
    # 37 festival
    [f"{SARAH} taking photos of {NOAH} in a yukata with her smartphone",
     "Japanese summer festival street at dusk lined with food stalls, yakisoba, candy apples, paper lanterns"],
    # 38 goldfish
    [f"{NOAH} in a dark blue yukata crouching at a goldfish scooping stall at a Japanese festival, paper lanterns",
     f"Japanese local kids laughing and teaching {NOAH} how to scoop goldfish",
     f"{NOAH} cheering after scooping a goldfish, Japanese kids celebrating around him"],
    # 39 festival
    [f"{SARAH} and {TAKA} standing side by side watching children at a festival stall",
     f"{SARAH} showing a translation app on her smartphone to {TAKA}"],
    # 40 festival_dark
    [f"{NOAH} in a yukata holding his head in pain at a festival at night",
     f"{SARAH} rushing to {NOAH} who has collapsed on the ground at a festival, people gathering"],
    # 41 ambulance
    ["Japanese ambulance with red lights arriving at a summer festival at night, crowd making way",
     "Japanese paramedic kneeling and looking into the eyes of a worried American mother"],
    # 42 hospital_corridor
    [f"{SARAH} in a yukata sitting alone in a Japanese hospital corridor, holding papers",
     f"{SATO} coming out of a treatment room and speaking calmly to {SARAH}",
     f"{SATO} shaking his head apologetically"],
    # 43 hospital_wall
    [f"{NOAH} lying in a hospital bed with an IV drip at night, looking at the ceiling",
     "hospital window at night showing only the concrete wall of the next building, faint colored glow",
     f"{NOAH} turning his face toward the window in a dark hospital room",
     f"{SARAH} holding her son's cold hand by a hospital bed at night"],
    # 44 hospital_corridor
    [f"{SARAH} crying alone in a dim hospital corridor at night"],
    # 45 goldfish_bag
    ["a plastic bag with one small red goldfish placed beside a hospital pillow at night",
     f"{SARAH} sitting beside her sleeping son in a hospital room at night"],
    # 46 hospital_day
    [f"{TAKA} in work clothes standing at the door of a hospital room holding a paper bag",
     f"{NOAH} sitting up in a hospital bed looking surprised",
     f"{TAKA} sitting on a chair beside a hospital bed, silent"],
    # 47 shell
    ["a Japanese firework shell cut in half showing small black star pellets packed inside, on a wooden table",
     f"{NOAH} looking curiously into a half-cut firework shell in a hospital bed",
     "a single small black firework star pellet on a child's palm, close-up",
     f"{TAKA} explaining with a gentle smile beside a hospital bed"],
    # 48 round_vs_tube
    ["perfectly round Japanese chrysanthemum firework over a river at night",
     "crowds on both banks of a Japanese river looking up at the night sky"],
    # 49 hospital_day
    [f"{NOAH} asking {TAKA} a question in a hospital room, daylight",
     f"{NOAH} with tears falling down his cheeks in a hospital bed",
     f"{TAKA} nodding deeply",
     f"{SARAH} listening in the hospital corridor through a half-open door"],
    # 50 hospital_evening
    [f"{SATO} entering a hospital room at sunset with a serious look"],
    # 51 scan_compare
    [f"{SATO} showing two brain MRI images side by side to {SARAH} on a monitor",
     "two nearly identical brain MRI scans side by side on a computer screen, close-up",
     f"{SARAH} leaning forward with a shocked hopeful face"],
    # 52 doctor_desk
    [f"{SATO} writing a detailed report in English late at night at his desk",
     f"{SATO} on the phone at his desk, international call",
     f"{SARAH} bowing to thank {SATO} in a hospital office"],
    # 53 notebook
    [f"Japanese nurses kindly talking to {NOAH} in a hospital bed using a translation device",
     f"{NOAH} writing Japanese words in romaji in a small notebook in a hospital bed"],
    # 54 hospital_day
    [f"Japanese children visiting {NOAH} in hospital, showing him a goldfish in a plastic bag",
     f"{TAKA} letting {NOAH} touch a wooden mold for firework shells in a hospital room",
     f"{SARAH} watching her son laughing in the hospital room, moved"],
    # 55 hospital_exit
    [f"{NOAH} walking out of a Japanese hospital on his own feet, holding his mother's hand",
     f"{TAKA} seeing them off in front of the hospital entrance"],
    # 56 hospital_us
    [f"{BENNETT} reading a document from Japan carefully in his office",
     f"{NOAH} smiling bravely in an American hospital bed before a medical test"],
    # 57 clinic_us
    [f"{SARAH} and {NOAH} sitting in a doctor's office waiting for results, tense",
     f"{BENNETT} looking straight at {SARAH} and speaking seriously",
     f"{SARAH} covering her face and crying with joy, {NOAH} rubbing her back",
     f"{BENNETT} bowing his head apologetically"],
    # 58 surgery
    ["surgical team operating in a modern operating room, bright surgical lights"],
    # 59 station
    [f"{NOAH} with short hair and a small scar walking out of a small Japanese train station in summer with {SARAH}"],
    # 60 riverside
    [f"{NOAH} walking ahead along a Japanese river embankment in summer, turning back to his mother"],
    # 61 workshop
    [f"{NOAH} opening a sliding door of an old Japanese wooden workshop",
     f"{TAKA} sitting at his workbench grinning, workshop full of firework shells"],
    # 62 shell_half
    ["half of a large firework shell with small star pellets neatly lined inside, on a wooden workbench",
     f"close-up of {TAKA}'s hands placing a star pellet with tweezers inside a firework shell",
     f"{NOAH} watching intently without blinking in a workshop"],
    # 63 yukata
    [f"{NOAH} wearing a dark blue yukata whose sleeves are slightly too short, evening",
     f"{SARAH} looking at her son in a yukata with tears of emotion"],
    # 64 festival
    [f"Japanese kids running to greet {NOAH} at a goldfish stall at a summer festival at dusk"],
    # 65 fireworks_start
    [f"{NOAH} and {SARAH} sitting on a river embankment at night looking up at the sky, waiting"],
    # 66 fireworks
    ["giant perfectly round golden firework bursting over a Japanese river at night",
     f"{NOAH}'s face lit by fireworks, looking up in awe, night"],
    # 67 fireworks_gold
    [f"{NOAH} with tears on his cheeks looking up at fireworks at night",
     "golden fireworks reflected in a river at night",
     f"{SARAH} and {NOAH} sitting together on a riverbank under fireworks, seen from behind"],
    # 68 fireworks_crowd
    ["huge crowd of people on both river banks looking up at round fireworks at night, silhouettes"],
    # 69 fireworks_finale
    ["grand finale of many round Japanese fireworks filling the night sky over a river",
     f"{NOAH} standing up and clapping on the riverbank at night"],
    # 70 riverbank_night
    [f"{TAKA} in work clothes walking on an empty riverbank at night after fireworks",
     f"{NOAH} looking up at {TAKA} on a riverbank at night"],
    # 71 star_gift
    ["a single small firework star pellet wrapped in Japanese paper on a child's two palms, close-up",
     f"{TAKA} handing a small paper packet to {NOAH} at night"],
    # 72 riverbank_night
    [f"{TAKA} looking at the river at night, profile",
     f"{TAKA} speaking to {SARAH} at night on the riverbank",
     f"{SARAH} bowing and saying thank you to {TAKA} with tears, night"],
    # 73 midwest_summer
    [f"{NOAH} healthy and smiling with friends at an American school playground in summer"],
    # 74 riverside
    [f"{NOAH} and {SARAH} walking along a Japanese river embankment in summer, happy",
     f"{NOAH} talking eagerly to {TAKA} in the fireworks workshop"],
    # 75 photo_wall
    [f"framed photo on a bedroom wall of {NOAH} in a yukata, {SARAH}, and {TAKA} with Japanese kids by a river",
     "a single small firework star pellet on a boy's desk next to anime figures, soft light"],
    # 76 scan_compare
    [f"{SATO} looking at two brain scans, thoughtful"],
    # 77 clinic_jp
    ["doctor's hands on a CT scanner control panel in a Japanese hospital"],
    # 78 lanterns
    ["Japanese small town street lined with glowing red paper lanterns at dusk"],
    # 79 fireworks_crowd
    ["round Japanese fireworks seen from a river bank with many people looking up, night",
     "perfectly symmetrical round firework, close view"],
    # 80 ending
    [f"{NOAH} and {SARAH} smiling together under summer fireworks"],
]


def prompt_text(p):
    return f"{p}, {STYLE}, no text, no watermark"
