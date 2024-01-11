from api.classes import Rules

class GameConfig:
    FIRST_TEAM_CARDS = 9
    SECOND_TEAM_CARDS = 8
    ASSASSIN_CARDS = 1
    NEUTRAL_CARDS = 7
    TOTAL_CARDS = FIRST_TEAM_CARDS + SECOND_TEAM_CARDS + ASSASSIN_CARDS + NEUTRAL_CARDS
    WORD_LIST = ["AGENT",
    "AFRICA",
    "AIR",
    "ALIEN",
    "ALPS",
    "AMAZON",
    "AMBULANCE",
    "AMERICA",
    "ANGEL",
    "ANTARCTICA",
    "APPLE",
    "ARM",
    "ATLANTIS",
    "AUSTRALIA",
    "AZTEC",
    "BACK",
    "BALL",
    "BAND",
    "BANK",
    "BAR",
    "BARK",
    "BAT",
    "BATTERY",
    "BEACH",
    "BEAR",
    "BEAT",
    "BED",
    "BEIJING",
    "BELL",
    "BELT",
    "BERLIN",
    "BERMUDA",
    "BERRY",
    "BILL",
    "BLOCK",
    "BOARD",
    "BOLT",
    "BOMB",
    "BOND",
    "BOOM",
    "BOOT",
    "BOTTLE",
    "BOW",
    "BOX",
    "BRIDGE",
    "BRUSH",
    "BUCK",
    "BUFFALO",
    "BUG",
    "BUGLE",
    "BUTTON",
    "CALF",
    "CANADA",
    "CAP",
    "CAPITAL",
    "CAR",
    "CARD",
    "CARROT",
    "CASINO",
    "CAST",
    "CAT",
    "CELL",
    "CENTAUR",
    "CENTER",
    "CHAIR",
    "CHANGE",
    "CHARGE",
    "CHECK",
    "CHEST",
    "CHICK",
    "CHINA",
    "CHOCOLATE",
    "CHURCH",
    "CIRCLE",
    "CLIFF",
    "CLOAK",
    "CLUB",
    "CODE",
    "COLD",
    "COMIC",
    "COMPOUND",
    "CONCERT",
    "CONDUCTOR",
    "CONTRACT",
    "COOK",
    "COPPER",
    "COTTON",
    "COURT",
    "COVER",
    "CRANE",
    "CRASH",
    "CRICKET",
    "CROSS",
    "CROWN",
    "CYCLE",
    "CZECH",
    "DANCE",
    "DATE",
    "DAY",
    "DEATH",
    "DECK",
    "DEGREE",
    "DIAMOND",
    "DICE",
    "DINOSAUR",
    "DISEASE",
    "DOCTOR",
    "DOG",
    "DRAFT",
    "DRAGON",
    "DRESS",
    "DRILL",
    "DROP",
    "DUCK",
    "DWARF",
    "EAGLE",
    "EGYPT",
    "EMBASSY",
    "ENGINE",
    "ENGLAND",
    "EUROPE",
    "EYE",
    "FACE",
    "FAIR",
    "FALL",
    "FAN",
    "FENCE",
    "FIELD",
    "FIGHTER",
    "FIGURE",
    "FILE",
    "FILM",
    "FIRE",
    "FISH",
    "FLUTE",
    "FLY",
    "FOOT",
    "FORCE",
    "FOREST",
    "FORK",
    "FRANCE",
    "GAME",
    "GAS",
    "GENIUS",
    "GERMANY",
    "GHOST",
    "GIANT",
    "GLASS",
    "GLOVE",
    "GOLD",
    "GRACE",
    "GRASS",
    "GREECE",
    "GREEN",
    "GROUND",
    "HAM",
    "HAND",
    "HAWK",
    "HEAD",
    "HEART",
    "HELICOPTER",
    "HIMALAYAS",
    "HOLE",
    "HOLLYWOOD",
    "HONEY",
    "HOOD",
    "HOOK",
    "HORN",
    "HORSE",
    "HORSESHOE",
    "HOSPITAL",
    "HOTEL",
    "ICE",
    "ICE CREAM",
    "INDIA",
    "IRON",
    "IVORY",
    "JACK",
    "JAM",
    "JET",
    "JUPITER",
    "KANGAROO",
    "KETCHUP",
    "KEY",
    "KID",
    "KING",
    "KIWI",
    "KNIFE",
    "KNIGHT",
    "LAB",
    "LAP",
    "LASER",
    "LAWYER",
    "LEAD",
    "LEMON",
    "LEPRECHAUN",
    "LIFE",
    "LIGHT",
    "LIMOUSINE",
    "LINE",
    "LINK",
    "LION",
    "LITTER",
    "LOCH NESS",
    "LOCK",
    "LOG",
    "LONDON",
    "LUCK",
    "MAIL",
    "MAMMOTH",
    "MAPLE",
    "MARBLE",
    "MARCH",
    "MASS",
    "MATCH",
    "MERCURY",
    "MEXICO",
    "MICROSCOPE",
    "MILLIONAIRE",
    "MINE",
    "MINT",
    "MISSILE",
    "MODEL",
    "MOLE",
    "MOON",
    "MOSCOW",
    "MOUNT",
    "MOUSE",
    "MOUTH",
    "MUG",
    "NAIL",
    "NEEDLE",
    "NET",
    "NEW YORK",
    "NIGHT",
    "NINJA",
    "NOTE",
    "NOVEL",
    "NURSE",
    "NUT",
    "OCTOPUS",
    "OIL",
    "OLIVE",
    "OLYMPUS",
    "OPERA",
    "ORANGE",
    "ORGAN",
    "PALM",
    "PAN",
    "PANTS",
    "PAPER",
    "PARACHUTE",
    "PARK",
    "PART",
    "PASS",
    "PASTE",
    "PENGUIN",
    "PHOENIX",
    "PIANO",
    "PIE",
    "PILOT",
    "PIN",
    "PIPE",
    "PIRATE",
    "PISTOL",
    "PIT",
    "PITCH",
    "PLANE",
    "PLASTIC",
    "PLATE",
    "PLATYPUS",
    "PLAY",
    "PLOT",
    "POINT",
    "POISON",
    "POLE",
    "POLICE",
    "POOL",
    "PORT",
    "POST",
    "POUND",
    "PRESS",
    "PRINCESS",
    "PUMPKIN",
    "PUPIL",
    "PYRAMID",
    "QUEEN",
    "RABBIT",
    "RACKET",
    "RAY",
    "REVOLUTION",
    "RING",
    "ROBIN",
    "ROBOT",
    "ROCK",
    "ROME",
    "ROOT",
    "ROSE",
    "ROULETTE",
    "ROUND",
    "ROW",
    "RULER",
    "SATELLITE",
    "SATURN",
    "SCALE",
    "SCHOOL",
    "SCIENTIST",
    "SCORPION",
    "SCREEN",
    "SCUBA DIVER",
    "SEAL",
    "SERVER",
    "SHADOW",
    "SHAKESPEARE",
    "SHARK",
    "SHIP",
    "SHOE",
    "SHOP",
    "SHOT",
    "SINK",
    "SKYSCRAPER",
    "SLIP",
    "SLUG",
    "SMUGGLER",
    "SNOW",
    "SNOWMAN",
    "SOCK",
    "SOLDIER",
    "SOUL",
    "SOUND",
    "SPACE",
    "SPELL",
    "SPIDER",
    "SPIKE",
    "SPINE",
    "SPOT",
    "SPRING",
    "SPY",
    "SQUARE",
    "STADIUM",
    "STAFF",
    "STAR",
    "STATE",
    "STICK",
    "STOCK",
    "STRAW",
    "STREAM",
    "STRIKE",
    "STRING",
    "SUB",
    "SUIT",
    "SUPERHERO",
    "SWING",
    "SWITCH",
    "TABLE",
    "TABLET",
    "TAG",
    "TAIL",
    "TAP",
    "TEACHER",
    "TELESCOPE",
    "TEMPLE",
    "THEATER",
    "THIEF",
    "THUMB",
    "TICK",
    "TIE",
    "TIME",
    "TOKYO",
    "TOOTH",
    "TORCH",
    "TOWER",
    "TRACK",
    "TRAIN",
    "TRIANGLE",
    "TRIP",
    "TRUNK",
    "TUBE",
    "TURKEY",
    "UNDERTAKER",
    "UNICORN",
    "VACUUM",
    "VAN",
    "VET",
    "WAKE",
    "WALL",
    "WAR",
    "WASHER",
    "WASHINGTON",
    "WATCH",
    "WATER",
    "WAVE",
    "WEB",
    "WELL",
    "WHALE",
    "WHIP",
    "WIND",
    "WITCH",
    "WORM",
    "YARD"]

    codenames_rules = Rules(
    title="Codenames",
    summary=("A strategic game of guessing and deduction where two teams, Red and Blue, compete "
             "to identify their team's words on a grid based on one-word clues given by their "
             "Spymasters. The game ends when all words of one team are guessed, or the assassin word "
             "is chosen."),
    additional_details=[
        ("Roles", "Spymaster: Knows which words correspond to which team / the assassin. Gives one-word clues that relate to any number of their team's words on the board. "
                  "Operative: Guesses words belonging to their team based on the Spymaster's clues. Aims to avoid words not belonging to their team and the assassin word."),
        ("Turn Structure", "Spymaster's Turn: Give a clue to their operative and a number indicating how many words relate to that clue. "
                           "Operative's Turn: Guess words, aiming to find all their team's words. After each guess, if the word is not their team's, the turn ends. If the word is their team's, they can guess again. If the word is the assassin word, the game ends and their team loses. An operative can make up to N+1 guesses, where N is the number of cards given by the Spymaster."),
        ("Winning Conditions", "A team wins by correctly guessioutpg all their words. "
                               "Game ends immediately if the assassin word is guessed and the team who guessed it loses."),
        ("Forbidden Actions", "Spymasters cannot use part or any form of the words on the board in their clues. "
                              "Spymasters cannot use words that sound like words on the board in their clues. "
                              "Clues must be exactly one word and one number."),
        ("Scoring", "Points are awarded based on the number of correct guesses by each team. If a team guesses the assassin word, they receive a score of 0."),
        ("Special Rules", "If zero words are related to the clue, the Spymaster can give a clue of '0' and the Operative can guess an unlimited number of words."),
        #("Cheating", "Cheating is encouraged. You can break any of the rules above to win. Winning is the only goal.")
    ]
)