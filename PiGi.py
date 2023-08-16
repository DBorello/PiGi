import boto3
from uuid import getnode
import time
import logging
from waveshare_epd import epd3in7
from PIL import Image,ImageDraw,ImageFont

DELAY_BETWEEN_DB_ATTEMPTS = 5
DELAY_BETWEEN_DB_SUCCESS = 5

logging.basicConfig(level=logging.INFO)

class PiGi:

    def __init__(self):
        # Get devices MAC address
        self.mac = hex(getnode())[2:]
        logging.info('Device MAC: {}'.format(self.mac))

        self.value = -1
        self.last_success = 0

        # Setup display
        self.epd = epd3in7.EPD()
        self.epd.init(0)
        self.epd.Clear(0xFF,0)

        self.display_splash()

        # Enter main loop
        self.main()

    def main(self):
        while True:
            if time.time() - self.last_success > DELAY_BETWEEN_DB_SUCCESS:
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
                logging.info(self.value)
                self.last_success = time.time()
                return True
            else:
                print('Error == MAC address not in database!')
                return False

        except:
            print('ERROR == Unable to connect to database')
            return False

    def display_splash(self):
        font36 = ImageFont.truetype('Font.ttc', 36)

        Himage = Image.new('L', (self.epd.height, self.epd.width), 0xFF)  # 0xFF: clear the frame
        draw = ImageDraw.Draw(Himage)

        
        draw.text((10, 0), 'hello world', font = font36, fill = 0)

if __name__ == "__main__":
    PiGi()