from traceback import format_exc
from requests import Session as RequestSession

class MapTools:
	def __init__(self):
		self.qpack_pattern = {0: {0: '^', 1: '[^]'}, 1: {0: '" /><player x="', 1: '^0'}, 2: {0: '" /><enemy x="', 1: '^1'}, 3: {0: '" /><door x="', 1: '^2'}, 4: {0: '" /><box x="', 1: '^3'}, 5: {0: '" /><gun x="', 1: '^4'}, 6: {0: '" /><pushf x="', 1: '^5'}, 7: {0: '" /><decor x="', 1: '^6'}, 8: {0: '" /><trigger enabled="true', 1: '^7'}, 9: {0: '" /><trigger enabled="false', 1: '^8'}, 10: {0: '" /><timer enabled="true', 1: '^9'}, 11: {0: '" /><timer enabled="false', 1: '^a'}, 12: {0: '" /><inf mark="', 1: '^b'}, 13: {0: ' /><bg x="', 1: '^c'}, 14: {0: ' /><lamp x="', 1: '^d'}, 15: {0: ' /><region x="', 1: '^e'}, 16: {0: '<player x="', 1: '^f'}, 17: {0: '" damage="', 1: '^g'}, 18: {0: '" maxspeed="', 1: '^h'}, 19: {0: '" model="gun_', 1: '^i'}, 20: {0: '" model="', 1: '^j'}, 21: {0: '" botaction="', 1: '^k'}, 22: {0: '" ondeath="', 1: '^l'}, 23: {0: '" actions_', 1: '^m'}, 24: {0: '_targetB="', 1: '^n'}, 25: {0: '_type="', 1: '^o'}, 26: {0: '_targetA="', 1: '^p'}, 27: {0: '" team="', 1: '^q'}, 28: {0: '" side="', 1: '^r'}, 29: {0: '" command="', 1: '^s'}, 30: {0: '" flare="', 1: '^t'}, 31: {0: '" power="', 1: '^u'}, 32: {0: '" moving="true', 1: '^w'}, 33: {0: '" moving="false', 1: '^x'}, 34: {0: '" tarx="', 1: '^y'}, 35: {0: '" tary="', 1: '^z'}, 36: {0: '" tox="', 1: '^A'}, 37: {0: '" toy="', 1: '^B'}, 38: {0: '" hea="', 1: '^C'}, 39: {0: '" hmax="', 1: '^D'}, 40: {0: '" incar="', 1: '^E'}, 41: {0: '" char="', 1: '^F'}, 42: {0: '" maxcalls="', 1: '^G'}, 43: {0: '" vis="false', 1: '^H'}, 44: {0: '" vis="true', 1: '^I'}, 45: {0: '" use_on="', 1: '^J'}, 46: {0: '" use_target="', 1: '^K'}, 47: {0: '" upg="0^', 1: '^L'}, 48: {0: '" upg="', 1: '^M'}, 49: {0: '^fgun_', 1: '^N'}, 50: {0: '" addx="', 1: '^O'}, 51: {0: '" addy="', 1: '^P'}, 52: {0: '" y="', 1: '^Q'}, 53: {0: '" w="', 1: '^R'}, 54: {0: '" h="', 1: '^S'}, 55: {0: '" m="', 1: '^T'}, 56: {0: '" at="', 1: '^U'}, 57: {0: '" delay="', 1: '^W'}, 58: {0: '" target="', 1: '^X'}, 59: {0: '" stab="', 1: '^Y'}, 60: {0: '" mark="', 1: '^Z'}, 61: {0: '0^T0^3', 1: '^_'}, 62: {0: '0^x^y0^z0^h1^', 1: '^('}, 63: {0: '^m3^o-1^m3^p0^m3^n0^m4^o-1^m4^p0^m4^n0^m5^o-1^m5^p0^m5^n0^m6^o-1^m6^p0^m6^n0^m7^o-1^m7^p0^m7^n0^m8^o-1^m8^p0^m8^n0^m9^o-1^m9^p0^m9^n0^m10^o-1^m10^p0^m10^n0', 1: '^)'}, 64: {0: '^m5^o-1^m5^p0^m5^n0^m6^o-1^m6^p0^m6^n0^m7^o-1^m7^p0^m7^n0^m8^o-1^m8^p0^m8^n0^m9^o-1^m9^p0^m9^n0^m10^o-1^m10^p0^m10^n0', 1: '^$'}, 65: {0: '^A0^B0^C130^D130^q', 1: '^@'}, 66: {0: '0^u0.4^t1"^', 1: '^~'}, 67: {0: '0^Q1', 1: '^!'}, 68: {0: '0^R', 1: '^.'}, 69: {0: '0^S', 1: '^,'}, 70: {0: '0^Q-', 1: '^*'}, 71: {0: '0^Q', 1: '^-'}, 72: {0: '" /><water x="', 1: '^+'}, 73: {0: '" forteam="', 1: '^;'}, 74: {0: '^Ttrue', 1: '^:'}, 75: {0: 'true', 1: '^?'}, 76: {0: 'false', 1: '^<'}, 77: {0: '^m2^o-1^m2^p0^m2^n0^)', 1: '^>'}, 78: {0: 'pistol', 1: '^/'}, 79: {0: 'rifle', 1: '^#'}, 80: {0: 'shotgun', 1: '^%'}, 81: {0: 'real_', 1: '^&'}, 82: {0: '', 1: '<q.'}}
		self.qpack_pattern_length = 83
		self._session = RequestSession()
		self._session.headers.update( {
			'Accept' : 'text/xml, application/xml, application/xhtml+xml, text/html;q=0.9, text/plain;q=0.8, text/css, image/png, image/jpeg, image/gif;q=0.8, application/x-shockwave-flash, video/mp4;q=0.9, flv-application/octet-stream;q=0.8, video/x-flv;q=0.7, audio/mp4, application/futuresplash, */*;q=0.5',
			 'User-Agent' : 'Shockwave Flash',
			 'x-flash-version ' : '11,7,700,224',
			 'Host' : 'www.plazmaburst2.com'
			})

	def un_qpack(self, param1):
		i = self.qpack_pattern_length -1
		while i >= 0:
			param1 = param1.replace(self.qpack_pattern[i][1], self.qpack_pattern[i][0])
			i -= 1
		return param1

	def get_objects(self, param1):
		unpacked = self.un_qpack(param1)
		elements = []
		for x in unpacked.replace(' />', '').replace('[eq]', '=').split('<')[1:]:
			el = {}
			el['type'] = x.split()[0]
			for y in x.split()[1:]:
				try:
					kv = y.split('=')
					v = kv[1].strip('"')
				except Exception as e:
					print(f'kv: {kv}, {format_exc()}')
					continue
				try:
					v = int(v)
				except Exception:
					pass
				el[kv[0]] = v
			elements.append(el)
		return elements

	def getMapByIdOnline(self, mapid, xml=False):
		post_data = {
			'p' : 'undefined',
			'cmap' : mapid,
			'l' : 'undefined',
			'qpack' : '1.0',
			'rq' : 'cmap'
			}
		try:
			resp = self._session.post(url='http://www.plazmaburst2.com/pb2/server.php', data=post_data)
			resp.raise_for_status()
			if xml:
				return self.un_qpack(resp.text)
			else:
				return self.get_objects(resp.text)
		except Exception:
			print('Failed to retrieve mapdata')
			return None



