"""
The purpose of this tool is intended to open continuous ping until it fails 
a certain number of times consecutively. 
"""
__author__ = 'Xander Petty'
__contact__ = 'Alexander.Petty@williams.com'
__version__ = '1.0'

from scapy.all import IP, ICMP, sr1 
from socket import gethostbyname as nslookup
from socket import gethostbyaddr as reverse_lookup
from time import sleep
from flask import Flask, render_template, request
from wtforms import Label, TextField, validators
from flask_wtf import FlaskForm
from os import urandom

# BUILD NOTE - Constructing the backend as a class with functions first
class PingUntil():
    def __init__(self, ip, trigger):
        self.ip = ip 
        self.trigger = trigger
    def _craft_packet(self, ip, ttl):
        packet = IP(dst=ip, ttl=ttl)/ICMP()
        return packet 
    def run(self):
        errors = 0
        success = 0
        while int(errors) != int(self.trigger):
            # Rate limiting the amount of ICMPs to be sent.
            sleep(1)
            packet = self._craft_packet(self.ip, ttl=32)
            reply = sr1(packet, timeout=10, verbose=False)
            if reply == None:
                errors += 1
            else:
                errors = 0
                success += 1
                print(f'Reply from {reply.src}')
        hops = self.trace()
        # last_good_hop = hops[int(len(hops) - 1)]
        # return last_good_hop
        return hops 
    def trace(self):
        failed = 0
        ttl = 1
        hops = []
        while failed != 3:
            packet = self._craft_packet(self.ip, ttl=ttl)
            reply = sr1(packet, timeout=2, verbose=False)
            if reply == None:
                failed += 1
            elif reply.src == self.ip:
                break
            else:
                failed = 0
                hops.append(reply.src)
                ttl += 1
        return hops 

class PingForm(FlaskForm):
    ip_label = Label('ip_label', text='Enter the IP Address to ping: ')
    ip_entry = TextField(id='ip_entry', validators=[validators.required()])
    trigger_label = Label('trigger_label', text='Enter the number of failed pings to set trigger: ')
    trigger_entry = TextField(id='trigger_entry', validators=[validators.required()])

app = Flask(__name__)
app.config['DEBUG'] = True 
app.config['SECRET_KEY'] = urandom(24)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        form = PingForm()
        return render_template('main.html', form=form)
    elif request.method == 'POST':
        ip = request.form['ip_entry']
        trigger = request.form['trigger_entry']
        pinger = PingUntil(ip, trigger)
        fail_hops = pinger.run()
        return render_template('results.html', target_ip=ip, hops=fail_hops)


if __name__ == '__main__':
    app.run(ssl_context='adhoc')
