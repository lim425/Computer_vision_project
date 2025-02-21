import argparse
from collections import defaultdict, deque

import cv2
import numpy as np
from ultralytics import YOLO

import supervision as sv

SOURCE = np.array([[1252, 787], [2298, 803], [5039, 2159], [-550, 2159]])

TARGET_WIDTH = 25
TARGET_HEIGHT = 250

TARGET = np.array(
    [
        [0, 0],
        [TARGET_WIDTH - 1, 0],
        [TARGET_WIDTH - 1, TARGET_HEIGHT - 1],
        [0, TARGET_HEIGHT - 1],
    ]
)


class ViewTransformer:
    def __init__(self, source: np.ndarray, target: np.ndarray) -> None:
        source = source.astype(np.float32)
        target = target.astype(np.float32)
        self.m = cv2.getPerspectiveTransform(source, target)

    def transform_points(self, points: np.ndarray) -> np.ndarray:
        if points.size == 0:
            return points

        reshaped_points = points.reshape(-1, 1, 2).astype(np.float32)
        transformed_points = cv2.perspectiveTransform(reshaped_points, self.m)
        return transformed_points.reshape(-1, 2)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Vehicle Speed Estimation using Ultralytics and Supervision"
    )
    parser.add_argument(
        "--source_video_path",
        required=False,
        default="C:/Users/Asus/Downloads/mv_video.mp4", # Provide a default input video file
        help="Path to the source video file",
        type=str,
    )
    parser.add_argument(
        "--target_video_path",
        required=False,
        default="C:/Users/Asus/Downloads/mv_output_video.mp4",  # Provide a default output video file
        help="Path to the target video file (output)",
        type=str,
    )
    parser.add_argument(
        "--confidence_threshold",
        default=0.3,
        help="Confidence threshold for the model",
        type=float,
    )
    parser.add_argument(
        "--iou_threshold", default=0.7, help="IOU threshold for the model", type=float
    )

    return parser.parse_args()



if __name__ == "__main__":
    args = parse_arguments()

    video_info = sv.VideoInfo.from_video_path(video_path=args.source_video_path)
    model = YOLO("yolov8x.pt")

    byte_track = sv.ByteTrack(
        frame_rate=video_info.fps, track_activation_threshold=args.confidence_threshold
    )

    thickness = sv.calculate_optimal_line_thickness(
        resolution_wh=video_info.resolution_wh
    )
    text_scale = sv.calculate_optimal_text_scale(resolution_wh=video_info.resolution_wh)
    box_annotator = sv.BoxAnnotator(thickness=thickness)
    label_annotator = sv.LabelAnnotator(
        text_scale=text_scale,
        text_thickness=thickness,
        text_position=sv.Position.BOTTOM_CENTER,
    )
    trace_annotator = sv.TraceAnnotator(
        thickness=thickness,
        trace_length=video_info.fps * 2,
        position=sv.Position.BOTTOM_CENTER,
    )

    frame_generator = sv.get_video_frames_generator(source_path=args.source_video_path)

    polygon_zone = sv.PolygonZone(polygon=SOURCE)
    view_transformer = ViewTransformer(source=SOURCE, target=TARGET)

    coordinates = defaultdict(lambda: deque(maxlen=video_info.fps))
    coordinates_before = defaultdict(lambda: deque(maxlen=video_info.fps))
    limits_leftline = [350, 1500, 1750, 1500] # x1, y1, x2, y2
    limits_rightline = [2000, 1100, 2850, 1100]  # x1, y1, x2, y2
    totalCount_left = []
    totalCount_right = []

    with sv.VideoSink(args.target_video_path, video_info) as sink:
        for frame in frame_generator:
            result = model(frame)[0]
            detections = sv.Detections.from_ultralytics(result)
            detections = detections[detections.confidence > args.confidence_threshold]
            detections = detections[polygon_zone.trigger(detections)]
            detections = detections.with_nms(threshold=args.iou_threshold)
            detections = byte_track.update_with_detections(detections=detections)

            points_b4_transform = detections.get_anchors_coordinates(anchor=sv.Position.BOTTOM_CENTER)
            points = view_transformer.transform_points(points=points_b4_transform).astype(int)

            for tracker_id, [_, y], [cx, cy] in zip(detections.tracker_id, points, points_b4_transform):
                coordinates[tracker_id].append(y)
                coordinates_before[tracker_id].append((cx,cy))

            line_color_left = (0, 0, 255)  # Default color left line is red
            line_color_right = (0, 0, 255)  # Default color right line is red
            labels = []
            for tracker_id in detections.tracker_id:
                if len(coordinates[tracker_id]) < video_info.fps / 2:
                    labels.append(f"#{tracker_id}")
                else:
                    coordinate_start = coordinates[tracker_id][-1]
                    coordinate_end = coordinates[tracker_id][0]
                    distance = abs(coordinate_start - coordinate_end)
                    time = len(coordinates[tracker_id]) / video_info.fps
                    speed = distance / time * 3.6
                    labels.append(f"#{tracker_id} {int(speed)} km/h")

                # Left side
                if limits_leftline[0] < coordinates_before[tracker_id][-1][0] < limits_leftline[2] and limits_leftline[1] - 15 < \
                        coordinates_before[tracker_id][-1][1] < limits_leftline[1] + 15:
                    if totalCount_left.count(tracker_id) == 0:
                        totalCount_left.append(tracker_id)
                        line_color_left = (0, 255, 0)  # Change line color to green when the car crosses the line

                # Right side
                if limits_rightline[0] < coordinates_before[tracker_id][-1][0] < limits_rightline[2] and limits_rightline[1] - 15 < \
                        coordinates_before[tracker_id][-1][1] < limits_rightline[1] + 15:
                    if totalCount_right.count(tracker_id) == 0:
                        totalCount_right.append(tracker_id)
                        line_color_right = (0, 255, 0)  # Change line color to green when the car crosses the line

            # Draw the line with the updated color
            cv2.line(frame, (limits_leftline[0], limits_leftline[1]), (limits_leftline[2], limits_leftline[3]), line_color_left, 7)
            cv2.line(frame, (limits_rightline[0], limits_rightline[1]), (limits_rightline[2], limits_rightline[3]), line_color_right,7)

            # Draw the count with the updated line color
            cv2.rectangle(frame, (0, 0), (1200, 500), (252, 156, 180), -1)
            cv2.rectangle(frame, (0, 0), (1200, 500), (0, 0, 0), 4)
            cv2.putText(frame, f'Left Lane:{str(len(totalCount_left))}', (100, 100), cv2.FONT_HERSHEY_PLAIN, 6, (0,35,90), 8)
            cv2.putText(frame, f'Right Lane:{str(len(totalCount_right))}', (100, 250), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 0), 8)
            cv2.putText(frame, f'Total Vehicles:{str(len(totalCount_left)+len(totalCount_right))}', (100, 400), cv2.FONT_HERSHEY_PLAIN, 6,(0, 0, 0), 8)

            frame = trace_annotator.annotate(
                scene=frame, detections=detections
            )
            frame = box_annotator.annotate(
                scene=frame, detections=detections
            )
            frame = label_annotator.annotate(
                scene=frame, detections=detections, labels=labels
            )
            sink.write_frame(frame)
            # resized_frame = frame.copy()
            # resized_frame = cv2.resize(resized_frame, (1280, 720))
            # # resized_frame = cv2.resize(annotated_frame, (1280, 720))
            cv2.imshow("frame", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cv2.destroyAllWindows()
