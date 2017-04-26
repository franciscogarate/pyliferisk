#!/usr/bin/python
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    NOTE: It's possible to import tables of an external source, i.e. txt or csv files.
#    In that case, you can use the following instructions:
#
#    import csv
#    file_source = open('tables/mortalitytables.csv','r')

'''
Instructions:
- Important: The first item indicate the age when the table starts. For example, UK43 table is 0 for the first 30 ages. 
- The probability is qx * 1000.
'''
UK43 = (
30, 0.003478, 0.00382329742845617, 0.00420665812441071, 0.00463413030393461, 0.00510795717283819, 0.00563575090736918,
0.00622141498152889, 0.00687337443505803, 0.00759752973591324, 0.00840248875612539, 1000)
USLIFE2002F = (
0, 6.271, 0.418, 0.281, 0.201, 0.17, 0.163, 0.127, 0.123, 0.133, 0.132, 0.126, 0.13, 0.145, 0.186, 0.21, 0.253, 0.389,
0.44, 0.466, 0.457, 0.454, 0.502, 0.467, 0.453, 0.486, 0.498, 0.51, 0.507, 0.565, 0.599, 0.632, 0.668, 0.724, 0.786,
0.853, 0.958, 1.034, 1.12, 1.221, 1.433, 1.493, 1.653, 1.75, 1.995, 2.091, 2.304, 2.376, 2.577, 2.859, 3.031, 3.194,
3.522, 3.634, 4.142, 4.434, 5.1, 5.006, 5.886, 6.441, 7.266, 7.576, 8.476, 9.201, 10.101, 11.149, 12.107, 13.059,
14.571, 15.591, 17.396, 18.991, 20.454, 22.525, 24.633, 27.135, 30.098, 32.631, 36.094, 39.472, 44.11, 49.3, 53.298,
62.179, 64.55, 75.055, 83.221, 91.996, 101.39, 111.404, 122.037, 133.28, 145.119, 157.532, 170.488, 183.953, 197.88,
212.217, 226.905, 241.875, 257.053, 1000)
GKM95 = (
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.5785, 1.5951, 1.6006, 1.595, 1.5785, 1.5503, 1.5094, 1.4643, 1.4238,
1.388, 1.3574, 1.3325, 1.3137, 1.3018, 1.2968, 1.2995, 1.3104, 1.3299, 1.3586, 1.397, 1.4454, 1.5045, 1.5754, 1.6591,
1.7566, 1.8694, 1.9983, 2.1445, 2.3096, 2.497, 2.7107, 2.9545, 3.2325, 3.5482, 3.9057, 4.3087, 4.7606, 5.2655, 5.8269,
6.4474, 7.1294, 7.8756, 8.6884, 9.5704, 10.5241, 11.5521, 12.6571, 13.8417, 15.1083, 16.4598, 18.0706, 20.0313, 22.3416,
25.0018, 28.0117, 31.3714, 35.0808, 39.14, 43.549, 48.3078, 53.4163, 58.8745, 64.6826, 70.8404, 77.348, 84.2053,
91.4124, 98.9693, 106.876, 115.1324, 123.7386, 132.6945, 142.0002, 151.6557, 161.6609, 172.016, 182.7207, 193.7753,
205.1796, 216.9337, 229.0375, 241.4911, 254.2945, 267.4477, 280.9506, 294.8032, 309.0057, 323.5579, 338.4599, 353.7116,
369.3131, 385.2644, 401.5655, 418.2163, 435.2169, 452.5672, 470.2673, 488.3172, 506.7169, 525.4663, 544.5654, 564.0144,
583.8131, 603.9616, 624.4598, 1000)
GKM80 = (
0, 1.079164418, 1.079328111, 1.079491074, 1.078648977, 1.078808304, 1.078966889, 1.07912473, 1.079281824, 1.079438167,
1.078582902, 1.078735552, 1.078887439, 1.07903856, 1.079188913, 1.079338494, 1.091696392, 1.103074859, 1.115509249,
1.127983798, 1.14049906, 1.152032478, 1.164628481, 1.17624136, 1.188920249, 1.200614698, 1.213378658, 1.225156828,
1.238008086, 1.249872172, 1.261778756, 1.275799472, 1.299203577, 1.339307962, 1.398282971, 1.47728018, 1.57747125,
1.700053362, 1.84730159, 2.020492065, 2.222000536, 2.452169539, 2.712457364, 3.004407169, 3.330723082, 3.691050454,
4.08940921, 4.524653838, 5.00006467, 5.515902633, 6.093303575, 6.70602534, 7.38240668, 8.130912696, 8.957368172,
9.871712963, 10.88263678, 11.99880843, 13.23019678, 14.59189245, 16.0927442, 17.74847251, 19.57514438, 21.58700442,
23.80304185, 26.24264453, 28.92465053, 31.87316461, 35.11008985, 38.66236283, 42.55528778, 46.81680975, 51.47595595,
56.56395942, 62.11341884, 68.15239806, 74.71882662, 81.83949419, 89.54942873, 97.87569155, 106.8492548, 116.4957406,
126.8384694, 137.8895462, 149.6622015, 162.1708993, 175.3964191, 189.3441074, 203.9871682, 219.293842, 235.2373808,
251.7516816, 268.7829697, 286.2631264, 304.1267943, 322.3033949, 340.6467977, 359.1075207, 377.5510204, 395.8534233,
414.2059058, 431.880109, 448.441247, 465.2173913, 479.6747967, 500, 500, 500, 500, 500, 500, 1000)
GKF95 = (
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2959, 0.3317, 0.3427, 0.3392, 0.3303, 0.3262, 0.3364, 0.3613, 0.391,
0.4213, 0.4514, 0.4819, 0.5129, 0.5448, 0.578, 0.6126, 0.6492, 0.6877, 0.7287, 0.7726, 0.8193, 0.8693, 0.9216, 0.9756,
1.0304, 1.085, 1.1389, 1.1911, 1.2416, 1.2937, 1.3517, 1.4197, 1.502, 1.6022, 1.7249, 1.8738, 2.0531, 2.2649, 2.5056,
2.7701, 3.0534, 3.3504, 3.656, 3.9654, 4.2734, 4.5752, 4.8654, 5.1379, 5.5084, 6.09, 6.8875, 7.9057, 9.1493, 10.6232,
12.332, 14.2806, 16.4736, 18.916, 21.6123, 24.5675, 27.7862, 31.2732, 35.0334, 39.0713, 43.3919, 47.9999, 52.9, 58.097,
63.5957, 69.4009, 75.5172, 81.9495, 88.7025, 95.781, 103.1898, 110.9336, 119.0172, 127.4454, 136.2228, 145.3544,
154.8448, 164.6988, 174.9211, 185.5166, 196.49, 207.8461, 219.5896, 231.7253, 244.258, 257.1923, 270.5332, 284.2853,
298.4535, 313.0424, 328.0568, 343.5016, 359.3815, 375.7011, 392.4654, 409.6791, 427.3468, 445.4735, 464.0639, 483.1226,
502.6546, 522.6644, 543.1571, 564.1372, 585.6095, 607.5788, 630.05, 1000)
GKM95 = (
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.5785, 1.5951, 1.6006, 1.595, 1.5785, 1.5503, 1.5094, 1.4643, 1.4238,
1.388, 1.3574, 1.3325, 1.3137, 1.3018, 1.2968, 1.2995, 1.3104, 1.3299, 1.3586, 1.397, 1.4454, 1.5045, 1.5754, 1.6591,
1.7566, 1.8694, 1.9983, 2.1445, 2.3096, 2.497, 2.7107, 2.9545, 3.2325, 3.5482, 3.9057, 4.3087, 4.7606, 5.2655, 5.8269,
6.4474, 7.1294, 7.8756, 8.6884, 9.5704, 10.5241, 11.5521, 12.6571, 13.8417, 15.1083, 16.4598, 18.0706, 20.0313, 22.3416,
25.0018, 28.0117, 31.3714, 35.0808, 39.14, 43.549, 48.3078, 53.4163, 58.8745, 64.6826, 70.8404, 77.348, 84.2053,
91.4124, 98.9693, 106.876, 115.1324, 123.7386, 132.6945, 142.0002, 151.6557, 161.6609, 172.016, 182.7207, 193.7753,
205.1796, 216.9337, 229.0375, 241.4911, 254.2945, 267.4477, 280.9506, 294.8032, 309.0057, 323.5579, 338.4599, 353.7116,
369.3131, 385.2644, 401.5655, 418.2163, 435.2169, 452.5672, 470.2673, 488.3172, 506.7169, 525.4663, 544.5654, 564.0144,
583.8131, 603.9616, 624.4598, 1000)
GRF80 = (
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.4712, 0.4843, 0.5003, 0.5192, 0.541, 0.5658, 0.5935, 0.624, 0.6575,
0.6939, 0.7333, 0.7755, 0.8206, 0.8687, 0.9196, 0.9735, 1.0303, 1.09, 1.1526, 1.2181, 1.2866, 1.3579, 1.4322, 1.5093,
1.5894, 1.6724, 1.7583, 1.8471, 1.9392, 2.0181, 2.0729, 2.11, 2.136, 2.1575, 2.181, 2.213, 2.2601, 2.3289, 2.4259,
2.5576, 2.7306, 2.9515, 3.2267, 3.5628, 3.9664, 4.444, 5.0022, 5.6474, 6.3864, 7.2255, 8.171, 9.2345, 10.4321, 11.7802,
13.2968, 15.0022, 16.9186, 19.0706, 21.4853, 24.1923, 27.224, 30.6155, 34.405, 38.6331, 43.3433, 48.5815, 54.3957,
60.8355, 67.9514, 75.7938, 84.4121, 93.8531, 104.1596, 115.3685, 127.5088, 140.5995, 154.6474, 169.6451, 185.569,
202.378, 220.0122, 238.3932, 257.424, 276.9907, 296.9648, 317.2062, 337.567, 357.8957, 378.042, 397.8608, 417.2163,
435.986, 454.0628, 471.3574, 487.7992, 503.3364, 517.9354, 531.5796, 544.2678, 556.0123, 566.8365, 576.7731, 1000)
GRM80 = (
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.7481, 0.7552, 0.7639, 0.7741, 0.7859, 0.7993, 0.8143, 0.8309, 0.849,
0.8687, 0.89, 0.9128, 0.9372, 0.9633, 0.9908, 1.0202, 1.0558, 1.1032, 1.1634, 1.237, 1.3251, 1.4283, 1.5477, 1.684,
1.838, 2.0106, 2.2027, 2.415, 2.6486, 2.9041, 3.1824, 3.4844, 3.8109, 4.1628, 4.5409, 4.946, 5.379, 5.8408, 6.3322,
6.854, 7.4071, 7.9923, 8.6104, 9.2623, 9.9693, 10.7572, 11.6353, 12.6135, 13.7031, 14.9161, 16.2662, 17.7682, 19.4386,
21.2951, 23.3574, 25.647, 28.1871, 31.003, 34.122, 37.5735, 41.3891, 45.6023, 50.2487, 55.3658, 60.9926, 67.1696,
73.938, 81.3394, 89.4152, 98.2057, 107.749, 118.0801, 129.2296, 141.2224, 154.0761, 167.8, 182.3929, 197.8426, 214.1242,
231.1994, 249.0158, 267.5074, 286.594, 306.1831, 326.171, 346.4446, 366.8841, 387.3658, 407.7649, 427.9586, 447.829,
467.2659, 486.1689, 504.4494, 522.0318, 538.8543, 554.8694, 570.043, 584.3546, 597.7955, 610.3683, 622.085, 1000)
GKF80 = (
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.994, 1.006, 1.018, 1.03, 1.042, 1.055, 1.067, 1.079, 1.091, 1.103,
1.116, 1.128, 1.14, 1.152, 1.164, 1.177, 1.189, 1.201, 1.213, 1.225, 1.238, 1.25, 1.262, 1.276, 1.299, 1.34, 1.398,
1.477, 1.577, 1.7, 1.847, 2.021, 2.222, 2.452, 2.712, 3.005, 3.331, 3.691, 4.089, 4.525, 5, 5.516, 6.094, 6.706, 7.382,
8.13, 8.958, 9.872, 10.882, 11.998, 13.231, 14.591, 16.093, 17.749, 19.575, 21.587, 23.803, 26.242, 28.925, 31.873,
35.111, 38.662, 42.555, 46.817, 51.476, 56.565, 62.113, 68.153, 74.718, 81.839, 89.548, 97.876, 106.85, 116.496,
126.836, 137.888, 149.663, 162.167, 175.397, 189.325, 203.986, 219.296, 235.235, 251.753, 268.791, 286.281, 304.144,
322.298, 340.651, 359.109, 377.576, 395.955, 414.15, 432.072, 449.633, 466.757, 483.372, 499.417, 514.842, 529.606,
543.677, 557.036, 1000)
GKM80 = (
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.079, 1.091, 1.103, 1.116, 1.128, 1.14, 1.152, 1.164, 1.177, 1.189,
1.201, 1.213, 1.225, 1.238, 1.25, 1.262, 1.276, 1.299, 1.34, 1.398, 1.477, 1.577, 1.7, 1.847, 2.021, 2.222, 2.452,
2.712, 3.004, 3.33, 3.691, 4.089, 4.524, 5, 5.516, 6.094, 6.706, 7.382, 8.13, 8.958, 9.872, 10.882, 11.998, 13.231,
14.591, 16.093, 17.749, 19.575, 21.587, 23.803, 26.242, 28.925, 31.873, 35.111, 38.662, 42.555, 46.816, 51.476, 56.564,
62.113, 68.153, 74.718, 81.839, 89.548, 97.876, 106.85, 116.496, 126.836, 137.888, 149.663, 162.167, 175.397, 189.343,
203.986, 219.296, 235.235, 251.753, 268.791, 286.281, 304.144, 322.298, 340.651, 359.109, 377.576, 395.955, 414.15,
432.072, 449.633, 466.757, 483.372, 499.417, 514.842, 529.606, 543.677, 557.036, 569.668, 581.572, 592.752, 603.217,
612.985, 622.077, 630.517, 1000)
GRM95 = (
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.2879, 1.289, 1.2902, 1.2913, 1.2924, 1.2936, 1.2947, 1.2958, 1.297,
1.2981, 1.2992, 1.3004, 1.3015, 1.3026, 1.3038, 1.3057, 1.3146, 1.3325, 1.3596, 1.3965, 1.4436, 1.5014, 1.571, 1.6535,
1.7501, 1.8617, 1.9896, 2.1348, 2.299, 2.4855, 2.6984, 2.9414, 3.2187, 3.5338, 3.8715, 4.2176, 4.5778, 4.9576, 5.3626,
5.7985, 6.2708, 6.7851, 7.347, 7.9621, 8.6361, 9.3744, 10.1828, 11.0668, 11.9579, 12.8181, 13.6967, 14.64, 15.6913,
16.8912, 18.2776, 19.8861, 21.7496, 23.8892, 26.2863, 28.9139, 31.7462, 34.7587, 37.9279, 41.2316, 44.6485, 48.1587,
51.743, 55.3833, 59.0624, 62.7642, 66.4732, 70.175, 73.8924, 77.7907, 82.0603, 86.88, 92.4166, 98.8263, 106.2543,
114.5014, 123.2765, 132.5794, 142.4102, 152.769, 163.6556, 175.0702, 187.0127, 199.483, 212.4813, 226.0075, 240.0615,
254.6435, 269.7534, 285.3912, 301.5569, 318.2504, 335.4719, 353.2213, 371.4986, 390.3038, 409.637, 429.498, 449.8869,
470.8037, 492.2484, 514.2211, 536.7216, 559.75, 583.3064, 607.3906, 632.0028, 1000)
GRF95 = (
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.3179, 0.3199, 0.3219, 0.3239, 0.3259, 0.3286, 0.3424, 0.3664, 0.3953,
0.4247, 0.4541, 0.4839, 0.5143, 0.5456, 0.5783, 0.6124, 0.6485, 0.6867, 0.7274, 0.7709, 0.8174, 0.8671, 0.9192, 0.973,
1.0277, 1.0822, 1.136, 1.188, 1.2384, 1.2904, 1.3484, 1.4163, 1.4916, 1.5698, 1.6526, 1.7417, 1.8387, 1.9453, 2.0633,
2.1941, 2.3396, 2.5014, 2.6811, 2.8805, 3.1012, 3.3448, 3.5914, 3.8417, 4.1264, 4.4735, 4.9086, 5.4484, 6.0827, 6.7954,
7.5719, 8.3984, 9.2619, 10.1507, 11.0538, 11.961, 12.8778, 13.8681, 15.0041, 16.352, 17.9716, 19.9171, 22.2372, 24.9755,
28.1523, 31.7134, 35.5905, 39.7196, 44.0415, 48.5011, 53.0474, 57.633, 62.2144, 66.8049, 71.6261, 76.9316, 82.9524,
89.6957, 97.0253, 104.9412, 113.4435, 122.5322, 132.2071, 142.4684, 153.316, 164.75, 176.7703, 189.3769, 202.5699,
216.3492, 230.7148, 245.6668, 261.2051, 277.3297, 294.0407, 311.338, 329.2217, 347.6916, 366.748, 386.3906, 406.6196,
427.4349, 448.8366, 470.8246, 493.3989, 516.5595, 540.3065, 1000)
FIN = (199, 0, 1000)
TEST = (98, 0, 0.05, 1000)
SPAINPERM2000 = (
0, 26.7846, 2.1132, 1.5074, 0.9754, 0.9087, 0.7162, 0.6291, 0.5478, 0.4416, 0.3952, 0.4077, 0.3208, 0.3627, 0.3534,
0.3583, 0.3766, 0.4236, 0.4811, 0.5094, 0.5359, 0.5216, 0.5315, 0.4942, 0.5058, 0.5142, 0.5111, 0.5411, 0.5811, 0.5853,
0.6213, 0.6048, 0.5977, 0.5553, 0.5234, 0.5529, 0.6324, 0.6409, 0.6331, 0.6477, 0.6392, 0.7344, 0.6776, 0.7747, 0.8119,
0.8530, 0.9197, 0.9173, 0.9841, 0.9983, 1.1737, 1.3150, 1.4560, 1.4857, 1.7040, 1.7653, 1.8616, 1.8907, 2.0703, 2.2248,
2.3472, 2.5721, 2.7313, 2.9537, 3.0638, 3.2829, 3.6204, 3.9212, 4.2317, 4.5801, 5.0495, 5.4721, 6.1110, 6.7021, 7.5592,
8.4368, 9.4458, 10.6256, 11.9844, 13.3730, 15.0130, 17.1280, 19.7247, 22.1471, 25.3717, 29.4682, 33.6982, 37.9036,
43.1518, 48.5546, 55.1153, 62.7627, 68.7645, 79.5625, 91.9339, 107.1328, 124.6729, 144.9143, 168.2791, 195.2608,
226.9151, 260.9836, 308.0680, 329.1760, 350.7650, 372.8190, 395.3310, 418.3050, 441.7560, 468.9810, 497.8840, 528.5680,
561.1430, 595.7250, 632.4390, 671.4160, 1000)
SPAININE2004 = (
0, 3.935, 0.323, 0.214, 0.167, 0.141, 0.117, 0.113, 0.111, 0.116, 0.11, 0.107, 0.115, 0.138, 0.155, 0.196, 0.261, 0.326,
0.378, 0.437, 0.468, 0.467, 0.474, 0.483, 0.486, 0.485, 0.482, 0.494, 0.503, 0.518, 0.546, 0.585, 0.631, 0.677, 0.736,
0.809, 0.877, 0.956, 1.053, 1.143, 1.232, 1.333, 1.427, 1.551, 1.706, 1.858, 2.053, 2.251, 2.447, 2.637, 2.879, 3.113,
3.396, 3.668, 3.903, 4.179, 4.574, 4.952, 5.275, 5.697, 6.247, 6.791, 7.308, 7.637, 8.521, 9.403, 10.288, 11.111, 12.77,
13.704, 14.964, 16.401, 18.326, 20.342, 22.695, 25.211, 28.288, 31.585, 35.788, 40.192, 45.517, 51.074, 57.965, 64.674,
72.901, 81.152, 91.414, 102.445, 115.601, 127.651, 142.332, 156.778, 160.356, 175.837, 201.915, 237.282, 280.631,
330.655, 386.048, 445.502, 507.71, 571.366, 1000)
SPAININE2005 = (
2.583791, 0.508471, 0.460709, 0.430675, 0.414095, 0.402603, 0.401485, 0.401637, 0.406583, 0.402789, 0.399976, 0.408149,
0.423926, 0.436973, 0.464055, 0.517948, 0.574353, 0.615905, 0.663226, 0.687875, 0.693000, 0.703723, 0.701644, 0.704153,
0.705664, 0.705153, 0.709204, 0.714820, 0.731303, 0.747248, 0.776918, 0.810428, 0.837414, 0.881681, 0.939679, 0.991422,
1.063405, 1.166164, 1.269737, 1.354198, 1.454751, 1.559673, 1.686756, 1.843112, 2.017662, 2.224748, 2.423707, 2.630145,
2.828441, 3.096794, 3.382685, 3.695538, 4.030610, 4.334374, 4.708664, 5.151774, 5.630567, 6.038401, 6.569489, 7.151412,
7.710619, 8.318870, 8.848244, 9.750154, 10.650585, 11.628118, 12.570646, 14.079738, 15.102284, 16.146185, 17.679584,
19.585263, 21.455168, 23.417133, 26.116740, 28.580127, 31.301970, 34.651468, 38.331617, 42.363058, 46.633814, 51.472470,
56.637311, 62.146305, 68.348696, 75.354973, 83.553689, 91.973595, 100.813746, 110.061319, 119.423813, 125.759154,
136.452986, 151.647540, 169.224154, 188.708038, 210.983462, 234.076092, 250.813155, 278.171669, 323.697196, 366.598032,
420.585061, 482.189978, 550.891054, 609.209875, 653.209714, 698.176428, 745.156923, 807.109051, 877.065598, 957.230143,
1000)
HKM2009 = (
0, 1.62815, 0.24345, 0.199, 0.16076, 0.12872, 0.10283, 0.08294, 0.06895, 0.06047, 0.05701, 0.05809, 0.06323, 0.0721,
0.08473, 0.10147, 0.12525, 0.15755, 0.19842, 0.24661, 0.29976, 0.35237, 0.40026, 0.44062, 0.47259, 0.49717, 0.51894,
0.54266, 0.57322, 0.6118, 0.65779, 0.70727, 0.75595, 0.79919, 0.83598, 0.86691, 0.89017, 0.90796, 0.92644, 0.95062,
0.98613, 1.04055, 1.11886, 1.22347, 1.35712, 1.52048, 1.71008, 1.92155, 2.14961, 2.39393, 2.65575, 2.93589, 3.23758,
3.56647, 3.92649, 4.32134, 4.74218, 5.18691, 5.66013, 6.17296, 6.74044, 7.36759, 8.06662, 8.85691, 9.76132, 10.80268,
11.99491, 13.34838, 14.86986, 16.57772, 18.48815, 20.55715, 22.77203, 25.15114, 27.74459, 30.6209, 33.86068, 37.53675,
41.70636, 46.42029, 51.70618, 57.57565, 64.02948, 71.05935, 78.65227, 86.79437, 95.65884, 105.29281, 115.74404,
127.06046, 139.28975, 152.47878, 166.67301, 181.91585, 198.24791, 215.70627, 234.32368, 254.12773, 275.14001, 297.37534,
320.84097, 1000.0)
HKF2009 = (
0, 1.71176, 0.36236, 0.28905, 0.22588, 0.17286, 0.12998, 0.09717, 0.07406, 0.06033, 0.05531, 0.05816, 0.06768, 0.0823,
0.10015, 0.11936, 0.13766, 0.15385, 0.16779, 0.17881, 0.18682, 0.19209, 0.19563, 0.19928, 0.2038, 0.20985, 0.21759,
0.22701, 0.23786, 0.25056, 0.26554, 0.2836, 0.30516, 0.33031, 0.35907, 0.39126, 0.42494, 0.45907, 0.49348, 0.52895,
0.56699, 0.60918, 0.65763, 0.715, 0.78335, 0.86436, 0.96201, 1.07726, 1.20804, 1.35263, 1.50806, 1.66723, 1.82507,
1.97851, 2.12686, 2.27176, 2.40602, 2.53181, 2.6607, 2.80477, 2.97893, 3.19954, 3.48048, 3.83307, 4.26937, 4.79716,
5.39818, 6.06192, 6.78556, 7.58538, 8.48609, 9.49678, 10.64095, 11.95631, 13.48294, 15.26009, 17.31959, 19.68458,
22.3697, 25.38593, 28.73599, 32.42417, 36.448, 40.80318, 45.4852, 50.48926, 56.01148, 62.10012, 68.80696, 76.18735,
84.30023, 93.2081, 102.97691, 113.67585, 125.37711, 138.15546, 152.0877, 167.25202, 183.72719, 201.59151, 220.92166,
1000.0)
HKM2010 = (
0, 1.8693, 0.40241, 0.30526, 0.22388, 0.15827, 0.10835, 0.07375, 0.05376, 0.04726, 0.05243, 0.06725, 0.08917, 0.11529,
0.14297, 0.17007, 0.19385, 0.21372, 0.23125, 0.24666, 0.26088, 0.27663, 0.29614, 0.32112, 0.35193, 0.38796, 0.42704,
0.46672, 0.50431, 0.53891, 0.57046, 0.59843, 0.62399, 0.65002, 0.67834, 0.7109, 0.7486, 0.79247, 0.84366, 0.90424,
0.97622, 1.06058, 1.15805, 1.26918, 1.39573, 1.53941, 1.69825, 1.87201, 2.0622, 2.27246, 2.50746, 2.77304, 3.07396,
3.41395, 3.79649, 4.22343, 4.68489, 5.17567, 5.69523, 6.2506, 6.85299, 7.50582, 8.22012, 9.01454, 9.90857, 10.92172,
12.06048, 13.3321, 14.74454, 16.31774, 18.07183, 19.97101, 22.01014, 24.21445, 26.63724, 29.34757, 32.42318, 35.93295,
39.93025, 44.46194, 49.55279, 55.2141, 61.44608, 68.24063, 75.58551, 83.46767, 92.06303, 101.42055, 111.59025,
122.62282, 134.56916, 147.47989, 161.40477, 176.39204, 192.48766, 209.73459, 228.17189, 247.83385, 268.74909, 290.93966,
314.4201, 1000.0)
HKF2010 = (
0, 1.4714, 0.32926, 0.24593, 0.17667, 0.1215, 0.08019, 0.05219, 0.03673, 0.03216, 0.03604, 0.04586, 0.05875, 0.07189,
0.08352, 0.09291, 0.10165, 0.11176, 0.12569, 0.14317, 0.16315, 0.18228, 0.19788, 0.208, 0.21236, 0.2119, 0.20917,
0.20719, 0.20946, 0.21743, 0.23161, 0.25014, 0.27105, 0.29224, 0.31407, 0.33778, 0.36761, 0.40664, 0.45679, 0.518,
0.58871, 0.66261, 0.7348, 0.80185, 0.86381, 0.92305, 0.98624, 1.05994, 1.15054, 1.26023, 1.38881, 1.5317, 1.68347,
1.83782, 1.9936, 2.15157, 2.30391, 2.45159, 2.60438, 2.77282, 2.97039, 3.22086, 3.5402, 3.93654, 4.41466, 4.97198,
5.56236, 6.15883, 6.75354, 7.36522, 8.0304, 8.77032, 9.63109, 10.68351, 11.99105, 13.61271, 15.59225, 17.95917,
20.73033, 23.917, 27.51948, 31.5434, 35.98403, 40.83487, 46.08969, 51.74182, 57.99623, 64.90312, 72.51463, 80.88461,
90.0682, 100.1214, 111.10047, 123.06135, 136.05888, 150.14602, 165.37294, 181.78602, 199.42686, 218.33121, 238.52789,
1000.0)
HKM2011 = (
0, 1.6134, 0.33637, 0.26255, 0.2009, 0.1514, 0.11392, 0.08803, 0.07317, 0.0681, 0.07104, 0.08011, 0.09317, 0.10813,
0.12364, 0.13914, 0.15596, 0.17561, 0.19982, 0.2282, 0.25974, 0.2916, 0.32151, 0.34782, 0.37015, 0.38911, 0.40588,
0.42263, 0.44251, 0.46724, 0.4981, 0.53724, 0.58496, 0.63969, 0.70061, 0.76629, 0.83083, 0.89101, 0.9463, 0.99828,
1.05062, 1.10857, 1.17823, 1.26663, 1.3784, 1.5166, 1.68268, 1.87525, 2.09009, 2.32705, 2.58604, 2.86232, 3.15445,
3.46427, 3.79531, 4.15292, 4.53033, 4.92992, 5.36317, 5.84549, 6.39553, 7.05012, 7.831, 8.74486, 9.79339, 10.96668,
12.18725, 13.40952, 14.6196, 15.84303, 17.13412, 18.53385, 20.11734, 21.99347, 24.2526, 26.97426, 30.21105, 33.99398,
38.33641, 43.2436, 48.70735, 54.73035, 61.30069, 68.40509, 76.03132, 84.16646, 93.03703, 102.69035, 113.17399,
124.53533, 136.82099, 150.07625, 164.34438, 179.66597, 196.07809, 213.6136, 232.30025, 252.15994, 273.20789, 295.45188,
318.89159, 1000.0)
HKF2011 = (
0, 1.03024, 0.4159, 0.32917, 0.25456, 0.19208, 0.14164, 0.10295, 0.07548, 0.05835, 0.05016, 0.04938, 0.05415, 0.06247,
0.07268, 0.08358, 0.09513, 0.10775, 0.12238, 0.13834, 0.15477, 0.17001, 0.18297, 0.19314, 0.20029, 0.20471, 0.20591,
0.2047, 0.20315, 0.20297, 0.20608, 0.21644, 0.23609, 0.26522, 0.30362, 0.34984, 0.3991, 0.44746, 0.49183, 0.5317,
0.56828, 0.60392, 0.64251, 0.68951, 0.74786, 0.81966, 0.90814, 1.01347, 1.13275, 1.26466, 1.40704, 1.55257, 1.69696,
1.83899, 1.97987, 2.12337, 2.27618, 2.44563, 2.63967, 2.86274, 3.11709, 3.38999, 3.67453, 3.96952, 4.28362, 4.63087,
5.00882, 5.42953, 5.91954, 6.50886, 7.23008, 8.09982, 9.13638, 10.35966, 11.80357, 13.50002, 15.47314, 17.73944,
20.3085, 23.18683, 26.37474, 29.87499, 33.68473, 37.79997, 42.21679, 46.931, 52.14672, 57.91283, 64.28213, 71.31146,
79.06176, 87.59815, 96.98988, 107.31024, 118.63634, 131.0488, 144.6313, 159.46992, 175.6524, 193.2671, 212.40182,
1000.0)
HKM2012 = (
0, 1.40257, 0.21356, 0.18939, 0.16837, 0.15048, 0.13573, 0.1241, 0.11563, 0.11031, 0.10815, 0.1092, 0.11353, 0.1213,
0.1327, 0.14801, 0.1697, 0.19866, 0.23418, 0.27476, 0.31795, 0.35794, 0.39074, 0.4142, 0.42788, 0.4333, 0.43427,
0.43558, 0.44301, 0.45916, 0.48526, 0.52014, 0.5615, 0.60586, 0.65315, 0.70402, 0.76104, 0.8264, 0.90191, 0.98784,
1.08348, 1.1836, 1.28482, 1.38566, 1.4875, 1.59372, 1.70686, 1.83193, 1.97639, 2.14631, 2.34714, 2.58304, 2.85573,
3.16458, 3.51232, 3.90101, 4.32487, 4.78147, 5.27177, 5.80149, 6.37896, 7.00328, 7.6807, 8.42457, 9.25101, 10.17744,
11.18882, 12.28753, 13.4933, 14.84255, 16.37971, 18.14429, 20.17354, 22.50232, 25.17109, 28.21033, 31.63276, 35.4402,
39.62738, 44.18563, 49.10302, 54.37692, 59.99836, 65.95933, 72.25328, 78.87336, 86.07291, 93.89752, 102.39539,
111.61729, 121.61649, 132.44865, 144.17156, 156.84491, 170.52993, 185.28897, 201.1849, 218.28051, 236.63771, 256.31664,
277.37467, 1000.0)
HKF2012 = (
0, 1.58436, 0.27693, 0.24424, 0.21461, 0.18804, 0.16451, 0.14393, 0.12624, 0.11123, 0.09864, 0.08821, 0.07967, 0.07285,
0.06779, 0.06469, 0.0649, 0.06918, 0.07766, 0.08986, 0.10478, 0.11992, 0.13341, 0.14397, 0.15128, 0.15585, 0.15908,
0.16296, 0.17002, 0.18145, 0.19789, 0.21901, 0.24402, 0.27168, 0.30213, 0.33579, 0.37412, 0.41814, 0.46839, 0.52479,
0.58673, 0.65174, 0.71804, 0.78449, 0.85125, 0.91933, 0.98894, 1.06193, 1.14174, 1.23119, 1.33312, 1.45402, 1.5967,
1.76022, 1.9433, 2.14258, 2.34064, 2.52777, 2.70196, 2.86841, 3.03865, 3.23229, 3.46903, 3.76874, 4.14304, 4.59727,
5.10387, 5.64547, 6.21484, 6.82862, 7.51525, 8.27846, 9.14682, 10.17357, 11.41417, 12.92564, 14.75772, 16.9488,
19.52502, 22.50735, 25.90376, 29.7221, 33.96059, 38.61412, 43.67665, 49.1417, 55.20422, 61.91595, 69.33099, 77.50546,
86.49716, 96.36513, 107.16909, 118.96881, 131.82337, 145.7903, 160.92464, 177.27793, 194.89709, 213.82325, 234.09059,
1000.0)
HKM2013 = (
0, 2.05028, 0.29541, 0.25613, 0.22162, 0.19188, 0.16687, 0.14651, 0.1307, 0.11919, 0.11163, 0.10767, 0.10692, 0.109,
0.11373, 0.1211, 0.13193, 0.14674, 0.16575, 0.1886, 0.21461, 0.24214, 0.26994, 0.29716, 0.32357, 0.34949, 0.376,
0.40445, 0.43643, 0.47257, 0.51305, 0.55823, 0.60757, 0.65969, 0.71385, 0.7692, 0.82102, 0.86751, 0.9098, 0.95032,
0.99321, 1.04594, 1.11477, 1.20475, 1.31865, 1.45688, 1.61197, 1.77777, 1.94952, 2.12911, 2.32156, 2.53522, 2.7792,
3.0634, 3.39366, 3.77313, 4.19998, 4.67003, 5.17681, 5.72087, 6.30415, 6.90477, 7.51886, 8.16044, 8.85137, 9.62198,
10.51305, 11.55944, 12.79013, 14.22844, 15.88573, 17.7088, 19.6648, 21.74112, 23.97142, 26.41159, 29.13665, 32.21827,
35.71553, 39.6826, 44.15199, 49.13671, 54.64151, 60.66174, 67.18757, 74.20845, 81.89832, 90.31083, 99.50224, 109.53119,
120.45852, 132.34686, 145.26023, 159.26348, 174.42164, 190.79918, 208.45907, 227.46181, 247.86429, 269.71855, 293.07043,
1000.0)
HKF2013 = (
0, 1.24323, 0.24019, 0.20991, 0.18268, 0.15848, 0.13736, 0.11938, 0.10454, 0.09299, 0.08488, 0.08033, 0.07935, 0.08177,
0.08714, 0.0948, 0.10375, 0.1132, 0.12256, 0.1314, 0.13959, 0.14739, 0.15535, 0.16427, 0.17433, 0.18555, 0.19755,
0.20998, 0.22252, 0.23523, 0.24834, 0.26134, 0.27441, 0.28842, 0.30435, 0.32342, 0.34746, 0.37773, 0.41493, 0.45962,
0.51185, 0.57044, 0.63414, 0.70166, 0.77294, 0.84844, 0.92756, 1.01106, 1.10109, 1.19961, 1.30887, 1.43359, 1.57627,
1.73722, 1.91621, 2.11156, 2.31462, 2.5198, 2.72454, 2.93053, 3.14261, 3.35938, 3.58701, 3.83924, 4.12933, 4.47154,
4.86991, 5.33132, 5.86547, 6.48968, 7.22175, 8.0341, 8.92399, 9.91345, 11.04752, 12.38421, 13.98859, 15.91869, 18.22022,
20.93391, 24.08281, 27.67942, 31.72731, 36.22342, 41.16151, 46.53476, 52.51794, 59.1655, 66.53431, 74.68336, 83.67334,
93.5661, 104.42405, 116.30941, 129.28335, 143.40503, 158.73056, 175.31182, 193.19526, 212.42061, 233.0196, 1000.0)
HKM2014 = (
0, 1.37916, 0.2039, 0.17335, 0.14633, 0.12287, 0.10304, 0.08701, 0.07481, 0.06687, 0.06366, 0.06558, 0.07288, 0.08553,
0.10285, 0.12375, 0.14648, 0.1695, 0.19152, 0.21175, 0.22991, 0.246, 0.26084, 0.27612, 0.29251, 0.3106, 0.32997,
0.35055, 0.37255, 0.39693, 0.42489, 0.45841, 0.49885, 0.54697, 0.60331, 0.66783, 0.73942, 0.81675, 0.89826, 0.98363,
1.073, 1.1655, 1.26165, 1.36341, 1.47246, 1.59085, 1.71602, 1.84827, 1.99079, 2.1488, 2.32879, 2.53923, 2.78665,
3.07554, 3.41018, 3.79241, 4.22147, 4.69367, 5.20243, 5.74639, 6.32495, 6.90587, 7.48033, 8.06292, 8.67901, 9.36611,
10.18197, 11.17467, 12.38267, 13.8322, 15.53181, 17.41227, 19.42562, 21.54518, 23.80297, 26.25937, 29.00089, 32.1121,
35.66394, 39.72208, 44.32698, 49.49402, 55.22991, 61.52991, 68.38275, 75.77631, 83.87528, 92.73293, 102.40434,
112.94607, 124.41578, 136.8717, 150.37208, 164.9745, 180.73509, 197.70767, 215.9428, 235.48676, 256.38042, 278.65814,
302.34658, 1000.0)
HKF2014 = (
0, 1.99422, 0.32291, 0.25135, 0.19187, 0.14446, 0.10896, 0.08487, 0.0715, 0.06741, 0.07047, 0.07844, 0.08872, 0.09871,
0.10663, 0.11158, 0.11359, 0.11387, 0.11479, 0.11676, 0.11995, 0.12371, 0.12752, 0.131, 0.1345, 0.13865, 0.14534,
0.15583, 0.17071, 0.18992, 0.21272, 0.23634, 0.25862, 0.27806, 0.29466, 0.3094, 0.32378, 0.34019, 0.36198, 0.39118,
0.4293, 0.4781, 0.53773, 0.6067, 0.68475, 0.77123, 0.86281, 0.95763, 1.05527, 1.15666, 1.26394, 1.38222, 1.51563,
1.6674, 1.8386, 2.0286, 2.23064, 2.43961, 2.65204, 2.8691, 3.09463, 3.32758, 3.57305, 3.84228, 4.14586, 4.49517,
4.88043, 5.30306, 5.77563, 6.32186, 6.9708, 7.72595, 8.60526, 9.64107, 10.87802, 12.36308, 14.13851, 16.23757, 18.68347,
21.49513, 24.68039, 28.24604, 32.19102, 36.51121, 41.20158, 46.2567, 51.8699, 58.09296, 64.98083, 72.59154, 80.986,
90.22778, 100.38273, 111.51856, 123.70423, 137.00932, 151.50313, 167.25381, 184.32719, 202.78561, 222.68656, 1000.0)
