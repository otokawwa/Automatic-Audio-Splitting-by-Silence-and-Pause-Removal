import os
import auditok
import tkinter as tk
from tkinter import filedialog


def remove_silence(input_filepath):
    print(f"Анализ файла: {input_filepath}...")

    base_dir = os.path.dirname(input_filepath)
    filename = os.path.basename(input_filepath)

    part_dir = os.path.join(base_dir, "part_silense")
    full_dir = os.path.join(base_dir, "full_silence")

    os.makedirs(part_dir, exist_ok=True)
    os.makedirs(full_dir, exist_ok=True)

    events = list(auditok.split(
        input_filepath,
        energy_threshold=50,
        min_dur=0.1,
        max_silence=0.3
    ))

    if not events:
        print("ОШИБКА: Речь не найдена. Попробуйте понизить порог (energy_threshold).")
        return

    print(f"Найдено фрагментов с речью: {len(events)}. Начинаю сохранение и склейку...")

    final_audio = None

    for i, event in enumerate(events):
        part_filepath = os.path.join(part_dir, f"part_{i + 1}.wav")
        event.save(part_filepath)

        if final_audio is None:
            final_audio = event
        else:
            final_audio += event

    output_filename = f"no_silence_{filename}"
    full_filepath = os.path.join(full_dir, output_filename)

    final_audio.save(full_filepath)

    print(f"\nГотово!")
    print(f" - Отдельные куски лежат в: {part_dir}")
    print(f" - Очищенный аудиофайл лежит в: {full_filepath}")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    print("Ожидание выбора файла...")

    selected_file = filedialog.askopenfilename(
        title="Выберите аудиофайл (.wav)",
        filetypes=[("Аудиофайлы WAV", "*.wav"), ("Все файлы", "*.*")]
    )

    if selected_file:
        remove_silence(selected_file)
    else:
        print("Файл не был выбран. Отмена операции.")

    input("\nНажмите Enter, чтобы закрыть программу...")