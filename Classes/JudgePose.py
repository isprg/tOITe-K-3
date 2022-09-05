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

# 外積
def vec_cross(vec1, vec2):
	a = np.cross(vec1, vec2)
	if a > 0:
		return 1
	elif a < 0:
		return -1
	else:
		return 0

def draw_landamrks(img, points, line_pic, radius, line_color, circle_color):
	img_ = img.copy()

	for i, point in enumerate(points):
		if 0 <= point[0] <= img.shape[1] and 0<= point[1] <= img.shape[0]:
			pass
		else:
			continue

		if 0 <= i <= 10 or 17 <= i <= 22 or 29 <= i <= 32:
			continue

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
		if this_angle >= 180 :
			this_angle = 360 - this_angle
		if correctAngle - sJudgeMargin <= this_angle and this_angle <= correctAngle + sJudgeMargin:
			flag = True


	return flag
