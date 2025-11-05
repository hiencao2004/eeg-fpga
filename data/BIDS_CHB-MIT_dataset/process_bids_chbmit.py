# ===================== DEBUG 1 SUBJECT =====================
import os, glob, random, pickle
import numpy as np
import pandas as pd
import mne
import mne_bids
from tqdm import tqdm

# ========== CONFIG ==========
BIDS_ROOT = "/content/drive/MyDrive/BIDS_CHB-MIT/BIDS_CHB-MIT"
OUTPUT_DIR = "/content/drive/MyDrive/EESNN_processed_data"
TARGET_FREQ = 64.0
WINDOW_SEC = 4.0
BALANCE_RATIO = 5
SUBJECT = "13"   # <---- CHỌN SUBJECT TẠI ĐÂY
EXPECTED_CHANNELS = 18
# ============================

os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_single_subject(subject):
    print(f"\n=== ĐANG XỬ LÝ BỆNH NHÂN {subject} ===")

    pos_epochs_data, neg_epochs_data = [], []
    seizure_events_summary = []

    bids_path_template = mne_bids.BIDSPath(root=BIDS_ROOT,
                                          subject=subject,
                                          datatype='eeg',
                                          extension='.edf')
    bids_paths = list(bids_path_template.match())
    print(f"🧩 Tìm thấy {len(bids_paths)} file EDF cho subject {subject}")

    for bids_path in tqdm(bids_paths, desc=f"Files {subject}", leave=False):
        try:
            raw = mne_bids.read_raw_bids(bids_path=bids_path, verbose=False)
            raw.load_data()
            orig_sfreq = float(raw.info['sfreq'])
            raw_duration = raw.n_times / orig_sfreq

            # pick EEG
            raw.pick_types(eeg=True, exclude='bads')
            num_channels = len(raw.ch_names)
            if num_channels != EXPECTED_CHANNELS:
                print(f"⚠️ {bids_path.basename}: {num_channels} kênh (mong đợi {EXPECTED_CHANNELS})")

            # tìm file events.tsv tương ứng
            folder = str(bids_path.fpath.parent)
            base = bids_path.fpath.stem.replace("_eeg", "")
            ev_candidates = glob.glob(os.path.join(folder, f"{base}_events.tsv"))
            events_tsv_path = ev_candidates[0] if ev_candidates else None

            if events_tsv_path and os.path.exists(events_tsv_path):
                df_ev = pd.read_csv(events_tsv_path, sep="\t")
                if "onset" in df_ev.columns and "duration" in df_ev.columns:
                    onsets = df_ev["onset"].astype(float).values
                    durs = df_ev["duration"].astype(float).values
                    if onsets.max() > raw_duration * 5:
                        onsets = onsets / orig_sfreq
                        durs = durs / orig_sfreq
                    if "eventType" in df_ev.columns:
                        descs = df_ev["eventType"].astype(str).tolist()
                    else:
                        descs = df_ev.astype(str).agg("|".join, axis=1).tolist()

                    ann = mne.Annotations(onset=onsets, duration=durs, description=descs)
                    raw.set_annotations(ann)

                    # debug: in eventType duy nhất
                    uniq = [d.lower() for d in set(df_ev["eventType"].astype(str))]
                    if any("sz" in d or "seiz" in d for d in uniq):
                        print(f"⚡ Có seizure trong: {events_tsv_path} → {uniq}")
                else:
                    print(f"⚠️ {events_tsv_path} không có cột onset/duration")

            # filter + resample
            raw.filter(0.5, 30.0, fir_design='firwin', verbose=False)
            raw.notch_filter(60, verbose=False)
            raw.resample(TARGET_FREQ, verbose=False)

            # normalize
            data = raw.get_data()
            data = (data - data.mean(axis=1, keepdims=True)) / (data.std(axis=1, keepdims=True) + 1e-6)
            raw._data = data.astype(np.float32)

            # epochs
            epochs = mne.make_fixed_length_epochs(raw, duration=WINDOW_SEC, preload=True, verbose=False)
            all_epoch_data = epochs.get_data(picks="eeg")

            annots = raw.annotations if raw.annotations is not None else mne.Annotations([], [], [])
            seizure_keywords = ["sz", "seiz", "ictal", "seizure"]

            for a, d in zip(annots.onset, annots.description):
                if any(k in d.lower() for k in seizure_keywords):
                    seizure_events_summary.append({
                        "file": str(bids_path.fpath),
                        "onset": a,
                        "desc": d
                    })

            # labeling epoch
            epoch_times = epochs.events[:, 0] / raw.info['sfreq']
            for i, start in enumerate(epoch_times):
                stop = start + WINDOW_SEC
                label = 0
                for a, dur, d in zip(annots.onset, annots.duration, annots.description):
                    if (a < stop) and (a + dur > start):
                        if any(k in d.lower() for k in seizure_keywords):
                            label = 1
                            break
                if label == 1:
                    pos_epochs_data.append(all_epoch_data[i])
                else:
                    neg_epochs_data.append(all_epoch_data[i])

            raw.close()
            del raw, epochs, all_epoch_data

        except Exception as e:
            print(f"⚠️ Lỗi khi xử lý {bids_path.basename}: {e}")

    print(f"\nTổng kết subject {subject}: {len(pos_epochs_data)} seizure | {len(neg_epochs_data)} non-seizure")

    if seizure_events_summary:
        df = pd.DataFrame(seizure_events_summary)
        csv_path = os.path.join(OUTPUT_DIR, f"chb{subject}_events_debug.csv")
        df.to_csv(csv_path, index=False)
        print(f"Lưu tóm tắt event: {csv_path}")

    if pos_epochs_data:
        pos_path = os.path.join(OUTPUT_DIR, f"chb{subject}_pos_array.pkl")
        with open(pos_path, 'wb') as f:
            pickle.dump(np.array(pos_epochs_data, dtype=np.float32), f)
        print(f" Lưu {len(pos_epochs_data)} epoch seizure → {pos_path}")
    else:
        print(" Không có epoch nào gán seizure trong subject này.")

    if neg_epochs_data:
        neg_path = os.path.join(OUTPUT_DIR, f"chb{subject}_neg_array.pkl")
        with open(neg_path, 'wb') as f:
            pickle.dump(np.array(neg_epochs_data, dtype=np.float32), f)
        print(f"Lưu {len(neg_epochs_data)} epoch non-seizure → {neg_path}")

# chạy 1 subject
process_single_subject(SUBJECT)
