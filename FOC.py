import numpy as np

class FOC(object):
    def __init__(self, i_d=0, i_q=1, speed=1, theta=45):
        self.i_d = i_d
        self.i_q = i_q
        self.theta = theta
        self.speed = speed

    # 通过当前角度转换返回弧度radian
    def d2r(self, degree):
        return self.speed*degree*np.pi/180

    # 通过Id, Iq计算Ia,Ib,Ic
    def dq2abc(self):
        # park转换矩阵
        park_matrix = np.array((
            [np.cos(self.d2r(self.theta)), np.sin(self.d2r(self.theta))],
            [-np.sin(self.d2r(self.theta)), np.cos(self.d2r(self.theta))]
        ))
        # dq矩阵
        dq_matrix = np.array(([self.i_d, self.i_q]))
        # dq矩阵 和 park转换矩阵 矩阵乘积 得到 alpha_beta矩阵
        alpha_beta_matrix = np.dot(dq_matrix, park_matrix)

        # clart转换矩阵
        clart_matrix = np.array((
            [1, -0.5, -0.5],
            [0, np.sqrt(3) / 2, -np.sqrt(3) / 2]
        ))

        # (_, sample_num) = alpha_beta_matrix.shape
        # print(sample_num)
        # print(alpha_beta_matrix.shape)
        num_dimension = alpha_beta_matrix.ndim
        # alpha_beta矩阵 和 clart转换矩阵 矩阵乘积 得到 a_b_c矩阵
        if num_dimension == 1:
            a_b_c_matrix = np.dot(alpha_beta_matrix, clart_matrix)
        elif num_dimension == 2:
            _, sample_num = alpha_beta_matrix.shape
            a_b_c_matrix = np.zeros((3, sample_num))
            for i in range(sample_num):
                a_b_c_matrix[:, i] = np.dot(alpha_beta_matrix[:, i], clart_matrix)

        return a_b_c_matrix

    def set_id(self, i_d):
        self.i_d = i_d

    def set_iq(self, i_q):
        self.i_q = i_q

    def set_speed(self, speed):
        self.speed = speed

    def set_theta(self, theta):
        self.theta = theta


    def get_id(self):
        return self.i_d

    def get_iq(self):
        return self.i_q

    def get_speed(self):
        return self.speed

    def get_theta(self):
        return self.theta


if __name__ == '__main__':
    foc = FOC()
    a_b_c = foc.dq2abc()
    print(a_b_c)

    foc.set_theta(359)
    a_b_c = foc.dq2abc()
    print('359', a_b_c)

    foc.set_theta(360)
    a_b_c = foc.dq2abc()
    print('360', a_b_c)

    foc.set_theta(0)
    a_b_c = foc.dq2abc()
    print('0', a_b_c)




    x = np.linspace(0, 360, 360)
    foc.set_theta(x)
    a_b_c = foc.dq2abc()
    print(a_b_c)











