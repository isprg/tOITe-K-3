import cv2
import numpy as np

def makeListOfAngles(vLandmarks, vPoints):
	angles = []

	# 左肩を中心とした右肩から左肘までの角度
	angles.append(measureAngleWrap(vLandmarks, vPoints, [12, 11, 14]))
	# 左肘を中心とした左肩から左手首までの角度
	angles.append(measureAngleWrap(vLandmarks, vPoints, [14, 12, 16]))
	# 左腰を中心とした左肩から左膝まで角度
	angles.append(measureAngleWrap(vLandmarks, vPoints, [24, 12, 26]))
	# 左膝を中心とした左腰から左足首までの角度
	angles.append(measureAngleWrap(vLandmarks, vPoints, [26, 24, 28]))
	# 右肩を中心とした左肩から右肘までの角度
	angles.append(measureAngleWrap(vLandmarks, vPoints, [11, 13, 12]))
	# 右肘を中心とした右肩から右手首までの角度
	angles.append(measureAngleWrap(vLandmarks, vPoints, [13, 15, 11]))
	# 右腰を中心とした右肩から右膝まで角度
	angles.append(measureAngleWrap(vLandmarks, vPoints, [23, 11, 25]))
	# 右膝を中心とした右腰から右足首までの角度
	angles.append(measureAngleWrap(vLandmarks, vPoints, [25, 23, 27]))

	return angles

def measureAngleWrap(vLandmarks, vPoints, vPointNumbers):
	visibilityThresh = 0.3
	if (vLandmarks[vPointNumbers[0]].visibility > visibilityThresh
	and vLandmarks[vPointNumbers[1]].visibility > visibilityThresh
	and vLandmarks[vPointNumbers[2]].visibility > visibilityThresh):
		return measureAngle(vPoints, vPointNumbers)
	else:
		return -1

# aを中心とするabからのcの角度
def measureAngle(vPoints, vPointNumbers):
	vPostPivot = np.array(vPoints[vPointNumbers[0]])
	vPostAround1 = np.array(vPoints[vPointNumbers[1]])
	vPostAround2 = np.array(vPoints[vPointNumbers[2]])

	if (np.array_equal(vPostPivot, vPostAround1)
	or np.array_equal(vPostAround1, vPostAround2)
	or np.array_equal(vPostAround2, vPostPivot)):
		return -1

	if ((vPostPivot[0] >= 0 and vPostPivot[1] >= 0)
	and (vPostAround1[0] >= 0 and vPostAround1[1] >= 0)
	and (vPostAround2[0] >= 0 and vPostAround2[1] >= 0)):
		pass
	else:
		return -1

	vec1 = vPostAround1 - vPostPivot
	vec2 = vPostAround2 - vPostPivot
	absvec1 = np.linalg.norm(vec1)
	absvec2 = np.linalg.norm(vec2)
	inner = np.inner(vec1, vec2)
	cos_theta = inner/ (absvec1*absvec2)

	rad = np.arccos(cos_theta)

	degree = np.rad2deg(rad)
	if vec_cross(vec1, vec2) == -1:
		return degree
	else:
		return 360 - degree

# tuple型(pivot, edge1, edge2)
def point2Angle(points):
	vPivot = np.array(points[0])
	vEdge1 = np.array(points[1])
	vEdge2 = np.array(points[2])

	vec1 = vEdge1 - vPivot
	vec2 = vEdge2 - vPivot

	# コサインの計算
	length_vec_a = np.linalg.norm(vec1)
	length_vec_c = np.linalg.norm(vec2)
	inner_product = np.inner(vec1, vec2)
	cos = inner_product / (length_vec_a * length_vec_c)

	# 角度（ラジアン）の計算
	rad = np.arccos(cos)

	# 弧度法から度数法（rad ➔ 度）への変換
	degree = np.rad2deg(rad)

	return degree


# 外積
def vec_cross(vec1, vec2):
	a = np.cross(vec1, vec2)
	if a > 0:
		return 1
	elif a < 0:
		return -1
	else:
		return 0


#-- Pose Landmark URL --
# https://google.github.io/mediapipe/solutions/pose
def draw_landamrks(img, points, line_pic, radius, line_color, circle_color):
	img_ = img.copy()

	False_point = [1,2,3,4,5,6,7,8,9,10,17,18,19,20,21,22,29,30,31,32]
	for i, point in enumerate(points):
		if(i in False_point): continue

		if(i==0):
			# 肩の中心x座標
			shoulder_mid_x = (points[12][0]+points[11][0])//2
			# y座標
			shoulder_mid_y = (points[12][1]+points[11][1])//2
			shoulder_mid_point = (shoulder_mid_x, shoulder_mid_y)
			cv2.line(img_, points[0], shoulder_mid_point, color=line_color, thickness=line_pic, lineType=cv2.LINE_4)

		if 11 <= i <= 14 or 23 <= i <= 26:
			if i == 11:
				cv2.line(img_, points[11], points[12], color=line_color, thickness=line_pic, lineType=cv2.LINE_4)
				cv2.line(img_, points[11], points[23], color=line_color, thickness=line_pic, lineType=cv2.LINE_4)
			elif i == 12:
				cv2.line(img_, points[12], points[24], color=line_color, thickness=line_pic, lineType=cv2.LINE_4)
			elif i == 23:
				cv2.line(img_, points[23], points[24], color=line_color, thickness=line_pic, lineType=cv2.LINE_4)

			cv2.line(img_, points[i], points[i+2], color=line_color, thickness=line_pic, lineType=cv2.LINE_4)

		img_ = cv2.circle(img_, center=point, radius=radius, color=circle_color, thickness=-1, lineType=cv2.LINE_4)

	return img_

def judge_pose(vLandmarks, vPoints, correctAngle, sJudgeMargin):
	# currentAngles = makeListOfAngles(vLandmarks, vPoints)
	#print(currentAngles[0],currentAngles[1],currentAngles[4],currentAngles[5])
	#print(vLandmarks[26],vLandmarks[25])
	flag = False
	# for i in range(0, 8):
	# 	if i in (2, 3, 6, 7):
	# 		continue
	# 	if correctAngles[i] - sJudgeMargin  <= currentAngles[i] \
	# 	and currentAngles[i] <= correctAngles[i] + sJudgeMargin:
	# 		pass
	# 	else:
	# 		flag = False

	# 肩の中心x座標
	shoulder_mid_x = (vPoints[12][0]+vPoints[11][0])/2
	# y座標
	shoulder_mid_y = (vPoints[12][1]+vPoints[11][1])/2
	shoulder_mid_point = (shoulder_mid_x, shoulder_mid_y)

	# 腰の中心x座標
	hip_mid_x = (vPoints[24][0]+vPoints[23][0])/2
	# y座標
	hip_mid_y = (vPoints[24][1]+vPoints[23][1])/2
	hip_mid_point = (hip_mid_x, hip_mid_y)

	array_left_shoulder = np.array(vPoints[11])
	array_right_shoulder = np.array(vPoints[12])
	a = np.linalg.norm(array_left_shoulder - array_right_shoulder)

	array_shoulder = np.array(shoulder_mid_point)
	array_hip = np.array(hip_mid_point)
	b = np.linalg.norm(array_shoulder - array_hip)

	if a / b <= 0.5:
		# xは腰の位置,yは肩の位置の座標
		hipx_shouldery = (hip_mid_x, shoulder_mid_y)

		this_angle = measureAngle([hip_mid_point, hipx_shouldery, shoulder_mid_point], [0, 1, 2])
		# print(this_angle)
		if this_angle >= 180 :
			this_angle = 360 - this_angle
		if correctAngle - sJudgeMargin <= this_angle and this_angle <= correctAngle + sJudgeMargin:
			flag = True



	# print('pos:head,',vPoints[0], 'shoulder,',vPoints[12], 'hip,',vPoints[24], '')
	# measureAngle(,)
	# print('pos:head,',vPoints[0], 'shoulder,',vPoints[12], 'hip,',vPoints[24])
	
	return flag


def judge_pose_kagiya(vLandmarks, vPoints, correctAngle, sJudgeMargin):
	flag = False

	up_correct = [d+sJudgeMargin for d in correctAngle]
	bottom_correct = [d-sJudgeMargin for d in correctAngle]

	up_correct[2] -= 5
	bottom_correct[2] += 5

	# 肩の中心x座標
	shoulder_mid_x = (vPoints[12][0]+vPoints[11][0])/2
	# y座標
	shoulder_mid_y = (vPoints[12][1]+vPoints[11][1])/2
	shoulder_mid_point = (shoulder_mid_x, shoulder_mid_y)

	# 腰の中心x座標
	hip_mid_x = (vPoints[24][0]+vPoints[23][0])/2
	# y座標
	hip_mid_y = (vPoints[24][1]+vPoints[23][1])/2
	hip_mid_point = (hip_mid_x, hip_mid_y)

	head2hip_point = (shoulder_mid_x ,(vPoints[0][1]+hip_mid_y)/2)
	vertical_point = (shoulder_mid_x,0)

	vAngles = []

	#-- 肩肘手先の角度 --
	vAngles.append(point2Angle((vPoints[13], shoulder_mid_point, vPoints[15])))
	#-- 垂直(肩x)肩頭の角度 --
	vAngles.append(point2Angle((shoulder_mid_point, vertical_point, vPoints[0])))
	#-- 頭垂直(肩x)腰の角度 --
	vAngles.append(point2Angle((head2hip_point, vPoints[0], vertical_point)))

	# print('angles: arm,', vAngles[0], 'up,', vAngles[1], 'body,', vAngles[2])

	angleTF = [1 if (vAngles[i]<up_correct[i]) and (vAngles[i]>bottom_correct[i]) else 0 for i in range(3)]
	# print(angleTF)

	if (sum(angleTF) == 3):flag = True

	return flag
	
	
