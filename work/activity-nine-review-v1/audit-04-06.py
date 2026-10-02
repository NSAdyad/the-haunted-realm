from pathlib import Path
from PIL import Image, ImageChops, ImageStat
import hashlib
import json
import shutil

task_dir = Path(r'C:\Users\DELL\Documents\Codex\2026-09-30\ar\work\activity-nine-review-v1')
generated_dir = Path(r'C:\Users\DELL\.codex\generated_images\01a0f710-2ea6-77a0-a61d-942339b55666')
task_sources = {
    '04': 'exec-51e4f14f-4e3e-4508-a6ec-9657efe5b17d.png',
    '05': 'exec-f6b1c562-65eb-4de0-a019-5ef31bdc9826.png',
    '06': 'exec-fbc358aa-4f50-4ce0-9453-d5dd35a2b5fa.png',
}
task_notes = {
    '04': 'Visually inspected: two anatomically plausible hands and actual quiz response buzzers; upper both poised, lower left index finger in contact with depressed cap, other still poised. No service bells, captions, icons or unexpected readable text.',
    '05': 'Visually inspected: open physical menu dominant with MENU on subject, no readable vocabulary or food names; upper low steam/cooler paper, lower lifted steam ribbon and warmer clearer line structure. Same main setting and menu, subtle generation variation in framing remains.',
    '06': 'Visually inspected: upper translucent ruled slip hovering above silver tray, lower opaque slip touching tray with curled corner; cloche shifts slightly. No readable order content or visible person. Same main setting, subtle generation variation in framing remains.',
}
task_summary = []
for task_number, task_source_name in task_sources.items():
    task_source = generated_dir / task_source_name
    task_output = task_dir / f'activity-{task_number}-state-sheet.png'
    if task_output.exists():
        if task_output.read_bytes() != task_source.read_bytes():
            raise RuntimeError(f'Refusing to overwrite existing different asset: {task_output}')
    else:
        shutil.copy2(task_source, task_output)
    task_image = Image.open(task_output)
    task_alpha = task_image.getchannel('A') if 'A' in task_image.getbands() else None
    task_width, task_height = task_image.size
    task_middle = task_height // 2
    task_zero_rows = []
    if task_alpha is not None:
        for task_y in range(task_height):
            if task_alpha.crop((0, task_y, task_width, task_y + 1)).getextrema() == (0, 0):
                task_zero_rows.append(task_y)
        task_row_set = set(task_zero_rows)
        task_gap_top = task_middle
        task_gap_bottom = task_middle
        if task_middle in task_row_set:
            while task_gap_top - 1 in task_row_set:
                task_gap_top -= 1
            while task_gap_bottom + 1 in task_row_set:
                task_gap_bottom += 1
        task_histogram = task_alpha.histogram()
        task_top_bounds = task_alpha.crop((0, 0, task_width, task_middle)).getbbox()
        task_bottom_bounds = task_alpha.crop((0, task_middle, task_width, task_height)).getbbox()
    else:
        task_gap_top = None
        task_gap_bottom = None
        task_histogram = []
        task_top_bounds = None
        task_bottom_bounds = None
    task_upper = task_image.convert('RGBA').crop((0, 0, task_width, task_middle))
    task_lower = task_image.convert('RGBA').crop((0, task_middle, task_width, task_height))
    task_mean_difference = ImageStat.Stat(ImageChops.difference(task_upper, task_lower)).mean
    task_prompt = task_dir / f'activity-{task_number}-prompt.txt'
    task_metadata = {
        'activity': task_number,
        'tool': 'built-in image_gen.imagegen',
        'intent': 'new static review artwork only; no implementation',
        'source_path': str(task_source),
        'workspace_copy': str(task_output),
        'exact_prompt_path': str(task_prompt),
        'source_sha256': hashlib.sha256(task_source.read_bytes()).hexdigest(),
        'copy_sha256': hashlib.sha256(task_output.read_bytes()).hexdigest(),
        'prompt_sha256': hashlib.sha256(task_prompt.read_bytes()).hexdigest(),
        'size': task_image.size,
        'mode': task_image.mode,
        'alpha_extrema': task_alpha.getextrema() if task_alpha is not None else None,
        'fully_transparent_fraction': task_histogram[0] / (task_width * task_height) if task_histogram else None,
        'partially_transparent_fraction': sum(task_histogram[1:255]) / (task_width * task_height) if task_histogram else None,
        'exact_centre_row_fully_transparent': task_middle in task_zero_rows,
        'centre_row_alpha_extrema': task_alpha.crop((0, task_middle, task_width, task_middle + 1)).getextrema() if task_alpha is not None else None,
        'centre_row_alpha_mean': ImageStat.Stat(task_alpha.crop((0, task_middle, task_width, task_middle + 1))).mean[0] if task_alpha is not None else None,
        'centre_band_alpha_extrema': task_alpha.crop((0, task_middle - 8, task_width, task_middle + 9)).getextrema() if task_alpha is not None else None,
        'centre_band_alpha_mean': ImageStat.Stat(task_alpha.crop((0, task_middle - 8, task_width, task_middle + 9))).mean[0] if task_alpha is not None else None,
        'fully_transparent_rows_near_centre': [task_y for task_y in task_zero_rows if task_middle - 80 <= task_y <= task_middle + 80],
        'transparent_centre_gap_rows_inclusive': [task_gap_top, task_gap_bottom],
        'upper_alpha_bounds': task_top_bounds,
        'lower_alpha_bounds_relative_to_half': task_bottom_bounds,
        'upper_lower_mean_abs_channel_difference': task_mean_difference,
        'visual_review': task_notes[task_number],
        'regenerations': 0,
        'protected_sources': 'No protected source read, supplied as reference/edit target, written, or modified by this agent; root verified protected hashes before generation.'
    }
    task_metadata_path = task_dir / f'activity-{task_number}-metadata.json'
    task_metadata_path.write_text(json.dumps(task_metadata, indent=2), encoding='utf-8')
    task_summary.append({'activity': task_number, 'path': str(task_output), 'centre_row_alpha_extrema': task_metadata['centre_row_alpha_extrema'], 'centre_row_alpha_mean': task_metadata['centre_row_alpha_mean'], 'centre_band_alpha_extrema': task_metadata['centre_band_alpha_extrema'], 'centre_band_alpha_mean': task_metadata['centre_band_alpha_mean'], 'fully_transparent_rows_near_centre': task_metadata['fully_transparent_rows_near_centre']})
print(json.dumps(task_summary, indent=2))
