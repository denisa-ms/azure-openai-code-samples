from promptflow import tool
#import Custom Connection
from promptflow.connections import CustomConnection 
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.kusto.data.exceptions import KustoServiceError
from azure.kusto.data.helpers import dataframe_from_result_table

@tool
def vectordb_search(embedded_query: str,con: CustomConnection, distance: float) -> str:
  # Connect to adx using AAD app registration
  client = KustoClient(con.kusto_conn)
  kusto_db = con.kusto_db
  nr_of_answers = 3
  searchedEmbedding = embedded_query
  kusto_query = con.kusto_table + " | extend similarity = series_cosine_similarity(dynamic("+str(searchedEmbedding)+"), description_embedding) | top " + str(nr_of_answers) + " by similarity desc "
  response = client.execute(kusto_db, kusto_query)
  results=[]
  for row in response.primary_results[0]:
      results.append({'id': row['nr'],'name': row['name'], 'description': row['description']})
  return results
