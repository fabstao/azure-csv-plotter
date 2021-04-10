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

	def generateG(self,data,nombre):
		"""Use Pandas to retrieve data from Azure Monitor CSV

		Arguments:
		data -- Pandas DataFrame
		nombre -- filename with full path

		Return value:
		Null

		This function will output PDF files with plot from CSVs
		"""

		# BLOBs

		print("BLOB for: "+nombre)
		print(data.loc[data['Namespace']=="Blob",'TimeStamp':'Type'])
		miblob=data.loc[data['Namespace']=="Blob",'TimeStamp':'Total'] 

		# Ingress

		miblobingress=miblob.loc[data['Type']=="Ingress",['TimeStamp','Total']] 
		lineo=miblobingress.plot.line(x="TimeStamp",y="Total",by='TimeStamp')
		fig=lineo.get_figure()
		fig.savefig(os.path.splitext(nombre)[0]+'_ingress_blob.pdf')

		# Egress

		miblobegress=miblob.loc[data['Type']=="Egress",'TimeStamp':'Total'] 
		lineo=miblobegress.plot.line(x="TimeStamp",y="Total",by='TimeStamp')
		fig=lineo.get_figure()
		fig.savefig(os.path.splitext(nombre)[0]+'_egress_blob.pdf')

		# Transactions

		miblobtrans=miblob.loc[data['Type']=="Transactions",'TimeStamp':'Total'] 
		lineo=miblobtrans.plot.line(x="TimeStamp",y="Total",by='TimeStamp')
		fig=lineo.get_figure()
		fig.savefig(os.path.splitext(nombre)[0]+'_trans_blob.pdf')

		# BlobCapacity

		miblobbcap=miblob.loc[data['Type']=="BlobCapacity",'TimeStamp':'Average'] 
		lineo=miblobbcap.plot.line(by='TimeStamp')
		fig=lineo.get_figure()
		fig.savefig(os.path.splitext(nombre)[0]+'_bcap_blob.pdf')

		# TABLEs

		print("\nTABLE"+nombre)
		print(data.loc[data['Namespace']=="Table",'TimeStamp':'Type'])
		mitable=data.loc[data['Namespace']=="Table",'TimeStamp':'Type']

		# Ingress

		mitableingress=mitable.loc[data['Type']=="Ingress",'TimeStamp':'Total'] 
		lineo=mitableingress.plot.line(x="TimeStamp",y="Total",by='TimeStamp')
		fig=lineo.get_figure()
		fig.savefig(os.path.splitext(nombre)[0]+'_ingress_table.pdf')

		# Egress

		mitableegress=mitable.loc[data['Type']=="Egress",'TimeStamp':'Total'] 
		lineo=mitableegress.plot.line(x="TimeStamp",y="Total",by='TimeStamp')
		fig=lineo.get_figure()
		fig.savefig(os.path.splitext(nombre)[0]+'_egress_table.pdf')

		# Transactions

		mitabletrans=mitable.loc[data['Type']=="Transactions",'TimeStamp':'Total'] 
		lineo=mitabletrans.plot.line(x="TimeStamp",y="Total",by='TimeStamp')
		fig=lineo.get_figure()
		fig.savefig(os.path.splitext(nombre)[0]+'_trans_table.pdf')

		# TableCapacity

		mitabletcap=mitable.loc[data['Type']=="TableCapacity",'TimeStamp':'Average'] 
		lineo=mitabletcap.plot.line(by='TimeStamp')
		fig=lineo.get_figure()
		fig.savefig(os.path.splitext(nombre)[0]+'_tcap_table.pdf')

#def cleanPath(path):
	# Clean path from full filename
#	head, tail = ntpath.split(path)
#	return tail or ntpath.basename(head)

path=sys.argv[1]
lista=glob.glob(path+"/*.csv")
migraph = GraphCsv()
maindict = { "TimeStamp" : [],
			"Average": [],
			"Total": [],
			"Type": [],
			"Namespace": []
		}

print(lista)
for i in lista:
	print("Executing: "+i)
	data = pd.read_csv(path+"/"+i,header=0)
	data = data[['TimeStamp','Average','Total','Type','Namespace']]
	maindf=pd.DataFrame(maindict)
	maindf=maindf.append(data)

print(maindf.nlargest(40,['Average','Total']))
nombre="Storage_summary"
migraph.generateG(data,nombre)
