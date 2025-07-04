import cv2
import numpy as np
import subprocess
import os
import random

def euclidean_dist(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def get_int_input(prompt, default):
    val = input(f"{prompt} [default: {default}]: ").strip()
    return int(val) if val.isdigit() else default

def get_float_input(prompt, default):
    val = input(f"{prompt} [default: {default}]: ").strip()
    try:
        return float(val)
    except:
        return default

def get_yes_no_input(prompt, default='y'):
    val = input(f"{prompt} [y/n, default: {default}]: ").strip().lower()
    if val in ['y', 'yes']:
        return True
    elif val in ['n', 'no']:
        return False
    else:
        return default.lower() in ['y', 'yes']

def main():
    input_video = input("Enter input video filename [default: input.mp4]: ").strip() or "input.mp4"
    output_video = input("Enter output video filename [default: output.mp4]: ").strip() or "output.mp4"

    # User-configurable parameters
    max_boxes = get_int_input("Max boxes per frame", 20)
    max_trace_length = get_int_input("Max trace length (number of frames to track)", 30)
    max_total_lines = get_int_input("Max total connection lines per frame (0 to disable lines)", 5)
    max_jump_distance = get_float_input("Max pixel jump distance for tracking lines", 20)
    max_box_size = get_int_input("Max bounding box width/height (0 to disable filtering)", 300)

    # Drawing settings (user can customize)
    BOX_THICKNESS = get_int_input("Box thickness", 1)
    LINE_THICKNESS = get_int_input("Line thickness", 1)
    FONT_SCALE = get_float_input("Font scale", 0.5)
    FONT_THICKNESS = get_int_input("Font thickness", 1)

    show_coordinates = get_yes_no_input("Show coordinates on boxes?", 'y')

    # Pixelation options
    use_pixelation = get_yes_no_input("Enable pixelation effect inside boxes?", 'y')
    if use_pixelation:
        pixel_size = get_int_input("Pixelation block size (larger = more pixelated)", 10)
        if pixel_size < 1:
            pixel_size = 10
        max_pixelate_box_size = get_int_input("Max box width/height for pixelation (0 to disable size limit)", 100)
    else:
        pixel_size = None
        max_pixelate_box_size = 0

    # Sensitivity setting
    sensitivity_choice = input("Detection sensitivity? [low/medium/high, default: medium]: ").strip().lower() or "medium"
    if sensitivity_choice == "high":
        contour_area_threshold = 30
        var_threshold = 5
    elif sensitivity_choice == "low":
        contour_area_threshold = 200
        var_threshold = 25
    else:  # medium
        contour_area_threshold = 80
        var_threshold = 10

    COLOR = (255, 255, 255)
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    MIN_TRACK_LINE_LENGTH = 10
    MIN_WEB_LINE_LENGTH = 20
    temp_video = "temp_video_no_audio.mp4"

    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        print(f"Error opening video: {input_video}")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_video, fourcc, fps, (width, height))

    fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=var_threshold, detectShadows=False)

    # Prime background subtractor to prevent delay
    for _ in range(10):
        ret, warm_frame = cap.read()
        if not ret:
            break
        fgbg.apply(warm_frame)
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # rewind video to frame 0

    trace_points = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        fgmask = fgbg.apply(frame)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

        contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        centers = []
        for cnt in contours:
            if len(centers) >= max_boxes:
                break
            if cv2.contourArea(cnt) > contour_area_threshold:
                x, y, w, h = cv2.boundingRect(cnt)
                # Filter out too big boxes if max_box_size enabled
                if max_box_size > 0 and (w > max_box_size or h > max_box_size):
                    continue
                cx, cy = x + w // 2, y + h // 2
                centers.append((cx, cy))

                roi = frame[y:y+h, x:x+w].copy()

                if use_pixelation:
                    if max_pixelate_box_size == 0 or (w <= max_pixelate_box_size and h <= max_pixelate_box_size):
                        small = cv2.resize(roi, (max(1, w // pixel_size), max(1, h // pixel_size)), interpolation=cv2.INTER_LINEAR)
                        pixelated = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
                        frame[y:y+h, x:x+w] = pixelated

                cv2.rectangle(frame, (x, y), (x + w, y + h), COLOR, BOX_THICKNESS)

                if show_coordinates:
                    label = f"({cx}, {cy})"
                    text_size, _ = cv2.getTextSize(label, FONT, FONT_SCALE, FONT_THICKNESS)
                    text_x = x
                    text_y = y - 5 if y - 5 > text_size[1] else y + text_size[1] + 5
                    cv2.putText(frame, label, (text_x, text_y), FONT, FONT_SCALE, COLOR, FONT_THICKNESS)

        trace_points.append(centers)
        if len(trace_points) > max_trace_length + 1:
            trace_points.pop(0)

        if max_total_lines > 0:
            line_count = 0
            if len(trace_points) > 1:
                prev_centers = trace_points[-2]
                curr_centers = trace_points[-1]
                matched_prev = set()

                for c_curr in curr_centers:
                    if line_count >= max_total_lines:
                        break
                    min_dist = float('inf')
                    best_j = None
                    for j, c_prev in enumerate(prev_centers):
                        if j in matched_prev:
                            continue
                        dist = euclidean_dist(c_prev, c_curr)
                        if dist < min_dist and dist < max_jump_distance:
                            min_dist = dist
                            best_j = j
                    if best_j is not None and min_dist >= MIN_TRACK_LINE_LENGTH:
                        cv2.line(frame, prev_centers[best_j], c_curr, COLOR, LINE_THICKNESS)
                        line_count += 1
                        matched_prev.add(best_j)

            remaining_lines = max_total_lines - line_count
            if remaining_lines > 0 and len(centers) > 1:
                all_pairs = [(i, j) for i in range(len(centers)) for j in range(i + 1, len(centers))]
                random.shuffle(all_pairs)
                lines_drawn = 0
                for i, j in all_pairs:
                    if lines_drawn >= remaining_lines:
                        break
                    pt1, pt2 = centers[i], centers[j]
                    if euclidean_dist(pt1, pt2) >= MIN_WEB_LINE_LENGTH:
                        cv2.line(frame, pt1, pt2, COLOR, LINE_THICKNESS)
                        lines_drawn += 1

        out.write(frame)
        cv2.imshow('Visual Tracker', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            print("Stopped by user.")
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print("Merging audio...")

    cmd = [
        'ffmpeg', '-y',
        '-i', temp_video,
        '-i', input_video,
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-map', '0:v:0',
        '-map', '1:a:0',
        '-movflags', '+faststart',
        output_video
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Output saved to {output_video}")
    except subprocess.CalledProcessError:
        print("Audio merge failed.")

    try:
        os.remove(temp_video)
    except:
        pass

if __name__ == "__main__":
    main()
