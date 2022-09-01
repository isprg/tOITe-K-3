import time
import cv2
import mediapipe as mp
from numpy import uint8
from ClsImageProcess import ClsImageProcess
from JudgePose import makeListOfAngles
from JudgePose import draw_landamrks
from JudgePose import judge_pose

class ClsImageProcessPose(ClsImageProcess):
	def initProcess(self):
		self.isROIdefined = False
		self.ratioROI = 0.5
		self.flag = False  # ポーズができたかのフラグ
		self.flag_onstart = 0  # ポーズができた時の時間を格納する場所
		self.sJudgeMargin = 5
		self.mp_pose = mp.solutions.pose
		#self.pose_subject = self.mp_pose.Pose(
		#	static_image_mode=True,
		#	min_detection_confidence=0.5,
		#	min_tracking_confidence=0.5)
		self.pose = self.mp_pose.Pose(
			min_detection_confidence=0.5,
			min_tracking_confidence=0.5)

		imOverlayOrig_inst = cv2.imread('./png/sign_inst2.png', -1)
		self.imOverlayMask_inst = imOverlayOrig_inst[:,:,3]
		self.imOverlayMask_inst = cv2.cvtColor(self.imOverlayMask_inst, cv2.COLOR_GRAY2BGR)
		self.imOverlayMask_inst	 = self.imOverlayMask_inst / 255
		self.imOverlayOrig_inst = imOverlayOrig_inst[:,:,:3]
		# self.window.setEnableOverlay(True, 300, 0)
		# self.window.setOverlayImage(self.imOverlayOrig_inst, self.imOverlayMask_inst)

		imOverlayOrig_correct = cv2.imread('./png/sign_correct_cyan.png', -1)
		self.imOverlayMask_correct = imOverlayOrig_correct[:,:,3]
		self.imOverlayMask_correct = cv2.cvtColor(self.imOverlayMask_correct, cv2.COLOR_GRAY2BGR)
		self.imOverlayMask_correct	 = self.imOverlayMask_correct / 255
		self.imOverlayOrig_correct = imOverlayOrig_correct[:,:,:3]
		self.window.setEnableOverlay(True, 0, 0)
		# self.window.setOverlayImage(self.imOverlayOrig_correct, self.imOverlayMask_inst)

	def setRatioROI(self, ratioROI):
		self.ratioROI = ratioROI

	def defineCorrectPose(self, strImgPath):
		#imCorrect = cv2.imread(strImgPath)
		#imCorrect = cv2.resize(
		#	imCorrect, (int(imCorrect.shape[1]*0.9), int(imCorrect.shape[0]*0.9)))
		#results = self.pose_subject.process(cv2.cvtColor(imCorrect, cv2.COLOR_BGR2RGB))
		#vLandmark = [landmark for landmark in results.pose_landmarks.landmark]
		#vPoints = [(landmark.x * imCorrect.shape[1], landmark.y * imCorrect.shape[0])
		#			for landmark in vLandmark]
		#self.correctAngles = makeListOfAngles(vLandmark, vPoints)
		self.correctAngle = 20
		# print(self.correctAngle)

	def defineROI(self, img):
		width = int(img.shape[1] * self.ratioROI)
		self.leftPosROI = int((img.shape[1] - width) / 2)
		self.rightPosROI = img.shape[1] - self.leftPosROI
		self.isROIdefined = True

	def reset(self):
		#self.isROIdefined = False
		#self.ratioROI = 0.5
		self.flag = False  # ポーズができたかのフラグ
		self.flag_onstart = 0  # ポーズができた時の時間を格納する場所
		#self.sJudgeMargin = 20
		#self.mp_pose = mp.solutions.pose
		#self.pose = self.mp_pose.Pose(
		#	min_detection_confidence=0.5,
		#	min_tracking_confidence=0.5)

	def process(self):
		# self.defineCorrectPose("")
		if self.isROIdefined == False:
			self.defineROI(self.imSensor)
		imROI = self.imSensor[:, self.leftPosROI:self.rightPosROI]
		self.imSensor[:,:self.leftPosROI] = (self.imSensor[:,:self.leftPosROI]*0.5).astype(uint8)
		self.imSensor[:,self.rightPosROI:] = (self.imSensor[:,self.rightPosROI:]*0.5).astype(uint8)
		imROI = cv2.cvtColor(imROI, cv2.COLOR_BGR2RGB)

		imROI.flags.writeable = False
		results = self.pose.process(imROI)
		imROI.flags.writeable = True
		imROI = cv2.cvtColor(imROI, cv2.COLOR_RGB2BGR)

		self.imSensor[:, self.leftPosROI:self.rightPosROI] = imROI

		# 切り抜いた場所の左右に黄色の線を引く
		self.imSensor = cv2.line(self.imSensor, (self.leftPosROI, 0), (
			self.leftPosROI, self.imSensor.shape[0]), (0, 0, 255), thickness=2, lineType=cv2.LINE_8)
		self.imSensor = cv2.line(self.imSensor, (self.rightPosROI, 0), (
			self.rightPosROI, self.imSensor.shape[0]), (0, 0, 255), thickness=2, lineType=cv2.LINE_8)

		if results.pose_landmarks:
			# x座標に切り抜いた左側の位置を足し合わす
			vPoints = [(int(landmark.x*imROI.shape[1]+self.leftPosROI), int(landmark.y*imROI.shape[0]))
						for landmark in results.pose_landmarks.landmark]
			pose_flag = judge_pose(
				results.pose_landmarks.landmark, vPoints, self.correctAngle, self.sJudgeMargin)
			self.imSensor = draw_landamrks(
				self.imSensor, vPoints, 2, 3, (0, 255, 0), (0, 0, 255))

			# ポーズが正解だった時にクラスの判定フラグをTrueにする。また、ここで正解した時間を記録する
			if pose_flag is True:
				self.flag = True
				self.flag_onstart = time.time()

		# クラスのポーズ判定フラグによって左上に表示する画像を変える
		if self.flag is True:
			self.window.setOverlayImage(self.imOverlayOrig_correct, self.imOverlayMask_correct)
			self.imProcessed = self.imSensor

			# ポーズ判定で正解して３秒以上経過したらクラスのフラグをFalseにし、processの返り値をTrueにする
			if time.time() - self.flag_onstart >= 2:
				self.flag = False
				print("正解")
				return True
		else:
			self.window.setOverlayImage(self.imOverlayOrig_inst, self.imOverlayMask_inst)
			self.imProcessed = self.imSensor


		return 0

if __name__ == '__main__':
	CProc = ClsImageProcessPose
	import os

	if os.name == 'nt':
		strPlatform = 'WIN'
	else:
		strPlatform = 'JETSON'

	sCameraNumber = 0
	sSensorWidth = 640
	sSensorHeight = 360
	sMonitorWidth = 1024
	sMonitorHeight = 600
	tplWindowName = ('full',)
	sFlipMode = 1

	proc = CProc(
		strPlatform,
		sCameraNumber,
		sSensorWidth,
		sSensorHeight,
		sMonitorWidth,
		sMonitorHeight,
		tplWindowName,
		sFlipMode)

	proc.createWindows()
	proc.setRatioROI(0.5)
	proc.defineCorrectPose("result_pose/guriko_pose.jpg")

	while True:
		proc.execute()
		sKey = cv2.waitKey(1) & 0xFF
		if sKey == ord('q'):
			del proc
			break
