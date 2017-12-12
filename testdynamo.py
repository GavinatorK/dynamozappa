import boto3
from boto3.dynamodb.conditions import Key, Attr
# Get the service resource.
#dynamodb = boto3.client('dynamodb',region_name='us-east-1')

class DynamoHelper(object):
    def __init__(self, region_name='us-east-1'):
        self.ddb=boto3.resource('dynamodb',region_name='us-east-1')
        self.client=boto3.client('dynamodb',region_name='us-east-1')


    def createTable(self,tableName, KeySchema=None, test=False):

        # Create the DynamoDB table.
        # KeySchema is a list of dictionaries
        if test:
            table = self.ddb.create_table(
                TableName=tableName,
                KeySchema=[
                    {
                        'AttributeName': 'username',
                        'KeyType': 'HASH'
                    }
                    #,
                    # {
                    #     'AttributeName': 'last_name',
                    #     'KeyType': 'RANGE'
                    # }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'username',
                        'AttributeType': 'S'
                    },
                    # ,
                    # {
                    #     'AttributeName': 'last_name',
                    #     'AttributeType': 'S'
                    # },

                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )

        else:
            table = self.ddb.create_table(
                TableName=tableName,
                KeySchema=keySchema
                )
        # Wait until the table exists.
        table.meta.client.get_waiter('table_exists').wait(TableName=tableName)

        # Print out some data about the table.
        print(table.item_count)

    def getTableCreationDate(self,tableName):
        table=self.ddb.Table(tableName)
        return table.creation_date_time

    def createItem(self,tableName, item):
        # Item is a dictionary with field:value
        table=self.ddb.Table(tableName)
        table.put_item(Item=item)

    def getItem(self,tableName, key):
        # key is a dictionary with primaryKey: val, Rangekey:Val
        table=self.ddb.Table(tableName)
        response=table.get_item(Key=key)
        print "response is "+str(response)
        if "Item" in response:
            return response['Item']
        else:
            return None


    def updateItem(self,tableName, key, updateExpression, expressionAttributeValues):

        # key is dictionary with primary:val, RangeKey: value
        # updateExpression is a string ex: 'SET age = :val1', age is one of fields in the KeySchema
        # ExpressionAttributeValues is a dictionary to pass values for updateExpression ex: :val1=26
        table=self.ddb.Table(tableName)
        table.update_item(
        Key=key,
        UpdateExpression=updateExpression,
        ExpressionAttributeValues=expressionAttributeValues
    )

    def deleteItem(self,tableName, key):
        # key is dictionary with primary:val, RangeKey: value
        table=self.ddb.Table(tableName)
        table.delete_item(Key=key)

    def deleteTable(self,tableName):
        table=self.ddb.Table(tableName)
        table.delete()

    def listTables(self):
        # returns a list of tables
        return self.client.list_tables()['TableNames']

    def scanTable(self, tableName, FilterExpression):
        # use this method to query on non-key Attributes
        # 'ComparisonOperator': 'EQ'|'NE'|'IN'|'LE'|'LT'|'GE'|'GT'|'BETWEEN'|'NOT_NULL'|'NULL'|'CONTAINS'|'NOT_CONTAINS'|'BEGINS_WITH'
        #  ConditionalOperator='AND'|'OR'
        #FilterExpression=Attr('first_name').begins_with('J') & Attr('account_type').eq('super_user')
        table=self.ddb.Table(tableName)
        response = table.scan(FilterExpression=eval(FilterExpression))
        items = response['Items']
        return items
