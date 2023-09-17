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
        self.get_mac()
        self.value = -1
        self.msg = ''
        self.last_success = 0

        # Setup display
        self.epd = epd3in7.EPD()
       

        self.display_splash()

        # Enter main loop
        self.main()

    def get_mac(self):
        f = open('/sys/class/net/wlan0/address')
        self.mac = f.read().strip().replace(':','')
        f.close()
        logging.info('Device MAC: {}'.format(self.mac))
    
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
            r = table.get_item(Key = {'mac':self.mac})
        except Exception as e:
            print(e)
            print('ERROR == Unable to connect to database')
            return False

        # Fetch value
        
        if 'Item' in r.keys():
            new_value = r['Item']['value']
            self.msg = r['Item'].get('msg','')
            self.last_success = time.time()
            logging.info(new_value)

            if new_value != self.value:
                self.value = new_value      
                self.display_value()

            

            return True
        else:
            print('Error == MAC address not in database!')
            return False



    def display_splash(self):
        self.epd.init(0)
        self.epd.Clear(0xFF,0)

        Himage = Image.new('L', (self.epd.height, self.epd.width), 0xFF)  # 0xFF: clear the frame
        draw = ImageDraw.Draw(Himage)

        draw.text((self.epd.height/2, 100), 'PiGi'.format(self.value), font = ImageFont.truetype('Font.ttc', 96), fill = 0, anchor = 'mm')
        draw.text((self.epd.height/2, 260), 'MAC: {}'.format(self.mac), font = ImageFont.truetype('Font.ttc', 48), fill = 0, anchor = 'mb')
        self.epd.display_4Gray(self.epd.getbuffer_4Gray(Himage))
        self.epd.sleep()

    def display_value(self):
        self.epd.init(0)
        self.epd.Clear(0xFF,0)

        Himage = Image.new('L', (self.epd.height, self.epd.width), 0xFF)  # 0xFF: clear the frame
        draw = ImageDraw.Draw(Himage)

        draw.text((self.epd.height/2, 100), '$ {:,.0f}'.format(self.value), font = ImageFont.truetype('Font.ttc', 96), fill = 0, anchor = 'mm')
        draw.text((self.epd.height/2, 260), self.msg, font = ImageFont.truetype('Font.ttc', 48), fill = 0, anchor = 'mb')
        self.epd.display_4Gray(self.epd.getbuffer_4Gray(Himage))
        self.epd.sleep()

if __name__ == "__main__":
    PiGi()
