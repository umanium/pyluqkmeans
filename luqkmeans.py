# kmeans class for data

import sys, math, random, luqdataprovider as prv, matplotlib.pyplot as plt, matplotlib.image as mpimg

class Data:
    'tipe data untuk data yg digunakan; berupa array'
    def __init__(self, arr) :
        self.arr = arr
        self.n = len(arr)
        self.cluster = -1
    def __repr__(self):
        return str(self.arr)
    def __len__(self):
        return len(self.arr)
    def setData(self, arr):
        self.arr = arr
    def getData(self, idx):
        return self.arr[idx]
    def getCluster(self):
        return self.cluster
    def printDataWithCluster(self):
        print "data: %r, cluster %d" % (self.arr, self.cluster)
    def setCluster(self, c):
        self.cluster = c

class Cluster:
    'tipe data untuk cluster; terdiri dari centroid dan method-method lain'
    def __init__(self, centroid) :
        self.data = []
        self.centroid = centroid #tipe datanya Data !!
        self.n = len(centroid)
    def __repr__(self):
        return str(self.centroid)
    def getCentroid(self, idx):
        return self.centroid.getData(idx)
    def generateCentroid(self):
        sum_data = lambda i: reduce(lambda x,p: x + p.arr[i], self.data, 0.0)
        temp_centroid = []
        if len(self.data) > 0:
            for i in range(self.n):
                temp_centroid.append(sum_data(i)/len(self.data))
            self.centroid = Data(temp_centroid)
    def resetData(self): # mereset data di cluster sekaligus menghitung jarak centroid sekarang dari yang lalu    
        old_centroid = self.centroid
        self.generateCentroid()
        self.data = []
        return euclidanDistance(old_centroid, self.centroid)
    def addData(self, data):
        self.data.append(data)
    def printData(self):
        print(self.data)
    def isGreaterThan(self,clust):
        # hitung kuantitas masing2
        qty1 = 0
        qty2 = 0
        for i in range(self.n) :
            qty1 = qty1 + self.getCentroid(i)
            qty2 = qty2 + clust.getCentroid(i)
            if qty1 > qty2:
                return True
            else:
                return False

def euclidanDistance(a, b): # menghitung euclidan distance dari dua data
    if a.n != b.n: raise Exception("data tidak dapat dibandingkan; dimensinya berbeda")
    square = reduce(lambda x,y: x + pow((a.arr[y]-b.arr[y]), 2), range(a.n), 0.0)
    return math.sqrt(square)

def kMeans(data, k, eps):
    # data: array of Data; k: jumlah cluster; eps: epsilon, pergeseran terkecil
    init_centroid = random.sample(data, k)
    clusters = []
    for i in range(k):    
        clusters.append(Cluster(init_centroid[i]))

    indx = 0;
    # mulai iterasi
    while True:
        indx = indx+1

        print "iterasi %d: mulai, iterasi terhadap %d data" % (indx, len(data))
        # alokasi masing-masing data kepada clusternya masing-masing
        for d in data:
            min_dist = -1
            clust_class = -1
            for cl_num in range(k):
                cur_dist = euclidanDistance(d, clusters[cl_num].centroid)        
                if min_dist == -1:
                    min_dist = cur_dist
                    clust_class = cl_num
                if cur_dist < min_dist:
                    min_dist = cur_dist
                    clust_class = cl_num
            d.setCluster(clust_class)
            clusters[clust_class].addData(d)
        print "iterasi %d: fase 1 selesai" % indx

        # mereset seluruh cluster (sekalian menghitung perpindahannya)
        max_dist = 0.0
        for num in range(k):
            cur_dist = clusters[num].resetData()
            print("cluster %d delta nya %f." % (num, cur_dist))
            max_dist = max(max_dist, cur_dist)
        print "iterasi %d: fase 2 selesai" % indx
        if max_dist < eps:
            break
    print "total iterasi: %d" % indx
    return clusters

def convertData(input_arr):
    # input_arr berupa array of array [[2, 3, 4, 5], [1, 2, 3, 4]] dst
    result = []
    if len(input_arr) == 0: # cek apakah kosong
        raise Exception("input kosong")
    arr_n = len(input_arr[0])
    if arr_n == 0: # cek apakah isi data nya kosong
        raise Exception("data tidak valid")
    for arr in input_arr: # cek apakah panjang data nya seragam
        if len(arr) != arr_n:
            raise Exception("dimensi data tidak seragam")
        result.append(Data(arr))

    return result
  
def plotData(data_arr, clust):
    colors = ['gx', 'bx', 'rx', 'cx', 'mx', 'yx', 'kx', 'wx']
    color_clusters = ['go', 'bo', 'ro', 'co', 'mo', 'yo', 'ko', 'wo']
    for dt in data_arr:
        plt.plot(dt.getData(0), dt.getData(1), colors[dt.getCluster()])
    for i in range(len(clust)):
        plt.plot(clust[i].getCentroid(0), clust[i].getCentroid(1), color_clusters[i])
    plt.show()
  
# main
test = prv.provideRandomData(100,2,0,10)
#img = mpimg.imread('Firefox_wallpaper.png')
#plt.imshow(img)
print("loading image....")
imagedata = prv.provideImageData('stop.png')
nordata = prv.normalizeImage(imagedata)
#plt.imshow(nordata)
imagedata_used = convertData(imagedata[0])
#print(test)
print("converting data...")
data_used = convertData(test)

print("clustering data...")
clust = kMeans(imagedata_used, 2, 0.01)
#ubah image

clr1 = [0., 0., 0., 1.]
clr2 = [1., 1., 1., 1.]

if clust[0].isGreaterThan(clust[1]):
    clr1, clr2 = clr2, clr1

data_after_converted = []
for dt in imagedata_used:
    cur_clust = dt.getCluster()

    if cur_clust == 0:
        data_after_converted.append(clr1)
    else:
        data_after_converted.append(clr2)

data_clustered = [data_after_converted, imagedata[1], imagedata[2]]
image_clustered = prv.normalizeImage(data_clustered)
# print(str(image_clustered))
plt.imshow(image_clustered)

print("clustering finished.")
plt.show()
#print(a,b,c)
#print "hasil clustering: %r" % clust
#for dt in data_used:
#  dt.printDataWithCluster()
#plotData(data_used, clust)

#next:
#bikin randomisasi data
#test kmeans nya bener apa engga
#bikin modul buat masukin dari file ext ke data

