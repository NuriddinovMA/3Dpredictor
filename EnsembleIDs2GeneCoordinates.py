from pybiomart import Dataset, Server
import  pandas as pd
import logging

input_file = "input/GSE95111_genes.fpkm_table.txt"
inp_data = pd.read_csv(input_file,delimiter="\t")
inp_data["Gene_ID"] = inp_data["tracking_id"].apply(lambda x: x.split(".")[0])

server = Server(host='http://www.ensembl.org')
mart = server['ENSEMBL_MART_ENSEMBL']
dataset = mart["mmusculus_gene_ensembl"]

query = dataset.query(attributes=['ensembl_gene_id',
                          'start_position',
                          'end_position',
                          'external_gene_name',
                          'chromosome_name'],
                        )

FinalData = pd.merge(left=inp_data,right=query,how="inner",
                     left_on="Gene_ID",right_on="Gene stable ID",
                     validate="1:1")

if len(FinalData) != len(inp_data):
    logging.getLogger(__name__).warning("Some data missing in Ensemble, "+str(len(inp_data)-len(FinalData)) + " out of "+str(len(inp_data)))

FinalData.to_csv(input_file+"pre.txt",sep="\t",index=False)