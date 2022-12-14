import time
import cv2
import mediapipe as mp
from numpy import uint8
from ClsImageProcess import ClsImageProcess
from JudgePose import makeListOfAngles
from JudgePose import draw_landamrks
from JudgePose import judge_pose_kagiya

def resize_fix_ratio(image, resized_h):
	h, w = image.shape[:2]
	resized_w = int((resized_h / h) * w)

	image = cv2.resize(image, dsize=(resized_w, resized_h))

	return image


def overlay_png(main_image, overlay_image, a):
	h, w = overlay_image.shape[:2]

	if w > main_image.shape[1]:
		diff = w - main_image.shape[1]
		overlay_image = overlay_image[:, int(diff / 2) + (diff % 2) : -int(diff / 2)]

		w = main_image.shape[1]

	overlay_rgb = overlay_image[:, :, 0:3]

	main_image_tmp = main_image[0:h, 0:w].copy()

	# print(main_image_tmp.shape)

	main_image_tmp[overlay_image[:, :, 3] >= 30] = (
		main_image_tmp[overlay_image[:, :, 3] >= 30] * (1 - a)
		+ overlay_rgb[overlay_image[:, :, 3] >= 30] * a
	)

	main_image[0:h, 0:w] = main_image_tmp

	return main_image


def overlay(main_image, overlay_image, a):
	h, w = overlay_image.shape[:2]

	if w > main_image.shape[1]:
		diff = w - main_image.shape[1]
		overlay_image = overlay_image[:, int(diff / 2) + (diff % 2) : -int(diff / 2)]

	main_image_tmp = main_image[0:h, 0:w].copy()

	# print(overlay_image.shape, main_image_tmp.shape)
	main_image_tmp = main_image_tmp * (1 - a) + overlay_image * a
	main_image[0:h, 0:w] = main_image_tmp
	return main_image
	

class ClsImageProcessPose(ClsImageProcess):
	def initProcess(self):
		self.isROIdefined = False
		self.ratioROI = 0.5
		self.flag = False  # ポーズができたかのフラグ
		self.flag_onstart = 0  # ポーズができた時の時間を格納する場所
		self.sJudgeMargin = 15
		self.mp_pose = mp.solutions.pose
		#self.pose_subject = self.mp_pose.Pose(
		#	static_image_mode=True,
		#	min_detection_confidence=0.5,
		#	min_tracking_confidence=0.5)
		self.pose = self.mp_pose.Pose(
			min_detection_confidence=0.5,
			min_tracking_confidence=0.5)

		# imOverlayOrig_pose = cv2.imread('./images/sign_pose.png', -1)
		# # imOverlayOrig_pose = cv2.resize(imOverlayOrig_pose, dsize=(self.sWidthWindow, self.sHeightWindow))
		# self.imOverlayMask_pose = imOverlayOrig_pose[:,:,3]
		# self.imOverlayMask_pose = cv2.cvtColor(self.imOverlayMask_pose, cv2.COLOR_GRAY2BGR)
		# self.imOverlayMask_pose	 = self.imOverlayMask_pose / 255
		# self.imOverlayOrig_pose = imOverlayOrig_pose[:,:,:3]

		imOverlayOrig_inst = cv2.imread('./images/sign_inst2.png', -1)
		self.imOverlayMask_inst = imOverlayOrig_inst[:,:,3]
		self.imOverlayMask_inst = cv2.cvtColor(self.imOverlayMask_inst, cv2.COLOR_GRAY2BGR)
		self.imOverlayMask_inst[self.imOverlayMask_inst[:,:] >= 1]	 = self.imOverlayMask_inst[self.imOverlayMask_inst[:,:] >= 1] / 255
		self.imOverlayOrig_inst = imOverlayOrig_inst[:,:,:3]
		# self.window.setEnableOverlay(True, 300, 0)
		# self.window.setOverlayImage(self.imOverlayOrig_inst, self.imOverlayMask_inst)

		imOverlayOrig_correct = cv2.imread('./images/sign_correct.png', -1)
		self.imOverlayMask_correct = imOverlayOrig_correct[:,:,3]
		self.imOverlayMask_correct = cv2.cvtColor(self.imOverlayMask_correct, cv2.COLOR_GRAY2BGR)
		self.imOverlayMask_correct	 = self.imOverlayMask_correct / 255
		self.imOverlayOrig_correct = imOverlayOrig_correct[:,:,:3]

		self.window.setEnableOverlay(True, 750, 0)
		# self.window.setOverlayImage(self.imOverlayOrig_correct, self.imOverlayMask_inst)

		self.__image_main_bg = cv2.imread('./images/pose/main_bg.png', -1)
		self.__image_main_edge = cv2.imread('./images/pose/main_edge.png', -1)
		# self.__image_main_human = cv2.imread('./images/pose/main_human.png', -1)
		self.__image_main_bg = resize_fix_ratio(self.__image_main_bg, 270)
		self.__image_main_edge = resize_fix_ratio(self.__image_main_edge, 270)

	def setRatioROI(self, ratioROI):
		self.ratioROI = ratioROI

	#-- 正解の角度を入れる --
	def defineCorrectPose(self, strImgPath):
		#imCorrect = cv2.imread(strImgPath)
		#imCorrect = cv2.resize(
		#	imCorrect, (int(imCorrect.shape[1]*0.9), int(imCorrect.shape[0]*0.9)))
		#results = self.pose_subject.process(cv2.cvtColor(imCorrect, cv2.COLOR_BGR2RGB))
		#vLandmark = [landmark for landmark in results.pose_landmarks.landmark]
		#vPoints = [(landmark.x * imCorrect.shape[1], landmark.y * imCorrect.shape[0])
		#			for landmark in vLandmark]
		#self.correctAngles = makeListOfAngles(vLandmark, vPoints)
		self.correctAngle = [70,58,45]
		# print(self.correctAngle)

	def defineROI(self, img):
		width = int(img.shape[1] * self.ratioROI)
		# self.leftPosROI = int((img.shape[1] - width) / 2)
		#self.rightPosROI = img.shape[1] - int((img.shape[1] - width) * 0.8)
		self.leftPosROI = 0
		self.rightPosROI = int(img.shape[1] * 0.7)
		#self.rightPosROI = 270
		print(self.rightPosROI)
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
		imROI = self.imSensor[:, self.leftPosROI:self.rightPosROI] # ポーズ判定範囲
		self.imSensor[:,:self.leftPosROI] = (self.imSensor[:,:self.leftPosROI]*0.5).astype(uint8)
		self.imSensor[:,self.rightPosROI:] = (self.imSensor[:,self.rightPosROI:]*0.5).astype(uint8)
		imROI = cv2.cvtColor(imROI, cv2.COLOR_BGR2RGB)
		#print(self.imSensor.shape)
		imROI.flags.writeable = False
		results = self.pose.process(imROI)
		imROI.flags.writeable = True
		imROI = cv2.cvtColor(imROI, cv2.COLOR_RGB2BGR)


		#self.__image_main_bg = resize_fix_ratio(self.__image_main_bg, 270)
		#self.__image_main_edge = resize_fix_ratio(self.__image_main_edge, 270)
		# self.imSensor[:360,self.leftPosROI:self.rightPosROI] = self.__image
		self.imSensor = overlay(
			self.imSensor, self.__image_main_bg[:, :, 0:3], 150 / 255
		)
		self.imSensor = overlay_png(self.imSensor, self.__image_main_edge, 1)
	

		# 切り抜いた場所の左右に赤色の線を引く
		# self.imSensor = cv2.line(self.imSensor, (self.leftPosROI, 0), (
		# 	self.leftPosROI, self.imSensor.shape[0]), (0, 0, 255), thickness=2, lineType=cv2.LINE_8)
		self.imSensor = cv2.line(self.imSensor, (self.rightPosROI, 0), (
			self.rightPosROI, self.imSensor.shape[0]), (0, 0, 255), thickness=2, lineType=cv2.LINE_8)


		if results.pose_landmarks:
			# x座標に切り抜いた左側の位置を足し合わす
			vPoints = [(int(landmark.x*imROI.shape[1]+self.leftPosROI), int(landmark.y*imROI.shape[0]))
						for landmark in results.pose_landmarks.landmark]
			pose_flag = judge_pose_kagiya(
				results.pose_landmarks.landmark, vPoints, self.correctAngle, self.sJudgeMargin)
			self.imSensor = draw_landamrks(
				self.imSensor, vPoints, 2, 3, (0, 255, 0), (0, 0, 255))

			# ポーズが正解だった時にクラスの判定フラグをTrueにする。また、ここで正解した時間を記録する
			if pose_flag is True:
				self.flag = True
				self.flag_onstart = time.time()

		# self.window.setOverlayImage(self.imOverlayOrig_pose, self.imOverlayMask_pose)
		# クラスのポーズ判定フラグによって左上に表示する画像を変える
		if self.flag is True:
			self.window.setOverlayImage(self.imOverlayOrig_correct, self.imOverlayMask_correct)
			self.imProcessed = self.imSensor

			# ポーズ判定で正解して３秒以上経過したらクラスのフラグをFalseにし、processの返り値をTrueにする
			if time.time() - self.flag_onstart >= 2:
				self.flag = False
				# print("正解")
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
	sSensorWidth = 480
	sSensorHeight = 270
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
