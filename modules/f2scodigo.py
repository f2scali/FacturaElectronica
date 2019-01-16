# -*- coding: utf-8 -*-
class ObjCode128():
    """docstring for ObjCode128"""
    _patterns = {
        0   :   33,    1   :   34,    2   :   35,
        3   :   36,    4   :   37,    5   :   38,
        6   :   39,    7   :   40,    8   :   41,
        9   :   42,    10  :   43,    11  :   44,
        12  :   45,    13  :   46,    14  :   47,
        15  :   48,    16  :   49,    17  :   50,
        18  :   51,    19  :   52,    20  :   53,
        21  :   54,    22  :   55,    23  :   56,
        24  :   57,    25  :   58,    26  :   59,
        27  :   60,    28  :   61,    29  :   62,
        30  :   63,    31  :   64,    32  :   65,
        33  :   66,    34  :   67,    35  :   68,
        36  :   69,    37  :   70,    38  :   71,
        39  :   72,    40  :   73,    41  :   74,
        42  :   75,    43  :   76,    44  :   77,
        45  :   78,    46  :   79,    47  :   80,
        48  :   81,    49  :   82,    50  :   83,
        51  :   84,    52  :   85,    53  :   86,
        54  :   87,    55  :   88,    56  :   89,
        57  :   90,    58  :   91,    59  :   92,
        60  :   93,    61  :   94,    62  :   95,
        63  :   96,    64  :   97,    65  :   98,
        66  :   99,    67  :  100,    68  :   101,
        69  :  102,    70  :  103,    71  :   104,
        72  :  105,    73  :  106,    74  :   107,
        75  :  108,    76  :  109,    77  :   110,
        78  :  111,    79  :  112,    80  :   113,
        81  :  114,    82  :  115,    83  :   116,
        84  :  117,    85  :  118,    86  :   119,
        87  :  120,    88  :  121,    89  :   122,
        90  :  123,    91  :  124,    92  :   125,
        93  :  126,    94  :  161,    95  :   162,
        96  :  163,    97  :  164,    98  :   165,
        99  :  166,    100 :  167,    101 :   168,
        102 :  169,    103 :  170,    104 :   171,
        105 :  172,    106 :  173
    }

    seta = {
            ' ' :   0,        '!' :   1,        '"' :   2,        '#' :   3,
            '$' :   4,        '%' :   5,        '&' :   6,       '\'' :   7,
            '(' :   8,        ')' :   9,        '*' :  10,        '+' :  11,
            ',' :  12,        '-' :  13,        '.' :  14,        '/' :  15,
            '0' :  16,        '1' :  17,        '2' :  18,        '3' :  19,
            '4' :  20,        '5' :  21,        '6' :  22,        '7' :  23,
            '8' :  24,        '9' :  25,        ':' :  26,        ';' :  27,
            '<' :  28,        '=' :  29,        '>' :  30,        '?' :  31,
            '@' :  32,        'A' :  33,        'B' :  34,        'C' :  35,
            'D' :  36,        'E' :  37,        'F' :  38,        'G' :  39,
            'H' :  40,        'I' :  41,        'J' :  42,        'K' :  43,
            'L' :  44,        'M' :  45,        'N' :  46,        'O' :  47,
            'P' :  48,        'Q' :  49,        'R' :  50,        'S' :  51,
            'T' :  52,        'U' :  53,        'V' :  54,        'W' :  55,
            'X' :  56,        'Y' :  57,        'Z' :  58,        '[' :  59,
           '\\' :  60,        ']' :  61,        '^' :  62,        '_' :  63,
         '\x00' :  64,     '\x01' :  65,     '\x02' :  66,     '\x03' :  67,
         '\x04' :  68,     '\x05' :  69,     '\x06' :  70,     '\x07' :  71,
         '\x08' :  72,     '\x09' :  73,     '\x0a' :  74,     '\x0b' :  75,
         '\x0c' :  76,     '\x0d' :  77,     '\x0e' :  78,     '\x0f' :  79,
         '\x10' :  80,     '\x11' :  81,     '\x12' :  82,     '\x13' :  83,
         '\x14' :  84,     '\x15' :  85,     '\x16' :  86,     '\x17' :  87,
         '\x18' :  88,     '\x19' :  89,     '\x1a' :  90,     '\x1b' :  91,
         '\x1c' :  92,     '\x1d' :  93,     '\x1e' :  94,     '\x1f' :  95,
         '\xf3' :  96,     '\xf2' :  97,    'SHIFT' :  98,     'TO_C' :  99,
         'TO_B' : 100,     '\xf4' : 101,     '\xf1' : 102
    }

    setb = {
            ' ' :   0,        '!' :   1,        '"' :   2,        '#' :   3,
            '$' :   4,        '%' :   5,        '&' :   6,       '\'' :   7,
            '(' :   8,        ')' :   9,        '*' :  10,        '+' :  11,
            ',' :  12,        '-' :  13,        '.' :  14,        '/' :  15,
            '0' :  16,        '1' :  17,        '2' :  18,        '3' :  19,
            '4' :  20,        '5' :  21,        '6' :  22,        '7' :  23,
            '8' :  24,        '9' :  25,        ':' :  26,        ';' :  27,
            '<' :  28,        '=' :  29,        '>' :  30,        '?' :  31,
            '@' :  32,        'A' :  33,        'B' :  34,        'C' :  35,
            'D' :  36,        'E' :  37,        'F' :  38,        'G' :  39,
            'H' :  40,        'I' :  41,        'J' :  42,        'K' :  43,
            'L' :  44,        'M' :  45,        'N' :  46,        'O' :  47,
            'P' :  48,        'Q' :  49,        'R' :  50,        'S' :  51,
            'T' :  52,        'U' :  53,        'V' :  54,        'W' :  55,
            'X' :  56,        'Y' :  57,        'Z' :  58,        '[' :  59,
           '\\' :  60,        ']' :  61,        '^' :  62,        '_' :  63,
            '`' :  64,        'a' :  65,        'b' :  66,        'c' :  67,
            'd' :  68,        'e' :  69,        'f' :  70,        'g' :  71,
            'h' :  72,        'i' :  73,        'j' :  74,        'k' :  75,
            'l' :  76,        'm' :  77,        'n' :  78,        'o' :  79,
            'p' :  80,        'q' :  81,        'r' :  82,        's' :  83,
            't' :  84,        'u' :  85,        'v' :  86,        'w' :  87,
            'x' :  88,        'y' :  89,        'z' :  90,        '{' :  91,
            '|' :  92,        '}' :  93,        '~' :  94,     '\x7f' :  95,
         '\xf3' :  96,     '\xf2' :  97,    'SHIFT' :  98,     'TO_C' :  99,
         '\xf4' : 100,     'TO_A' : 101,     '\xf1' : 102
    }

    setc = {
        '00': 0, '01': 1, '02': 2, '03': 3, '04': 4,
        '05': 5, '06': 6, '07': 7, '08': 8, '09': 9,
        '10':10, '11':11, '12':12, '13':13, '14':14,
        '15':15, '16':16, '17':17, '18':18, '19':19,
        '20':20, '21':21, '22':22, '23':23, '24':24,
        '25':25, '26':26, '27':27, '28':28, '29':29,
        '30':30, '31':31, '32':32, '33':33, '34':34,
        '35':35, '36':36, '37':37, '38':38, '39':39,
        '40':40, '41':41, '42':42, '43':43, '44':44,
        '45':45, '46':46, '47':47, '48':48, '49':49,
        '50':50, '51':51, '52':52, '53':53, '54':54,
        '55':55, '56':56, '57':57, '58':58, '59':59,
        '60':60, '61':61, '62':62, '63':63, '64':64,
        '65':65, '66':66, '67':67, '68':68, '69':69,
        '70':70, '71':71, '72':72, '73':73, '74':74,
        '75':75, '76':76, '77':77, '78':78, '79':79,
        '80':80, '81':81, '82':82, '83':83, '84':84,
        '85':85, '86':86, '87':87, '88':88, '89':89,
        '90':90, '91':91, '92':92, '93':93, '94':94,
        '95':95, '96':96, '97':97, '98':98, '99':99,

        'TO_B' : 100,    'TO_A' : 101,    '\xf1' : 102
    }

    starta, startb, startc, stop = 103, 104, 105, 106

    setmap = {
        'TO_A' : (seta, setb),
        'TO_B' : (setb, seta),
        'TO_C' : (setc, None),
        'START_A' : (starta, seta, setb),
        'START_B' : (startb, setb, seta),
        'START_C' : (startc, setc, None),
    }
    cStarts = ('START_C','TO_A','TO_B')
    tos = list(setmap.keys())
    def __init__(self,valor):
        self.valor = valor

    def Procesar(self):
        salida ='{}{}'.format(chr(self._patterns[self.startc]),chr(169))    
        calculo= 102
        pos = 2

        codigo=self.valor.replace("(","")
        codigo=codigo.replace(")","")


        for indice in range(0,len(codigo),2):
            valor = int(codigo[indice:indice+2])
            calculo+=valor * pos
            salida += '{}'.format(chr(self._patterns[valor]))
            pos +=1 
        digchk = calculo % 103
        salida += '{}'.format(chr(self._patterns[digchk]))
        return salida.decode('cp437')
        