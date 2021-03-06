import argparse
import numpy as np
import math
import torch
import sys 
import os
import pdb
from os.path import join
import matplotlib.pyplot as plt
# from visualize import *
sys.path.append(".")
# from models import *


# def identity3d_tensor(dim):
#     step = np.arange(0,dim)/(dim-1) # Double, so need to specify dtype
#     rgb = torch.tensor(step, dtype=torch.float32).expand(3, dim) # n,c,dim
#     LUT = torch.empty(3,dim,dim,dim)
#     LUT[0] = rgb[0].unsqueeze(0).unsqueeze(0).repeat(dim, dim, 1) # r
#     LUT[1] = rgb[1].unsqueeze(1).unsqueeze(0).repeat(dim, 1, dim) # g
#     LUT[2] = rgb[2].unsqueeze(1).unsqueeze(1).repeat(1, dim, dim) # b
#     return LUT
def identity3d_tensor(dim): # 3,d,d,d
    step = np.arange(0,dim)/(dim-1) # Double, so need to specify dtype
    rgb = torch.tensor(step, dtype=torch.float32)
    LUT = torch.empty(3,dim,dim,dim)
    LUT[0] = rgb.unsqueeze(0).unsqueeze(0).expand(dim, dim, dim) # r
    LUT[1] = rgb.unsqueeze(-1).unsqueeze(0).expand(dim, dim, dim) # g
    LUT[2] = rgb.unsqueeze(-1).unsqueeze(-1).expand(dim, dim, dim) # b
    return LUT

def identity2d_tensor(dim): # 2,d,d
    # Double, so need to specify dtype
    step = torch.tensor(np.arange(0,dim)/(dim-1), dtype=torch.float32)
    hs = torch.empty(2,dim,dim)
    hs[0] = step.unsqueeze(0).repeat(dim, 1) # r
    hs[1] = step.unsqueeze(1).repeat(1, dim) # g
    return hs
    
def identity1d_tensor(dim): # 1,d
    step = np.arange(0,dim)/(dim-1) # Double, so need to specify dtype
    return torch.tensor(step, dtype=torch.float32).unsqueeze(0)

def random_curve(num, dim, mode="resp"): # return num, dim
    res = identity1d_tensor(dim).repeat(num, 1)
    for i in range(num):
        gain = np.random.uniform(0.9,2)
        gamma = np.random.uniform(1,4)
        if np.random.uniform(-1,1) > 0:
            gamma = 1/gamma
        bias = np.random.uniform(-0.2,0.2)
        res[i] = torch.clip(torch.pow(res[i]*gain, gamma) + bias, 0, 1)
        # draw_curve(res[i],title="gain=%f, gamma=%f, bias=%f" % (gain, gamma, bias))
        # y = res[i].reshape(1,dim)
        # plt.plot(np.arange(0,dim)/(dim-1), y[0].numpy(), c="r", linewidth=10, )
        # plt.plot(np.arange(0,dim)/(dim-1), y[1].numpy(), c="g", linewidth=5, label="wb=%f, gamma=%f, bias=%f" % (wb[1], gamma[1], bias[1]))
        # plt.plot(np.arange(0,dim)/(dim-1), y[2].numpy(), c="b", linewidth=2, label="wb=%f, gamma=%f, bias=%f" % (wb[2], gamma[2], bias[2]))
        # plt.axvline(0, ls=":")
        # plt.axvline(1, ls=":")
        # plt.axhline(0, ls=":")
        # plt.axhline(1, ls=":")
        # plt.ylim((-0.5,1.5))
        # plt.xlim((-0.5,1.5))
        # # plt.show()
        # plt.legend()
        # plt.pause(1)
        # plt.clf()
    return res
    
if __name__ == "__main__":
    pass
    # random_curve(128, 33)

# ????????????????????????
idt3d = identity3d_tensor(8)
# print(idt3d[0,0,0,:])
# print(idt3d[0,4,4,:])

# print(idt3d[2,:,0,0])
# print(idt3d[2,:,4,4])

# print(idt3d[0,:,:,0])
# print(idt3d[0,:,:,1])
# print(idt3d[0,:,:,7])

# print(idt3d[2,0,:,:])
# print(idt3d[2,1,:,:])
# print(idt3d[2,7,:,:])

def writedown_identity_3DLUT(dim, output_file):
    step = 1.0 / (dim - 1)
    with open(output_file, 'w') as f:
        for k in range(dim):
            for j in range(dim):
                for i in range(dim):
                    f.write('{:.6f}  {:.6f}  {:.6f}\n'.format(step * i, step * j, step * k))

def writedown_gamma_3DLUT(dim, output_file, gamma=1):
    step = np.arange(0,dim)/(dim-1)
    print(step)
    step = np.power(step, 1/gamma)
    print(step)
    with open(output_file, 'w') as f:
        for k in range(dim):
            for j in range(dim):
                for i in range(dim):
                    f.write('{:.6f}  {:.6f}  {:.6f}\n'.format(step[i], step[j], step[k]))

# n,3,ddd  n,3
# or
# 3,ddd  3
def cube_wb(cube, wb):
    if len(cube.shape) == 4:
        cube[0,:,:,:] *= wb[0]
        cube[1,:,:,:] *= wb[1]
        cube[2,:,:,:] *= wb[2]
    else:
        wb = wb.unsqueeze(-1).unsqueeze(-1).unsqueeze(-1)
        cube[:,0] *= wb[:,0]
        cube[:,1] *= wb[:,1]
        cube[:,2] *= wb[:,2]
    return cube
# n,3,d  n,3
# or
# 3,d  3
def curve_wb(curve, wb):
    if len(curve.shape) == 2:
        cube[0] *= wb[0]
        cube[1] *= wb[1]
        cube[2] *= wb[2]
    else:
        wb = wb.unsqueeze(-1)
        cube[:,0] *= wb[:,0]
        cube[:,1] *= wb[:,1]
        cube[:,2] *= wb[:,2]
    return curve

def writedown_wb_3DLUT(dim, output_file, wb=[0.82943738, 1.02267336, 1.2246885]):# r,g,b
    step = np.arange(0,dim)/(dim-1)
    print(step)
    steps = []
    for scale in wb:
        steps.append(step * scale)
    with open(output_file, 'w') as f:
        for k in range(dim):
            for j in range(dim):
                for i in range(dim):
                    f.write('{:.6f}  {:.6f}  {:.6f}\n'.format(steps[0][i], steps[1][j], steps[2][k]))

def read_3dlut_from_file(file_name, return_type="tensor"):
    file = open(file_name, 'r')
    lines = file.readlines()
    start, end = 0, 0 # ???cube???????????????
    for i in range(len(lines)):
        if lines[i][0].isdigit() or lines[i].startswith("-"):
            start = i
            break
    for i in range(len(lines)-1,start,-1):
        if lines[i][0].isdigit() or lines[i].startswith("-"):
            end = i
            break
    lines = lines[start: end+1]
    if len(lines) == 262144:
        dim = 64
    elif len(lines) == 35937:
        dim = 33
    else:
        dim = int(np.round(math.pow(len(lines), 1/3)))
    print("dim = ", dim)
    buffer = np.zeros((3,dim,dim,dim), dtype=np.float32)
    # ???lut????????????????????????rgb
    # r???????????????????????????b??????????????????
    # ????????????????????????k????????????????????????????????????????????????
    # ??????LUT???????????? cbgr?????????c??? rgb
    for i in range(0,dim):# b
        for j in range(0,dim):# g
            for k in range(0,dim):# r
                n = i * dim*dim + j * dim + k
                x = lines[n].split()
                buffer[0,i,j,k] = float(x[0])# r
                buffer[1,i,j,k] = float(x[1])# g
                buffer[2,i,j,k] = float(x[2])# b

    if return_type in["numpy", "np"]:
        return buffer
    elif return_type in["tensor", "ts"]:
        return torch.from_numpy(buffer)
        # buffer = torch.zeros(3,dim,dim,dim) # ?????????torch???????????????????????????np????????????torch
    else:
        raise ValueError("return_type should be np or ts")

def read_3dlut_from_ckp_to_np(file_name, dim, idx=-1):
    ckp = torch.load(file_name)
    if idx >= 0:
        lut = LUT3D_zero(dim)
        lut.load_state_dict(ckp[str(idx)])
        return lut.LUT.detach().numpy()
    else:
        luts = []
        for i in range(len(LUTs_ckp)):
            lut = LUT3D_zero(dim)
            lut.load_state_dict(ckp[str(i)])
            luts.append(lut.LUT.detach().numpy())
        return luts


# from visualize import draw3D

def from_1d1(v): # n,1,dim  or  n,-1  return n,1,dim,dim,dim
    n = v.shape[0]
    if len(v.shape) == 2: # ??????dim???reshape
        v = v.reshape(n, 1, -1)
    dim = v.shape[2]

    v = v.unsqueeze(-1).unsqueeze(-1) #n,1,d -> n,1,d,1,1
    v = v.expand(n,1,dim,dim,dim)
    return v

def from_3d1(rgb, LUT=None): # n,3,dim  or  n,-1
    n = rgb.shape[0]
    if len(rgb.shape) == 2: # ??????dim???reshape
        rgb = rgb.reshape(n, 3, -1)
    dim = rgb.shape[2]
    if LUT is None:
        LUT = torch.zeros(n, 3, dim, dim, dim).type(rgb.type())
        LUT[:,0] = rgb[:,0].unsqueeze(1).unsqueeze(1).expand(n, dim, dim, dim) # r
        LUT[:,1] = rgb[:,1].unsqueeze(1).unsqueeze(-1).expand(n, dim, dim, dim) # g
        LUT[:,2] = rgb[:,2].unsqueeze(-1).unsqueeze(-1).expand(n, dim, dim, dim) # b
    else:
        LUT[:,0] += rgb[:,0].reshape(n,1,1,dim).expand(n, dim, dim, dim) # r
        LUT[:,1] += rgb[:,1].reshape(n,1,dim,1).expand(n, dim, dim, dim) # g
        LUT[:,2] += rgb[:,2].reshape(n,dim,1,1).expand(n, dim, dim, dim) # b
        
    return LUT

# tp = (d1to3(identity1d_tensor(33).unsqueeze(0).expand(1,3,33))-read_3dlut_from_file("lut/IdentityLUT33.txt").unsqueeze(0))
# print( (tp.abs()<1e-6).all())

def from_1d2(hs): # n,2,dim,dim  or  n,2,-1  return n,2,dim,dim,dim
    n = hs.shape[0]
    if len(hs.shape) == 2:
        dim = int(np.sqrt(hs.shape[2]))
        hs = hs.reshape(n,2,dim,dim)
    dim = hs.shape[2]

    hs = hs.unsqueeze(2) # n,2,1,dim,dim
    hs = hs.expand(n,2,dim,dim,dim) # 1??? dim*dim ????????? dim??? dim*dim
    return hs

# hs: n,2,dim,dim  or  n,2,-1
# v: n,1,dim  or  n,-1
def from_1d1_1d2(v, hs): 
    n = v.shape[0]
    if len(v.shape) == 2:
        v = v.reshape(n,1,-1)
        dim = v.shape[2]
    if len(hs.shape) == 2:
        dim = int(np.sqrt(hs.shape[2]))
        hs = hs.reshape(n,2,dim,dim)
    dim = hs.shape[2]

    LUT = torch.empty(n, 3, dim, dim, dim).type(hs.type())
    hs = d2_1(hs)
    LUT[:,:2,...] = hs
    v = d1_1(v) # n,1,d,d,d
    LUT[:,2,...] = v[:,0]
    return LUT

# hs = identity2d_tensor(64).unsqueeze(0)
# v = identity1d_tensor(64).unsqueeze(0)
# hsv = d1_1_d2_1(v, hs)
# print(((hsv - identity3d_tensor(64).unsqueeze(0)).abs() < 1e-16).all())
# print(((hsv - read_3dlut_from_file("lut/IdentityLUT64.txt").unsqueeze(0)).abs() < 1e-6).all())

def cube_to_lut(cube): # (n,)3,d,d,d
    if len(cube.shape) == 5:
        to_shape = [
            [0,2,3,1],
            [0,2,1,3],
        ]
    else:
        to_shape = [
            [1,2,0],
            [1,0,2],
        ]
    if isinstance(cube, torch.Tensor):
        lut = torch.empty_like(cube)
        lut[...,0,:,:,:] = cube[...,0,:,:,:].permute(*to_shape[0])
        lut[...,1,:,:,:] = cube[...,1,:,:,:].permute(*to_shape[1])
        lut[...,2,:,:,:] = cube[...,2,:,:,:]
    else:
        lut = np.empty_like(cube)
        lut[...,0,:,:,:] = cube[...,0,:,:,:].transpose(*to_shape[0])
        lut[...,1,:,:,:] = cube[...,1,:,:,:].transpose(*to_shape[1])
        lut[...,2,:,:,:] = cube[...,2,:,:,:]
    return lut

def lut_to_cube(lut): # (n,)3,d,d,d
    if len(lut.shape) == 5:
        to_shape = [
            [0,3,1,2],
            [0,2,1,3],
        ]
    else:
        to_shape = [
            [2,0,1],
            [1,0,2],
        ]

    if isinstance(lut, torch.Tensor):
        cube = torch.empty_like(lut)
        cube[...,0,:,:,:] = lut[...,0,:,:,:].permute(*to_shape[0])
        cube[...,1,:,:,:] = lut[...,1,:,:,:].permute(*to_shape[1])
        cube[...,2,:,:,:] = lut[...,2,:,:,:]
    else:
        cube = np.empty_like(lut)
        cube[...,0,:,:,:] = lut[...,0,:,:,:].transpose(*to_shape[0])
        cube[...,1,:,:,:] = lut[...,1,:,:,:].transpose(*to_shape[1])
        cube[...,2,:,:,:] = lut[...,2,:,:,:]
    return cube
    
import matplotlib.pyplot as plt
if __name__ == '__main__':
    idt = identity1d_tensor(16).unsqueeze(0).expand(1,3,16)
    draw3D(from_3d1(idt)[0])
    # root = "../LUT"
    # save_root = "../LUT_np/"
    # os.makedirs(save_root, exist_ok=True)
    # ls = os.listdir(root)
    # for name in ls:
    #     path = os.path.join(root, name)
    #     lut = read_3dlut_from_file(path, "np")
    #     np.save(os.path.join(save_root, name), lut)
        # torch.save(lut, os.path.join(save_root, "%s.pth" % name))

    # plt.get_current_fig_manager().full_screen_toggle()
    # draw_inverse(identity_tensor(16))
    # root = "lut/3/"
    # ls = os.listdir(root)
    # gt_root2 = "../??????????????????/new_save_models/Pre/fiveK-LUT3D-16 tv:0.0001 mn:0.0"
    # gt_ls2 = sorted(os.listdir(gt_root2))
    # for i in range(10):
    #     gt2 = torch.load(join(gt_root2, gt_ls2[1]))["LUT"].detach().cpu().numpy()
    #     draw_inverse(gt2)
    #     plt.pause(2)
    #     plt.clf()
    # draw_inverse(read_3dlut_from_file(root+ls[0]))
    # draw_inverse(torch.load(root+ls[0]))