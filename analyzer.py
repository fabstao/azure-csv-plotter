# ********************************************************
#
#   (C) 2021 Rackspace, fabian.salamanca@rackspace.com
#
# ********************************************************

import pandas as pd
import sys,glob,ntpath,os
import matplotlib.pyplot as plt

if len(sys.argv) < 2:
    print("ERROR: Usage: " + sys.argv[0] + " <path>")
    sys.exit(1)

class GraphCsv: 
	def __init__(self):
		pass

	def generateG(self, data, nombre, metrics, namespaces):
		"""Use Pandas to retrieve data from Azure Monitor CSV

		Arguments:
		data -- Pandas DataFrame
		nombre -- filename with full path

		Return value:
		Null

		This function will output PDF files with plot from CSVs
		"""

		print("\nGenerating PDFs\n")
		for ns in namespaces:
			print(ns+" for: "+nombre)
			midf=data.loc[data['Namespace']==ns,'TimeStamp':'Type'] 
			print(midf)

			for metric in metrics: 
				miy = "Total"
				if metric == "BlobCapacity" or metric == "TableCapacity":
					miy = "Average"
				specifdf=midf.loc[midf['Type']==metric,['TimeStamp',miy]]
				lineo=specifdf.plot.line(x="TimeStamp", y=miy,by='TimeStamp')
				fig=lineo.get_figure()
				fig.savefig(os.path.splitext(nombre)[0]+ns+metric+'.pdf')

def cleanPath(path):
	# Clean path from full filename
	head, tail = ntpath.split(path)
	return tail or ntpath.basename(head)

path=sys.argv[1]
lista=glob.glob(path+"/*.csv")
migraph = GraphCsv()
namespaces = ["Blob","Table"]
metrics = ["Ingress", "Egress", "Transactions", "BlobCapacity", "TableCapacity"]

for i in lista:
	print("Executing "+i)
	data = pd.read_csv(path+"/"+i,header=0)
	data = data[['TimeStamp','Average','Total','Type','Namespace']]
	nombre=cleanPath(i)
	migraph.generateG(data, nombre, metrics, namespaces)

