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

import csv
from .lifecontingencies import *
import os
script_dir = os.path.dirname(__file__)

UK43 = (30,0.003478,0.00382329742845617,0.00420665812441071,0.00463413030393461,0.00510795717283819,0.00563575090736918,0.00622141498152889,0.00687337443505803,0.00759752973591324,0.00840248875612539,1000)
USLIFE2002F = (0,6.271,0.418,0.281,0.201,0.17,0.163,0.127,0.123,0.133,0.132,0.126,0.13,0.145,0.186,0.21,0.253,0.389,0.44,0.466,0.457,0.454,0.502,0.467,0.453,0.486,0.498,0.51,0.507,0.565,0.599,0.632,0.668,0.724,0.786,0.853,0.958,1.034,1.12,1.221,1.433,1.493,1.653,1.75,1.995,2.091,2.304,2.376,2.577,2.859,3.031,3.194,3.522,3.634,4.142,4.434,5.1,5.006,5.886,6.441,7.266,7.576,8.476,9.201,10.101,11.149,12.107,13.059,14.571,15.591,17.396,18.991,20.454,22.525,24.633,27.135,30.098,32.631,36.094,39.472,44.11,49.3,53.298,62.179,64.55,75.055,83.221,91.996,101.39,111.404,122.037,133.28,145.119,157.532,170.488,183.953,197.88,212.217,226.905,241.875,257.053,1000)
GKM95 = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1.5785,1.5951,1.6006,1.595,1.5785,1.5503,1.5094,1.4643,1.4238,1.388,1.3574,1.3325,1.3137,1.3018,1.2968,1.2995,1.3104,1.3299,1.3586,1.397,1.4454,1.5045,1.5754,1.6591,1.7566,1.8694,1.9983,2.1445,2.3096,2.497,2.7107,2.9545,3.2325,3.5482,3.9057,4.3087,4.7606,5.2655,5.8269,6.4474,7.1294,7.8756,8.6884,9.5704,10.5241,11.5521,12.6571,13.8417,15.1083,16.4598,18.0706,20.0313,22.3416,25.0018,28.0117,31.3714,35.0808,39.14,43.549,48.3078,53.4163,58.8745,64.6826,70.8404,77.348,84.2053,91.4124,98.9693,106.876,115.1324,123.7386,132.6945,142.0002,151.6557,161.6609,172.016,182.7207,193.7753,205.1796,216.9337,229.0375,241.4911,254.2945,267.4477,280.9506,294.8032,309.0057,323.5579,338.4599,353.7116,369.3131,385.2644,401.5655,418.2163,435.2169,452.5672,470.2673,488.3172,506.7169,525.4663,544.5654,564.0144,583.8131,603.9616,624.4598,1000)
GKM80 = (0,1.079164418,1.079328111,1.079491074,1.078648977,1.078808304,1.078966889,1.07912473,1.079281824,1.079438167,1.078582902,1.078735552,1.078887439,1.07903856,1.079188913,1.079338494,1.091696392,1.103074859,1.115509249,1.127983798,1.14049906,1.152032478,1.164628481,1.17624136,1.188920249,1.200614698,1.213378658,1.225156828,1.238008086,1.249872172,1.261778756,1.275799472,1.299203577,1.339307962,1.398282971,1.47728018,1.57747125,1.700053362,1.84730159,2.020492065,2.222000536,2.452169539,2.712457364,3.004407169,3.330723082,3.691050454,4.08940921,4.524653838,5.00006467,5.515902633,6.093303575,6.70602534,7.38240668,8.130912696,8.957368172,9.871712963,10.88263678,11.99880843,13.23019678,14.59189245,16.0927442,17.74847251,19.57514438,21.58700442,23.80304185,26.24264453,28.92465053,31.87316461,35.11008985,38.66236283,42.55528778,46.81680975,51.47595595,56.56395942,62.11341884,68.15239806,74.71882662,81.83949419,89.54942873,97.87569155,106.8492548,116.4957406,126.8384694,137.8895462,149.6622015,162.1708993,175.3964191,189.3441074,203.9871682,219.293842,235.2373808,251.7516816,268.7829697,286.2631264,304.1267943,322.3033949,340.6467977,359.1075207,377.5510204,395.8534233,414.2059058,431.880109,448.441247,465.2173913,479.6747967,500,500,500,500,500,500,1000)
GKF95 = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.2959,0.3317,0.3427,0.3392,0.3303,0.3262,0.3364,0.3613,0.391,0.4213,0.4514,0.4819,0.5129,0.5448,0.578,0.6126,0.6492,0.6877,0.7287,0.7726,0.8193,0.8693,0.9216,0.9756,1.0304,1.085,1.1389,1.1911,1.2416,1.2937,1.3517,1.4197,1.502,1.6022,1.7249,1.8738,2.0531,2.2649,2.5056,2.7701,3.0534,3.3504,3.656,3.9654,4.2734,4.5752,4.8654,5.1379,5.5084,6.09,6.8875,7.9057,9.1493,10.6232,12.332,14.2806,16.4736,18.916,21.6123,24.5675,27.7862,31.2732,35.0334,39.0713,43.3919,47.9999,52.9,58.097,63.5957,69.4009,75.5172,81.9495,88.7025,95.781,103.1898,110.9336,119.0172,127.4454,136.2228,145.3544,154.8448,164.6988,174.9211,185.5166,196.49,207.8461,219.5896,231.7253,244.258,257.1923,270.5332,284.2853,298.4535,313.0424,328.0568,343.5016,359.3815,375.7011,392.4654,409.6791,427.3468,445.4735,464.0639,483.1226,502.6546,522.6644,543.1571,564.1372,585.6095,607.5788,630.05,1000)
GKM95 = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1.5785,1.5951,1.6006,1.595,1.5785,1.5503,1.5094,1.4643,1.4238,1.388,1.3574,1.3325,1.3137,1.3018,1.2968,1.2995,1.3104,1.3299,1.3586,1.397,1.4454,1.5045,1.5754,1.6591,1.7566,1.8694,1.9983,2.1445,2.3096,2.497,2.7107,2.9545,3.2325,3.5482,3.9057,4.3087,4.7606,5.2655,5.8269,6.4474,7.1294,7.8756,8.6884,9.5704,10.5241,11.5521,12.6571,13.8417,15.1083,16.4598,18.0706,20.0313,22.3416,25.0018,28.0117,31.3714,35.0808,39.14,43.549,48.3078,53.4163,58.8745,64.6826,70.8404,77.348,84.2053,91.4124,98.9693,106.876,115.1324,123.7386,132.6945,142.0002,151.6557,161.6609,172.016,182.7207,193.7753,205.1796,216.9337,229.0375,241.4911,254.2945,267.4477,280.9506,294.8032,309.0057,323.5579,338.4599,353.7116,369.3131,385.2644,401.5655,418.2163,435.2169,452.5672,470.2673,488.3172,506.7169,525.4663,544.5654,564.0144,583.8131,603.9616,624.4598,1000)
GRF80 = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.4712,0.4843,0.5003,0.5192,0.541,0.5658,0.5935,0.624,0.6575,0.6939,0.7333,0.7755,0.8206,0.8687,0.9196,0.9735,1.0303,1.09,1.1526,1.2181,1.2866,1.3579,1.4322,1.5093,1.5894,1.6724,1.7583,1.8471,1.9392,2.0181,2.0729,2.11,2.136,2.1575,2.181,2.213,2.2601,2.3289,2.4259,2.5576,2.7306,2.9515,3.2267,3.5628,3.9664,4.444,5.0022,5.6474,6.3864,7.2255,8.171,9.2345,10.4321,11.7802,13.2968,15.0022,16.9186,19.0706,21.4853,24.1923,27.224,30.6155,34.405,38.6331,43.3433,48.5815,54.3957,60.8355,67.9514,75.7938,84.4121,93.8531,104.1596,115.3685,127.5088,140.5995,154.6474,169.6451,185.569,202.378,220.0122,238.3932,257.424,276.9907,296.9648,317.2062,337.567,357.8957,378.042,397.8608,417.2163,435.986,454.0628,471.3574,487.7992,503.3364,517.9354,531.5796,544.2678,556.0123,566.8365,576.7731,1000)
GRM80 = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.7481,0.7552,0.7639,0.7741,0.7859,0.7993,0.8143,0.8309,0.849,0.8687,0.89,0.9128,0.9372,0.9633,0.9908,1.0202,1.0558,1.1032,1.1634,1.237,1.3251,1.4283,1.5477,1.684,1.838,2.0106,2.2027,2.415,2.6486,2.9041,3.1824,3.4844,3.8109,4.1628,4.5409,4.946,5.379,5.8408,6.3322,6.854,7.4071,7.9923,8.6104,9.2623,9.9693,10.7572,11.6353,12.6135,13.7031,14.9161,16.2662,17.7682,19.4386,21.2951,23.3574,25.647,28.1871,31.003,34.122,37.5735,41.3891,45.6023,50.2487,55.3658,60.9926,67.1696,73.938,81.3394,89.4152,98.2057,107.749,118.0801,129.2296,141.2224,154.0761,167.8,182.3929,197.8426,214.1242,231.1994,249.0158,267.5074,286.594,306.1831,326.171,346.4446,366.8841,387.3658,407.7649,427.9586,447.829,467.2659,486.1689,504.4494,522.0318,538.8543,554.8694,570.043,584.3546,597.7955,610.3683,622.085,1000)
GKF80 = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.994,1.006,1.018,1.03,1.042,1.055,1.067,1.079,1.091,1.103,1.116,1.128,1.14,1.152,1.164,1.177,1.189,1.201,1.213,1.225,1.238,1.25,1.262,1.276,1.299,1.34,1.398,1.477,1.577,1.7,1.847,2.021,2.222,2.452,2.712,3.005,3.331,3.691,4.089,4.525,5,5.516,6.094,6.706,7.382,8.13,8.958,9.872,10.882,11.998,13.231,14.591,16.093,17.749,19.575,21.587,23.803,26.242,28.925,31.873,35.111,38.662,42.555,46.817,51.476,56.565,62.113,68.153,74.718,81.839,89.548,97.876,106.85,116.496,126.836,137.888,149.663,162.167,175.397,189.325,203.986,219.296,235.235,251.753,268.791,286.281,304.144,322.298,340.651,359.109,377.576,395.955,414.15,432.072,449.633,466.757,483.372,499.417,514.842,529.606,543.677,557.036,1000)
GKM80 = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1.079,1.091,1.103,1.116,1.128,1.14,1.152,1.164,1.177,1.189,1.201,1.213,1.225,1.238,1.25,1.262,1.276,1.299,1.34,1.398,1.477,1.577,1.7,1.847,2.021,2.222,2.452,2.712,3.004,3.33,3.691,4.089,4.524,5,5.516,6.094,6.706,7.382,8.13,8.958,9.872,10.882,11.998,13.231,14.591,16.093,17.749,19.575,21.587,23.803,26.242,28.925,31.873,35.111,38.662,42.555,46.816,51.476,56.564,62.113,68.153,74.718,81.839,89.548,97.876,106.85,116.496,126.836,137.888,149.663,162.167,175.397,189.343,203.986,219.296,235.235,251.753,268.791,286.281,304.144,322.298,340.651,359.109,377.576,395.955,414.15,432.072,449.633,466.757,483.372,499.417,514.842,529.606,543.677,557.036,569.668,581.572,592.752,603.217,612.985,622.077,630.517,1000)
GRM95 = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1.2879,1.289,1.2902,1.2913,1.2924,1.2936,1.2947,1.2958,1.297,1.2981,1.2992,1.3004,1.3015,1.3026,1.3038,1.3057,1.3146,1.3325,1.3596,1.3965,1.4436,1.5014,1.571,1.6535,1.7501,1.8617,1.9896,2.1348,2.299,2.4855,2.6984,2.9414,3.2187,3.5338,3.8715,4.2176,4.5778,4.9576,5.3626,5.7985,6.2708,6.7851,7.347,7.9621,8.6361,9.3744,10.1828,11.0668,11.9579,12.8181,13.6967,14.64,15.6913,16.8912,18.2776,19.8861,21.7496,23.8892,26.2863,28.9139,31.7462,34.7587,37.9279,41.2316,44.6485,48.1587,51.743,55.3833,59.0624,62.7642,66.4732,70.175,73.8924,77.7907,82.0603,86.88,92.4166,98.8263,106.2543,114.5014,123.2765,132.5794,142.4102,152.769,163.6556,175.0702,187.0127,199.483,212.4813,226.0075,240.0615,254.6435,269.7534,285.3912,301.5569,318.2504,335.4719,353.2213,371.4986,390.3038,409.637,429.498,449.8869,470.8037,492.2484,514.2211,536.7216,559.75,583.3064,607.3906,632.0028,1000)
GRF95 = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.3179,0.3199,0.3219,0.3239,0.3259,0.3286,0.3424,0.3664,0.3953,0.4247,0.4541,0.4839,0.5143,0.5456,0.5783,0.6124,0.6485,0.6867,0.7274,0.7709,0.8174,0.8671,0.9192,0.973,1.0277,1.0822,1.136,1.188,1.2384,1.2904,1.3484,1.4163,1.4916,1.5698,1.6526,1.7417,1.8387,1.9453,2.0633,2.1941,2.3396,2.5014,2.6811,2.8805,3.1012,3.3448,3.5914,3.8417,4.1264,4.4735,4.9086,5.4484,6.0827,6.7954,7.5719,8.3984,9.2619,10.1507,11.0538,11.961,12.8778,13.8681,15.0041,16.352,17.9716,19.9171,22.2372,24.9755,28.1523,31.7134,35.5905,39.7196,44.0415,48.5011,53.0474,57.633,62.2144,66.8049,71.6261,76.9316,82.9524,89.6957,97.0253,104.9412,113.4435,122.5322,132.2071,142.4684,153.316,164.75,176.7703,189.3769,202.5699,216.3492,230.7148,245.6668,261.2051,277.3297,294.0407,311.338,329.2217,347.6916,366.748,386.3906,406.6196,427.4349,448.8366,470.8246,493.3989,516.5595,540.3065,1000)
FIN = (199,0,1000)
TEST = (98,0,0.05,1000)
SPAINPERM2000 = (0,26.7846,2.1132,1.5074,0.9754,0.9087,0.7162,0.6291,0.5478,0.4416,0.3952,0.4077,0.3208,0.3627,0.3534,0.3583,0.3766,0.4236,0.4811,0.5094,0.5359,0.5216,0.5315,0.4942,0.5058,0.5142,0.5111,0.5411,0.5811,0.5853,0.6213,0.6048,0.5977,0.5553,0.5234,0.5529,0.6324,0.6409,0.6331,0.6477,0.6392,0.7344,0.6776,0.7747,0.8119,0.8530,0.9197,0.9173,0.9841,0.9983,1.1737,1.3150,1.4560,1.4857,1.7040,1.7653,1.8616,1.8907,2.0703,2.2248,2.3472,2.5721,2.7313,2.9537,3.0638,3.2829,3.6204,3.9212,4.2317,4.5801,5.0495,5.4721,6.1110,6.7021,7.5592,8.4368,9.4458,10.6256,11.9844,13.3730,15.0130,17.1280,19.7247,22.1471,25.3717,29.4682,33.6982,37.9036,43.1518,48.5546,55.1153,62.7627,68.7645,79.5625,91.9339,107.1328,124.6729,144.9143,168.2791,195.2608,226.9151,260.9836,308.0680,329.1760,350.7650,372.8190,395.3310,418.3050,441.7560,468.9810,497.8840,528.5680,561.1430,595.7250,632.4390,671.4160,1000)
SPAININE2004 = (0,3.935,0.323,0.214,0.167,0.141,0.117,0.113,0.111,0.116,0.11,0.107,0.115,0.138,0.155,0.196,0.261,0.326,0.378,0.437,0.468,0.467,0.474,0.483,0.486,0.485,0.482,0.494,0.503,0.518,0.546,0.585,0.631,0.677,0.736,0.809,0.877,0.956,1.053,1.143,1.232,1.333,1.427,1.551,1.706,1.858,2.053,2.251,2.447,2.637,2.879,3.113,3.396,3.668,3.903,4.179,4.574,4.952,5.275,5.697,6.247,6.791,7.308,7.637,8.521,9.403,10.288,11.111,12.77,13.704,14.964,16.401,18.326,20.342,22.695,25.211,28.288,31.585,35.788,40.192,45.517,51.074,57.965,64.674,72.901,81.152,91.414,102.445,115.601,127.651,142.332,156.778,160.356,175.837,201.915,237.282,280.631,330.655,386.048,445.502,507.71,571.366,1000)
SPAININE2005 = (2.583791,0.508471,0.460709,0.430675,0.414095,0.402603,0.401485,0.401637,0.406583,0.402789,0.399976,0.408149,0.423926,0.436973,0.464055,0.517948,0.574353,0.615905,0.663226,0.687875,0.693000,0.703723,0.701644,0.704153,0.705664,0.705153,0.709204,0.714820,0.731303,0.747248,0.776918,0.810428,0.837414,0.881681,0.939679,0.991422,1.063405,1.166164,1.269737,1.354198,1.454751,1.559673,1.686756,1.843112,2.017662,2.224748,2.423707,2.630145,2.828441,3.096794,3.382685,3.695538,4.030610,4.334374,4.708664,5.151774,5.630567,6.038401,6.569489,7.151412,7.710619,8.318870,8.848244,9.750154,10.650585,11.628118,12.570646,14.079738,15.102284,16.146185,17.679584,19.585263,21.455168,23.417133,26.116740,28.580127,31.301970,34.651468,38.331617,42.363058,46.633814,51.472470,56.637311,62.146305,68.348696,75.354973,83.553689,91.973595,100.813746,110.061319,119.423813,125.759154,136.452986,151.647540,169.224154,188.708038,210.983462,234.076092,250.813155,278.171669,323.697196,366.598032,420.585061,482.189978,550.891054,609.209875,653.209714,698.176428,745.156923,807.109051,877.065598,957.230143,1000)

def get_TGHF05(gender):
    """
    gender: H for male and F for female
    generation: ex 1952
    """
    FR_TGHF05 = csv.reader(open(os.path.join(script_dir, 'tables/FR_TG' + gender + '05.csv'),'r'))
    res = None
    col_names = []
    for row in FR_TGHF05:
        if res==None:
            res = {}
            for col in row[1:]:
                res[col] = []
                col_names.append(col)
        else:
            col_index = 0
            for col in row[1:]:
                if len(col)>0:
                    val = float(col)
                else:
                    val = 100000.0
                res[col_names[col_index]].append(val)
                col_index += 1
    for col in col_names:
        res[col] = MortalityTable(l_x = res[col])
    return res
