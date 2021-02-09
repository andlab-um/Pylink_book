#!/usr/bin/env python3## Filename: heatmap_simple.py# Author: Zhiguo Wang# Date: 2/8/2021## Description:# Extract fixations from the ASC file to create a heatmapimport osimport refrom PIL import Image, ImageOpsimport numpy as npfrom matplotlib import cm  # colormap from matplotlibcmd = 'edf2asc freeview/freeview.edf'os.popen(cmd).read()# open the converted ASC fileasc = open('freeview/freeview.asc', 'r')alpha = 0.5  # transparency for the heatmaptrial_start = Falsetrial_number = 0scn_w, scn_h = [-32768, -32768]for line in asc:    # Extract all numerical values from a data line    values = [float(x) for x in re.findall(r'-?\d+\.?\d*', line)]    # Get the correct screen resolution from the GAZE_COORDS message    # MSG	4302897 DISPLAY_COORDS 0 0 1279 799    if re.search('DISPLAY_COORDS', line):        scn_w = int(values[-2]) + 1        scn_h = int(values[-1]) + 1    # message marking image onset    if re.search('image_onset', line):          trial_start = True        trial_number += 1        print(f'processing trial # {trial_number}...')        # creat a meshgrid to construct the heatmap        w, h = np.meshgrid(np.linspace(0, scn_w, scn_w),                           np.linspace(0, scn_h, scn_h))        heatmap = np.exp(-w**2 - h**2) * 0    if trial_start:        if re.search('EFIX R', line):            # EFIX R 80790373 80790527 155 855.5 596.0 881 63.60 63.75            start_t, end_t, duration, x, y, peak_vel, res_x, res_y = values                        # add the new fixation to the heatmap            heatmap += duration * np.exp(-1.0*(w - x)**2/(2*res_x**2) -                                         1.0*(h - y)**2/(2*res_y**2))        # Get the path to the background image         # MSG	3558923 !V IMGLOAD FILL images\woods.jpg        if 'IMGLOAD' in line:            bg_image = line.rstrip().split()[-1]    if re.search('image_offset', line):  # a message marking image offset        pic = Image.open(bg_image)        background_pic = pic.resize((scn_w, scn_h))  # resize the image                # Apply a colormap (from the colormap library of MatplotLib)        heatmap = heatmap/np.max(heatmap)        heatmap = Image.fromarray(np.uint8(cm.seismic(heatmap)*255))                # blending        heatmap = Image.blend(background_pic, heatmap, alpha)                # Save the heatmap as an PNG file        heatmap.save(f'heatmap_trial_{trial_number}.png', 'PNG')        trial_start = Falseasc.close()  # close the ASC file