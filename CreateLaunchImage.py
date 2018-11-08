#!/usr/bin/env
# -*- coding: utf-8 -*-

import os
import io
from PIL import Image
import json

import tkMessageBox


kConfigFile = "LaunchImageCfg.json"

def scale9Image(img, dst_size, box = None):
    '''
    defaul 1/3 scale
    :九宫格
    +--+--+--+
    |  |  |  |
    +--+--+--+
    |  |  |  |
    +--+--+--+
    |  |  |  |
    +--+--+--+
    '''
    img_size = img.size
    img_width = img_size[0]
    img_heigh = img_size[1]

    if box == None:
        box = [img_width/3, img_heigh/3, img_width*2/3, img_heigh*2/3]
    box_lt = (0, 0, box[0], box[1])
    box_tt = (box[0], 0, box[2], box[1])
    box_rt = (box[2], 0, img_width, box[1])

    box_ll = (0, box[1], box[0], box[3])
    box_cc = (box[0], box[1], box[2], box[3])
    box_rr = (box[2], box[1], img_width, box[3])

    box_lb = (0, box[3], box[0], img_heigh)
    box_bb = (box[0], box[3], box[2], img_heigh)
    box_rb = (box[2], box[3], img_width, img_heigh)

    img_lt = img.crop(box_lt)
    # img_lt.save("lt.png")
    img_tt = img.crop(box_tt)
    # img_tt.save("tt.png")
    img_rt = img.crop(box_rt)
    # img_rt.save("rt.png")
    img_ll = img.crop(box_ll)
    # img_ll.save("ll.png")
    img_cc = img.crop(box_cc)
    # img_cc.save("cc.png")
    img_rr = img.crop(box_rr)
    # img_rr.save("rr.png")
    img_lb = img.crop(box_lb)
    # img_lb.save("lb.png")
    img_bb = img.crop(box_bb)
    # img_bb.save("bb.png")
    img_rb = img.crop(box_rb)
    # img_rb.save("rb.png")

    dst_width = dst_size[0]
    dst_height = dst_size[1]

    cl = dst_height - img_lt.height - img_lb.height
    ct = dst_width - img_lt.width - img_rt.width
    cr = dst_height - img_lt.height - img_lb.height
    cb = dst_width - img_lt.width - img_rt.width

    new_img_tt = img_tt.resize((ct, img_tt.height))
    # new_img_tt.save("new_tt.png")
    new_img_ll = img_ll.resize((img_ll.width, cl))
    # new_img_ll.save("new_ll.png")
    new_img_rr = img_rr.resize((img_rr.width, cr))
    # new_img_rr.save("new_rr.png")
    new_img_bb = img_bb.resize((cb, img_bb.height))
    # new_img_bb.save("new_bb.png")
    new_img_cc = img_cc.resize((ct, cl))
    # new_img_cc.save("new_cc.png")

    base_img = Image.new('RGBA', (dst_width, dst_height))


    base_img.paste(img_lt, box_lt)
    base_img.paste(new_img_tt, (box[0], 0, box[0] + new_img_tt.width, new_img_tt.height))
    base_img.paste(img_rt, (box[0] + new_img_tt.width, 0, box[0] + new_img_tt.width + img_rt.width, img_rt.height))

    base_img.paste(new_img_ll, (0, box[1], new_img_ll.width, box[1] + new_img_ll.height))
    base_img.paste(new_img_cc, (box[0], box[1], box[0] + new_img_cc.width, box[1] + new_img_cc.height))
    st_x = box[0] + new_img_cc.width
    st_y = box[1]
    base_img.paste(new_img_rr, (st_x, st_y, st_x + new_img_rr.width, st_y + new_img_rr.height))

    st_x = 0
    st_y = box[1] + new_img_ll.height
    base_img.paste(img_lb, (st_x, st_y, st_x + img_lb.width, st_y + img_lb.height))
    st_x = box[0]
    st_y = box[1] + new_img_cc.height
    base_img.paste(new_img_bb, (st_x, st_y, st_x + new_img_bb.width, st_y + new_img_bb.height))
    st_x = box[0] + new_img_cc.width
    st_y = box[1] + new_img_cc.height
    base_img.paste(img_rb, (st_x, st_y, st_x + img_rb.width, st_y + img_rb.height))

    return base_img

def createLauncherImage(img, (img_w, img_h)):
    w = img.width
    h = img.height
    scale_x = w*1.0/img_w
    scale_y = h*1.0/img_h
    factor = scale_y
    if scale_x < scale_y:
        factor = scale_x

    dst_w = int(w/factor)
    dst_h = int(h/factor)
    dst_img = img.resize((dst_w, dst_h))

    start_x = (dst_w - img_w)/2
    start_y = (dst_h - img_h)/2

    base_img = dst_img.crop((start_x, start_y, start_x + img_w, start_y + img_h))

    return base_img




def loadCfg():
    fp = io.open(kConfigFile, "r")
    if fp == None:
        print("open file error")

    cfgData = json.load(fp)

    allList = cfgData["launch_image"]

    img = Image.open("image_input/launch_image.png")
    leftRotateImg = img.transpose(Image.ROTATE_90)

    print("init image width:height {}:{}".format(leftRotateImg.width, leftRotateImg.height))

    dstDir = "launchimage"
    curdir = os.path.abspath(dstDir)
    if not os.path.isdir(curdir):
        os.makedirs(curdir)
    for k in allList:
        print(str(k))
        file_name = k["file_name"]
        width = k["width"]
        height = k["height"]

        print("gen launch image {} width:{} height:{}".format(file_name, width, height))
        if img:
            #new_img = img.resize([width, height],box=[200,200,400,400])
            #new_img = scale9Image(img, (200, 200))
            if width < height:
                new_img = createLauncherImage(leftRotateImg, (width, height))
                new_img.save(dstDir + "/" + file_name + ".png")
            else:
                new_img = createLauncherImage(img, (width, height))
                new_img.save(dstDir + "/" + file_name + ".png")

    fp.close()





def main():
    loadCfg()
    pass

if __name__ == "__main__":
    main()
