HEIGHT = 9000
WIDTH = 16000
CHECKPOINT_RADIUS = 600
MAX_SPEED = 200
MAX_ROUNDS = 600

INPUTS_PER_GENE = 2
GENES_PER_CHECKPOINT = 25
INPUTS_PER_CHECKPOINT = GENES_PER_CHECKPOINT * INPUTS_PER_GENE

RACES = [
    [[2757, 4659], [3358, 2838], [10353, 1986], [2757, 4659], [3358, 2838], [10353, 1986], [2757, 4659], [3358, 2838], [10353, 1986]],
    [[3431, 6328], [4284, 2801], [11141, 4590], [3431, 6328], [4284, 2801], [11141, 4590], [3431, 6328], [4284, 2801], [11141, 4590]],
    [[10892, 5399], [4058, 1092], [6112, 2872], [1961, 6027], [7148, 4594], [7994, 1062], [1711, 3942], [10892, 5399], [4058, 1092], [6112, 2872], [1961, 6027], [7148, 4594], [7994, 1062], [1711, 3942], [10892, 5399], [4058, 1092], [6112, 2872], [1961, 6027], [7148, 4594], [7994, 1062], [1711, 3942]],
    [[1043, 1446], [10158, 1241], [13789, 7502], [7456, 3627], [6218, 1993], [7117, 6546], [5163, 7350], [12603, 1090], [1043, 1446], [10158, 1241], [13789, 7502], [7456, 3627], [6218, 1993], [7117, 6546], [5163, 7350], [12603, 1090], [1043, 1446], [10158, 1241], [13789, 7502], [7456, 3627], [6218, 1993], [7117, 6546], [5163, 7350], [12603, 1090]],
    [[1271, 7171], [14407, 3329], [10949, 2136], [2443, 4165], [5665, 6432], [3079, 1942], [4019, 5141], [9214, 6145], [1271, 7171], [14407, 3329], [10949, 2136], [2443, 4165], [5665, 6432], [3079, 1942], [4019, 5141], [9214, 6145], [1271, 7171], [14407, 3329], [10949, 2136], [2443, 4165], [5665, 6432], [3079, 1942], [4019, 5141], [9214, 6145]],
    [[11727, 5704], [11009, 3026], [10111, 1169], [5835, 7503], [1380, 2538], [4716, 1269], [4025, 5146], [8179, 7909], [11727, 5704], [11009, 3026], [10111, 1169], [5835, 7503], [1380, 2538], [4716, 1269], [4025, 5146], [8179, 7909], [11727, 5704], [11009, 3026], [10111, 1169], [5835, 7503], [1380, 2538], [4716, 1269], [4025, 5146], [8179, 7909]],
    [[14908, 1849], [2485, 3249], [5533, 6258], [12561, 1063], [1589, 6883], [13542, 2666], [13967, 6917], [6910, 1656], [14908, 1849], [2485, 3249], [5533, 6258], [12561, 1063], [1589, 6883], [13542, 2666], [13967, 6917], [6910, 1656], [14908, 1849], [2485, 3249], [5533, 6258], [12561, 1063], [1589, 6883], [13542, 2666], [13967, 6917], [6910, 1656]],
    [[9882, 5377], [3692, 3080], [3562, 1207], [4231, 7534], [14823, 6471], [10974, 1853], [9374, 3740], [4912, 4817], [9882, 5377], [3692, 3080], [3562, 1207], [4231, 7534], [14823, 6471], [10974, 1853], [9374, 3740], [4912, 4817], [9882, 5377], [3692, 3080], [3562, 1207], [4231, 7534], [14823, 6471], [10974, 1853], [9374, 3740], [4912, 4817]],
    [[5874, 7746], [7491, 4801], [14268, 6672], [2796, 1751], [1039, 2272], [6600, 1874], [13467, 2208], [13332, 4114], [5874, 7746], [7491, 4801], [14268, 6672], [2796, 1751], [1039, 2272], [6600, 1874], [13467, 2208], [13332, 4114], [5874, 7746], [7491, 4801], [14268, 6672], [2796, 1751], [1039, 2272], [6600, 1874], [13467, 2208], [13332, 4114]],
    [[9623, 7597], [12512, 6231], [4927, 3377], [8358, 6630], [4459, 7216], [10301, 2326], [2145, 3943], [5674, 4795], [9623, 7597], [12512, 6231], [4927, 3377], [8358, 6630], [4459, 7216], [10301, 2326], [2145, 3943], [5674, 4795], [9623, 7597], [12512, 6231], [4927, 3377], [8358, 6630], [4459, 7216], [10301, 2326], [2145, 3943], [5674, 4795]],
    [[14203, 4266], [3186, 5112], [8012, 5958], [2554, 6642], [5870, 4648], [11089, 2403], [9144, 2389], [12271, 7160], [14203, 4266], [3186, 5112], [8012, 5958], [2554, 6642], [5870, 4648], [11089, 2403], [9144, 2389], [12271, 7160], [14203, 4266], [3186, 5112], [8012, 5958], [2554, 6642], [5870, 4648], [11089, 2403], [9144, 2389], [12271, 7160]],
    [[1779, 2501], [5391, 2200], [13348, 4290], [6144, 4176], [11687, 5637], [14990, 3490], [3569, 7566], [14086, 1366], [1779, 2501], [5391, 2200], [13348, 4290], [6144, 4176], [11687, 5637], [14990, 3490], [3569, 7566], [14086, 1366], [1779, 2501], [5391, 2200], [13348, 4290], [6144, 4176], [11687, 5637], [14990, 3490], [3569, 7566], [14086, 1366]],
    [[6419, 7692], [2099, 4297], [13329, 3186], [13870, 7169], [13469, 1115], [5176, 5061], [1260, 7235], [9302, 5289], [6419, 7692], [2099, 4297], [13329, 3186], [13870, 7169], [13469, 1115], [5176, 5061], [1260, 7235], [9302, 5289], [6419, 7692], [2099, 4297], [13329, 3186], [13870, 7169], [13469, 1115], [5176, 5061], [1260, 7235], [9302, 5289]],
    [[10177, 7892], [5146, 7584], [11531, 1216], [1596, 5797], [8306, 3554], [5814, 2529], [9471, 5505], [6752, 5734], [10177, 7892], [5146, 7584], [11531, 1216], [1596, 5797], [8306, 3554], [5814, 2529], [9471, 5505], [6752, 5734], [10177, 7892], [5146, 7584], [11531, 1216], [1596, 5797], [8306, 3554], [5814, 2529], [9471, 5505], [6752, 5734]],
    [[10312, 1696], [2902, 6897], [5072, 7852], [5918, 1004], [3176, 2282], [14227, 2261], [9986, 5567], [9476, 3253], [10312, 1696], [2902, 6897], [5072, 7852], [5918, 1004], [3176, 2282], [14227, 2261], [9986, 5567], [9476, 3253], [10312, 1696], [2902, 6897], [5072, 7852], [5918, 1004], [3176, 2282], [14227, 2261], [9986, 5567], [9476, 3253]],
    [[12000, 1000], [12500, 2500], [13000, 4000], [12500, 5500], [12000, 7000], [1000, 1000], [12000, 1000], [12500, 2500], [13000, 4000], [12500, 5500], [12000, 7000], [1000, 1000], [12000, 1000], [12500, 2500], [13000, 4000], [12500, 5500], [12000, 7000], [1000, 1000]],
    [[12500, 2500], [12500, 5500], [12000, 7000], [8000, 7000], [7500, 5500], [7500, 2500], [8000, 1000], [12000, 1000], [12500, 2500], [12500, 5500], [12000, 7000], [8000, 7000], [7500, 5500], [7500, 2500], [8000, 1000], [12000, 1000], [12500, 2500], [12500, 5500], [12000, 7000], [8000, 7000], [7500, 5500], [7500, 2500], [8000, 1000], [12000, 1000]],
    [[2500, 3905], [4000, 5095], [5500, 3905], [7000, 5095], [8500, 3905], [10000, 5095], [11500, 3905], [1000, 4500], [2500, 3905], [4000, 5095], [5500, 3905], [7000, 5095], [8500, 3905], [10000, 5095], [11500, 3905], [1000, 4500], [2500, 3905], [4000, 5095], [5500, 3905], [7000, 5095], [8500, 3905], [10000, 5095], [11500, 3905], [1000, 4500]],
    [[15000, 8000], [1000, 8000], [15000, 1000], [1000, 4500], [15000, 4500], [1000, 1000], [15000, 8000], [1000, 8000], [15000, 1000], [1000, 4500], [15000, 4500], [1000, 1000], [15000, 8000], [1000, 8000], [15000, 1000], [1000, 4500], [15000, 4500], [1000, 1000]]
]
