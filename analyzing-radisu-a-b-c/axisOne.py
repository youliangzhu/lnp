import xml.etree.cElementTree as ET
from io import StringIO
import sys
from joblib import Parallel, delayed
import time
from sympy import *
import os

sys.setrecursionlimit(100000)  # 例如这里设置为十万

class XMLs:
    def __init__(self, file_name=None):
        self.all_beads_point = None
        self.root = ET.parse(file_name)
        self.filename = file_name

    @staticmethod
    def __gain_config(root):
        gala_node = root.getroot()
        configuration = list(gala_node)[0]
        return configuration

    def __get_one_title_node(self, title):
        return self.__gain_config(self.root).find(title)

    def __record_all_bead_point_and_index(self):
        self.all_beads_point = []
        t = self.__get_one_title_node('type')
        p = self.__get_one_title_node('position')
        t_IO = StringIO(t.text)
        p_IO = StringIO(p.text)
        t_IO.readline()
        p_IO.readline()

        n = int(p.attrib['num'])
        k = 0
        while k < n:
            t_l = t_IO.readline()
            p_l = p_IO.readline()
            t_l = t_l.replace('\n', '')
            trans_p_l = []
            if t_l not in exclude:
                p_l = p_l.replace('\n', '').split(' ')
                for p_i in p_l:
                    if p_i:
                        trans_p_l.append(float(p_i))
                trans_p_l.append(k)
                trans_p_l.append(t_l)
                self.all_beads_point.append(trans_p_l)
            k += 1

    @staticmethod
    def axis(pos):
        x = 0
        y = 0
        z = 0
        for i in range(len(pos)):
            x = x + pos[i][0]
            y = y + pos[i][1]
            z = z + pos[i][2]

        xcm = x / len(pos)
        ycm = y / len(pos)
        zcm = z / len(pos)

        nsxx = 0
        nsxy = 0
        nsxz = 0
        nsyx = 0
        nsyy = 0
        nsyz = 0
        nszx = 0
        nszy = 0
        nszz = 0
        # nrg = 0
        for j in range(len(pos)):
            a = pos[j][0]
            b = pos[j][1]
            c = pos[j][2]
            nsxx = nsxx + (a - xcm) * (a - xcm)
            nsxy = nsxy + (a - xcm) * (b - ycm)
            nsxz = nsxz + (a - xcm) * (c - zcm)
            nsyx = nsyx + (b - ycm) * (a - xcm)
            nsyy = nsyy + (b - ycm) * (b - ycm)
            nsyz = nsyz + (b - ycm) * (c - zcm)
            nszx = nszx + (c - zcm) * (a - xcm)
            nszy = nszy + (c - zcm) * (b - ycm)
            nszz = nszz + (c - zcm) * (c - zcm)
            # rx = a - xcm
            # ry = b - ycm
            # rz = c - zcm
            # rg = rx ** 2 + ry ** 2 + rz ** 2
            # nrg = nrg + rg
        sxx = nsxx / len(pos)
        sxy = nsxy / len(pos)
        sxz = nsxz / len(pos)
        syx = nsyx / len(pos)
        syy = nsyy / len(pos)
        syz = nsyz / len(pos)
        szx = nszx / len(pos)
        szy = nszy / len(pos)
        szz = nszz / len(pos)
        # rg2 = nrg / len(pos)
        # rg = rg2 ** (0.5)
        M = Matrix([[sxx, sxy, sxz], [syx, syy, syz], [szx, szy, szz]])

        # print("计算矩阵的对角化矩阵")
        P, D = M.diagonalize()
        return D

    def run(self):
        self.__record_all_bead_point_and_index()
        box = self.__get_one_title_node("box")
        lx = float(box.attrib["lx"])
        ly = float(box.attrib["ly"])
        lz = float(box.attrib["lz"])
        self.box = [lx, ly, lz]

        G1 = 0
        for i in self.all_beads_point:
            if i[-1] == 'G':
                G1 = i
                break

        new_all = []
        for i in self.all_beads_point:
            dx = i[0] - G1[0]
            dy = i[1] - G1[1]
            dz = i[2] - G1[2]

            dx -= self.box[0] * round(dx / self.box[0])
            dy -= self.box[1] * round(dy / self.box[1])
            dz -= self.box[2] * round(dz / self.box[2])

            new_all.append([dx, dy, dz])

        D = self.axis(new_all)
        D1 = [D[0], D[4], D[8]]
        D1 = sorted(D1)
        return self.__gain_config(self.root).attrib["time_step"], D1

def data_extract_function(f_i, f_k):
    print(f_i, f_k)
    xml = XMLs(f_i)
    return xml.run()

def separate_file(filepath):
    files = []
    for file_name in os.listdir(filepath):
        if file_name.startswith('particles.') and file_name.endswith('.xml'):
            input_path = os.path.join(filepath, file_name)
            files.append(input_path)
    return files

if __name__ == '__main__':
    start_time = time.time()

    # file_l = sys.argv[1:]
    file_l = separate_file(r"D:\draft_box\puzzle\puzzle36\translocation\tran-soft")

    exclude = ['W']

    # file_l = [
    #     r"D:\draft_box\puzzle\puzzle36\translocation\tran-hard\particles.0000200000.xml"
    # ]

    # n_jobs ： cpu一次调用几核
    Back_Value = Parallel(n_jobs=1)(
        [delayed(data_extract_function)(f_i, k) for k, f_i in enumerate(file_l)])
    print(Back_Value)
    # put log
    with open("axisOne.log", "w") as Wfile:
        Wfile.write("timeStep" + "\t" + "c" + "\t" + "b" + "\t" + "a" + "\n")
        for i in Back_Value:
            Wfile.write(i[0] + "\t" + str(i[1][0]) + "\t" + str(i[1][1]) + "\t" + str(i[1][2]) + "\n")
    print('程序运作持续时间： ', time.time() - start_time)
