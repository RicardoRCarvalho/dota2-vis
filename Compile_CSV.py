from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

# Input CSV
INPUT_CSV = BASE_DIR / "visibilidade_TI_Aurora Gaming_x_BetBoom Team_Group StageGame 1_Dire.csv"

# Output CSV
OUTPUT_CSV = BASE_DIR / "compiled.csv"

def range_sort_key(r):
    if r == "- 0":
        return -1
    start = int(r.split(" - ")[0])
    return start

def mmss_to_seconds(v):
    v = int(v)
    minutes = v // 100
    seconds = v % 100
    return minutes * 60 + seconds

def is_valid_mmss(v):
    try:
        v = int(v)
        sec = v % 100
        return 0 <= sec < 60
    except:
        return False

#If a video starts from the draft, this can help to not have random data, BEST TO MAKE SURE THAT IT STARTS WITH THE TIMER APPEARING
def clean_timer(df):
    df = df.copy()

    df["prediction"] = pd.to_numeric(df["prediction"], errors="coerce")
    df = df.dropna(subset=["prediction"])

    values = df["prediction"].values

    start_idx = None
    WINDOW = 5  # require consistency

    for i in range(len(values) - WINDOW):
        valid_steps = []

        for j in range(i, i + WINDOW - 1):
            v1 = values[j]
            v2 = values[j + 1]

            if not is_valid_mmss(v1) or not is_valid_mmss(v2):
                continue

            s1 = mmss_to_seconds(v1)
            s2 = mmss_to_seconds(v2)

            diff = s2 - s1

            # ONLY accept real timer movement (±1 second)
            if diff == 1 or diff == -1:
                valid_steps.append(diff)

        # require at least 3 consistent steps
        if len(valid_steps) >= 3:
            if all(d == 1 for d in valid_steps) or all(d == -1 for d in valid_steps):
                start_idx = i
                break

    if start_idx is not None:
        return df.iloc[start_idx:].reset_index(drop=True)

    return df

def main():
    if not INPUT_CSV.exists():
        print(f"ERROR: Input CSV not found:")
        print(INPUT_CSV)
        return

    print(f"\nRunning compiler on:")
    print(INPUT_CSV)

    df = pd.read_csv(INPUT_CSV)

    df = clean_timer(df)

    total_frames = df["frame"].nunique()

    players = df["jogador"].dropna().unique()

    ranges = sorted(
        df["range"].dropna().unique(),
        key=range_sort_key
    )

    compiled_data = []

    for player in players:
        player_df = df[df["jogador"] == player]
        visible_frames = player_df[
            player_df["visivel"] == 1
        ]["frame"].nunique()

        visible_percent = (
            visible_frames / total_frames
            if total_frames > 0
            else 0
        )

        row = {
            "jogador": player,
            "total_frames": total_frames,
            "visible_frames": visible_frames,
            "visible_percent": visible_percent
        }

        for r in ranges:

            range_df = player_df[
                player_df["range"] == r
            ]

            range_total_frames = range_df[
                "frame"
            ].nunique()

            range_visible_frames = range_df[
                range_df["visivel"] == 1
            ]["frame"].nunique()

            range_percent = (
                range_visible_frames / range_total_frames
                if range_total_frames > 0
                else 0
            )

            row[f"{r}_frames"] = range_total_frames

            row[f"{r}_visible_frames"] = range_visible_frames

            row[f"{r}_percent"] = range_percent

        compiled_data.append(row)

    compiled_df = pd.DataFrame(compiled_data)

    base_cols = [
        "jogador",
        "total_frames",
        "visible_frames",
        "visible_percent"
    ]

    ordered_range_cols = []

    for r in ranges:

        ordered_range_cols.extend([
            f"{r}_frames",
            f"{r}_visible_frames",
            f"{r}_percent"
        ])

    final_cols = base_cols + ordered_range_cols

    final_cols = [
        column
        for column in final_cols
        if column in compiled_df.columns
    ]

    compiled_df = compiled_df[final_cols]

    compiled_df.to_csv(
        OUTPUT_CSV,
        index=False
    )

if __name__ == "__main__":
    main()