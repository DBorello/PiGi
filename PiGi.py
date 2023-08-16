import boto3
from uuid import getnode
import time

DELAY_BETWEEN_DB_ATTEMPTS = 10
DELAY_BETWEEN_DB_SUCCESS = 30

class PiGi:

    def __init__(self):
        # Get devices MAC address
        self.mac = hex(getnode())[2:]
        print('Device MAC: {}'.format(self.mac))

        self.value = -1

        # Enter main loop
        self.main()

    def main(self):
        while True:
            self.get_value()

            time.sleep(DELAY_BETWEEN_DB_ATTEMPTS)

    def get_value(self):
        try:
            # Connect to database
            dynamo_client  =  boto3.resource(service_name = 'dynamodb',region_name = 'us-east-2',
                        aws_access_key_id = 'AKIA4WTCSRYNTMBKC5GC',
                        aws_secret_access_key = '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')
            table = dynamo_client.Table('PiGi')

            # Fetch value
            r = table.get_item(Key = {'mac':self.mac})
            if 'Item' in r.keys():
                self.value = r['Item']['value']
                print(self.value)
            else:
                print('Error == MAC address not in database!')

        except:
            print('ERROR == Unable to connect to database')
            return False

if __name__ == "__main__":
    PiGi()