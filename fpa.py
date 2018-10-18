import quaternion
import math
import numpy as np
import fpa_parameter

def fpa(sensor):
    
    gyro_x = sensor.sensor_data.gyroscope.gyro_x
    gyro_y = sensor.sensor_data.gyroscope.gyro_y
    gyro_z = sensor.sensor_data.gyroscope.gyro_z 
    q = [0,0,0,0]
    q[0] = sensor.sensor_data.quaternion.qua1
    q[1] = sensor.sensor_data.quaternion.qua2
    q[2] = sensor.sensor_data.quaternion.qua3
    q[3] = sensor.sensor_data.quaternion.qua4 

    q_conj = quaternion.quatern_conj_program(q)

    q_acc_s = [0,0,0,0]
    q_acc_s[0] = 0
    q_acc_s[1] = sensor.sensor_data.acceleration.acc_x
    q_acc_s[2] = sensor.sensor_data.acceleration.acc_y
    q_acc_s[3] = sensor.sensor_data.acceleration.acc_z

    q_temp = quaternion.quaternprod(q_acc_s,q_conj)
    q_acc_g = quaternion.quaternprod(q,q_temp)
    q_acc_g[3] = q_acc_g[3] - fpa_parameter.gravity_world_constant

    gryoscope_norm = math.sqrt(gyro_x*gyro_x + gyro_y*gyro_y + gyro_z*gyro_z)
    #print(gyro_x)
    #print(gyro_y)
    #print(gyro_z)
    #if gryoscope_norm > 0.8:
        #print(gryoscope_norm)
    if fpa_parameter.zupt_state == fpa_parameter.swing:
        if gryoscope_norm <= fpa_parameter.zupt_gryo_threshold:
            fpa_parameter.zupt_count =fpa_parameter.zupt_count + 1
            print("count" + str(fpa_parameter.zupt_count))
            if fpa_parameter.zupt_count > fpa_parameter.swing_count_threshold:
                fpa_parameter.zupt_state = fpa_parameter.stance
                fpa_parameter.zupt_count = 0
                fpa_parameter.flag_swing_to_stance = 1
        else:
            fpa_parameter.zupt_count = 0
            fpa_parameter.flag_swing_to_stance = 0
            fpa_parameter.flag_stance_to_swing = 0
            
    else:
        if gryoscope_norm >= fpa_parameter.zupt_gryo_threshold:
            fpa_parameter.zupt_count = fpa_parameter.zupt_count +1
            print("stancecount:"+ str(fpa_parameter.zupt_count))
            if fpa_parameter.zupt_count > fpa_parameter.stance_count_threshold:
                fpa_parameter.zupt_state = fpa_parameter.swing
                fpa_parameter.zupt_count = 0
                fpa_parameter.flag_stance_to_swing = 1
        else:
            fpa_parameter.zupt_count = 0
            fpa_parameter.flag_swing_to_stance = 0
            fpa_parameter.flag_stance_to_swing = 0

    # Integrate acceleration minus gravity
    temp = fpa_parameter.dt*fpa_parameter.gravitational_acceleration_constant
    if fpa_parameter.zupt_state == fpa_parameter.stance:
        velocity_world_x = 0
        velocity_world_y = 0
        velocity_world_z = 0
    else:
        velocity_world_x = fpa_parameter.velocity_world_x_old + q_acc_g[1]*temp
        velocity_world_y = fpa_parameter.velocity_world_y_old + q_acc_g[2]*temp
        velocity_world_z = fpa_parameter.velocity_world_z_old + q_acc_g[3]*temp
    temp = fpa_parameter.dt
    position_world_x = fpa_parameter.position_world_x_old + velocity_world_x * temp
    position_world_y = fpa_parameter.position_world_y_old + velocity_world_y * temp
    position_world_z = fpa_parameter.position_world_z_old + velocity_world_z * temp

    # Heading vector
    heading_vector_x = position_world_x - fpa_parameter.position_world_x_lasttime
    heading_vector_y = position_world_y - fpa_parameter.position_world_y_lasttime
    heading_vector_z = position_world_z - fpa_parameter.position_world_z_lasttime

    if heading_vector_x ==0 and heading_vector_y == 0 and heading_vector_z ==0:
        heading_vector_norm_temp_x = 0
        heading_vector_norm_temp_y = 0
        heading_vector_norm_temp_z = 0
    else:
        temp = math.sqrt(heading_vector_x*heading_vector_x + heading_vector_y*heading_vector_y +heading_vector_z*heading_vector_z)
        heading_vector_norm_temp_x = heading_vector_x/temp
        heading_vector_norm_temp_y = heading_vector_y/temp
        heading_vector_norm_temp_z = heading_vector_z/temp


    heading_vector_x = (1-fpa_parameter.fpa_weight)*fpa_parameter.heading_vector_x_old + fpa_parameter.fpa_weight*heading_vector_norm_temp_x
    heading_vector_y = (1-fpa_parameter.fpa_weight)*fpa_parameter.heading_vector_y_old + fpa_parameter.fpa_weight*heading_vector_norm_temp_y
    heading_vector_z = (1-fpa_parameter.fpa_weight)*fpa_parameter.heading_vector_z_old + fpa_parameter.fpa_weight*heading_vector_norm_temp_z

    if heading_vector_x == 0 and heading_vector_y == 0 and heading_vector_z ==0:
        heading_vector_norm_temp_x = 0
        heading_vector_norm_temp_y = 0
        heading_vector_norm_temp_z = 0
    else:
        temp = math.sqrt(heading_vector_x*heading_vector_x + heading_vector_y*heading_vector_y +heading_vector_z*heading_vector_z)
        heading_vector_norm_temp_x = heading_vector_x/temp
        heading_vector_norm_temp_y = heading_vector_y/temp
        heading_vector_norm_temp_z = heading_vector_z/temp

    # Foot Vector
    q_foot_vector_calibration = [0,0,0,0]
    q_foot_vector_calibration[0] = 0
    q_foot_vector_calibration[1] = 0
    q_foot_vector_calibration[2] = 1
    q_foot_vector_calibration[3] = 0

    q_temp = quaternion.quaternprod(q_foot_vector_calibration, q_conj)
    q_foot_vector = quaternion.quaternprod(q,q_temp)
    temp = math.sqrt(q_foot_vector[0]*q_foot_vector[0]+q_foot_vector[1]*q_foot_vector[1]+q_foot_vector[2]*q_foot_vector[2]+q_foot_vector[3]*q_foot_vector[3])
    q_foot_vector[0] = q_foot_vector[0]/temp
    q_foot_vector[1] = q_foot_vector[1]/temp
    q_foot_vector[2] = q_foot_vector[2]/temp
    q_foot_vector[3] = q_foot_vector[3]/temp

    temp2 = math.sqrt(q_foot_vector[1]*q_foot_vector[1]+q_foot_vector[2]*q_foot_vector[2])
    temp3 = math.sqrt(fpa_parameter.heading_vector_x_old*fpa_parameter.heading_vector_x_old+fpa_parameter.heading_vector_y_old*fpa_parameter.heading_vector_y_old)
    temp4 = q_foot_vector[1]*fpa_parameter.heading_vector_x_old + q_foot_vector[2]*fpa_parameter.heading_vector_y_old
    print('state:'+str(fpa_parameter.zupt_state))
    print('temp2:'+str(temp2))
    print('temp3:'+str(temp3))
    print('temp4:'+str(temp4))
    if temp2 != 0 and temp3 != 0:
        if q_foot_vector[2]*fpa_parameter.heading_vector_x_old - q_foot_vector[1]*fpa_parameter.heading_vector_y_old:
            fpa_temp = math.acos(temp4/temp3/temp2)*180/math.pi
        else:
            fpa_temp = -math.acos(temp4/temp3/temp2)*180/math.pi
    else:
        fpa_temp = 0

    if  fpa_parameter.zupt_state == fpa_parameter.stance and fpa_parameter.stance_time<=15:
        if np.isnan(fpa_temp) == False:
            fpa_parameter.fpa_sum = fpa_parameter.fpa_sum+fpa_temp
            fpa_parameter.fpalist.append(fpa_parameter.fpa_sum)
            #print(fpa_parameter.fpalist)
        fpa_parameter.stance_time = fpa_parameter.stance_time +1
        #print("stancetime" + str(fpa_parameter.stance_time))
    
    if fpa_parameter.flag_swing_to_stance == 1:
        fpa_parameter.position_world_x_last_time = position_world_x
        fpa_parameter.position_world_y_last_time = position_world_y
        fpa_parameter.position_world_z_last_time = position_world_z
        
        if np.isnan(heading_vector_norm_temp_x)== False:
            fpa_parameter.heading_vector_x_old = heading_vector_norm_temp_x
        if np.isnan(heading_vector_norm_temp_y)== False:          
            fpa_parameter.heading_vector_y_old = heading_vector_norm_temp_y
        if np.isnan(heading_vector_norm_temp_z)== False:         
            fpa_parameter.heading_vector_z_old = heading_vector_norm_temp_z

    if fpa_parameter.flag_stance_to_swing == 1:
        if fpa_parameter.stance_time>0:
            fpa_parameter.fpa_result = fpa_parameter.fpa_sum/fpa_parameter.stance_time
        else:
            fpa_parameter.fpa_result =360
        fpa_parameter.fpa_sum = 0
        fpa_parameter.stance_time = 0
        fpa_parameter.step_count = fpa_parameter.step_count +1

        

    '''if np.isnan(q_acc_g[1])== False:
        fpa_parameter.acceleration_world_x_old = q_acc_g[1]
    if np.isnan(q_acc_g[2])== False:
        fpa_parameter.acceleration_world_y_old = q_acc_g[2]
    if np.isnan(q_acc_g[3])== False:
        fpa_parameter.acceleration_world_z_old = q_acc_g[3]'''
    if np.isnan(velocity_world_x)== False:
        fpa_parameter.velocity_world_x_old = velocity_world_x
    if np.isnan(velocity_world_y)== False:
        fpa_parameter.velocity_world_y_old = velocity_world_y
    if np.isnan(velocity_world_z)== False:
        fpa_parameter.velocity_world_z_old = velocity_world_z

    if np.isnan(position_world_x)== False:
        fpa_parameter.position_world_x_old = position_world_x
    if np.isnan(position_world_y)== False:
        fpa_parameter.position_world_y_old = position_world_y
    if np.isnan(position_world_z)== False:
        fpa_parameter.position_world_z_old = position_world_z

    print('stance_to_swing:'+str(fpa_parameter.flag_stance_to_swing))
    print('swing_to_stance:'+str(fpa_parameter.flag_swing_to_stance))
    fpa_parameter.flag_stance_to_swing = 0
    fpa_parameter.flag_swing_to_stance = 0
    
    if fpa_parameter.fpa_result !=0:
        return fpa_parameter.fpa_result, fpa_parameter.step_count

    else:
        return 0, 0


