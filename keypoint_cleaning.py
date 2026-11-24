from pathlib import Path
import os, sys

KEYPOINT_START = 5
CLEAN_FILE_END = "-clean"

def clean_keypoints(input_filename: Path, output_filename: Path) -> int:

    if os.path.getsize(input_filename) == 0:
        return 0
    
    with open(input_filename, "r") as input_file, open(output_filename, "w") as output_file:
        line = input_file.readline().strip()
        inpoints = line.split(" ")

        outpoints = [x for x in inpoints[:KEYPOINT_START]]
        num_zeroed = 0

        for i in range(KEYPOINT_START, len(inpoints), 3):
            x, y, vis = inpoints[i], inpoints[i+1], inpoints[i+2]
            if vis == "0":
                x, y = "0", "0"
                num_zeroed += 1

            outpoints.append(x)
            outpoints.append(y)
            outpoints.append(vis)

        output_file.write(" ".join(outpoints))
        output_file.write("\n")
        return num_zeroed

def clean_training(dir_name: str) -> tuple[int, int]:
    total_points_zeroed = 0
    total_training_examples = 0
    missing_imgs = []

    orig_dir = Path(dir_name)
    clean_dir = Path(f"{dir_name}{CLEAN_FILE_END}")

    new_img_dir = Path(clean_dir / "images" / "Train")
    new_img_dir.mkdir(parents=True, exist_ok=True)

    new_label_dir = Path(clean_dir / "labels" / "Train")
    new_label_dir.mkdir(parents=True, exist_ok=True)

    for label in Path(orig_dir / "labels" / "Train").glob("*.txt"):

        img = Path(orig_dir / "images" / "Train" / label.with_suffix(".jpg").name)
        if not img.exists():
            missing_imgs.append(img.name)
            continue
        img.copy_into(new_img_dir)

        new_label = Path(new_label_dir / label.name)
        total_points_zeroed += clean_keypoints(label, new_label)
        total_training_examples += 1

    if missing_imgs:
        print("Missing images:")
        for img in missing_imgs:
            print(img)
        sys.exit(1)

    return total_training_examples, total_points_zeroed

if __name__ == "__main__":
    examples, zeroed = clean_training("c:/Users/ericd/repos/nba-analysis/data/nets-arena")
    print(f"Points zeroed: {zeroed}")
    print(f"Examples seen: {examples}")



        


