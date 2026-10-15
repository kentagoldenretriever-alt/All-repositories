"""script.txt の各 "# scene:" ブロック(登場順)に使うストック動画の検索語。

各ブロックはショットのリスト。各ショットは「優先度順の候補語句」のリストで、
語句の単語がクリップ名(slug)に多く含まれるほど優先される。
"""

BLOCK_QUERIES = [
    # 1 title
    [["sad boy window", "boy behind window"]],
    # 2 midwest
    [["small town", "rural town", "farm field"]],
    # 3 scan_us
    [["doctor brain scan", "doctor reviewing scan"]],
    # 4 noah_room
    [["boy watching tv", "child watching tv", "kid tv"], ["mother hugging son", "mother hug child"]],
    # 5 airplane
    [["airplane window clouds", "plane window"]],
    # 6 tokyo
    [["tokyo crossing crowd", "shibuya crossing", "tokyo street crowd"], ["tokyo street people", "japan street people"]],
    # 7 workshop
    [["craftsman workshop hands", "carpenter workshop", "workshop tools"]],
    # 8 lanterns
    [["red lanterns night", "lanterns hanging"], ["boy holding lantern", "silhouette boy lantern"]],
    # 9 hospital_wall
    [["boy hospital bed", "child hospital bed", "sick boy bed"]],
    # 10 scan_compare
    [["doctor scan screen", "doctor brain scan tablet"], ["x-ray doctor", "mri results"]],
    # 11 fireworks
    [["fireworks night sky", "fireworks display"]],
    # 12 ct_chart
    [["ct scan machine", "patient brain scan hospital", "mri machine"]],
    # 13 clinic_jp
    [["clinic reception", "hospital reception"], ["doctor monitor", "medical monitor"]],
    # 14 midwest
    [["factory chimney", "industrial factory", "small town"], ["woman factory worker", "woman working factory"]],
    # 15 dawn
    [["sunrise morning house", "dawn sky", "early morning"], ["cashier supermarket", "woman cashier"], ["mother sleeping child", "child sleeping bed"]],
    # 16 noah_room
    [["boy watching tv", "kid watching cartoons"], ["boy bedroom", "child bedroom"], ["mother son sofa", "mother child talking"]],
    # 17 midwest_spring
    [["boy headache", "child headache", "kid sick"], ["glass falling", "spilled milk", "broken glass"], ["boy classroom", "student classroom tired"], ["worried mother", "mother worried"]],
    # 18 hospital_us
    [["boy falling", "child fall"], ["hospital building", "hospital exterior"], ["doctor talking woman", "doctor patient talking"]],
    # 19 scan_us
    [["doctor showing scan patient", "doctor mri patient"], ["woman shocked crying", "woman crying"], ["doctor serious", "doctor thinking"]],
    # 20 parking
    [["woman crying car", "sad woman car", "woman car"]],
    # 21 living_room
    [["boy sofa tv", "child sofa"], ["woman crying floor", "sad woman sitting floor"]],
    # 22 kitchen_table
    [["mother son table talking", "family table talking"], ["sad boy table", "boy table"], ["holding hands table", "hands holding"]],
    # 23 noah_room_dark
    [["boy bed dark", "child under blanket", "boy blanket"], ["woman door", "woman standing door"]],
    # 24 kitchen_night
    [["washing dishes", "woman washing dishes sink"], ["boy standing", "boy looking camera"], ["woman turning surprised", "woman kitchen"], ["mother hugging son", "mother hug child crying"]],
    # 25 kitchen_table
    [["woman calculator bills", "woman paperwork table"], ["doctor documents", "doctor clipboard"]],
    # 26 airplane
    [["boy airplane window", "child airplane", "plane window"]],
    # 27 airport
    [["airport arrivals", "airport hall people"], ["wheelchair airport", "wheelchair"], ["airport walking suitcase", "airport travelers"]],
    # 28 tokyo
    [["akihabara", "neon signs japanese", "tokyo neon"], ["tokyo street day", "japan street"], ["hot summer sweating", "sun heat"]],
    # 29 hotel
    [["hotel room bed", "sick in bed"], ["hotel reception", "receptionist"]],
    # 30 riverside
    [["train station japan", "tokyo train station"], ["river countryside", "river green"], ["boy wind", "boy smiling outdoors"]],
    # 31 lanterns
    [["lanterns garden night", "red lanterns"], ["japanese building trees", "traditional japanese"]],
    # 32 inn_evening
    [["old man portrait", "elderly man"], ["old man looking", "old man face"]],
    # 33 lanterns
    [["silhouette boy lantern", "boy lantern"], ["hands wood", "craftsman hands"], ["mother son walking", "family walking evening"]],
    # 34 inn_night
    [["old man night", "old man dark"]],
    # 35 senko
    [["sparkler close", "sparks sparkler"], ["child sparkler", "kid sparkler"], ["old man smiling", "old man portrait"], ["boy sparkler night", "sparklers night"]],
    # 36 festival_morning
    [["boy mirror", "child mirror"]],
    # 37 festival
    [["woman taking photo phone", "taking photo smartphone"], ["festival night lights", "street food night market"]],
    # 38 goldfish
    [["goldfish prize", "goldfish"], ["children laughing", "kids playing together"], ["goldfish swimming", "goldfish water"]],
    # 39 festival
    [["festival crowd night", "night market"], ["translator phone", "smartphone translate", "showing phone"]],
    # 40 festival_dark
    [["boy headache", "child pain"], ["woman panic", "woman screaming"]],
    # 41 ambulance
    [["ambulance", "emergency lights"], ["paramedic", "emergency medical"]],
    # 42 hospital_corridor
    [["woman waiting hospital", "woman sitting corridor"], ["doctor walking hallway", "doctor hallway"], ["doctor talking woman", "doctor consoling"]],
    # 43 hospital_wall
    [["iv drip", "iv fluid hospital"], ["window night", "dark window"], ["vital signs monitor", "heart rate monitor"], ["holding hands hospital", "hand holding patient"]],
    # 44 hospital_corridor
    [["woman crying alone", "sad woman crying"]],
    # 45 goldfish_bag
    [["goldfish glass", "goldfish"], ["mother watching child sleeping", "child sleeping"]],
    # 46 hospital_day
    [["old man walking", "elderly man"], ["child hospital bed", "girl hospital bed"], ["old man sitting", "old man chair"]],
    # 47 shell
    [["gunpowder", "sparks close"], ["child looking curious", "boy curious"], ["hand palm", "small object hand"], ["old man smiling", "grandfather smiling"]],
    # 48 round_vs_tube
    [["golden firework", "fireworks sky"], ["people watching fireworks", "crowd fireworks"]],
    # 49 hospital_day
    [["grandfather grandson talking", "old man child"], ["boy crying", "child crying"], ["old man nodding", "old man portrait"], ["woman listening door", "woman leaning wall"]],
    # 50 hospital_evening
    [["doctor walking hallway", "doctor entering room"]],
    # 51 scan_compare
    [["doctor shows patient brain scan", "doctor showing mri"], ["brain scan screen", "x-ray screen"], ["woman hopeful", "woman surprised"]],
    # 52 doctor_desk
    [["doctor writing report", "doctor writing desk"], ["doctor phone call", "doctor phone"], ["woman thanking doctor", "doctor patient handshake"]],
    # 53 notebook
    [["nurse child", "nurse patient talking"], ["child writing notebook", "boy writing"]],
    # 54 hospital_day
    [["children visiting hospital", "kids smiling"], ["wood carving hands", "hands wood"], ["mother smiling child", "happy mother"]],
    # 55 hospital_exit
    [["walking out hospital", "mother child walking"], ["old man waving", "elderly man smiling"]],
    # 56 hospital_us
    [["doctor reading document", "doctor reviewing papers"], ["child hospital bed smiling", "child in hospital smiles"]],
    # 57 clinic_us
    [["family doctor office waiting", "waiting room"], ["doctor talking patient", "doctor explaining"], ["woman crying joy", "woman tears happy"], ["doctor apologizing", "doctor serious"]],
    # 58 surgery
    [["surgery operating room", "surgeons operating"]],
    # 59 station
    [["train station", "train arriving"]],
    # 60 riverside
    [["boy walking river", "boy walking"]],
    # 61 workshop
    [["sliding door", "opening door"], ["craftsman workshop", "old man working"]],
    # 62 shell_half
    [["tweezers", "small parts hands"], ["hands crafting", "craftsman hands detail"], ["boy watching", "child watching curious"]],
    # 63 yukata
    [["boy kimono", "child traditional clothes", "boy portrait"], ["mother tears", "woman emotional"]],
    # 64 festival
    [["kids running festival", "children running"]],
    # 65 fireworks_start
    [["people waiting night", "crowd night"]],
    # 66 fireworks
    [["large firework show", "large fireworks display"], ["boy looking up", "child looking up sky"]],
    # 67 fireworks_gold
    [["child watching fireworks", "boy fireworks"], ["fireworks reflection water", "fireworks river"], ["family watching fireworks", "people seeing fireworks"]],
    # 68 fireworks_crowd
    [["crowd fireworks", "people watching fireworks"]],
    # 69 fireworks_finale
    [["night sky full of fireworks", "fireworks finale", "multicolor fireworks"], ["applause clapping", "people clapping"]],
    # 70 riverbank_night
    [["old man walking night", "old man night"], ["boy night", "child night"]],
    # 71 star_gift
    [["hands giving small gift", "small gift hands"], ["old man giving", "grandfather gift"]],
    # 72 riverbank_night
    [["river night", "river city night"], ["old man talking", "old man portrait"], ["woman thanking", "woman bowing"]],
    # 73 midwest_summer
    [["kids playing playground", "children playing outdoors"]],
    # 74 riverside
    [["mother son walking summer", "family walking park"], ["grandfather grandson", "old man boy"]],
    # 75 photo_wall
    [["family photo frame", "photo album"], ["desk lamp night", "desk"]],
    # 76 scan_compare
    [["doctor reviewing brain scan", "doctor scan"]],
    # 77 clinic_jp
    [["ct scan", "patient brain scan"]],
    # 78 lanterns
    [["red lanterns bamboo", "lanterns night"]],
    # 79 fireworks_crowd
    [["fireworks over city", "fireworks city"], ["beautiful fireworks display", "golden firework"]],
    # 80 ending
    [["fireworks couple", "fireworks beach people"]],
]
