height = 2 #height in meters

def node_distance(node1, node2):
	"""
	calculates euclidean distance between 2 3dim nodes, NOT VECTOR
	"""
	[x1, y1, z1] = node1
	[x2, y2, z2] = node2
	
	dist = sqrt( (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2 )
	return dist


def center_of_nodes(node1, node2, multiplier=0.5):
	"""
	calculates centerpoint of 2 nodes. can specify multipler to any value to find 0.xx along line from node1 to node2
	"""
	[x1, y1, z1] = node1
	[x2	, y2, z2] = node2
	scaled_vector_from_1to2 = [ (x2 - x1)*multiplier , (y2 - y1)*multiplier , (z2 - z1)*multiplier ]
	 
	[x_ans, y_ans, z_ans] = scaled_vector_from_1to2
	#add node1 values to start vector from node1 - gives use value multiplier away from node1 to node2
	x_ans += x1
	y_ans += y1
	z_ans += z1

	return [x_ans, y_ans, z_ans]

def within_half_sphere(center_coord, point, radius):
	"""
	checks if point is within half sphere defined by center coord
	returns 1 for above, -1 for below, 0 for failure. All checked along y-axis	
	"""
	x, y, z = point
	x_c, y_c, z_c = center_coord
	distance_squared = (x - x_c)**2 + (y - y_c)**2 + (z - z_c)**2
	
	if distance_squared <= radius**2:#within sphere!
		return True
	else:
		return False

def cos_theta_vectors(v1, v2):
	"""
	returns cos(theta) of two vectors using dot product. strictly positive
	"""
	[x1, y1, z1] = v1
	[x2	, y2, z2] = v2
	
	numerator = abs( x1*x2 + y1*y2 + z1*z2 )
	abs_v1 = sqrt( x1**2 + y1**2 + z1**2 )
	abs_v2 = sqrt( x2**2 + y2**2 + z2**2 )
	
	return numerator/abs_v1/abs_v2


def is_hold_valid(rh, lh, rf, lf): #sideness , and hand or foot
	"""
	checks if a hold is valid by calculating if a body center is within distance of nodes
	see function comments for alg
	"""
	
	#return values initialized in "false" configuration (if not valid)
	return_bool = False
	body_center = -1

	shoulder_multiplier = 0.85
	waist_multiplier = 0.5
	
	wingspan = height
	shoulder_h = height * shoulder_multiplier
	vert_reach = height * 1.35 #arm length + shoulder_h, armlen is wingspan/2
	arm_len = 0.5 * wingspan
	leg_len = waist_multiplier * height
	

	hand_dist = node_distance(rh, lh)
	foot_dist = node_distance(rf, lf)

	hand_center = center_of_nodes(rh, lh)
	foot_center = center_of_nodes(rf, lf)
	
	theoret_body_len = node_distance(foot_center, hand_center)
	theoret_body_center = center_of_nodes(foot_center, hand_center)
	
	#legs spreading out causes effective height to lower. calcing this height dif
	#geometrically. Needs effective height vector and foot vector
	[fc_x, fc_y, fc_z] = foot_center
	[hc_x, hc_y, hc_z] = hand_center

	[lf_x, lf_y, lf_z] = lf
	[rf_x, rf_y, rf_z] = rf
	foot_vector = [lf_x - rf_x, lf_y - rf_y, lf_z - rf_z]
	body_vector = [fc_x - hc_x, fc_y - hc_y, fc_z - hc_z] 

	height_dif = leg_len * cos_theta_vectors(foot_vector, body_vector)
	effective_vert_reach = vert_reach - height_dif

	#finding shoulder_multiplier for theoret_body_len
	theoret_len_should_mult = shoulder_multiplier * height / theoret_body_len
	#theoret_len_waist_mult = waist_multiplier * height / theoret_body_len

	#these positions will be used as the center of spheres to see if holds are within reach of the person! 
	shoulder_pos = center_of_nodes(foot_center, hand_center, theoret_len_should_mult)
	#waist_pos = center_of_nodes(foot_center, hand_center, theoret_len_waist_mult)
	
	
	#if theoret_body_len <= shoulder_h and hand_dist <= wingspan and foot_dist <= wingspan:
	#	#arms legs can reach up to wingspan distance
	#	return_bool = True
	# not needed anymore, the sphere calculations are sufficient to covering this condition more accurately

	if theoret_body_len <= effective_vert_reach and foot_dist <= wingspan and hand_dist <= wingspan:
		#check if arms are within sphere with radius armlen if the hand nodes are above the shoulders!
		
		#first check if hand_dist is in upper or lower half of sphere (do this by checking some sphere with some large radius (here, 2*r)
		lh_con = within_half_sphere(shoulder_pos, lh, 2*arm_len)
		rh_con = within_half_sphere(shoulder_pos, rh, 2*arm_len)

		#if both negative, return true. if one of them positive, recalculate with appropriate radius
		#we return true if negative regardless of if the arms are within the sphere relative to shoulders, as irl you can just
		# bend your torso down, meaning your arms functionally can always be at wingspan distance apart (and conditional already
		# checks that they arent larger than wingspan!!)
		
		if lh_con == 1:
			lh_con = within_half_sphere(shoulder_pos, lh, arm_len)
		if rh_con == 1:
			rh_con = within_half_sphere(shoulder_pos, lh, arm_len)

		if lh_con and rh_con: #wont pass through if one of them is zero!!!
			return_bool = True


	if return_bool: body_center = theoret_body_center

	return [return_bool, body_center]
