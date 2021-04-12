# ********************************************************
#
#   (C) 2021 Rackspace, fabian.salamanca@rackspace.com
#
# ********************************************************

import pandas as pd
import sys,glob,ntpath,os
import matplotlib.pyplot as plt
import xappend

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
		nombre -- Name for output PDF file

		Return value:
		Null

		This function will output PDF files with plot from CSVs
		"""
		print("\nGenerating PDFs\n")
		for ns in namespaces:
			print(ns+" for: "+nombre)
			midf=data.loc[data['Namespace']==ns,'TimeStamp':'Name'] 
			print(midf)

			for metric in metrics: 
				miy = "Total"
				if metric == "BlobCapacity" or metric == "TableCapacity":
					miy = "Average"
				specifdf=midf.loc[midf['Type']==metric,['TimeStamp',miy]]
				lineo=specifdf.plot.line(x="TimeStamp", y=miy,by='TimeStamp')
				fig=lineo.get_figure()
				fig.savefig(os.path.splitext(nombre)[0]+ns+metric+'.pdf')


	def tsummary(self,data,nombre, metrics, namespaces):
		"""Use Pandas to summarize data from Azure Monitor CSV

		Arguments:
		data -- Pandas DataFrame
		nombre -- Name for output PDF file

		Return value:
		Null

		This function will output PDF files with plot from CSVs
		"""

		for ns in namespaces:
			print(ns+" for: "+nombre)
			print(data.loc[data['Namespace']==ns,'TimeStamp':'Name'])
			midf=data.loc[data['Namespace']==ns,'TimeStamp':'Name']  

			for metric in metrics:
				miy = "Total"
				if metric == "BlobCapacity" or metric == "TableCapacity":
					miy = "Average"
				if not (( ns == "Blob" and metric == "TableCapacity" ) or  ( ns == "Table" and metric == "BlobCapacity" )):
					specifdf=midf.loc[midf['Type']==metric,['TimeStamp', miy, 'Name']]
					specifdf=specifdf.nlargest(30,miy)
					xappend.append_df_to_excel(nombre+"_summ.xlsx", specifdf, sheet_name=ns +" "+ metric)


path=sys.argv[1]
lista=glob.glob(path+"/*.csv")
migraph = GraphCsv()
maindict = { "TimeStamp" : [],
			"Average": [],
			"Total": [],
			"Type": [],
			"Namespace": [],
			"Name": []
		}

maindf=pd.DataFrame(maindict)
for i in lista:
	print("Executing: "+i)
	fname = os.path.splitext(i)[0]
	data = pd.read_csv(path+"/"+i,header=0)
	data = data[['TimeStamp','Average','Total','Type','Namespace']]
	data.loc[:, 'Name'] = pd.Series(data=fname,index=data.index)
	maindf=maindf.append(data)


print("Main DataFrame:")
print(maindf.nlargest(40,['Average','Total']))
nombre="Storage_summary"
namespaces = ["Blob","Table"]
metrics = ["Ingress", "Egress", "Transactions", "BlobCapacity", "TableCapacity"]
migraph.generateG(maindf,nombre,metrics,namespaces)
migraph.tsummary(maindf,nombre,metrics,namespaces)
