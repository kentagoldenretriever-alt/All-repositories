"""script.txt の各 "# scene:" ブロック(登場順)に使うストック動画の検索語(Pexels 用)。

各ブロックはショットのリスト。各ショットは優先度順の検索語句のリストで、
Pexels の検索結果の上位から、まだ使っていないクリップを選ぶ。
"""

BLOCK_QUERIES = [
    # 1 title
    [["shinkansen bullet train", "bullet train japan"]],
    # 2 alan_tokyo_station
    [["tokyo station platform", "shinkansen platform"], ["senior man smiling confident", "older businessman smiling"],
     ["bullet train arriving station", "shinkansen arriving"]],
    # 3 departure_board
    [["departure board train station", "train departure information display"], ["man looking up at departure board", "traveler looking at timetable"],
     ["shinkansen departing", "bullet train leaving station"]],
    # 4 onboard_teaser
    [["bullet train window view", "train window landscape fast"], ["water bottle on train table", "bottle on table train"]],
    # 5 night_track_teaser
    [["railway track at night", "train tracks night lights"], ["little girl drawing", "girl with colored pencils"]],
    # 6 shinkansen_hero
    [["shinkansen mount fuji", "bullet train passing fast"]],
    # 7 france_city
    [["bordeaux france city", "toulouse france aerial"], ["engineering student university", "mechanical engineering"],
     ["train engineer analyzing data", "engineer computer charts"], ["railway control work office", "train schedule planning"]],
    # 8 tgv
    [["tgv high speed train france", "french high speed train"], ["train crossing countryside france", "high speed train countryside"]],
    # 9 study_models
    [["model train collection", "toy train model"], ["grandfather granddaughter home", "grandfather and grandchild playing"],
     ["little girl smiling at grandfather", "girl listening grandfather"], ["grandfather smiling kindly", "happy senior man home"]],
    # 10 meeting_room
    [["business meeting presentation screen", "meeting room presentation"], ["boss pointing at screen", "manager presentation data"],
     ["senior man arms crossed thinking", "serious older man thinking"], ["young engineer speaking meeting", "young man talking in meeting"],
     ["closing folder documents", "businessman closing file"]],
    # 11 office_hallway
    [["office corridor walking colleagues", "two businessmen walking office"], ["colleagues talking hallway", "coworkers conversation office"]],
    # 12 grandpa_girl_home
    [["grandfather stroking granddaughter hair", "grandparent hugging child"], ["girl taking photo camera", "child holding camera"],
     ["senior man thinking evening home", "old man looking out window evening"]],
    # 13 airport_arrival
    [["haneda airport", "airport arrival hall japan"], ["japanese businessman bowing", "business handshake airport"],
     ["airport clock", "airport walking travelers"], ["tokyo hotel lobby", "hotel check in"]],
    # 14 hotel_night_tokyo
    [["tokyo night view from hotel window", "tokyo skyline night"], ["man reading documents hotel room", "businessman reading papers night"]],
    # 15 platform_arrival
    [["tokyo station", "people walking train platform japan"], ["shinkansen arriving platform", "bullet train arriving"]],
    # 16 cleaning_crew
    [["train cleaning staff", "cleaning train seats"], ["checking wristwatch", "man looking at watch"],
     ["train interior empty seats", "shinkansen interior"], ["workers teamwork efficient", "cleaning crew working"],
     ["train doors opening platform", "passengers waiting platform japan"]],
    # 17 staff_bow
    [["japanese staff bowing", "japanese people bowing"], ["man writing in notebook", "writing notes notebook"]],
    # 18 boarding
    [["boarding bullet train", "passengers boarding train japan"], ["man sitting train seat", "businessman on train"]],
    # 19 city_departure
    [["train leaving tokyo city", "train passing buildings tokyo"], ["view from train window city", "train window city view"],
     ["train curve city", "train through city"]],
    # 20 acceleration
    [["high speed train window view", "fast train window"], ["landscape passing fast train window", "motion blur train window"],
     ["bullet train speeding", "shinkansen high speed"]],
    # 21 water_bottle
    [["water bottle on table", "glass of water on train table"], ["passenger using laptop on train", "working laptop train"],
     ["passenger sleeping on train", "person resting train seat"], ["man looking at watch surprised", "surprised man"]],
    # 22 distributed_power
    [["train wheels bogie", "train wheels close up"], ["electric train motor", "train undercarriage"],
     ["shinkansen side view", "bullet train passing"], ["train schedule diagram", "timetable"],
     ["man writing notebook train", "notes on train"]],
    # 23 girl_card
    [["colored pencils falling", "colored pencils"], ["little girl drawing card", "girl drawing with colored pencils"],
     ["grandfather and granddaughter on train", "old man and girl travel"], ["handmade birthday card", "birthday card drawing"],
     ["little girl smiling", "happy little girl"], ["old man smiling gently", "elderly man smiling"]],
    # 24 overtaking
    [["train timetable paper", "colorful chart document"], ["train passing station without stopping", "train passing platform fast"],
     ["train waiting at station", "train stopped platform"], ["shinkansen passing", "bullet train passing station"]],
    # 25 arrival_osaka
    [["train arriving station slowing", "train pulling into station"], ["girl looking out train window", "child looking out window train"],
     ["people getting off train", "passengers exiting train"], ["grandfather and girl waving", "girl waving goodbye"]],
    # 26 crowd_platform
    [["crowd train platform japan", "crowded station japan"], ["writing notebook", "man writing journal"]],
    # 27 return_tokyo
    [["bullet train morning", "train early morning"], ["man thinking on train window", "pensive man train"]],
    # 28 control_room
    [["control room monitors", "operations control center"], ["operator watching screens", "people monitoring screens"],
     ["railway control room", "train traffic control"], ["map lines screen", "network diagram screen"]],
    # 29 delay_recovery
    [["operators discussing screens", "team control room discussion"], ["train departing station", "train leaving platform"],
     ["focused operator", "concentrated man computer"], ["trains crossing", "multiple trains station"]],
    # 30 museum_train
    [["old train museum", "vintage train exhibit"], ["retro train front", "old locomotive"]],
    # 31 museum_inside
    [["train driver cab", "train cockpit"], ["speedometer gauge", "old gauge"], ["museum exhibit panels", "museum display"],
     ["old machine parts", "vintage mechanical parts"]],
    # 32 night_maintenance
    [["railway workers at night", "track maintenance night"], ["safety helmet vest worker", "workers safety gear"],
     ["railway switch", "railroad switch"], ["overhead power lines railway", "catenary"]],
    # 33 rail_inspection
    [["inspecting rail track", "worker inspecting railway"], ["workers checking with flashlight", "flashlight night work"],
     ["engineer checking clipboard", "worker writing report"]],
    # 34 night_work_flow
    [["night work team", "workers night"], ["writing report clipboard", "checklist"], ["tools on ground", "maintenance tools"],
     ["worker smiling", "construction worker portrait"]],
    # 35 trust_connected
    [["little girl hugging grandmother", "granddaughter grandmother hug"], ["railway tracks perspective", "train tracks"],
     ["people commuting train japan", "commuters"]],
    # 36 dawn_track
    [["sunrise over railway", "railway tracks sunrise"], ["dawn sky city", "sunrise city"], ["man looking at tracks", "man standing railway"]],
    # 37 notebook_reflection
    [["writing notebook", "opening notebook"], ["older man bowing", "man bowing respectfully"], ["two men smiling", "men handshake"]],
    # 38 first_train_morning
    [["first train morning", "train morning light"], ["bullet train sunrise", "train sunrise"]],
    # 39 report_meeting
    [["business presentation france office", "presentation to executives"], ["senior executive asking question", "executive meeting"],
     ["notebook on table meeting", "documents on table"], ["presenter speaking confidently", "man giving presentation"],
     ["team listening presentation", "audience listening meeting"]],
    # 40 granddaughter_visit
    [["girl running to grandfather", "granddaughter visiting grandparents"], ["looking at photo", "holding photograph"],
     ["grandfather talking to granddaughter", "grandpa storytelling"], ["little girl curious", "girl asking question"]],
    # 41 models_shelf
    [["model train shelf", "toy train"], ["grandfather granddaughter hug", "grandpa hugging girl"]],
    # 42 closing_shinkansen
    [["bullet train model", "shinkansen"], ["shinkansen speed", "bullet train passing"]],
    # 43 closing_people
    [["family reunion station", "family meeting at station"], ["commuters japan station", "people walking station japan"],
     ["railway tracks night", "train at night"]],
    # 44 ending
    [["shinkansen sunset", "bullet train evening"]],
]
