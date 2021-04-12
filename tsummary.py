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

	def generateG(self,data,nombre):
		"""Use Pandas to retrieve data from Azure Monitor CSV

		Arguments:
		data -- Pandas DataFrame
		nombre -- Name for output PDF file

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

	def tsummary(self,data,nombre):
		"""Use Pandas to summarize data from Azure Monitor CSV

		Arguments:
		data -- Pandas DataFrame
		nombre -- Name for output PDF file

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
		miblobingress=miblobingress.nlargest(30,'Total')
		xappend.append_df_to_excel(nombre+"_summ.xlsx", miblobingress, sheet_name="Blob Ingress")

		# Egress

		miblobegress=miblob.loc[data['Type']=="Egress",'TimeStamp':'Total'] 
		miblobegress=miblobegress.nlargest(30,'Total')
		xappend.append_df_to_excel(nombre+"_summ.xlsx", miblobegress, sheet_name="Blob Egress")

		# Transactions

		miblobtrans=miblob.loc[data['Type']=="Transactions",'TimeStamp':'Total'] 
		miblobtrans=miblobtrans.nlargest(30,'Total')
		xappend.append_df_to_excel(nombre+"_summ.xlsx", miblobtrans, sheet_name="Blob Transactions")

		# BlobCapacity

		miblobbcap=miblob.loc[data['Type']=="BlobCapacity",'TimeStamp':'Average'] 
		miblobbcap=miblobbcap.nlargest(30,'Average')
		xappend.append_df_to_excel(nombre+"_summ.xlsx", miblobbcap, sheet_name="Blob Capacity")

		# TABLEs

		print("\nTABLE"+nombre)
		print(data.loc[data['Namespace']=="Table",'TimeStamp':'Type'])
		mitable=data.loc[data['Namespace']=="Table",'TimeStamp':'Type']

		# Ingress

		mitableingress=mitable.loc[data['Type']=="Ingress",'TimeStamp':'Total'] 
		mitableingress=mitableingress.nlargest(30,'Total')
		xappend.append_df_to_excel(nombre+"_summ.xlsx", mitableingress, sheet_name="Table Ingress")

		# Egress

		mitableegress=mitable.loc[data['Type']=="Egress",'TimeStamp':'Total'] 
		mitableegress=mitableegress.nlargest(30,'Total')
		xappend.append_df_to_excel(nombre+"_summ.xlsx", mitableegress, sheet_name="Table Egress")

		# Transactions

		mitabletrans=mitable.loc[data['Type']=="Transactions",'TimeStamp':'Total'] 
		mitabletrans=mitabletrans.nlargest(30,'Total')
		xappend.append_df_to_excel(nombre+"_summ.xlsx", mitabletrans, sheet_name="Table Transactions")

		# TableCapacity

		mitabletcap=mitable.loc[data['Type']=="TableCapacity",'TimeStamp':'Average'] 
		mitabletcap=mitabletcap.nlargest(30,'Average')
		xappend.append_df_to_excel(nombre+"_summ.xlsx", mitabletcap, sheet_name="Table Capacity")

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
migraph.tsummary(data,nombre)
