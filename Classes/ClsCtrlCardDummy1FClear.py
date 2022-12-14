from importlib.resources import path


class ClsCtrlCard:
	def __init__(self, Prob_List):
		self.CurrentID = None

		# 記録と問題名の対応を表すテーブル
		self.dictRecord_Table = {}
		for key in Prob_List:
			self.dictRecord_Table[key] = "0"

	def Finalize(self):
		path

	def setCard(self):
		return True

	def reset_record_table(self):
		for key in self.dictRecord_Table.keys():
			self.dictRecord_Table[key] = "0"

	def initCard(self):
		#self.dictRecord_Table["labo"] = "T"
		#self.dictRecord_Table["room"] = "T"
		self.dictRecord_Table["tutorial"] = "T"
		self.dictRecord_Table["tearai1"] = "T"
		self.dictRecord_Table["tearai2"] = "T"
		self.dictRecord_Table["hondana"] = "T"
		return True

	def retry_to_initCard(self):
		path

	def getID(self):
		return self.CurrentID

	def write_result(self, strProb_Name, strAns):
		if strProb_Name not in self.dictRecord_Table:
			return False
		self.dictRecord_Table[strProb_Name] = strAns
		print(self.dictRecord_Table)
		return True

	def retry_to_write(self):
		return True

	def updata_record_table(self):
		path

	def read_result(self):
		self.initCard()
		return self.dictRecord_Table.copy()

	def check_exist(self):
		return True

	def check_identity(self):
		return True
